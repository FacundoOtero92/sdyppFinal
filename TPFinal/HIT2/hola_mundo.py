from numba import cuda

@cuda.jit
def mykernel():
    pass

def main():
    # Llamada al kernel con 1 bloque y 1 hilo
    mykernel[1, 1]()
    print("Hello World!")

if __name__ == "__main__":
    main()
