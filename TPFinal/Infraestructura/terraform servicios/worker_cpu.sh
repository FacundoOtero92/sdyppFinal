#!/bin/bash

sudo apt update
sudo apt install python3
sudo apt install python3-pip -y
pip install opencv-python numpy pika google-cloud-storage
pip install Flask


#Docker
sudo apt install docker.io -y

# Esperar  que Docker esté cargado
sleep 10

# Clonar los contenedores
sudo docker pull facundootero/worker_cpu

# Esperar  antes de ejecutar el contenedor
sleep 30

# Correr el contenedor
sudo docker run --rm --name worker_cpu -p 5000:5000 facundootero/worker_cpu