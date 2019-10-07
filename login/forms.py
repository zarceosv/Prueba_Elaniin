# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, Textarea
from login.models import Persona, Rol, Usuario

class LoginForm(forms.Form):
	usuario = forms.CharField(label='Nombre de usuario', max_length=50, required = True)
	contra = forms.CharField(label='Contraseña', max_length=50, required = True)

class NuevaPersona(ModelForm):
	qs_usuario =forms.ModelChoiceField(queryset = Rol.objects.all().order_by('nombre'),
										)
	class Meta:
		model = Persona
		fields = ['apellido', 'nombre',]

class NuevoUsuario(ModelForm):
	class Meta:
		model = Usuario
		fields = ['nombre_usuario', 'contra']


class ImagenPerfil(forms.ModelForm):
	class Meta:
		model = Persona
		fields = ('foto', )

