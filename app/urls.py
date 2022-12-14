from django.urls import path #, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'app'

urlpatterns = [
    path('', login_request, name='login'),
    path('naslovna/', naslovna, name='naslovna'),
    path('profili/', profili, name='profili'),
    path('logout/', logout_request, name= 'logout'),
    path('register/', register_request, name='register'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('nova_objava/', nova_objava, name='nova_objava'),
    path('objava/<int:pk>', objava, name='objava'),
    path('objava/<int:objava_id>/brisi_objavu/', brisi_objavu, name='brisi_objavu'),
    path('objava/<int:objava_id>/brisi_komentar/<int:komentar_id>/', brisi_komentar, name='brisi_komentar'),
    path('profil/<int:pk>', profil, name='profil'),
    path('profil/<int:pk>/prate/', prate, name='prate'),
    path('profil/<int:pk>/prati/', prati, name='prati'),
    path('uredi_profil/', uredi_profil, name='uredi_profil'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)