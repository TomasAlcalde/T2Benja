def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    if nombre not in usuarios_no_permitidos:
        
        return True
    
    else:
        return False



def serializar_mensaje(mensaje: str) -> bytearray:
    if not mensaje:
        return bytearray()  # Retornar un bytearray vacío en caso de

    else:
        # Codificar el mensaje utilizando UTF-8
        mensaje_codificado = mensaje.encode('utf-8', 'big')  # Codificacion big-endian
        return bytearray(mensaje_codificado)
    
    


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    # Inicializamos las tres partes A, B y C

    parte_a = bytearray()
    parte_b = bytearray()
    parte_c = bytearray()
    partes = [parte_a, parte_b, parte_c]

    contador = 0
    inverso = False

    for byte in mensaje:
        if inverso:
            partes[2 - contador % 3].append(byte)
        else:
            partes[contador % 3].append(byte)

        if contador % 3 == 2: # si ya cumplimos un ciclo, es decir el ciclo ahora es impar
            inverso = not inverso

        contador += 1

    return(partes)






def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    
    
    partes = separar_mensaje(mensaje)

    suma = partes[0][0] + partes[1][-1] + partes[2][0] #Parte de A,B,C

    if suma % 2 == 0: #si es par
        resultado = bytearray([1]) + partes[0] + partes[2] + partes[1]
        
    else:
        resultado = bytearray([0]) + partes[1] + partes[0] + partes[2]

    return resultado

    


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    long_mensaje = len(mensaje).to_bytes(4, 'big')

    # Llenar con ceros si es necesario para ajustarse a bloques de 36 bytes
    padding = bytearray(36 - len(mensaje) % 36) if len(mensaje) % 36 != 0 else bytearray()

    # Crear la lista que contendrá los bloques de bytes
    bloques = []

    # Separar el mensaje en bloques de 36 bytes
    for i in range(0, len(mensaje) + len(padding), 36):
        bloque = bytearray()

        # Agregar el número de bloque
        bloque.extend(i.to_bytes(4, 'big'))

        # Agregar el bloque de mensaje o los bytes de padding
        if i < len(mensaje):
            bloque.extend(mensaje[i:i + 36])
        else:
            bloque.extend(padding)

        bloques.append(bloque)

    # Devolver la lista con los bloques
    return [long_mensaje] + bloques
