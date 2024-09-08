import time
import numpy as np
from numba import cuda

# Definir el kernel CUDA
@cuda.jit
def add_kernel(a, b, c):
    idx = cuda.grid(1)  # Obtener el índice global del hilo
    if idx < a.size:  # Verificar que el índice está dentro del rango del arreglo
        c[idx] = a[idx] + b[idx]  # Sumar los elementos correspondientes de a y b

inicio = time.time()

# Crear arreglos de ejemplo
a = np.random.randn(400).astype(np.float32)  # Crear un arreglo con 400 elementos aleatorios
b = np.random.randn(400).astype(np.float32)  # Crear otro arreglo con 400 elementos aleatorios
c = np.empty_like(a)  # Crear un arreglo vacío para almacenar los resultados

# Copiar datos a la GPU
d_a = cuda.to_device(a)  # Copiar el arreglo a la GPU
d_b = cuda.to_device(b)  # Copiar el segundo arreglo a la GPU
d_c = cuda.device_array_like(a)  # Crear un arreglo vacío en la GPU para los resultados

# Configurar dimensiones de bloque y grid
threads_per_block = 128  # Número de hilos por bloque
blocks_per_grid = (a.size + (threads_per_block - 1)) // threads_per_block  # Número de bloques necesarios ((400 + 127) // 128) = 4

# Ejecutar kernel
# add_kernel[4, 128](d_a, d_b, d_c)
add_kernel[blocks_per_grid, threads_per_block](d_a, d_b, d_c)  # Ejecutar el kernel

# Copiar resultado de vuelta a la CPU
d_c.copy_to_host(c)  # Copiar el resultado desde la GPU a la CPU

fin = time.time()
print(fin - inicio)

# Imprimir el resultado
print(c)  # Mostrar el resultado
