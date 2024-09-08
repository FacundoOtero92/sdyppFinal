import cupy as cp
import numpy as np

def main():
    # Generar 32M números aleatorios en la CPU.
    rng = np.random.default_rng(1337)
    h_vec = rng.integers(low=0, high=np.iinfo(np.int32).max, size=32 << 20, dtype=np.int32)

    # Transferir datos al dispositivo (GPU).
    d_vec = cp.asarray(h_vec)

    # Ordenar datos en el dispositivo.
    d_vec.sort()

    # Transferir datos de vuelta al host (CPU).
    h_vec_sorted = cp.asnumpy(d_vec)
    print(h_vec_sorted)

if __name__ == "__main__":
    main()
