# Configuración Servidor.

## Configuración entorno

1. Estos son los pasos para instalar la aplicación den algun entorno.

> Instalar Apache

	sudo apt-get update
	sudo apt-get install apache2

> Instalar PIP

	sudo apt install python3-pip

> Instalar virtualenv

	sudo apt install python3-virtualenv

> Instalar Python (version 3.10 como mínimo. OPCIONAL)

	sudo apt update
	# Instalar Python 3.10 como mínimo.
	python3 --version

> Instalar mod_wsgi, esto es para la interacción de apacho con python

	sudo apt-get install libapache2-mod-wsgi-py3


> Instalar programas necesario para que se use la libreria mysql:

	sudo apt-get update
	sudo apt-get install -y libmysqlclient-dev python3-dev
	sudo apt-get install -y pkg-config

# Configuración entorno desarrollo (python).
	
> Seguir los siguientes pasos: 
		
	cd /var/www/html/
	
	sudo chmod -R 777 [carpeta_repositorio]
	cd /[carpeta_repositorio]
	virtualenv env
	sudo chmod -R 777 /env
	source env/bin/activate
	pip install -r requirements.txt

# Configuración Crons para integraciones u otras cosas.

1.  Crear archivo .env en la raiz del proyecto con el siguiente comando:

			 #  crear archivo
			sudo nano .env
			 
			 # agregar las siguientes lineas en el archivo
			 
			HOST = '[IP del servidor de base de datos]'
			USER = '[usuario]'
			PASSWORD = '[contraseña]'
			PORT = [ puerto a la base de datos (default 3306)]
			DB = '[nombre de la base de datos]'

			LOG_DIRECTORY = 'log'

			ENVIRONMENTS = "[entorno puede ser desarrollo|produccion]"


			SECRET_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGVjaCIsIm5hbWUiOiIxMDA4MjAyMzExMTAiLCJpYXQiOjE1MTY
			EXPIRE_DATE = 1
			
			
3.  Crear entorno en donde se instalaran las librerias de python:

			 # ir a la raiz del proyecto y ejecutar el siguiente comando
			 virtualenv env
			 source env/bin/activate
			 # ejecutar el archivo requirements.txt con el siguiente comando
			 pip install -r requirements

			 
4.  Levantar servicio (SOLO EN EL CASO QUE SEA NECESARIO)

			# primero se debe crear en script con extension .service, ejemplo 'tu_script.service', con la siguiente sintaxis:

			[Unit]
			Description=Tu Script

			[Service]
			ExecStart=/var/www/html/python-integraciones-out/env/bin/python /var/www/html/python-integraciones-out/index.py
			WorkingDirectory=/var/www/html/python-integraciones-out
			Restart=always
			User=nombre_de_usuario

			[Install]
			WantedBy=default.target
			
			# La ruta en ExecStart para que apunte al intérprete de Python en tu entorno virtual, que se encuentra en /var/www/html/[nombre app]/env/bin/python. Asegúrate de ajustar esto según la ubicación real de tu entorno virtual.

			# Luego, sigue los pasos para copiar el archivo de unidad, recargar la configuración de systemd y habilitar el servicio, como se mencionó en la respuesta anterior:

			sudo cp tu_script.service /etc/systemd/system/
			sudo systemctl daemon-reload
			sudo systemctl enable tu_script.service
			sudo systemctl start tu_script.service
		
			# Esto debería configurar tu script como un servicio administrado por systemd y ejecutarse con el entorno virtual especificado.


# Configuración archivo .env

> Para que la aplicacion funcione sin problemas con la base de datos y otroas variables de entorno se debe configurar un archivo dentro de la raiz de los directorios, ese archivo se llama .env, para crearlo se deben seguir los siguientes pasos.

			# ir a la raiz del proyecto y ejecutar el siguiente comando
			sudo nano .env
			
			# agregar lo siguiente (estos datos deben ir por obligación)
			DB_HOST = 'HOST DE LA BASE DE DATOS'
			DB_USER = 'USUARIO DE LA BASE DE DATOS'
			DB_PASSWORD = 'CLAVE DE LA BASE DE DATOS'
			DB_PORT = 5432
			DB_NAME = 'postgres'
			DB_TYPE = 'postgresql'

			LOG_DIRECTORY = 'logs'

			ENVIRONMENTS = "produccion"

			SECRET_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdGVjaCIsIm5hbWUiOiIxMDA4MjAyMzExMTAiLCJpYXQiOjE1>
			EXPIRE_DATE = 1
			
			# Se deben guardar los datos y reiniciar apache con sudo systemctl restart apache2

