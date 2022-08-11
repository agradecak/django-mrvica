from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.

models = [ Profil, Srce, Komentar, Objava, Slika ]

admin.site.unregister(Group)
admin.site.register(models)
