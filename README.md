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

4. Instala las dependencias del proyecto.

- pip install -r requirements.txt


5. Crea una nueva base de datos en MySQL (Nombrarla "banco_cf")


6. Crea un archivo .env con las siguientes variables y añade los valores de acuerdo a tu sistema.

-	SECRET_KEY=django-insecure-584_!@77sjwi)t$)s&b4&r1i=jcp@98by@8_%p@p%)3hf*8izn
-	DEBUG=True
-	DB_NAME=banco_cf
-	DB_USER=<user>
-	DB_PASSWORD=<password>
-	ENCODED_KEY=5Evr_8ZYn8azghSvxiQGNN4yuAjyjEWzw5S0s_tyF3Q=
-	EMAIL_HOST_USER=<email>
-	EMAIL_HOST_PASSWORD=<password>


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

15. Iniciar Celery: En el terminal, ubicado en el directorio (ruta al repositorio local)/BancoCF (ejecutar lo siguiente en dos terminales):
-  celery -A banco_cf worker
-  celery -A banco_cf beat

Tips para operar:
- Si se crea un usuario solo se mostrará la contraseña luego de crearlo (tomar nota).
- Ingresar mail valido para probar restaurar contraseña (seguro ingresa en spam)
- Solo los usuarios precargados tienen saldo.
- Si se crea una tarjeta solo se mostrará el PIN luego de crearla (tomar nota).

Aquí abajo dejo la información pasada en limpio tanto de usuarios como tarjetas pre cargadas.

Usuarios:

Username        Password
ismael          Tr2VEjYHJj
conrado         nWkMEN4kZn
atilio          g6KwrEzJTN

Admin-user
gus             admingus

Tarjetas

Card number             PIN
4546-8574-1856-5565     4345
5595-3458-9989-7125     1595
4858-6696-5887-1578     1234
5854-6656-2587-1547     4345
4546-9896-2357-1478     0023