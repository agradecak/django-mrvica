from importlib.metadata import requires
from tkinter import Widget
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import *

# Create your forms here.


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Korisničko ime",
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "ivoivic",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    password = forms.CharField(
        label="Lozinka",
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "lozinka",
			}
		),
	)

class ResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(
        label="Email",
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"placeholder": "ivoivic@email.com",
				"class": "input is-grey-light is-medium",
			}
		),
	)

class NewUserForm(UserCreationForm):
	username = forms.CharField(
        label="Korisničko ime",
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"placeholder": "ivoivic",
				"class": "input is-grey-light is-medium",
			}
		),
	)

	email = forms.EmailField(
        label="Email",
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"placeholder": "ivoivic@email.com",
				"class": "input is-grey-light is-medium",
			}
		),
	)

	password1 = forms.CharField(
        label="Lozinka",
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "lozinka",
			}
		),
	)

	password2 = forms.CharField(
        label="Potvrda lozinke",
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input is-grey-light is-medium",
				"placeholder": "lozinka",
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
                "placeholder": "Brze krafne",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    sastojci = forms.CharField(
        label="Sastojci",
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "200ml mlijeka\n350g brašna\n...",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    upute = forms.CharField(
        label="Upute",
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "pećnicu upaliti na 180°C\npromiješati suhe sastojke\n...",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    napomene = forms.CharField(
        label="Napomene",
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "mlijeko mora biti na sobnoj",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    class Meta:
        model = Objava
        exclude = ("stvorio", "objava_lajkovi", "objava_komentari", )


class KomentarForm(forms.ModelForm):
    tijelo = forms.CharField(
        label="Komentar",
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Odličan recept!",
                "class": "input is-grey-light is-medium",
            }
        ),
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