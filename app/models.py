from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profil(models.Model):
    korisnik = models.OneToOneField(User, on_delete=models.CASCADE)
    ime = models.CharField(max_length=50)
    #hendl = models.CharField(max_length=50)
    opis = models.CharField(max_length=255)
    lokacija = models.CharField(max_length=50)
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
    tijelo = models.CharField(max_length=255)
    stvorio = models.ForeignKey(User, related_name='komentari', on_delete=models.CASCADE)
    vrijeme_komentiranja = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Komentari'
        ordering = ('-vrijeme_komentiranja',)

    def __str__(self):
        return "{} (objava {}) {}".format(self.stvorio.username, self.tvit.id, self.tijelo)

class Objava(models.Model):
    naslov = models.CharField(max_length=100)
    sastojci = models.TextField()
    upute = models.TextField()
    napomene = models.TextField()
    stvorio = models.ForeignKey(User, related_name='objave', on_delete=models.CASCADE)
    objava_lajkovi = models.ManyToManyField(User, related_name='srce_korisnik', blank=True, through=Srce)
    objava_komentari = models.ManyToManyField(User, related_name='komentar_korisnik', blank=True, through=Komentar)
    vrijeme_stvaranja = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Objave'
        ordering = ('-vrijeme_stvaranja',)

    def __str__(self):
            return "{} ({}): {}".format(self.stvorio.username, self.vrijeme_stvaranja, self.tijelo[:30])


@receiver(post_save, sender=User)
def stvori_profil(sender, instance, created, **kwargs):
    if created:
        user_profil = Profil(korisnik=instance)
        user_profil.save()
        user_profil.prati.add(instance.profil)
        user_profil.save()