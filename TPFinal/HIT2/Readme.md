# HIT 2

Leyendo la presentacion de CUDA probamos algunos codigos en Python para probar la libreria y aprender como funciona.
Primero hicimos un simple hola mundo, y luego seguimos paso a paso como sumar dos vectores de forma paralela especificando bloques e hilos y obteniendo un indice por cada hilo.

## Descripcion del entorno utilizado

Estamos trabajando con la libreria NUMBA de Python que deja utilizar funcionalidades de NVIDIA CUDA para programar algoritmos de GPU paralelos.
Para instalar este setup se tiene que instalar ademas de Python, el Toolkit para usar CUDA que se puede descargar de la pagina de NVIDIA, y la libreria NUMBA usando `pip install numba`, asi lo pude instalar y usar sin problemas.
Estoy usando Visual Studio Code para escribir estos programas, y afortunadamente cuento con el hardware nativo necesario, cuento con una grafica NVIDIA GeForce GTX 1660 SUPER con 6GB de VRAM, y uso CUDA 12.5
