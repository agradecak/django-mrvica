from gc import get_objects
import random
from urllib.request import HTTPRedirectHandler
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail, BadHeaderError
# from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.http import HttpResponse #, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import *
from .models import *

# Create your views here.

@login_required
def naslovna(request):
	profili = list(Profil.objects.exclude(korisnik=request.user))
	if len(profili) > 5:
		random_profili = random.sample(profili, 5)
	else:
		random_profili = profili
	return render(request, 'app/naslovna.html', {'profili': random_profili})

@login_required
def profili(request):
	profili = Profil.objects.exclude(korisnik=request.user)
	return render(request, 'app/profili.html', {'profili': profili})

@login_required
def nova_objava(request):
	if request.method == 'POST':
		obrazac_objave = ObjavaForm(request.POST)
		files = request.FILES.getlist("slika")
		if obrazac_objave.is_valid():
			objava = obrazac_objave.save(commit=False)
			objava.stvorio = request.user
			objava.save()
			for file in files:
				Slika.objects.create(objava=objava, slika=file)
			return redirect('app:objava', pk=objava.id)
	else:
		obrazac_objave = ObjavaForm()
		obrazac_slika = SlikaForm()
	return render(request, 'app/nova_objava.html', {'obrazac_objave': obrazac_objave, 'obrazac_slika': obrazac_slika})

@login_required
def objava(request, pk):
	objava = Objava.objects.get(pk=pk)
	trenutni_path = request.path

	if request.method == "POST":
		obrazac_komentara = KomentarForm(request.POST)
		if obrazac_komentara.is_valid():
			komentar = obrazac_komentara.save(commit=False)
			komentar.objava = objava
			komentar.stvorio = request.user
			komentar.save()
			messages.success(request, "Komentar uspje??no stvoren.")
		else:
			messages.error(request, "Komentar nije valjan.")

		logirani_korisnik = request.user
		radnja_srce = request.POST.get("srce")

		if radnja_srce == "voli":
			objava.objava_srca.add(logirani_korisnik)
		elif radnja_srce == "nevoli":
			objava.objava_srca.remove(logirani_korisnik)

		objava.save()
		return redirect(trenutni_path)
	else:
		obrazac_komentara = KomentarForm()
	return render(request, "app/objava.html", {"objava": objava, "obrazac_komentara": obrazac_komentara, })

@login_required
def brisi_objavu(request, objava_id):
	profil = request.user.profil
	objava = get_object_or_404(Objava, pk=objava_id)
	objava.delete()

	return redirect('app:profil', profil.id)

@login_required
def brisi_komentar(request, objava_id, komentar_id):
	komentar = get_object_or_404(Komentar, pk=komentar_id)
	komentar.delete()

	return redirect('app:objava', objava_id)
	

@login_required
def profil(request, pk):
	profil = Profil.objects.get(pk=pk)

	if request.method == "POST":
		logirani_profil = request.user.profil
		radnja_pracenje = request.POST.get("pracenje")

		if radnja_pracenje == "prati":
			logirani_profil.prati.add(profil)
		elif radnja_pracenje == "neprati":
			logirani_profil.prati.remove(profil)
		
		logirani_profil.save()
	
	return render(request, "app/profil.html", {"profil": profil})

@login_required
def prate(request, pk):
	profil = Profil.objects.get(pk=pk)
	return render(request, "app/prate.html", {"profil": profil})

@login_required
def prati(request, pk):
	profil = Profil.objects.get(pk=pk)
	return render(request, "app/prati.html", {"profil": profil})

@login_required
def uredi_profil(request):
	profil = request.user.profil

	if request.method == 'POST':
		profil_form = ProfilForm(request.POST, request.FILES, instance=profil)
		if profil_form.is_valid():
			novi_podaci = profil_form.save(commit=False)
			novi_podaci.save()

			return redirect('app:profil', pk=profil.id)
	else:
		profil_form = ProfilForm(instance=profil)
	return render(request, 'app/uredi_profil.html', {'profil_form': profil_form})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registracija uspje??na." )
			return redirect("app:uredi_profil")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	else:
		form = NewUserForm()
	return render (request, "app/register.html", {"register_form":form})

def login_request(request):
	if request.method == "POST":
		obrazac_prijave = UserLoginForm(request, data=request.POST)
		if obrazac_prijave.is_valid():
			username = obrazac_prijave.cleaned_data.get('username')
			password = obrazac_prijave.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("app:naslovna")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	else:
		obrazac_prijave = UserLoginForm()
	return render(request, "app/login.html", {"obrazac_prijave": obrazac_prijave})

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("app:login")


def password_reset_request(request):
	#if not request.user.is_authenticated:
	if request.method == "POST":
		password_reset_form = ResetPasswordForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "app/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Mrvica',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@mrvica.hr' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	else:
		password_reset_form = ResetPasswordForm()
	return render(request, "app/password/password_reset.html", {"password_reset_form":password_reset_form})
	# else:
		# return redirect("app:naslovna")