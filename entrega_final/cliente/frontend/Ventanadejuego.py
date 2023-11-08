import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from parametros import DURACION_NIVEL_INICIAL, ANCHO_LABERINTO, LARGO_LABERINTO, VELOCIDAD_CONEJO, VELOCIDAD_LOBO, PONDERADOR_LABERINTO_1, PONDERADOR_LABERINTO_2, PONDERADOR_LABERINTO_3, VELOCIDAD_ZANAHORIA


class Ventanajuego(QWidget):

    senal_tecla_movimiento = pyqtSignal(list, str)
    senal_tecla_pausa = pyqtSignal()
    senal_movimiento_lobo = pyqtSignal(list, int, int, int, str)
    senal_movimiento_zanahoria = pyqtSignal(list, int, int, int, str)
    senal_guardar_puntaje = pyqtSignal(str, int, int, int)

    def __init__(self):
        super().__init__()
        self.tablero_actual = []
        self.conejo_index = 1
        self.conejo_posx = 0
        self.conejo_posy = 0
        self.conejo_moviendo = False
        self.direccion = ''
        self.lobos = []
        self.canones = []
        self.vidas = 3
        self.inicializarUI()

    def inicializarUI(self):
        self.setGeometry(300, 100, 1260, 960)
        self.setWindowTitle("DCConejoChico Juego")
        self.setStyleSheet("background-color: pink;")

        # Estilo para el texto utilizado en vidas y tiempo
        style_label = """
        QLabel {
            color: #FF1493; 
            font-family: 'Arial';
            font-size: 20px;
            font-weight: bold; 
        }
        """
        #Estilo Botones
        style_button = """
        QPushButton {
            background-color: white;
            border: 2px solid #FF1493;
            border-radius: 15px; 
            color: solid #FF1493;
            padding: 5px;
            font-family: 'Arial';
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: pink;
            color: white;
        }
        """
        #Estilo Cuadrado Inventario
        style_inventario = """
        QLabel {
            background-color: #FFC0CB;  
            border-radius: 15px;
            border: 2px solid #FF1493;  
            color: #FF1493;  
            padding: 5px;
            font-family: 'Arial';
            font-size: 20px;
            font-weight: bold;
        }
        """

        # Texto de tiempo
        self.label_tiempo = QLabel("Tiempo: X segundos", self)
        self.label_tiempo.move(20, 20)  
        self.label_tiempo.setStyleSheet(style_label)

        # Inicializa el contador de tiempo
        self.tiempo_restante = DURACION_NIVEL_INICIAL  #Tiempo inicia;
        self.actualizar_tiempo()


        # Texto de vidas
        self.label_vidas = QLabel(f"Vidas restantes: {self.vidas}", self)
        self.label_vidas.move(20, 50)  
        self.label_vidas.setStyleSheet(style_label)

        # Botón para Pausa
        self.boton_comenzar = QPushButton('Pausa', self)
        self.boton_comenzar.move(20, 250)
        self.boton_comenzar.setStyleSheet(style_button)

        # Botón para salir del programa
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.move(180, 250)
        self.boton_salir.setStyleSheet(style_button)
        self.boton_salir.clicked.connect(self.cerrar_programa)

        # Cuadrado del inventario
        self.label_inventario_fondo = QLabel(self)
        self.label_inventario_fondo.setGeometry(20, 300, 220, 500)  
        self.label_inventario_fondo.setStyleSheet(style_inventario)
        self.label_inventario_fondo.show()

        # Título del inventario
        self.label_inventario_titulo = QLabel("Inventario", self.label_inventario_fondo)
        self.label_inventario_titulo.move(25, 10)  
        self.label_inventario_titulo.setStyleSheet("color: #FF1493;")  


    
### ---------------------- Funciones ---------------------- ###
    def abrir_ventana(self, nombre, lvl):
        self.nombre = nombre
        self.show()
        # Crea un QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.contador_tiempo)
        self.timer.start(1000)
        self.nivel = lvl
        self.tiempo_mov = (1 / VELOCIDAD_CONEJO) * 1000 #Tiempo en milisegundos de movimiento
        self.tiempo_mov_lobo = (1 / VELOCIDAD_LOBO) * 1000 
        self.tiempo_mov_zanahoria = (1 / VELOCIDAD_LOBO) * 1000 
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.actualizar_sprite_conejo)

        
        self.cargar_mapa()

    def cargar_mapa(self):
        # Lee la ruta del archivo segun el nivel en el que este se encuentre
        if self.nivel == 1:
            ruta_archivo = 'frontend/assets/laberintos/tablero_1.txt'
        elif self.nivel == 2:
            ruta_archivo = 'frontend/assets/laberintos/tablero_2.txt'
        elif self.nivel == 3:
            ruta_archivo = 'frontend/assets/laberintos/tablero_3.txt'
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()

        # Tamaño de cada celda del laberinto, ya que el tablero es de 960x960
        self.tamano_celda = 960 // 16
        for y, linea in enumerate(lineas):
            linea_tablero = []
            celdas = linea.strip().split(',')
            for x, celda in enumerate(celdas):
                if celda != '':
                    linea_tablero.append(celda)
                    self.cargar_imagen_celda(x, y, celda, self.tamano_celda)
                    self.cargar_imagen_item(x, y, celda, self.tamano_celda)
            self.tablero_actual.append(linea_tablero)
        
        # Movimiento y colision lobos
        for i, lobo in enumerate(self.lobos):
            lobo_timer = QTimer(self)
            lobo_timer.timeout.connect(lambda: self.intentarmover_lobo(i))
            lobo_timer.start(int(self.tiempo_mov_lobo))
            lobo.append(lobo_timer)  # Agrega el QTimer a la información del lobo

        # Movimiento y colision zanahorias
        for i, canon in enumerate(self.canones):
            canon_timer = QTimer(self)
            canon_timer.timeout.connect(lambda: self.disparar_zanahoria(i))
            canon_timer.start(int(self.tiempo_mov_zanahoria))
            canon.append(canon_timer)  # Agrega el QTimer a la información del canon

    def cargar_imagen_celda(self, x, y, simbolo, tamano_celda):
        # Diccionario que asocia cada símbolo con su imagen de fondo correspondiente
        imagenes = {
            "-": "bloque_fondo.jpeg",
            "C": "bloque_fondo.jpeg",
            "P": "bloque_pared.jpeg",
            "BM": "bloque_fondo.jpeg",
            "BC": "bloque_fondo.jpeg",
            "LH": "bloque_fondo.jpeg",
            "LV": "bloque_fondo.jpeg",
            "CU": "bloque_fondo.jpeg",
            "CD": "bloque_fondo.jpeg",
            "CL": "bloque_fondo.jpeg",
            "CR": "bloque_fondo.jpeg",
            "E": "bloque_fondo.jpeg",
            "S": "bloque_fondo.jpeg",
        }

        image = imagenes[simbolo]
        ruta_imagen = f'frontend/assets/sprites/{image}'
        pixmap_fondo = QPixmap(ruta_imagen).scaled(tamano_celda, tamano_celda)
        label = QLabel(self)
        label.setPixmap(pixmap_fondo)
        label.setGeometry(300 + x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda)
        label.show()

    def cargar_imagen_item(self, x, y, simbolo, tamano_celda):
        if simbolo == "-" or simbolo == "P":
            pass
        else:
            # Diccionario que asocia cada símbolo con su imagen de item correspondiente
            imagenes = {
                "C": "conejo_abajo_1.png",
                "BM": "bomba_manzana.png",
                "E": "bloque_fondo.jpeg",
                "S": "bloque_fondo.jpeg",
                "BM": "manzana_burbuja.png",
                "BC": "congelacion_burbuja.png",
                "LH": "lobo_horizontal_derecha_1.png",
                "LV": "lobo_vertical_abajo_1.png",
                "CU": "canon_arriba.png",
                "CD": "canon_abajo.png",
                "CL": "canon_izquierda.png",
                "CR": "canon_derecha.png",
            }

            image = imagenes[simbolo]
            ruta_imagen = f'frontend/assets/sprites/{image}'
            pixmap_item = QPixmap(ruta_imagen).scaled(tamano_celda, tamano_celda)
            if simbolo == "C":
                self.conejo_label = QLabel(self)
                self.conejo_label.setPixmap(pixmap_item)
                self.conejo_label.setGeometry(300 + x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda)
                self.conejo_posx = 300 + x * tamano_celda 
                self.conejo_posy = y * tamano_celda
                self.conejo_label.show()
            elif simbolo == "LV" or simbolo == "LH":
                if simbolo == "LV":
                    d = "abajo"
                elif simbolo == "LH":
                    d = "derecha"
                label = QLabel(self)
                self.lobos.append([simbolo, 300 + x * tamano_celda, y*tamano_celda, x, y, d, 1, label])
                label.setPixmap(pixmap_item)
                label.setGeometry(300 + x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda)
                label.show()
            elif simbolo == "CU" or simbolo == "CD" or simbolo == "CR" or simbolo == "CL":
                label = QLabel(self)
                self.canones.append([simbolo, 300 + x * tamano_celda, y*tamano_celda, x, y])
                label.setPixmap(pixmap_item)
                label.setGeometry(300 + x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda)
                label.show()
            else:
                label = QLabel(self)
                label.setPixmap(pixmap_item)
                label.setGeometry(300 + x * tamano_celda, y * tamano_celda, tamano_celda, tamano_celda)
                label.show()
        
    def contador_tiempo(self):
        # Disminuye el contador de tiempo y actualiza el texto mostrado
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.actualizar_tiempo()
        else:
            self.timer.stop()
            QMessageBox.information(self, "Tiempo agotado", "¡Se acabó el tiempo!")

    def actualizar_tiempo(self):
        # Actualiza el texto de tiempo con el tiempo restante
        self.label_tiempo.setText(f"Tiempo: {self.tiempo_restante} segundos")

    def keyPressEvent(self, event):
        key = event.key() #Revisa la tecla apretada en valor numerico
        print(key)
        # Dependiendo de la letra manda la señal al backend
        if key == 68:
            tablero = self.tablero_actual
            self.senal_tecla_movimiento.emit(tablero, "D")
        elif key == 65:
            tablero = self.tablero_actual
            self.senal_tecla_movimiento.emit(tablero, "A")
        elif key == 87:
            tablero = self.tablero_actual
            self.senal_tecla_movimiento.emit(tablero, "W")
        elif key == 83:
            tablero = self.tablero_actual
            self.senal_tecla_movimiento.emit(tablero, "S")
        

    def mover_conejo(self, tablero, letra, booleano, status):
        if not booleano:
            if status == "M":
                self.tablero_actual = tablero
                for y in range(16):
                    for x in range(16):
                        if tablero[y][x] == 'C':
                            self.actualizar_conejo_entrada(x, y)
                            self.actualizar_vidas(self.vidas - 1)
                        
        else:   
            self.tablero_actual = tablero
            self.direccion = letra
            self.conejo_moviendo = True
            self.conejo_index = 1  # Reinicia el índice del sprite
            self.timer_movimiento.start(int(self.tiempo_mov // 4))  # Inicia el temporizador para la animación
                
    def actualizar_sprite_conejo(self):
        if not self.conejo_moviendo:
            return

        # Actualiza la posición del conejo basado en la dirección
        if self.direccion == "D":
            self.conejo_posx += 960 // (16 * 4)
            ruta_sprite = f'frontend/assets/sprites/conejo_derecha_{self.conejo_index}.png'
        elif self.direccion == "A":
            self.conejo_posx -= 960 // (16 * 4)
            ruta_sprite = f'frontend/assets/sprites/conejo_izquierda_{self.conejo_index}.png'
        elif self.direccion == "W":
            self.conejo_posy -= 960 // (16 * 4)
            ruta_sprite = f'frontend/assets/sprites/conejo_arriba_{self.conejo_index}.png'
        elif self.direccion == "S":
            self.conejo_posy += 960 // (16 * 4)
            ruta_sprite = f'frontend/assets/sprites/conejo_abajo_{self.conejo_index}.png'

        # Actualiza el sprite del conejo
        pixmap_conejo = QPixmap(ruta_sprite).scaled(960 // 16, 960 // 16)
        self.conejo_label.setPixmap(pixmap_conejo)
        self.conejo_label.setGeometry(self.conejo_posx, self.conejo_posy, 960 // 16, 960 // 16)
        self.conejo_label.raise_()

        # Incrementa el índice del sprite y reinicia si es necesario
        self.conejo_index += 1
        if self.conejo_index > 4:
            self.conejo_index = 1
            self.conejo_moviendo = False
            if self.direccion == "D":
                direccion = "derecha"
            elif self.direccion == "A":
                direccion = "izquierda"
            elif self.direccion == "W":
                direccion = "arriba"
            elif self.direccion == "S":
                direccion = "abajo"
            ruta_sprite = f'frontend/assets/sprites/conejo_{direccion}_{self.conejo_index}.png'
            pixmap_conejo = QPixmap(ruta_sprite).scaled(960 // 16, 960 // 16)
            self.conejo_label.setPixmap(pixmap_conejo)
            self.conejo_label.setGeometry(self.conejo_posx, self.conejo_posy, 960 // 16, 960 // 16)
            self.conejo_label.raise_()
            self.timer_movimiento.stop()

    def intentarmover_lobo(self, indice_lobo):
        lobo = self.lobos[indice_lobo]
        direccion_actual = lobo[5]  
        self.senal_movimiento_lobo.emit(self.tablero_actual, indice_lobo, lobo[3], lobo[4], direccion_actual)

    def mover_lobo(self, tablero, indice, direccion, booleano, status):
        print(indice, direccion, status)
        if booleano == False:
            self.lobos[indice][5] = direccion
    
        else:
            if status == "M":
                self.tablero_actual = tablero
                for y in range(16):
                    for x in range(16):
                        if tablero[y][x] == 'C':
                            self.actualizar_conejo_entrada(x, y)
                            self.actualizar_vidas(self.vidas - 1)
            self.tablero_actual = tablero
            if direccion == 'abajo':
                self.lobos[indice][4] += 1
            elif direccion == 'arriba':
                self.lobos[indice][4] -= 1
            elif direccion == 'izquierda':
                self.lobos[indice][3] -= 1
            elif direccion == 'derecha':
                self.lobos[indice][3] += 1
            self.lobos[indice][5] = direccion
            self.actualizar_sprite_lobo(indice, direccion)
        
    def disparar_zanahoria(self, indice_canon):
        canon = self.canones[indice_canon]
        self.senal_movimiento_zanahoria.emit(self.tablero_actual, indice_canon, canon[3], canon[4], canon[0])
        

    def actualizar_sprite_lobo(self, indice_lobo, direccion):
        lobo = self.lobos[indice_lobo]
        # Incrementa el índice del sprite y reinicia si es necesario
        lobo[6] = (lobo[6] + 1) % 3 + 1
        if lobo[0] == "VH":
            ruta_sprite = f'frontend/assets/sprites/lobo_horinzontal_{direccion}_{lobo[6]}.png'
        else:
            ruta_sprite = f'frontend/assets/sprites/lobo_vertical_{direccion}_{lobo[6]}.png'
        pixmap_lobo = QPixmap(ruta_sprite).scaled(960 // 16, 960 // 16)
        lobo_label = lobo[7]  
        lobo_label.setPixmap(pixmap_lobo)
        # Actualiza la posición del QLabel del lobo
        lobo_label.setGeometry(300 + lobo[3] * (960 // 16), lobo[4] * (960 // 16), 960 // 16, 960 // 16)
        lobo_label.raise_()


    def actualizar_vidas(self, vidas):
        self.vidas = vidas
        self.label_vidas.setText(f"Vidas restantes: {vidas}")
        if self.vidas == 0:
            QMessageBox.warning(self, "Perdio", "No le quedan vidas")
            self.cerrar_programa()
            ### GUARDAR PUNTAJES ###

    def actualizar_conejo_entrada(self, x, y):
        ruta_imagen = f'frontend/assets/sprites/conejo_abajo_1.png'
        pixmap_item = QPixmap(ruta_imagen).scaled(self.tamano_celda, self.tamano_celda)
        self.conejo_label.setPixmap(pixmap_item)
        self.conejo_label.setGeometry(300 + x * self.tamano_celda, y * self.tamano_celda, self.tamano_celda, self.tamano_celda)
        self.conejo_posx = 300 + x * self.tamano_celda
        self.conejo_posy = y * self.tamano_celda
    
    def cerrar_programa(self):
        # Cierra el programa cuando se apreta el boton salir
        self.senal_guardar_puntaje.emit(self.nombre, 0, self.nivel - 1, self.vidas)
        self.close()  
        QApplication.instance().quit()  
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventanajuego()
    sys.exit(app.exec())
