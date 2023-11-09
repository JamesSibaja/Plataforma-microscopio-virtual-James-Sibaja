.PHONY: setup run

# Configurar el entorno
# docker compose exec web python VirtualMicroscope/manage.py makemigrations

# sudo a # pip3 install -r requirements.txt
setup:
 	# sudo apt-get install docker-ce docker-ce-cli containerd.io
	export DJANGO_SETTINGS_MODULE=settings
	mkdir -p venv VirtualMicroscope/media/slide VirtualMicroscope/media/archivo
	docker compose build
	sudo apt-get install python3-pip
	

    # Iniciar y configurar las bases de datos PostgreSQL
	docker compose up -d
	docker compose exec web python VirtualMicroscope/manage.py migrate
	docker compose exec web python VirtualMicroscope/manage.py createsuperuser
	sleep 10
	
    # Crear un superusuario (cambiar los valores de acuerdo a tus necesidades)
	docker compose exec web python VirtualMicroscope/manage.py createsuperuser --username=postgres --email=jsibajagranados2@gmail.com

# Arrancar el servidor Django y Celery
run:
	export DJANGO_SETTINGS_MODULE=settings
	docker compose up