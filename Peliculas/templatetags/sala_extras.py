# from django import template

# from Peliculas.models import Reserva
# register = template.Library()

# @register.filter
# def butaca_ocupada(fila, columna, sesion):
#     # Lógica para verificar si la butaca está ocupada en la sesión actual
#     try:
#         reserva = Reserva.objects.get(sesion=sesion, fila=fila, columna=columna)
#         return True  # La butaca está ocupada
#     except Reserva.DoesNotExist:
#         return False  # La butaca está disponible