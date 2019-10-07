# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts 			import render, redirect
from django.http 				import HttpResponse, HttpResponseRedirect
from django.conf 				import settings
from django.core.files.storage 	import FileSystemStorage
from .forms 					import  LoginForm, NuevaPersona, NuevoUsuario, ImagenPerfil
from .models 					import Usuario, Persona, Rol

import json

# Create your views here.
def InitLogin(request):
	form = LoginForm()

	return render(request,'registro/login.html', {'form': form} )

def Login(request):
	if request.POST != {}:
		contra = request.POST['txt_contra']
		usuario = request.POST['txt_usuario']
		usuario = Usuario.objects.filter(nombre_usuario__iexact = usuario,
										contra__iexact = contra
										)
		
		btnEditar = ''
		btnInactivar = ''
		btnEliminar = ''
		personas = ''
		if list(usuario) != []:
			persona = Persona.objects.get(usuario = usuario)
			if usuario[0].rol.abreviatura == 'ADM':
				personas = Persona.objects.all().exclude(pk = persona.persona_id)
				btnEditar = '<button class="btn btn-success" name="btn_editar" onClick = editarUsuario($(this)) data-toggle="modal"\
								data-target="#modal_editar">Editar</button>'

				btnInactivar = '<button class="btn btn-warning" name="btn_inactivar" onClick = inactivarUsuario($(this)) data-toggle="modal"\
								data-target="#modal_confirmacion">Inactivar</button>'

				btnEliminar = '<button class="btn btn-danger" name="btn_eliminar" onClick = eliminarUsuario($(this)) data-toggle="modal"\
								data-target="#modal_confirmacion">Eliminar</button>'
			
			data = {'persona_id': persona.persona_id,
					'persona_nombre': persona.nombre,
					'persona_apellido': persona.apellido,
					'persona_sexo': persona.sexo,
					'persona_activo': persona.activo,
					'persona_rol': True if usuario[0].rol.abreviatura == 'ADM' else False,
					'persona_foto': persona.foto,
					'persona': personas,
					'usuario': '',
					'acciones': btnEditar + ' ' + btnInactivar+ ' ' + btnEliminar
					}

			return render(request, 'registro/perfil.html',data)
		else:
			data = {}
			return render(request, 'registro/login.html', {'error':'error'})
	else:
		return HttpResponse("")

def GuardarCambiosPerfil(request):
	persona = Persona.objects.filter(persona_id = request.POST['persona_id_perfil'])
	if persona[0].usuario.contra == request.POST['txt_contra']:
		rol = Rol.objects.get(abreviatura = 'ADM' if 'chk_administrador' in request.POST.keys() else 'USR')
		persona.update(nombre = request.POST['txt_nombre'],
					apellido = request.POST['txt_apellido'],
					sexo = request.POST['rd_sexo'],
					activo = True if 'chk_activo' in request.POST.keys() else False
						)
		

		print request.POST
		if request.POST.__contains__('chk_contra_nueva'):
			Usuario.objects.filter(pk = persona[0].usuario_id
									).update(rol = rol.rol_id,
									contra = request.POST['txt_contra_nueva'])
		else:
			Usuario.objects.filter(pk = persona[0].usuario_id
									).update(rol = rol.rol_id)

		return render(request, 'registro/login.html',{})
	else:
		return render(request, 'registro/login.html',{})

def InactivarUsuario(request):
	Persona.objects.filter(persona_id = request.POST['persona_id'] ).update(activo = False)
	return HttpResponse(True, content_type = 'html/text')

def EditarUsuario(request):
	persona = list(Persona.objects.filter(persona_id = request.POST['persona_id'] ).values('persona_id',
																						'nombre',
																						'apellido',
																						'sexo',
																						'activo',
																						'usuario__nombre_usuario',
																						'usuario__rol__abreviatura'))
	return HttpResponse(json.dumps(persona[0]), content_type = 'application/json')

def GuadarCambios(request):
	persona = Persona.objects.filter(persona_id = request.POST['persona_id_editar'])
	rol = Rol.objects.get(abreviatura = request.POST['rol_editar'])
	usuario_log = Usuario.objects.filter(nombre_usuario = request.POST['txt_nombre_usuario_editar'])
	if list(usuario_log) == [] or (list(usuario_log) != [] and usuario_log[0].nombre_usuario == persona[0].usuario.nombre_usuario):
		error = True
		persona.update(nombre = request.POST['txt_nombre_editar'],
					apellido = request.POST['txt_apellido_editar'],
					sexo = request.POST['sexo_editar'],
					activo = True if 'chk_activo_editar' in request.POST.keys() else False
					)

		Usuario.objects.filter(pk = persona[0].usuario_id
								).update(rol = rol.rol_id,
										nombre_usuario = request.POST['txt_nombre_usuario_editar'])
	else:
		error = False

	return HttpResponse(error, content_type = 'html/text')

def GuardarImagen(request):
	print request.POST, '------------------------------'
	print request.FILES, '******'
	persona = Persona.objects.get(pk = request.POST['persona_id_perfil'])
	persona.foto = request.FILES['validatedCustomFile']


	persona.save()
	return render(request, 'registro/login.html',{})
	#return HttpResponse(request.FILES['validatedCustomFile'], content_type = 'image/jpeg')

def Success(request):
	return HttpResponse('successfuly uploaded', content_type = 'application/json')

def EliminarUsuario(request):
	Persona.objects.filter(persona_id = request.POST['persona_id']).delete()
	return HttpResponse(True, content_type = 'html/text')

def GuadarNuevo(request):
	nombre = request.POST['txt_nombre_nuevo']
	apellido = request.POST['txt_apellido_nuevo']
	sexo = request.POST['sexo_nuevo']
	activo = True if 'chk_activo_nuevo' in request.POST.keys() else False
	nombre_usuario =  request.POST['txt_nombre_usuario_nuevo']
	contra = request.POST['txt_contra_nuevo']
	contra_repe = request.POST['txt_contra_repe_nuevo']
	rol = Rol.objects.get(abreviatura =  request.POST['rol_nuevo'])
	error = ''
	usuario_log = Usuario.objects.filter(nombre_usuario = nombre_usuario)

	if list(usuario_log) != []:
		HttpResponse(False, content_type = 'html/text')
	else:
		usu = Usuario(nombre_usuario = nombre_usuario,
					contra = contra,
					rol = rol)
		usu.save()
		persona = Persona(nombre = nombre,
						apellido = apellido,
						sexo = sexo,
						activo = activo,
						usuario = usu)
		persona.save()

	return HttpResponse(True, content_type = 'html/text')


def  ListaUsuario(request):
	btnEditar = '<button class="btn btn-success" name="btn_editar" onClick = editarUsuario($(this)) data-toggle="modal"\
				data-target="#modal_editar">Editar</button>'

	btnInactivar = '<button class="btn btn-warning" name="btn_inactivar" onClick = inactivarUsuario($(this)) data-toggle="modal"\
					data-target="#modal_confirmacion">Inactivar</button>'

	btnEliminar = '<button class="btn btn-danger" name="btn_eliminar" onClick = eliminarUsuario($(this)) data-toggle="modal"\
					data-target="#modal_confirmacion">Eliminar</button>'

	personas = list(Persona.objects.values('persona_id', 
											'nombre', 
											'apellido',
											'activo',
											'usuario__nombre_usuario',
											'sexo',
											'usuario__rol__nombre'
											).exclude(persona_id = request.POST['persona_id_perfil'])
					)
	data = {'personas': personas,
			'acciones': btnEditar + ' ' + btnInactivar + ' ' + btnEliminar 
	}
	return HttpResponse(json.dumps(data),content_type = 'application/json')
