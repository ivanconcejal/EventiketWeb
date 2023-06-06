# Generated by Django 4.2.1 on 2023-06-01 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Peliculas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fila', models.IntegerField()),
                ('columna', models.IntegerField()),
                ('sesion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Peliculas.sesiones')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
