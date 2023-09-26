.PHONY: setup run

# Configurar el entorno
setup:
 	# sudo apt-get install docker-ce docker-ce-cli containerd.io
	sudo apt-get install python3-pip
	pip3 install -r requirements.txt

    # Iniciar y configurar las bases de datos PostgreSQL
	docker compose up -d
	docker compose exec web python manage.py makemigrations
	docker compose exec web python manage.py migrate
	sleep 10
	
    # Crear un superusuario (cambiar los valores de acuerdo a tus necesidades)
	docker-compose exec web python manage.py createsuperuser --username=postgres --email=jsibajagranados2@gmail.com

# Arrancar el servidor Django y Celery
run:
	docker-compose up