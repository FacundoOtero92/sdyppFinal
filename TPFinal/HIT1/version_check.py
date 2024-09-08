from numba import cuda

# Función para verificar errores de CUDA
def gpu_assert(err):
    if err != cuda.driver.Error.CUDA_SUCCESS:
        raise RuntimeError(f"GPUassert: {cuda.driver.driver.get_error_string(err)}")

# Sincronizar el dispositivo y verificar errores
try:
    cuda.synchronize()
    print("Synchronization successful.")
except cuda.CudaAPIError as e:
    gpu_assert(e.code)
