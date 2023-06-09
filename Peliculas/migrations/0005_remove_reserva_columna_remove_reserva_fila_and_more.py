# Generated by Django 4.2.1 on 2023-06-06 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Peliculas', '0004_rename_numero_butaca_columna_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='columna',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='fila',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='sesion',
        ),
        migrations.AddField(
            model_name='reserva',
            name='butacas_seleccionadas',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserva',
            name='confirmada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reserva',
            name='precio_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='butaca',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sala',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sesiones',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
