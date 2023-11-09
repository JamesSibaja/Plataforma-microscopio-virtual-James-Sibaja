# Utiliza una imagen base de Python para Django
FROM python:3.10.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# # Copiar el archivo de requerimientos y crear el entorno virtual
# COPY requirements.txt /app/

COPY . /app

# Crea un directorio para el entorno virtual
RUN python -m venv venv

# Activa el entorno virtual y actualiza pip
RUN . venv/bin/activate && pip install --upgrade pip

# Instala las dependencias desde requirements.txt
RUN pip install -r requirements.txt

    # # Copiar el resto de los archivos de la aplicación
    # COPY . /app/

# Actualiza el sistema y luego instala PostgreSQL y las herramientas de línea de comandos
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Instala la biblioteca libopenslide
RUN apt-get install -y libopenslide0

# Configura las variables de entorno para Django
ENV DJANGO_SETTINGS_MODULE=VirtualMicroscope.settings

# Agrega una pausa para dar tiempo a PostgreSQL para inicializarse
RUN sleep 10

# Expone el puerto 8000 para acceder al servidor Django
EXPOSE 8000

# Instala Daphne
RUN pip install daphne

# Comando para iniciar el servidor Django
CMD ["daphne", "VirtualMicroscope.asgi:application", "--port", "8000", "--bind", "0.0.0.0"]