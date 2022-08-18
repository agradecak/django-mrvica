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
    avatar = models.ImageField(default='profile.png', null=True, blank=True)
    datum_pridruzivanja = models.DateField(auto_now_add=True)
    prati = models.ManyToManyField('self', related_name='pracen_od', symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = 'Profili'

    def __str__(self):
        return "{} ({})".format(self.korisnik.username, self.id)


class Srce(models.Model):
    objava = models.ForeignKey('Objava', related_name='srca', on_delete=models.CASCADE)
    stvorio = models.ForeignKey(User, related_name='srca', on_delete=models.CASCADE)
    vrijeme_lajkanja = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Srca'

    def __str__(self):
        return "({}) {}".format(self.id, self.objava.tijelo)

class Komentar(models.Model):
    objava = models.ForeignKey('Objava', related_name='komentari', on_delete=models.CASCADE)
    tijelo = models.CharField(max_length=255, blank=False)
    stvorio = models.ForeignKey(User, related_name='komentari', on_delete=models.CASCADE)
    vrijeme_komentiranja = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Komentari'
        ordering = ('-vrijeme_komentiranja',)

    def __str__(self):
        return "{} (objava {}) {}".format(self.stvorio.username, self.tvit.id, self.tijelo)

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
            return "{} ({}): {}".format(self.stvorio.username, self.vrijeme_stvaranja, self.tijelo[:30])

    def sastojci_as_list(self):
        return self.sastojci.split('\n')

    def upute_as_list(self):
        return self.upute.split('\n')

class Slika(models.Model):
    objava = models.ForeignKey(Objava, related_name='objava_slike', on_delete=models.CASCADE)
    slika = models.ImageField()

    class Meta:
        verbose_name_plural = "Slike"

    def save(self,*args, **kwargs):
        if self.slika:
            img = Img.open(io.BytesIO(self.slika.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((100,100), Img.ANTIALIAS)
            output = io.BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)
            self.slika = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.slika.name.split('.')[0], 'image/jpeg',"Content-Type: charset=utf-8", None)
        super(Slika, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def stvori_profil(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        user_profil = Profil(korisnik=instance)
        user_profil.save()