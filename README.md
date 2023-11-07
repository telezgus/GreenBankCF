# Nombre del Proyecto

Web de un banco que permite ingresar con usuario y contraseña, consultar tarjetas, saldos y realizar transferencias.
Además un usuario administrativo, que permite añadir nuevos usuarios, tarjetas y elminar estas últimas.

## Requisitos

- Redis
- MySQL

## Instalación

Pasos para instalar el proyecto en el entorno local del usuario.

1. Clonar el repositorio.
   
- git clone https://github.com/telezgus/GreenBankCF branch main

2. Crea un entorno virtual para el proyecto.

- python -m venv env

3. Activa el entorno virtual.

- source env/bin/activate  # En sistemas basados en Unix
- env\Scripts\activate  # En sistemas Windows

4. Instala las dependencias del proyecto. Generalmente, las dependencias están listadas en un archivo requirements.txt. Puedes instalarlas con pip.

- pip install -r requirements.txt


5. Crea una nueva base de datos en MySQL (Puedes nombrarla "banco_cf" o segun tu criterio)


6. Crea un archivo .env con las siguientes variables y añade los valores de acuerdo a tu sistema.

	SECRET_KEY=django-insecure-584_!@77sjwi)t$)s&b4&r1i=jcp@98by@8_%p@p%)3hf*8izn
	DEBUG=True
	DB_NAME=banco_cf
	DB_USER=<user>
	DB_PASSWORD=<password>
	ENCODED_KEY=5Evr_8ZYn8azghSvxiQGNN4yuAjyjEWzw5S0s_tyF3Q=
	EMAIL_HOST_USER=<email>
	EMAIL_HOST_PASSWORD=<password>


8. Realiza las migraciones de la base de datos.

- python manage.py makemigrations
- python manage.py migrate


9. Crea un superusuario para acceder al panel de administración de Django.

- python manage.py createsuperuser


10. Ejecuta el Script para cargar usuarios y tarjetas.
- python manage.py shell
- from scripts.load_csv import load_all


11. Configurar variables restantes para envío de emails en settings.py


12. Inicia el servidor de Django.

- python manage.py runserver


13. Ingresar en el admin de Django. En Sites cambiar DOMAIN NAME = 127.0.0.1:8000 (ajustar de acuerdo a configuracion local) y DISPLAY NAME = Green Bank CF
	(esto modifica dentro del email de reset password estas variables)(No encontré como hacerlo con comandos)

14. Iniciar Redis
- ejecutar redis-server en la terminal

15. Iniciar Celery: 
	En el terminal, ubicado en el directorio (ruta al repositorio local)/BancoCF (ejecutar lo siguiente en dos terminales):
    		-  celery -A banco_cf worker
    		-  celery -A banco_cf beat
