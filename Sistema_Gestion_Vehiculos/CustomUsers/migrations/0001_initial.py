# Generated by Django 4.0.6 on 2022-09-05 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SGVUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Agente', 'Agente'), ('Supervisor', 'Supervisor')], max_length=13, verbose_name='Eliga el Rol de este Usuario')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electronico')),
                ('user_name', models.CharField(max_length=50, unique=True)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Ingreso')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='Ultimo Ingreso')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]