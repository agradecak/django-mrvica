from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'app'

urlpatterns = [
    path('homepage/', homepage, name='homepage'),
    path('', login_request, name='login'),
    path('logout/', logout_request, name= 'logout'),
    path('register/', register_request, name='register'),
    path('password_reset/', password_reset_request, name='password_reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)