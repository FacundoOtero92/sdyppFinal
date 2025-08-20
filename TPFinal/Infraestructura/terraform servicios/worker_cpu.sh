# #!/bin/bash

# sudo apt update
# sudo apt install python3
# sudo apt install python3-pip -y
# pip install opencv-python numpy pika google-cloud-storage
# pip install Flask


# #Docker
# sudo apt install docker.io -y

# # Esperar  que Docker esté cargado
# sleep 10

# # Clonar los contenedores
# sudo docker pull facundootero/worker_cpu

# # Esperar  antes de ejecutar el contenedor
# sleep 30

# # Correr el contenedor
# sudo docker run --rm --name worker_cpu -p 5000:5000 facundootero/worker_cpu
#!/usr/bin/env bash
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y python3 python3-pip docker.io

# Asegurar Docker arriba
systemctl enable --now docker
sleep 5

# Contenedor correcto (con guion, no guion_bajo)
docker rm -f worker-cpu || true
docker pull facundootero/worker-cpu:latest
docker run -d --restart unless-stopped --name worker-cpu -p 5000:5000 facundootero/worker-cpu:latest
