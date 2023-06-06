from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.peliculas,name="peliculas"),
    path('sesiones/<int:sesion_id>/', views.sala_detail, name='prueba'),
    path('enviar_correo_confirmacion', views.enviar_correo_confirmacion, name='enviar_correo_confirmacion'),
    path('reserva-confirmada/', views.reserva_confirmada, name='reserva_confirmada'),
    path('reserva-error/', views.reserva_error, name='reserva_error'),
    # path('reserva/<int:sesion_id>/', views.reserva, name='reserva'),
    # path('create_paypal_order/', views.create_paypal_order, name='create_paypal_order'),
    # path('capture_paypal_order/', views.capture_paypal_order, name='capture_paypal_order'),
]