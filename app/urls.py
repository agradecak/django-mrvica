from django.urls import path #, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'app'

urlpatterns = [
    path('naslovna/', naslovna, name='naslovna'),
    path('', login_request, name='login'),
    path('logout/', logout_request, name= 'logout'),
    path('register/', register_request, name='register'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('nova_objava/', nova_objava, name='nova_objava'),
    path('objava/<int:pk>', objava, name='objava'),
    path('profil/<int:pk>', profil, name='profil'),
    path('uredi_profil/', uredi_profil, name='uredi_profil'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)