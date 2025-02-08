FROM python:3.10.14-alpine3.20

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar solo el requirements.txt primero (para cacheo eficiente)
COPY requirements.txt .

# Actualizar pip y luego instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto de los archivos después de instalar dependencias
COPY . .

# Configurar el entorno para logs sin buffer
ENV PYTHONUNBUFFERED=1

# Ejecutar la aplicación
CMD ["python", "coordinator.py"]
