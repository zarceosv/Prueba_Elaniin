from django.conf.urls import url
from . import views

urlpatterns = [
	#url(r'^admin/', admin.site.urls),
	url(r'^login/', views.InitLogin, name='login'),
	url(r'^loginUsuario/', views.Login, name='loginUsuario'),
	url(r'^guardarCambiosPerfil/', views.GuardarCambiosPerfil, name='guardarCambiosPerfil'),
	url(r'^inactivarUsuario/', views.InactivarUsuario, name='inactivarUsuario'),
	url(r'^eliminarUsuario/', views.EliminarUsuario, name='eliminarUsuario'),
	url(r'^editarUsuario/', views.EditarUsuario, name='editarUsuario'),
	url(r'^guadarCambios/', views.GuadarCambios, name='guadarCambios'),
	url(r'^guardarImagen/', views.GuardarImagen, name='guardarImagen'),
	url(r'^success/', views.Success, name='success'),
	url(r'^guadarNuevo/', views.GuadarNuevo, name='guadarNuevo'),
	url(r'^actualizarListaUsuario/', views.ListaUsuario, name='actualizarListaUsuario'),


]