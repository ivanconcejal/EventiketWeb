from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import VRegistro, cerrar_sesion, logear, perfil, verificar_cuenta, confirmar_cuenta

urlpatterns = [
    path('perfil/', perfil, name='perfil'),
    path('crear_usuario/', VRegistro.as_view(), name='vregistro'),
    path('login/', logear, name='login'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('verificar-cuenta/<str:uidb64>/<str:token>/', verificar_cuenta, name='verificar_cuenta'),
    path('confirmar-cuenta/', confirmar_cuenta, name='confirmar_cuenta'),
]