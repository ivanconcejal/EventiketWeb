from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from paypalrestsdk import configure
from paypalrestsdk import Order
from Peliculas.admin import PeliculasAdmin
from Peliculas.models import Butaca, Pelicula, Sala, Sesiones
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Create your views here.
def peliculas(request):

    peliculas=Pelicula.objects.all()
    # Eliminar sesiones vencidas y crear nuevas
    for pelicula in peliculas:
        for sesion in pelicula.sesiones.all():
            sesion.eliminar_sesiones_vencidas()

    # Actualizar lista de películas con nuevas sesiones
    peliculas = Pelicula.objects.all()
    context = {'peliculas': peliculas}
    return render(request, "Peliculas/peliculas.html", context)


@login_required
def enviar_correo_confirmacion(request):
    if request.method == 'POST':
        # Obtener las butacas seleccionadas
        butacas_seleccionadas = request.POST.getlist('butacas_seleccionadas')

        if butacas_seleccionadas:
            # Obtener los detalles de la película
            titulo = request.POST.get('titulo')
            horas = request.POST.get('horas')
            minutos = request.POST.get('minutos')
            edad = request.POST.get('edad')
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')
            precio_total = request.POST.get('precio_total', '')
            sala_id = request.POST.get('sala_id')

            # Obtener el usuario actual
            usuario = request.user
            email = usuario.email

            # Envío del correo de confirmación
            subject = 'Confirmación de reserva'
            message = f'Hola {usuario.username},\n\nGracias por tu reserva. A continuación se muestra la información de tu reserva:\n\nPelícula: {titulo}\nHoras: {horas}\nMinutos: {minutos}\nEdad: {edad}\nFecha: {fecha}\nHora: {hora}\nButacas seleccionadas: {", ".join(butacas_seleccionadas)}\nPrecio Total: {precio_total}€\n\n¡Disfruta de la película!\n\nSaludos,'
            from_email = 'eventiketweb@gmail.com'
            to_email = [email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                messages.success(request, 'Correo de confirmación enviado.')
                if butacas_seleccionadas:
                    with transaction.atomic():
                        # Obtener el objeto de sala
                        sala = Sala.objects.get(id=sala_id)

                        # Marcar las butacas como ocupadas
                        for butaca in butacas_seleccionadas:
                            fila, columna = butaca.split('-')
                            try:
                                butaca_obj = Butaca.objects.get(sala=sala, fila=fila, columna=columna)
                                butaca_obj.ocupada = True
                                butaca_obj.save()
                            except Butaca.DoesNotExist:
                                # Manejar el caso en el que la butaca no exista
                                # Puedes mostrar un mensaje de error o realizar cualquier otra acción necesaria
                                pass
                return redirect('reserva_confirmada')  # Redirigir a una página de confirmación
            except Exception as e:
                # Manejar cualquier error en el envío del correo
                print(f'Error al enviar el correo de confirmación: {str(e)}')
                messages.error(request, 'Ocurrió un error al enviar el correo de confirmación.')
                return redirect('reserva_error')  # Redirigir a una página de error de reserva

    return render(request, 'Peliculas/prueba.html')
# def sala_detail(request, sesion_id):
#     sesion = get_object_or_404(Sesiones, pk=sesion_id)
#     sala = sesion.sala
#     num_filas = sala.num_filas
#     num_columnas = sala.num_columnas
#     nombre = sala.nombre
#     titulo = sesion.pelicula.titulo
#     imagen = sesion.pelicula.imagen
#     edad = sesion.pelicula.clasificacion_edad
#     horas = sesion.pelicula.duracion_horas
#     minutos = sesion.pelicula.duracion_minutos
#     fecha = sesion.fecha
#     hora = sesion.hora
#     precio = sesion.pelicula.precio

#     if request.method == 'POST':
#         butacas_seleccionadas = request.POST.get('butacas_seleccionadas')
#         request.session['butacas_seleccionadas'] = butacas_seleccionadas
#         return redirect('reserva', sesion_id=sesion_id)

#     return render(request, 'Peliculas/sala_detail.html', {'sesion_id': sesion_id, 'num_filas': num_filas, 'num_columnas': num_columnas,
#                                                           'nombre': nombre, 'titulo': titulo, 'imagen': imagen,
#                                                           'edad': edad, 'horas': horas, 'minutos': minutos,
#                                                           'fecha': fecha, 'hora': hora, 'precio': precio})

# def sala_detail(request, sesion_id):
#     sesion = get_object_or_404(Sesiones, pk=sesion_id)
#     sala = sesion.sala
#     num_filas = sala.num_filas
#     num_columnas = sala.num_columnas
#     nombre = sala.nombre
#     titulo = sesion.pelicula.titulo
#     imagen = sesion.pelicula.imagen
#     edad = sesion.pelicula.clasificacion_edad
#     horas = sesion.pelicula.duracion_horas
#     minutos = sesion.pelicula.duracion_minutos
#     fecha = sesion.fecha
#     hora = sesion.hora
#     precio = sesion.pelicula.precio

#     if request.method == 'POST':
#         butacas_seleccionadas = request.POST.getlist('butaca')
#         request.session['butacas_seleccionadas'] = butacas_seleccionadas

def sala_detail(request, sesion_id):
    sesion = get_object_or_404(Sesiones, pk=sesion_id)
    sala = sesion.sala
    num_filas = sala.num_filas
    num_columnas = sala.num_columnas
    nombre = sala.nombre
    titulo = sesion.pelicula.titulo
    imagen = sesion.pelicula.imagen
    edad = sesion.pelicula.clasificacion_edad
    horas = sesion.pelicula.duracion_horas
    minutos = sesion.pelicula.duracion_minutos
    fecha = sesion.fecha
    hora = sesion.hora
    precio = sesion.pelicula.precio
    fila_seleccionada = 1  # Actualiza esto con la fila seleccionada desde tu lógica
    columna_seleccionada = 1  # Actualiza esto con la columna seleccionada desde tu lógica
    butacas = sala.butacas.all()

    if request.method == 'POST':
        # Obtener las butacas seleccionadas
        butacas_seleccionadas = request.POST.getlist('butaca')
        request.session['butacas_seleccionadas'] = butacas_seleccionadas

        # Actualizar el estado de las butacas en la base de datos
        for butaca in butacas_seleccionadas:
            fila, columna = butaca.split('-')
            butaca_obj = Butaca.objects.get(sala=sala, fila=fila, columna=columna)
            butaca_obj.ocupada = True
            butaca_obj.save()

        return redirect('enviar_correo_confirmacion')

    context = {
        'sesion_id': sesion_id,
        'num_filas': num_filas,
        'num_columnas': num_columnas,
        'nombre': nombre,
        'titulo': titulo,
        'imagen': imagen,
        'edad': edad,
        'horas': horas,
        'minutos': minutos,
        'fecha': fecha,
        'hora': hora,
        'precio': precio,
        'fila_seleccionada': fila_seleccionada,
        'columna_seleccionada': columna_seleccionada,
        # 'butacas': butacas
    }

    return render(request, 'Peliculas/prueba.html', context)

def reserva_confirmada(request):
    return render(request, 'peliculas/reserva_confirmada.html')

def reserva_error(request):
    return render(request, 'peliculas/reserva_error.html')

# def reserva(request, sesion_id):
#     sesion = get_object_or_404(Sesiones, pk=sesion_id)

#     if request.method == 'POST':
#         nombre_pelicula = sesion.pelicula.titulo
#         duracion = f"{sesion.pelicula.duracion_horas}h {sesion.pelicula.duracion_minutos}min"
#         precio = sesion.pelicula.precio
#         fecha = sesion.fecha
#         hora = sesion.hora

#         butacas_seleccionadas = request.POST.get('butacas_seleccionadas')
#         if butacas_seleccionadas:
#             butacas_seleccionadas = butacas_seleccionadas.split(',')

#         butacas_reservadas = []
#         for butaca_id in butacas_seleccionadas:
#             butaca = get_object_or_404(Butaca, id=butaca_id)
#             butaca.ocupada = True
#             butaca.save()
#             butacas_reservadas.append(butaca)

#         return render(request, 'Peliculas/reserva.html', {'nombre_pelicula': nombre_pelicula,
#                                                           'duracion': duracion, 'precio': precio,
#                                                           'fecha': fecha, 'hora': hora,
#                                                           'butacas_reservadas': butacas_reservadas})

#     butacas = Butaca.objects.filter(sala=sesion.sala)

#     return render(request, 'Peliculas/reserva.html', {'sesion': sesion, 'butacas': butacas})

# def resumen_reserva(request, sesion_id):
#     sesion = get_object_or_404(Sesiones, pk=sesion_id)
#     pelicula = sesion.pelicula

#     # Obtener las butacas reservadas
#     butacas_reservadas = Butaca.objects.filter(reservada=True, sesion=sesion)

#     return render(request, 'Peliculas/resumen_reserva.html', {'pelicula': pelicula, 'precio': pelicula.precio, 'butacas_reservadas': butacas_reservadas})

# def create_paypal_order(request):
#     # Configurar las credenciales de PayPal
#     configure({
#         'mode': 'sandbox',  # Cambiar a 'live' en producción
#         'client_id': 'AUesPokbfzZQl019Nd6o00OdlDhwEC8-M5XL4T424C1DFwsBeE9sMxWVdH25udMSW26Er1-UHMydFjEx',
#         'client_secret': 'ELi2hwnKzg43EHpIFWOLgdM4EwxxfxDfToVJInqUL5jR33ibmDt--R5z7VlLJp35N6gerrnUpLeI4YrM'
#     })
    
#     # Crear un objeto de orden de PayPal
#     order = Order({
#         'intent': 'CAPTURE',
#         'purchase_units': [{
#             'amount': {
#                 'currency_code': 'EUR',
#                 'value': Pelicula.precio,
#             }
#         }]
#     })
    
#     # Crear la orden en PayPal
#     if order.create():
#         order_id = order.id
#         return JsonResponse({'id': order_id})
#     else:
#         return JsonResponse({'error': order.error})

# def capture_paypal_order(request):
#     # Configurar las credenciales de PayPal
#     configure({
#         'mode': 'sandbox',  # Cambiar a 'live' en producción
#         'client_id': 'AUesPokbfzZQl019Nd6o00OdlDhwEC8-M5XL4T424C1DFwsBeE9sMxWVdH25udMSW26Er1-UHMydFjEx',
#         'client_secret': 'ELi2hwnKzg43EHpIFWOLgdM4EwxxfxDfToVJInqUL5jR33ibmDt--R5z7VlLJp35N6gerrnUpLeI4YrM'
#     })
    
#     # Obtener el ID de la orden enviado en el cuerpo de la solicitud
#     order_id = request.POST.get('orderID')
    
#     # Capturar la orden en PayPal
#     order = Order.find(order_id)
#     if order.capture():
#         capture_data = {
#             'status': order.status,
#             'id': order.id,
#             # Otros datos de la captura...
#         }
#         return JsonResponse(capture_data)
#     else:
#         return JsonResponse({'error': order.error})