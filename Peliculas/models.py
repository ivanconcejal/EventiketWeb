from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


# Create your models here.
class Pelicula(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    duracion_horas = models.PositiveIntegerField()
    duracion_minutos = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='peliculas')
    CLASIFICACION_EDAD_CHOICES = [
        ('+0', '+0'),
        ('+7', '+7'),
        ('+12', '+12'),
        ('+16', '+16'),
        ('+18', '+18'),
    ]
    clasificacion_edad = models.CharField(max_length=3, choices=CLASIFICACION_EDAD_CHOICES)
    precio = models.DecimalField(max_digits=5, decimal_places=2)  # Campo de precio con 5 dígitos en total y 2 decimales
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'pelicula'
        verbose_name_plural = 'peliculas'

    def __str__(self):
        return self.titulo
        
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    num_filas = models.PositiveIntegerField(default=0)
    num_columnas = models.PositiveIntegerField(default=0)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='salas', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Crear las butacas si no existen
        for fila in range(1, self.num_filas + 1):
            for numero in range(1, self.num_columnas + 1):
                num_butaca = (fila - 1) * self.num_columnas + numero
                Butaca.objects.get_or_create(sala=self, fila=fila, numero=numero, num_butaca=num_butaca)

    def __str__(self):
        return self.nombre


class Butaca(models.Model):
    fila = models.PositiveIntegerField()
    columna = models.PositiveIntegerField()
    num_butaca = models.PositiveIntegerField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='butacas')
    ocupada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sala', 'fila', 'columna')

    def __str__(self):
        return f'{self.sala.nombre} - Fila {self.fila} - Columna {self.columna}'


class Sesiones(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='sesiones')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sesiones', null=True, blank=True)

    class Meta:
        verbose_name = 'sesion'
        verbose_name_plural = 'sesiones'

    def __str__(self):
        return f'{self.fecha} {self.hora} - {self.pelicula.titulo}'

    def eliminar_sesiones_vencidas(self):
        now = datetime.now()
        fecha_hora = datetime.combine(self.fecha, self.hora)
        if fecha_hora < now:
            self.delete()
            # Crear nueva sesión para el día siguiente a la misma hora
            new_fecha_hora = fecha_hora + timedelta(days=1)
            nueva_sesion = Sesiones(fecha=new_fecha_hora.date(), hora=new_fecha_hora.time(), pelicula=self.pelicula, sala=self.sala)
            nueva_sesion.save()


# class Reserva(models.Model):
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     butacas_seleccionadas = models.CharField(max_length=255)
#     pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, null=True)
#     precio_total = models.DecimalField(max_digits=6, decimal_places=2)
#     confirmada = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Reserva #{self.id} - Usuario: {self.usuario.username}"
