# Hit 3

## CCCL

El repositorio CCCL se ocupa de unificar tres librerias muy importantes en en desarrollo de algoritmos CUDA. Se encarga de facilitar la escritura de los desarrolladores con codigo eficiente, alta calidad, y facil de usar. Estas librerias son:

- Thrust: Mejora la productividad del programador y habilita la posibilidad de portar performance entre varias GPUs y CPUs multinucleo.
- CUB: Diseñado para algoritmos paralelos de gran velocidad a traves de todas las arquitecturas de GPU. Provee algoritmos cooperativos para que los programadores CUDA puedan crear kernels personalizados.
- libcudacxx: Es la libreria estandar de CUDA en C++, provee una implementacion de C++ que funciona tanto en el host como en el device, ademas de funcionalidades especificas de CUDA como control de cache, sincronizacion de primitivas, etc.

Este repositorio se actualizo por ultima vez el 30/04/2024

## Thrust

Thrust es una libreria C++ que facilita la programación en GPUs con una interfaz de alto nivel, aumentando la productividad de los programadores. Permite C++ realizar operaciones como ordenar, escanear y transformar en la GPU mucho más rápido que con los CPUs multinúcleo.

## Ejemplo [text](https://docs.nvidia.com/cuda/thrust/index.html#vectors)

Para que funcione el ejemplo tuve que instalar una libreria CuPy que es como NumPy pero para operar en la GPU. Lo instale haciendo `pip install cupy-cuda12x`, para mi version de CUDA.

## Diferencias entre programar con CUDA "puro" y programar con Thrust/cccl

La diferencia principal esta en el nivel de abstraccion, ya que Thrust y CCCL proporcionan una interfaz de alto nivel que contienen algoritmos y estructuras de datos paralelas ya predefinidas, ademas realiza gestion automatica de memoria lo que aumenta la produccion y mantenibilidad del codigo ya que el desarrollador no necesita programar estas funcionalidades de 0. Estas funciones predefinidas estan altamente optimizadas para muchos algoritmos lo que mejora el rendimiento del codigo.
Para cerrar, estas librerias tambien son faciles de usar y contienen una sintaxis sencilla de entender, lo que ayuda al programador preocuparse mas por la logica de negocio que los algoritmos de mas bajo nivel.
