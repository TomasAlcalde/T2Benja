def validacion_formato(nombre:str) -> bool:
    countador_mayusculas = 0
    countador_digitos = 0

    # Verificamos cada carácter en el nombre
    for caracter in nombre:
        
        if caracter.isupper():
            countador_mayusculas += 1
            
        if caracter.isdigit():
            countador_digitos += 1

    # Verificar condiciones de mayúsculas, dígitos y longitud
    if countador_mayusculas >= 1 and countador_digitos >= 1 and len(nombre) >= 3 and len(nombre) <= 16:
        return True
    else:
        return False
    


def riesgo_mortal(laberinto: list[list]) -> bool:
    
    #registramos ubicacion conejo
    fila_conejo, columna_conejo = -1, -1

    for fila, fila_datos in enumerate(laberinto):
        if "C" in fila_datos:
            columna_conejo = fila_datos.index("C")
            fila_conejo = fila
            break

    #revisamos a la derecha
    tiene_camino_derecha = False

    if fila_conejo != -1:
        columna_destino_derecha = -1
        for col in range(columna_conejo + 1, len(laberinto[fila_conejo])):
            if laberinto[fila_conejo][col] in ["LH", "CL"]:
                columna_destino_derecha = col
                break

        if columna_destino_derecha != -1:
            tiene_camino_derecha = True
            for col in range(columna_conejo + 1, columna_destino_derecha):
                if laberinto[fila_conejo][col] == "P":
                    tiene_camino_derecha = False
                    break

    #Revisamos a la izquierda
    tiene_camino_izquierda = False

    if fila_conejo != -1:
        tiene_camino_izquierda = False
        for col in range(columna_conejo - 1, -1, -1):
            if laberinto[fila_conejo][col] == "P":
                break
            elif laberinto[fila_conejo][col] in ["LH", "CR"]:
                tiene_camino_izquierda = True
                break

    #revisamos arriba

    tiene_camino_arriba = False

    if columna_conejo != -1:
        tiene_camino_arriba = False
        for fila in range(fila_conejo - 1, -1, -1):
            if laberinto[fila][columna_conejo] == "P":
                break
            elif laberinto[fila][columna_conejo] in ["LV", "CD"]:
                tiene_camino_arriba = True
                break

    #revisamos abajo

    tiene_camino_abajo = False

    if columna_conejo != -1:
        tiene_camino_abajo = False
        for fila in range(fila_conejo + 1, len(laberinto)):
            if laberinto[fila][columna_conejo] == "P":
                break
            elif laberinto[fila][columna_conejo] in ["CU", "LV"]:
                tiene_camino_abajo = True
                break

    
    if tiene_camino_abajo == True or tiene_camino_arriba == True or tiene_camino_derecha == True or tiene_camino_izquierda == True:
        return True
        
    else:
        return False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item in inventario:
        inventario.remove(item)  #Elimina primera instancia del ítem en el inventario
        return True, inventario.copy()
    
    else:
        
        return False, inventario.copy()
    


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    if cantidad_lobos == 0 or PUNTAJE_LOBO == 0:
        return 0.0
    puntaje_nivel = (tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO)
    puntaje_nivel = round(puntaje_nivel, 2)  # Redondear a dos decimales
    
    return puntaje_nivel
    


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    conejo_x, conejo_y = -1, -1
    for fila, fila_datos in enumerate(laberinto):
        if 'C' in fila_datos:
            conejo_x = fila_datos.index('C')
            conejo_y = fila
            break

    if conejo_x == -1 or conejo_y == -1:
        return False  # Conejochico no esta en el laberinto

    # 
    if tecla == 'W':
        
        # Movimiento hacia arriba
        if conejo_y > 0 and laberinto[conejo_y - 1][conejo_x] != 'P':
            return True
    elif tecla == 'A':
        
        # Movimiento hacia la izquierda
        if conejo_x > 0 and laberinto[conejo_y][conejo_x - 1] != 'P':
            return True
    elif tecla == 'S':
        
        # Movimiento hacia abajo
        if conejo_y < len(laberinto) - 1 and laberinto[conejo_y + 1][conejo_x] != 'P':
            return True
    elif tecla == 'D':
        # Movimiento hacia la derecha
        if conejo_x < len(laberinto[conejo_y]) - 1 and laberinto[conejo_y][conejo_x + 1] != 'P':
            return True

    return False  # La dirección no es válida


