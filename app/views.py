from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.http import HttpResponse
from .forms import *

# Create your views here.

def dashboard(request):
    return render(request, 'app/dashboard.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registracija uspješna." )
			return redirect("app:dashboard")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="app/register.html", context={"register_form":form})

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
				return redirect("app:dashboard")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = UserLoginForm()
	return render(request=request, template_name="app/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("app:dashboard")


def password_reset_request(request):
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
	password_reset_form = ResetPasswordForm()
	return render(request=request, template_name="app/password/password_reset.html", context={"password_reset_form":password_reset_form})