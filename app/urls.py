from django.urls import path, include
from .views import *

app_name = 'app'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name= 'logout'),
    path('register/', register_request, name='register'),
    path('password_reset/', password_reset_request, name='password_reset'),
]