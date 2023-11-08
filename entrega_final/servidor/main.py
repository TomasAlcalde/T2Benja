import sys
from servidor import Servidor
from leer_archivos import obtener_direccion

if __name__ == "__main__":
    direccion = obtener_direccion()
    Servidor(direccion["host"], direccion["port"])
    
    