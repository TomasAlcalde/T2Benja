import os
import json

def obtener_direccion():
    with open(os.path.join("parametros.json"), "rt", encoding="utf-8") as datos:
        data = json.load(datos)
    return data