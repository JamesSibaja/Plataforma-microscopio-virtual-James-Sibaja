.PHONY: setup run

# Configurar el entorno
setup:
    # Instalar los requisitos del proyecto Django
	sudo apt-get remove docker docker-engine docker.io containerd runc

	sudo apt-get update

	sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

	echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

	sudo apt-get update

	sudo apt-get install docker-ce docker-ce-cli containerd.io
	sudo apt-get install python3-pip
	pip3 install -r requirements.txt

    # Iniciar y configurar las bases de datos PostgreSQL
	docker-compose up -d
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

    # Crear un superusuario (cambiar los valores de acuerdo a tus necesidades)
	docker-compose exec web python manage.py createsuperuser --username=postgres --email=jsibajagranados2@gmail.com

# Arrancar el servidor Django y Celery
run:
	docker-compose up