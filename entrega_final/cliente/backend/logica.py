from PyQt6.QtCore import pyqtSignal, QObject

class LogicaLogin(QObject):

    senal_resultado_login = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def validacion_formato(self, nombre:str) -> bool:
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
            self.senal_resultado_login.emit(True)
        else:
            self.senal_resultado_login.emit(False)
    

class LogicaJuego(QObject):

    senal_resultado_movimiento = pyqtSignal(list, str, bool, str)
    senal_resultado_movimiento_lobo = pyqtSignal(list, int, str, bool, str)
    senal_resultado_movimiento_zanahoria = pyqtSignal(list, int, int, int, int, str, str)
    senal_nuevo_nivel = pyqtSignal()
    senal_resultado_borrar = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def validar_direccion(self, laberinto: list, tecla: str) -> (list, str, bool, str):
        conejo_x, conejo_y = -1, -1
        for fila, fila_datos in enumerate(laberinto):
            if 'C' in fila_datos:
                conejo_x = fila_datos.index('C')
                conejo_y = fila
                break


        if tecla == 'W':
            # Movimiento hacia arriba
            if conejo_y > 0 and (laberinto[conejo_y - 1][conejo_x] == 'LV' or laberinto[conejo_y - 1][conejo_x] == 'LH' or laberinto[conejo_y - 1][conejo_x] == 'Z'):
                for y in range(16):
                    for x in range(16):
                        if laberinto[y][x] == "E":
                            self.entrada = [x, y]
                            laberinto[y][x] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "W", False, "M")
            elif conejo_y > 0 and laberinto[conejo_y - 1][conejo_x] != 'P':
                laberinto[conejo_y - 1][conejo_x] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "W", True, "V")
            else:
                self.senal_resultado_movimiento.emit(laberinto, "W", False, "V")
        elif tecla == 'A':
            # Movimiento hacia la izquierda
            if conejo_x > 0 and (laberinto[conejo_y][conejo_x -1] == 'LV' or laberinto[conejo_y][conejo_x-1] == 'LH' or laberinto[conejo_y][conejo_x-1] == 'Z'):
                for y in range(16):
                    for x in range(16):
                        if laberinto[y][x] == "E":
                            self.entrada = [x, y]
                            laberinto[y][x] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "A", False, "M")
            elif conejo_x > 0 and laberinto[conejo_y][conejo_x - 1] != 'P':
                laberinto[conejo_y][conejo_x-1] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "A", True, "V")
            else:
                self.senal_resultado_movimiento.emit(laberinto, "A", False, "V")
        elif tecla == 'S':
            # Movimiento hacia abajo
            if laberinto[conejo_y+1][conejo_x] == 'S':
                self.senal_nuevo_nivel.emit()
            elif conejo_y < len(laberinto) - 1 and (laberinto[conejo_y+1][conejo_x] == 'LV' or laberinto[conejo_y+1][conejo_x] == 'LH' or laberinto[conejo_y+1][conejo_x] == 'Z'):
                for y in range(16):
                    for x in range(16):
                        if laberinto[y][x] == "E":
                            self.entrada = [x, y]
                            laberinto[y][x] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "S", False, "M")
            elif conejo_y < len(laberinto) - 1 and laberinto[conejo_y + 1][conejo_x] != 'P':
                laberinto[conejo_y+1][conejo_x] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "S", True, "V")
            else:
                self.senal_resultado_movimiento.emit(laberinto, "S", False, "V")
        elif tecla == 'D':
            # Movimiento hacia la derecha
            if conejo_x < len(laberinto) - 1 and (laberinto[conejo_y][conejo_x+1] == 'LV' or laberinto[conejo_y][conejo_x+1] == 'LH' or laberinto[conejo_y][conejo_x+1] == 'Z'):
                for y in range(16):
                    for x in range(16):
                        if laberinto[y][x] == "E":
                            self.entrada = [x, y]
                            laberinto[y][x] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "D", False, "M")
            elif conejo_x < len(laberinto[conejo_y]) - 1 and laberinto[conejo_y][conejo_x + 1] != 'P':
                laberinto[conejo_y][conejo_x+1] = "C"
                laberinto[conejo_y][conejo_x] = "-"
                self.senal_resultado_movimiento.emit(laberinto, "D", True, "V")
            else:
                self.senal_resultado_movimiento.emit(laberinto, "D", False, "V")

    def movimiento_lobo(self, laberinto: list, indice:int, x: int, y: int, direccion: str) -> (list, int, str, bool, str):
        if direccion == 'abajo':
            if laberinto[y+1][x] == "P":
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "arriba", False, 'V')
            elif laberinto[y+1][x] == "C":
                laberinto[y+1][x] == "LV"
                laberinto[y][x] == "-"
                for j in range(16):
                    for i in range(16):
                        if laberinto[j][i] == "C":
                            laberinto[j][i] = "-"
                        elif laberinto[j][i] == "E":
                            self.entrada = [i, j]
                            laberinto[j][i] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "abajo", True, 'M')
            else:
                laberinto[y+1][x] == "LV"
                laberinto[y][x] == "-"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "abajo", True, 'V')
        elif direccion == 'arriba':
            if laberinto[y-1][x] == "P":
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "abajo", False, 'V')
            elif laberinto[y-1][x] == "C":
                laberinto[y-1][x] == "LV"
                laberinto[y][x] == "-"
                for j in range(16):
                    for i in range(16):
                        if laberinto[j][i] == "C":
                            laberinto[j][i] = "-"
                        elif laberinto[j][i] == "E":
                            self.entrada = [i, j]
                            laberinto[j][i] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "arriba", True, 'M')
            else:
                laberinto[y-1][x] == "LV"
                laberinto[y][x] == "-"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "arriba", True, 'V')
        elif direccion == 'izquierda':
            if laberinto[y][x-1] == "P":
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "derecha", False, 'V')
            elif laberinto[y][x-1] == "C":
                laberinto[y][x-1] == "LH"
                laberinto[y][x] == "-"
                for j in range(16):
                    for i in range(16):
                        if laberinto[j][i] == "C":
                            laberinto[j][i] = "-"
                        elif laberinto[j][i] == "E":
                            self.entrada = [i, j]
                            laberinto[j][i] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "derecha", True, 'M')
            else:
                laberinto[y][x-1] == "LH"
                laberinto[y][x] == "-"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "izquierda", True, 'V')
        elif direccion == 'derecha':
            if laberinto[y][x+1] == "P":
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "izquierda", False, 'V')
            elif laberinto[y][x+1] == "C":
                laberinto[y][x+1] == "LH"
                laberinto[y][x] == "-"
                for j in range(16):
                    for i in range(16):
                        if laberinto[j][i] == "C":
                            laberinto[j][i] = "-"
                        elif laberinto[j][i] == "E":
                            self.entrada = [i, j]
                            laberinto[j][i] = "C"
                if self.entrada != 0:
                    laberinto[self.entrada[1]][self.entrada[0]] = "C"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "derecha", True, 'M')
            else:
                laberinto[y][x+1] == "LH"
                laberinto[y][x] == "-"
                self.senal_resultado_movimiento_lobo.emit(laberinto, indice, "derecha", True, 'V')

    def movimiento_zanahoria(self, laberinto: list, indice:int, x: int, y: int, direccion: str) -> (list, int, int, int, int, str):
        zanahoria = 0
        status = 0
        conejo = "V"
        if direccion == "CD":
            d = 'abajo'
            for i in range(y+1, 16):
                if laberinto[i][x] == 'Z':
                    zanahoria = 1
                    if laberinto[i+1][x] == 'P':
                        xy = [0, 0]
                        laberinto[i][x] = '-'
                        status = 0
                    else:
                        if laberinto[i+1][x] == 'C':
                            conejo = 'M'
                            for h in range(16):
                                for u in range(16):
                                    if laberinto[h][u] == "C":
                                        laberinto[h][u] = "-"
                                    elif laberinto[h][u] == "E":
                                        self.entrada = [u, h]
                                        laberinto[h][u] = "C"
                            if self.entrada != 0:
                                laberinto[self.entrada[1]][self.entrada[0]] = "C"
                        xy = [x, i+1]
                        laberinto[i+1][x] = 'Z'
                        laberinto[i][x] = '-'
                        status = 1
                    break
            if zanahoria == 0: 
                xy = [x, y+1]
                laberinto[y+1][x] = 'Z'
                status = 1
            self.senal_resultado_movimiento_zanahoria.emit(laberinto, indice, xy[0], xy[1], status, d, conejo)
        elif direccion == "CU":
            d = 'arriba'
            for i in range(y):
                z = y-1-i
                if laberinto[z][x] == 'Z':
                    zanahoria = 1
                    if laberinto[z-1][x] == 'P':
                        xy = [0, 0]
                        laberinto[z][x] = '-'
                        status = 0
                    else:
                        if laberinto[z-1][x] == 'C':
                            conejo = 'M'
                            for h in range(16):
                                for u in range(16):
                                    if laberinto[h][u] == "C":
                                        laberinto[h][u] = "-"
                                    elif laberinto[h][u] == "E":
                                        self.entrada = [u, h]
                                        laberinto[h][u] = "C"
                            if self.entrada != 0:
                                laberinto[self.entrada[1]][self.entrada[0]] = "C"
                        xy = [x, z-1]
                        laberinto[z-1][x] = 'Z'
                        laberinto[z][x] = '-'
                        status = 1
                    break
            if zanahoria == 0: 
                xy = [x, y-1]
                laberinto[y-1][x] = 'Z'
                status = 1
            self.senal_resultado_movimiento_zanahoria.emit(laberinto, indice, xy[0], xy[1], status, d, conejo)
        elif direccion == "CD":
            d = 'derecha'
            for i in range(x+1, 16):
                if laberinto[y][i] == 'Z':
                    zanahoria = 1
                    if laberinto[y][i+1] == 'P':
                        xy = [0, 0]
                        laberinto[y][i] = '-'
                        status = 0
                    else:
                        if laberinto[y][i+1] == 'C':
                            conejo = 'M'
                            for h in range(16):
                                for u in range(16):
                                    if laberinto[h][u] == "C":
                                        laberinto[h][u] = "-"
                                    elif laberinto[h][u] == "E":
                                        self.entrada = [u, h]
                                        laberinto[h][u] = "C"
                            if self.entrada != 0:
                                laberinto[self.entrada[1]][self.entrada[0]] = "C"
                        xy = [i+1, y]
                        laberinto[y][i+1] = 'Z'
                        laberinto[y][i] = '-'
                        status = 1
                    break
            if zanahoria == 0: 
                xy = [x+1, y]
                laberinto[y][x+1] = 'Z'
                status = 1
            self.senal_resultado_movimiento_zanahoria.emit(laberinto, indice, xy[0], xy[1], status, d, conejo)
        elif direccion == "CL":
            d = 'izquierda'
            for i in range(x):
                z = x-1-i
                if laberinto[y][z] == 'Z':
                    zanahoria = 1
                    if laberinto[y][z-1] == 'P':
                        xy = [0, 0]
                        laberinto[y][z] = '-'
                        status = 0
                    else:
                        if laberinto[y][z-1] == 'C':
                            conejo = 'M'
                            for h in range(16):
                                for u in range(16):
                                    if laberinto[h][u] == "C":
                                        laberinto[h][u] = "-"
                                    elif laberinto[h][u] == "E":
                                        self.entrada = [u, h]
                                        laberinto[h][u] = "C"
                            if self.entrada != 0:
                                laberinto[self.entrada[1]][self.entrada[0]] = "C"
                        xy = [z-1, y]
                        laberinto[y][z-1] = 'Z'
                        laberinto[y][z] = '-'
                        status = 1
                    break
            if zanahoria == 0: 
                xy = [x-1, y]
                laberinto[y][x-1] = 'Z'
                status = 1
            self.senal_resultado_movimiento_zanahoria.emit(laberinto, indice, xy[0], xy[1], status, d, conejo)
        
    def borrar_enemigos(self, laberinto):
        for y in range(16):
            for x in range(16):
                if laberinto[y][x] in ['CU', 'CD', 'CL', 'CR', 'Z', 'LH', 'LV']:
                    laberinto[y][x] = '-'
        self.senal_resultado_borrar.emit(laberinto)

        





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
    



