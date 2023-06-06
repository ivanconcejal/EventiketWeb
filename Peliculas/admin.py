from django.contrib import admin
from .models import Pelicula, Sesiones, Sala, Butaca

# Register your models here.
class PeliculasAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('titulo', 'created', 'updated')
    list_filter = ('titulo',) # Agrega el filtro por género

class SesionesAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'fecha', 'hora')
    list_filter = ('pelicula__titulo',) # Agrega el filtro por título de película

class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_filas', 'num_columnas', 'pelicula')
    list_filter = ('nombre',) # Agrega el filtro por género


class ButacaAdmin(admin.ModelAdmin):
    list_display = ('fila', 'columna', 'num_butaca', 'sala', 'ocupada')
    list_filter = ('sala', 'ocupada')
    search_fields = ('fila', 'columna', 'num_butaca', 'sala__nombre')

admin.site.register(Pelicula, PeliculasAdmin)
admin.site.register(Sesiones, SesionesAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Butaca, ButacaAdmin)