# Utiliza una imagen base de Python para Django
FROM python:3.10.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Instala PostgreSQL y las herramientas de línea de comandos
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Establece una contraseña para el superusuario de PostgreSQL (cámbiala por una segura)
RUN echo "postgres:microVirtual" | chpasswd

# Copia todo el contenido del proyecto al contenedor
COPY . .

# Configura las variables de entorno para Django
ENV DJANGO_SETTINGS_MODULE=VirtualMicroscope.settings

# Inicia el servicio PostgreSQL
RUN service postgresql start

# Crea una base de datos y un usuario de PostgreSQL
RUN su postgres -c 'createdb microscopio'
RUN su postgres -c 'createuser -s -r -d postgres'

# Realiza las migraciones de la base de datos
RUN python manage.py migrate

# Expone el puerto 8000 para acceder al servidor Django
EXPOSE 8000

# Comando para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]