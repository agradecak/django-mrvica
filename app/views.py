from urllib.request import HTTPRedirectHandler
from django.shortcuts import render, redirect
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
from .forms import *
from .models import *

# Create your views here.

@login_required
def naslovna(request):
	profili = Profil.objects.exclude(korisnik=request.user)
	return render(request, 'app/naslovna.html', {'profili': profili})

@login_required
def nova_objava(request):
	if request.method == 'POST':
		objava_form = ObjavaForm(request.POST)
		files = request.FILES.getlist("slika")
		if objava_form.is_valid():
			objava = objava_form.save(commit=False)
			objava.stvorio = request.user
			objava.save()
			for file in files:
				Slika.objects.create(objava=objava, slika=file)
			messages.success(request, "Objava uspješno stvorena.")
			return redirect('app:profil', pk=request.user.profil.id)
		
		else:
			messages.error(request, "Objava nije valjana.")
	else:
		objava_form = ObjavaForm()
		slika_form = SlikaForm()
	return render(request, 'app/nova_objava.html', {'objava_form': objava_form, 'slika_form': slika_form})

@login_required
def objava(request, pk):
	objava = Objava.objects.get(pk=pk)
	trenutni_path = request.path

	if request.method == "POST":
		komentar_form = KomentarForm(request.POST)
		if komentar_form.is_valid():
			komentar = komentar_form.save(commit=False)
			komentar.objava = objava
			komentar.stvorio = request.user
			komentar.save()
			messages.success(request, "Komentar uspješno stvoren.")
			return redirect(trenutni_path)
		else:
			messages.error(request, "Komentar nije valjan.")

		logirani_korisnik = request.user
		podaci = request.POST
		radnja_srce = podaci.get("srce")

		if radnja_srce == "voli":
			objava.objava_srca.add(logirani_korisnik)
		elif radnja_srce == "nevoli":
			objava.objava_srca.remove(logirani_korisnik)

		objava.save()
		return redirect(trenutni_path)
	else:
		komentar_form = KomentarForm()
	return render(request, "app/objava.html", {"objava": objava, "komentar_form": komentar_form})

@login_required
def profil(request, pk):
	profil = Profil.objects.get(pk=pk)
	if request.method == "POST":
		logirani_profil = request.user.profil
		podaci = request.POST
		radnja_pracenje = podaci.get("pracenje")

		if radnja_pracenje == "prati":
			logirani_profil.prati.add(profil)
		elif radnja_pracenje == "neprati":
			logirani_profil.prati.remove(profil)
		
		logirani_profil.save()
	
	return render(request, "app/profil.html", {"profil": profil})

@login_required
def uredi_profil(request):
	profil = request.user.profil

	if request.method == 'POST':
		profil_form = ProfilForm(request.POST, instance=profil)
		if profil_form.is_valid():
			novi_podaci = profil_form.save(commit=False)
			novi_podaci.save()

			return redirect('app:profil', pk=profil.id)
	else:
		profil_form = ProfilForm()
	return render(request, 'app/uredi_profil.html', {'profil_form': profil_form})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registracija uspješna." )
			return redirect("app:uredi_profil")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	else:
		form = NewUserForm()
	return render (request, "app/register.html", {"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = UserLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
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
		form = UserLoginForm()
	return render(request, "app/login.html", {"login_form":form})

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