# from importlib.metadata import requires
# from tkinter import Widget, Image
# from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import *

# Create your forms here.


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "input",
                "placeholder": "ivoivic",
            }
        ),
    )

    password = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input",
                "placeholder": "********",
			}
		),
	)

class ResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"class": "input",
                "placeholder": "ivoivic@email.com",
			}
		),
	)

class NewUserForm(UserCreationForm):
	username = forms.CharField(
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"class": "input",
                "placeholder": "ivoivic",
			}
		),
	)

	email = forms.EmailField(
		required=True,
		widget=forms.widgets.TextInput(
			attrs={
				"class": "input",
				"placeholder": "ivoivic@email.com",
			}
		),
	)

	password1 = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input",
				"placeholder": "********",
			}
		),
	)

	password2 = forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"type": "password",
				"class": "input",
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
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "mlijeko mora biti na sobnoj",
                "class": "input is-grey-light is-medium",
            }
        ),
    )

    class Meta:
        model = Objava
        exclude = ("stvorio", "objava_srca", "objava_komentari", )


class KomentarForm(forms.ModelForm):
    tijelo = forms.CharField(
        label="Komentar",
        required=True,
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
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Ivo Ivić",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="Ime",
    )

    opis = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Pekar iz Rijeke...",
                "class": "input is-grey-light is-medium",
            }
        ),
        label="Opis",
    )

    lokacija = forms.CharField(
        required=True,
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
        fields = ("slika",)