from importlib.metadata import requires
from tkinter import Widget
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

# Create your forms here.

class NewUserForm(UserCreationForm):
	username = forms.CharField(
		required=True,
		widget=forms.widgets.Textarea(
			attrs={
				"placeholder": "ivoivic",
				"class": "input is-grey-light is-medium",
			}
		),
		label="Korisničko ime",
	)

	email = forms.EmailField(
		required=True,
		widget=forms.widgets.Textarea(
			attrs={
				"placeholder": "ivoivic@email.com",
				"class": "input is-grey-light is-medium",
			}
		)
	)

	password1 = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "lozinka",
			}
		),
		label="Lozinka",
	)

	password2 = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "lozinka",
			}
		),
		label="Potvrda lozinke",
	)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ObjavaForm(forms.ModelForm):
    tijelo = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Šta je tvoje danas, to je sutra moje, lave...",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Objava
        exclude = ("stvorio", "objava_lajkovi", "objava_komentari", )


class KomentarForm(forms.ModelForm):
    tijelo = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Odličan recept!",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Komentar
        exclude = ("objava", "stvorio", )


class ProfilForm(forms.ModelForm):
    ime = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Ivo Ivić",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="Ime",
    )

    opis = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Pekar iz Rijeke...",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="Opis",
    )

    lokacija = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Rijeka",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="Lokacija",
    )

    class Meta:
        model = Profil
        exclude = ("korisnik", "prati", )