from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image as Img
import io
from django.core.files.uploadhandler import InMemoryUploadedFile

# Create your models here.

class Profil(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    ime = models.CharField(max_length=50, blank=False)
    opis = models.CharField(max_length=255, blank=False)
    lokacija = models.CharField(max_length=50, blank=False)
    avatar = models.ImageField(default='profile.jpg', null=True, blank=True)
    datum_pridruzivanja = models.DateField(auto_now_add=True)
    prati = models.ManyToManyField('self', related_name='pracen_od', symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = 'Profili'

    def __str__(self):
        return "{}({})".format(self.korisnik.username, self.id)

    def save(self, *args, **kwargs):
        if self.avatar:
            avatar_temp = Img.open(io.BytesIO(self.avatar.read()))
            visina, sirina = avatar_temp.size
            if avatar_temp.mode != 'RGB':
                avatar_temp = avatar_temp.convert('RGB')

            if visina > 128 and sirina > 128:
                avatar_temp.thumbnail((visina, sirina), Img.ANTIALIAS)

            if sirina < visina:
                lijevo = (visina - sirina) / 2
                desno = (visina + sirina) / 2
                vrh = 0
                dno = sirina
                avatar_temp = avatar_temp.crop((lijevo, vrh, desno, dno))

            elif visina < sirina:
                lijevo = 0
                desno = visina
                vrh = 0
                dno = visina
                avatar_temp = avatar_temp.crop((lijevo, vrh, desno, dno))

            if visina > 128 and sirina > 128:
                avatar_temp.thumbnail((128, 128), Img.ANTIALIAS)

            output = io.BytesIO()
            avatar_temp.save(output, format='JPEG')
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
    tijelo = models.CharField(max_length=255, blank=False)
    stvorio = models.ForeignKey(User, related_name='komentari', on_delete=models.CASCADE)
    vrijeme_komentiranja = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Komentari'
        ordering = ('-vrijeme_komentiranja',)

    def __str__(self):
        return "{} {} {}".format(self.id, self.stvorio.username, self.tijelo[0:20])

class Objava(models.Model):
    naslov = models.CharField(max_length=100, blank=False)
    sastojci = models.TextField(blank=False)
    upute = models.TextField(blank=False)
    napomene = models.TextField(blank=True)
    stvorio = models.ForeignKey(User, related_name='objave', on_delete=models.CASCADE)
    objava_srca = models.ManyToManyField(User, related_name='srce_korisnik', blank=True, through=Srce)
    objava_komentari = models.ManyToManyField(User, related_name='komentar_korisnik', blank=True, through=Komentar)
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

class Slika(models.Model):
    objava = models.ForeignKey(Objava, related_name='objava_slike', on_delete=models.CASCADE)
    slika = models.ImageField()

    class Meta:
        verbose_name_plural = "Slike"

    def __str__(self):
        return "{} {}({})".format(self.id, self.objava.naslov[0:20], self.objava.id)

    def save(self, *args, **kwargs):
        if self.slika:
            slika_temp = Img.open(io.BytesIO(self.slika.read()))
            visina, sirina = slika_temp.size
            if slika_temp.mode != 'RGB':
                slika_temp = slika_temp.convert('RGB')

            if visina > 480 and sirina > 480:
                slika_temp.thumbnail((visina, sirina), Img.ANTIALIAS)

            if sirina < visina:
                lijevo = (visina - sirina) / 2
                desno = (visina + sirina) / 2
                vrh = 0
                dno = sirina
                slika_temp = slika_temp.crop((lijevo, vrh, desno, dno))

            elif visina < sirina:
                lijevo = 0
                desno = visina
                vrh = 0
                dno = visina
                slika_temp = slika_temp.crop((lijevo, vrh, desno, dno))

            if visina > 480 and sirina > 480:
                slika_temp.thumbnail((480, 480), Img.ANTIALIAS)

            output = io.BytesIO()
            slika_temp.save(output, format='JPEG')
            output.seek(0)
            self.slika = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.slika.name.split('.')[0], 'image/jpeg',"Content-Type: charset=utf-8", None)
        super(Slika, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def stvori_profil(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        korisnik_profil = Profil(korisnik=instance)
        korisnik_profil.save()