from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image as Img
import io
from django.core.files.uploadhandler import InMemoryUploadedFile

# Pomoćne funkcije

def has_changed(instance, field):
        if not instance.pk:
            return False
        old_value = instance.__class__._default_manager.\
                 filter(pk=instance.pk).values(field).get()[field]
        return not getattr(instance, field) == old_value

# Modeli

class Profil(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    ime = models.CharField(max_length=50)
    opis = models.CharField(max_length=255)
    lokacija = models.CharField(max_length=50)
    avatar = models.ImageField(default='profile.jpg')
    datum_pridruzivanja = models.DateField(auto_now_add=True)
    prati = models.ManyToManyField('self', related_name='pracen_od', symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = 'Profili'

    def __str__(self):
        return "{}({})".format(self.korisnik.username, self.id)

    def save(self, *args, **kwargs):
        if has_changed(self, 'avatar'):
            slika_temp = Img.open(io.BytesIO(self.avatar.read()))
            sirina, visina = slika_temp.size
            nova_sirina, nova_visina = 128, 128

            if slika_temp.mode != 'RGB':
                slika_temp = slika_temp.convert('RGB')

            # ako je slika široka
            if sirina > visina:
                # dobivanje kvadrata rezanjem lijeve i desne strane
                x1 = (sirina - visina) / 2
                y1 = 0
                x2 = (sirina + visina) / 2
                y2 = visina
                slika_temp = slika_temp.crop((x1, y1, x2, y2))

            # ako je slika visoka
            elif visina > sirina:
                # dobivanje kvadrata rezanjem gornje i doljnje strane
                x1 = 0
                y1 = (visina - sirina) / 2
                x2 = sirina
                y2 = (visina + sirina) / 2
                slika_temp = slika_temp.crop((x1, y1, x2, y2))

            # ako su početne dimenzije veće od željenih
            if sirina > nova_sirina and visina > nova_visina:
                # skaliraj na željene dimenzije
                slika_temp.thumbnail((nova_sirina, nova_visina), Img.ANTIALIAS)

            output = io.BytesIO()
            # bajtove pretvori u sliku jpeg formata
            slika_temp.save(output, format='JPEG')
            output.seek(0)
            self.avatar = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.avatar.name.split('.')[0], 'image/jpeg',"Content-Type: charset=utf-8", None)

        super(Profil, self).save(*args, **kwargs)


class Srce(models.Model):
    objava = models.ForeignKey('Objava', related_name='srca', on_delete=models.CASCADE)
    stvorio = models.ForeignKey(User, related_name='srca', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Srca'

    def __str__(self):
        return "{} {}({})".format(self.id, self.objava.naslov[0:20], self.objava.id)

class Komentar(models.Model):
    objava = models.ForeignKey('Objava', related_name='komentari', on_delete=models.CASCADE)
    tijelo = models.CharField(max_length=255)
    stvorio = models.ForeignKey(User, related_name='komentari', on_delete=models.CASCADE)
    vrijeme_komentiranja = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Komentari'
        ordering = ('-vrijeme_komentiranja',)

    def __str__(self):
        return "{} {} {}".format(self.id, self.stvorio.username, self.tijelo[0:20])

class Objava(models.Model):
    naslov = models.CharField(max_length=100)
    sastojci = models.TextField()
    upute = models.TextField()
    napomene = models.TextField()
    stvorio = models.ForeignKey(User, related_name='objave', on_delete=models.CASCADE)
    objava_srca = models.ManyToManyField(User, related_name='srce_korisnik', blank=True, through=Srce)
    # objava_komentari = models.ManyToManyField(User, related_name='komentar_korisnik', blank=True, through=Komentar)
    vrijeme_stvaranja = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Objave'
        ordering = ('-vrijeme_stvaranja',)

    def __str__(self):
        return "{} {} {} {}".format(self.id, self.stvorio.username, self.vrijeme_stvaranja, self.naslov[0:20])

    def sastojci_as_list(self):
        return self.sastojci.split('\n')

    def upute_as_list(self):
        return self.upute.split('\n')
    
    def prva_slika(self):
        return self.objava_slike.first()  

class Slika(models.Model):
    objava = models.ForeignKey(Objava, related_name='objava_slike', on_delete=models.CASCADE)
    slika = models.ImageField()

    class Meta:
        verbose_name_plural = "Slike"

    def __str__(self):
        return "{} {}({})".format(self.id, self.objava.naslov[0:20], self.objava.id)

    def save(self, *args, **kwargs):
        slika_temp = Img.open(io.BytesIO(self.slika.read()))
        sirina, visina = slika_temp.size
        nova_sirina, nova_visina = 480, 480

        if slika_temp.mode != 'RGB':
            slika_temp = slika_temp.convert('RGB')

        # ako je slika široka
        if sirina > visina:
            # dobivanje kvadrata rezanjem lijeve i desne strane
            x1 = (sirina - visina) / 2
            y1 = 0
            x2 = (sirina + visina) / 2
            y2 = visina
            slika_temp = slika_temp.crop((x1, y1, x2, y2))

        # ako je slika visoka
        elif visina > sirina:
            # dobivanje kvadrata rezanjem gornje i doljnje strane
            x1 = 0
            y1 = (visina - sirina) / 2
            x2 = sirina
            y2 = (visina + sirina) / 2
            slika_temp = slika_temp.crop((x1, y1, x2, y2))

        # ako je kvadrat veći od željenih dimenzija
        if sirina > nova_sirina and visina > nova_visina:
            # skaliraj na željene dimenzije
            slika_temp.thumbnail((nova_sirina, nova_visina), Img.ANTIALIAS)

        output = io.BytesIO()
        # bajtove pretvori u sliku jpeg formata
        slika_temp.save(output, format='JPEG')
        output.seek(0)
        self.slika = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.slika.name.split('.')[0], 'image/jpeg',"Content-Type: charset=utf-8", None)
        super(Slika, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def stvori_profil(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        korisnik_profil = Profil(korisnik=instance)
        korisnik_profil.save()