# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Persona(models.Model):
	SEXO = sexo_choices = (
        ('M', 'Masculino'),
        ('F', 'Femenimo'),
    )
	persona_id = models.AutoField(primary_key=True)
	nombre = models.CharField("Nombre/s de la persona", max_length=50, null = True, blank = True)
	apellido = models.CharField("Apellido/s de la persona", max_length=50, null = True, blank = True)
	usuario = models.ForeignKey('Usuario', verbose_name = 'Usuario login')
	sexo = models.CharField('Sexo', max_length = 1, choices = SEXO)
	foto = models.ImageField(upload_to = 'fotos/', null = True, blank = True)
	activo = models.BooleanField("Activo", default=True)

    #falta ver lo de la imagen
	def __str__(self):
		return self.nombre

class Usuario(models.Model):
	usuario_id = models.AutoField(primary_key=True)
	nombre_usuario = models.CharField(max_length=50, null = True, blank = True)
	contra = models.CharField(max_length=50, null = True, blank = True)
	rol = models.ForeignKey('Rol', verbose_name = 'Rol del usuario')

class Rol(models.Model):
	rol_id = models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 50, null = True, blank = True)
	abreviatura = models.CharField(max_length = 3, null = True, blank = True)

	def __str__(self):
		return self.nombre

