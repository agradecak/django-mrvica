# from importlib.metadata import requires
# from tkinter import Widget, Image
# from urllib import request
from django import forms
from django.core.files.images import get_image_dimensions
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import *

# Forme

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "input is-grey-light is-medium",
                "placeholder": "ivoivic",
            }
        ),
    )

    password = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
                "placeholder": "********",
			}
		),
	)

class ResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"class": "input is-grey-light is-medium",
                "placeholder": "ivoivic@email.com",
			}
		),
	)

class NewUserForm(UserCreationForm):
	username = forms.CharField(
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"class": "input is-grey-light is-medium",
                "placeholder": "ivoivic",
			}
		),
	)

	email = forms.EmailField(
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"class": "input is-grey-light is-medium",
				"placeholder": "ivoivic@email.com",
			}
		),
	)

	password1 = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "********",
			}
		),
	)

	password2 = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "********",
			}
		),
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
    naslov = forms.CharField(
        label="Naslov",
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Tijesto za pizzu",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    sastojci = forms.CharField(
        label="Sastojci",
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "300g o??trog bra??na...",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    upute = forms.CharField(
        label="Upute",
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Pe??nicu upaliti na 180??C...",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    napomene = forms.CharField(
        label="Napomene",
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Mlijeko mora biti na sobnoj temperaturi...",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    class Meta:
        model = Objava
        exclude = ("stvorio", "objava_srca", )


class KomentarForm(forms.ModelForm):
    tijelo = forms.CharField(
        label="Komentar",
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Odli??an recept!",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    class Meta:
        model = Komentar
        exclude = ("objava", "stvorio", )


class ProfilForm(forms.ModelForm):
    ime = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Ivo Ivi??",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    opis = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Pekar kruhova i kru??nih proizvoda",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    lokacija = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Rijeka",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    avatar = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput
    )

    class Meta:
        model = Profil
        exclude = ("korisnik", "prati", )

class SlikaForm(forms.ModelForm):
    slika = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": True,
            }
        ),
    )

    class Meta:
        model = Slika
        exclude = ("objava", )