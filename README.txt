Pasos para instalar Django con MySQL

1) instalar Django:
    sudo apt installl Django==1.11

2) instalar el controlador de python MySQL
     pip install mysqlclient==1.3.9

3) crear el schema:
    LOGIN

4) crear el usuario 
    user:       login_usuario
    contraseña: Usuario_123

5) migrate.
    python manege.py migrate

6) insertar una persona, usuario, y roles
    - LONGIN_USUARIO.CSV
    - LOGIN_ROL.CSV
    - PERSONA.CSV

7) RUN SERVER
    En la carpeta del proyecto ejecutar en consola, python manage.py runserver

8) La ruta a probar es:
    http://localhost:8000/login/
    
    nombre de usuario : zarce
    contraseña: marvin123
    rol: ADM (Administrador)
        

