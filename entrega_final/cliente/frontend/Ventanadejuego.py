import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QMessageBox,
    QVBoxLayout
)
from PyQt6.QtCore import QTimer, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer

from parametros import (
    DURACION_NIVEL_INICIAL, VELOCIDAD_CONEJO, VELOCIDAD_LOBO, 
    PONDERADOR_LABERINTO_1, PONDERADOR_LABERINTO_2, 
    PONDERADOR_LABERINTO_3, VELOCIDAD_ZANAHORIA,
    PUNTAJE_LOBO, PUNTAJE_INF
)

class Ventanajuego(QWidget):

    senal_tecla_movimiento = pyqtSignal(list, str)
    senal_tecla_pausa = pyqtSignal()
    senal_movimiento_lobo = pyqtSignal(list, int, int, int, str)
    senal_movimiento_zanahoria = pyqtSignal(list, int, int, int, str)
    senal_borrar_enemigos = pyqtSignal(list)
    senal_recoger = pyqtSignal()
    senal_puntaje = pyqtSignal(int, int, int, int)
    senal_guardar_puntaje = pyqtSignal(str, int, int, int)

    def __init__(self):
        super().__init__()
        self.tablero_actual = []
        self.en_pausa = False
        self.orden_teclas_kil = ""
        self.orden_teclas_inf = ""  
        self.modo_inf = False
        self.conejo_index = 1
        self.conejo_posx = 0
        self.conejo_posy = 0
        self.conejo_moviendo = False
        self.direccion = ''
        self.lobos = []
        self.lobos_eliminados = 0
        self.canones = []
        self.vidas = 3
        self.puntaje_total = 0
        self.player = QMediaPlayer()
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
        self.boton_comenzar.clicked.connect(self.toggle_pausa)

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
        self.label_inventario_titulo.setGeometry(35, 10, 150, 40)   
        self.label_inventario_titulo.setStyleSheet("color: #FF1493;")  

        # Objetos
        self.layout_inventario = QVBoxLayout()
        self.layout_inventario.setContentsMargins(10, 50, 10, 10)
        self.layout_inventario.setSpacing(10)
        self.label_inventario_fondo.setLayout(self.layout_inventario)


    
### ---------------------- Funciones ---------------------- ###
    def abrir_ventana(self, nombre, lvl):
        self.nombre = nombre
        self.show()
        # Crea un QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.contador_tiempo)
        self.timer.start(1000)
        self.nivel = lvl
        if self.nivel == 1:
            ponderador = PONDERADOR_LABERINTO_1
        elif self.nivel == 2:
            ponderador = PONDERADOR_LABERINTO_2
        elif self.nivel == 3:
            ponderador = PONDERADOR_LABERINTO_3
        self.tiempo_mov = (1 / VELOCIDAD_CONEJO) * 1000 #Tiempo en milisegundos de movimiento
        self.tiempo_mov_lobo = (1 / VELOCIDAD_LOBO) * 1000 * ponderador
        self.tiempo_mov_zanahoria = (1 / VELOCIDAD_ZANAHORIA) * 1000 
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.actualizar_sprite_conejo)

        self.cargar_mapa()

    def recibir_datos(self, nombre, lvl, puntaje, vidas):
        self.vidas = vidas
        self.abrir_ventana(nombre, lvl)

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
            # Conecta el timeout del QTimer a una nueva función que incluye el índice.
            lobo_timer.timeout.connect(lambda i=i: self.intentar_mover_lobo_con_indice(i))
            lobo_timer.start(int(self.tiempo_mov_lobo))
            lobo.append(lobo_timer)  # Agrega el QTimer a la información del lobo

        # Movimiento y colision zanahorias
        for i, canon in enumerate(self.canones):
            canon_timer = QTimer(self)
            canon_timer.timeout.connect(lambda i=i: self.disparar_zanahoria_con_indice(i))
            canon_timer.start(int(self.tiempo_mov_zanahoria))
            canon.append(canon_timer)  # Agrega el QTimer a la información del canon
            label = QLabel(self)
            if canon[0] == "CD":
                d = 'abajo'
            elif canon[0] == "CU":
                d = 'arriba'
            elif canon[0] == "CD":
                d = 'derecha'
            elif canon[0] == "CL":
                d = 'izquierda'
            ruta_imagen = f'frontend/assets/sprites/zanahoria_{d}'
            pixmap_item = QPixmap(ruta_imagen).scaled(self.tamano_celda, self.tamano_celda)
            label.setPixmap(pixmap_item)
            label.setGeometry(300 + x * self.tamano_celda, y * self.tamano_celda, 
                              self.tamano_celda, self.tamano_celda)
            label.hide()
            canon.append(label)
            

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
                self.conejo_label.setGeometry(300 + x * tamano_celda, y * tamano_celda, 
                                              tamano_celda, tamano_celda)
                self.conejo_posx = 300 + x * tamano_celda 
                self.conejo_posy = y * tamano_celda
                self.conejo_label.show()
            elif simbolo == "LV" or simbolo == "LH":
                if simbolo == "LV":
                    d = "abajo"
                elif simbolo == "LH":
                    d = "derecha"
                label = QLabel(self)
                self.lobos.append([simbolo, 300 + x * tamano_celda, y*tamano_celda, 
                                   x, y, d, 1, label])
                label.setPixmap(pixmap_item)
                label.setGeometry(300 + x * tamano_celda, y * tamano_celda, 
                                  tamano_celda, tamano_celda)
                label.show()
            elif simbolo == "CU" or simbolo == "CD" or simbolo == "CR" or simbolo == "CL":
                label = QLabel(self)
                self.canones.append([simbolo, 300 + x * tamano_celda, y*tamano_celda, x, y])
                label.setPixmap(pixmap_item)
                label.setGeometry(300 + x * tamano_celda, y * tamano_celda, 
                                  tamano_celda, tamano_celda)
                label.show()
            else:
                label = QLabel(self)
                label.setPixmap(pixmap_item)
                label.setGeometry(300 + x * tamano_celda, y * tamano_celda, 
                                  tamano_celda, tamano_celda)
                label.show()
        
    def contador_tiempo(self):
        # Disminuye el contador de tiempo y actualiza el texto mostrado
        if not self.modo_inf:
            if self.tiempo_restante > 0:
                self.tiempo_restante -= 1
                self.actualizar_tiempo()
            else:
                self.timer.stop()
                QMessageBox.information(self, "Tiempo agotado", "¡Se acabó el tiempo!")
                self.actualizar_vidas(self.vidas - 1)
                self.timer.stop()
                self.timer_movimiento.stop()
                self.tiempo_restante = DURACION_NIVEL_INICIAL
                self.timer.start(1000)
                self.actualizar_tiempo()
                
            

    def actualizar_tiempo(self):
        # Actualiza el texto de tiempo con el tiempo restante
        self.label_tiempo.setText(f"Tiempo: {self.tiempo_restante} segundos")

    def toggle_pausa(self):
        # Esta función cambia el estado de pausa del juego
        self.en_pausa = not self.en_pausa
        if self.en_pausa:
            self.detener_juego()
        else:
            self.reanudar_juego()

    def detener_juego(self):
        # Detiene todos los timers y cualquier otra funcionalidad que deba pausarse
        self.timer.stop()
        self.timer_movimiento.stop()
        for lobo in self.lobos:
            lobo[-1].stop()
        for canon in self.canones:
            canon[-2].stop()

    def reanudar_juego(self):
        # Reanuda todos los timers y cualquier otra funcionalidad que estuviera en pausa
        self.timer.start()
        self.timer_movimiento.start()
        for lobo in self.lobos:
            lobo[-1].start()
        for canon in self.canones:
            canon[-2].start()

    def keyPressEvent(self, event):
        key = event.key() #Revisa la tecla apretada en valor numerico

        #print(key)
        # Si la letra es la "P", se pone en pausa
        if key == 80:  
            self.toggle_pausa()

        # Truco: Matar a los enemigos K + I + L
        if event.key() == 75: 
            self.orden_teclas_kil = "K"
        
        elif event.key() == 73 and self.orden_teclas_kil == "K":  
            self.orden_teclas_kil += "I"

        elif event.key() == 76 and self.orden_teclas_kil == "KI":  
            self.eliminar_enemigos()
            self.orden_teclas_kil = ""  # Resetea la secuencia después de activar el evento
        else:
            self.orden_teclas_kil = ""

        # Truco: Vidas y tiempo infinito I + N + F
        if event.key() == 73: 
            self.orden_teclas_inf = "I"
        elif event.key() == 78 and self.orden_teclas_inf == "I":  
            self.orden_teclas_inf += "N"
        elif event.key() == 70 and self.orden_teclas_inf == "IN":  
            self.activar_modo_infinito()
            self.orden_teclas_inf = ""  # Resetea la secuencia después de activar el evento
        else:
            self.orden_teclas_inf = ""

        # Si esta en pausa no funcionan las teclas
        if self.en_pausa:
            return
        
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
        elif key == 71:
            tablero = self.tablero_actual
            self.senal_recoger.emit()
    
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
            self.timer_movimiento.start(int(self.tiempo_mov // 4)) 
                
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
        self.senal_movimiento_lobo.emit(self.tablero_actual, indice_lobo, lobo[3], lobo[4], 
                                        direccion_actual)

    def intentar_mover_lobo_con_indice(self, indice_lobo):
        self.intentarmover_lobo(indice_lobo)

    def disparar_zanahoria_con_indice(self, indice_canon):
        self.disparar_zanahoria(indice_canon)

    def mover_lobo(self, tablero, indice, direccion, booleano, status):
        #print(indice,direccion, booleano)
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
        self.senal_movimiento_zanahoria.emit(self.tablero_actual, indice_canon, 
                                             canon[3], canon[4], canon[0])

    def mover_zanahoria(self, tablero, indice, x, y, status, direccion, conejo):
        self.tablero_actual = tablero
        if conejo == "M":
            self.tablero_actual = tablero
            for y in range(16):
                for x in range(16):
                    if tablero[y][x] == 'C':
                        self.actualizar_conejo_entrada(x, y)
                        self.actualizar_vidas(self.vidas - 1)
        self.actualizar_sprite_zanahoria(indice, x, y, status, direccion)
        

    def actualizar_sprite_lobo(self, indice_lobo, direccion):
        #print(self.lobos)
        lobo = self.lobos[indice_lobo]
        # Incrementa el índice del sprite y reinicia si es necesario
        lobo[6] = (lobo[6] + 1) % 3 + 1
        if lobo[0] == "LH":
            ruta_sprite = f'frontend/assets/sprites/lobo_horizontal_{direccion}_{lobo[6]}.png'
        else:
            ruta_sprite = f'frontend/assets/sprites/lobo_vertical_{direccion}_{lobo[6]}.png'
        pixmap_lobo = QPixmap(ruta_sprite).scaled(960 // 16, 960 // 16)
        lobo_label = lobo[7]  
        lobo_label.setPixmap(pixmap_lobo)
        # Actualiza la posición del QLabel del lobo
        lobo_label.setGeometry(300 + lobo[3] * (960 // 16), lobo[4] * (960 // 16), 
                               960 // 16, 960 // 16)
        lobo_label.raise_()

    def actualizar_sprite_zanahoria(self, indice_canon, x, y, status, direccion):
        canon = self.canones[indice_canon]
        if status == 0:
            canon[6].hide()
        else:
            canon[6].setGeometry(300 + x * (960 // 16), y * (960 // 16), 960 // 16, 960 // 16)
            canon[6].show()

    def actualizar_vidas(self, vidas):
        if not self.modo_inf:
            self.vidas = vidas
            self.label_vidas.setText(f"Vidas restantes: {vidas}")
            if self.vidas == 0:
                QMessageBox.warning(self, "Perdio", "No le quedan vidas")
                ########### Guardar puntaje ##########
                self.cerrar_programa()
        else:
            pass

    def activar_modo_infinito(self):
        self.modo_inf = True
        self.label_vidas.setText("Vidas restantes: ∞")
        
    def actualizar_tablero(self, tablero):
        self.tablero_actual = tablero
        #print(tablero)

    def actualizar_conejo_entrada(self, x, y):
        ruta_imagen = f'frontend/assets/sprites/conejo_abajo_1.png'
        pixmap_item = QPixmap(ruta_imagen).scaled(self.tamano_celda, self.tamano_celda)
        self.conejo_label.setPixmap(pixmap_item)
        self.conejo_label.setGeometry(300 + x * self.tamano_celda, y * self.tamano_celda, 
                                      self.tamano_celda, self.tamano_celda)
        self.conejo_posx = 300 + x * self.tamano_celda
        self.conejo_posy = y * self.tamano_celda
    
    def iniciar_nuevo_nivel(self, puntaje):
        
        if puntaje == 0.1111111:
            self.senal_puntaje.emit(self.tiempo_restante, self.vidas, 
                                    self.lobos_eliminados, PUNTAJE_LOBO)
        else: 
            if self.modo_inf == True:
                puntaje = PUNTAJE_INF
                self.modo_inf = False
            print(puntaje)
            self.puntaje_total += puntaje

            if self.nivel == 3:
                self.reproducir_sonido_victoria()
                QMessageBox.warning(self, "Ganaste!", f"Tu puntaje es:{self.puntaje_total}")
                ###### Guardar puntaje ##########
                self.cerrar_programa()

            self.timer.stop()
            self.timer_movimiento.stop()
            for lobo in self.lobos:
                lobo[-1].stop()  
            for canon in self.canones:
                canon[-2].stop()  

            # Limpiar la lista de lobos y cañones para el nuevo nivel
            self.lobos.clear()
            self.canones.clear()
            self.tablero_actual = []

            # Cargar el nuevo tablero
            self.nivel += 1

            # Reiniciar el tiempo
            self.tiempo_restante = DURACION_NIVEL_INICIAL
            self.actualizar_tiempo()

            # Reiniciar el timer del juego
            self.timer.start(1000)

            if self.nivel == 1:
                ponderador = PONDERADOR_LABERINTO_1
            elif self.nivel == 2:
                ponderador = PONDERADOR_LABERINTO_2
            elif self.nivel == 3:
                ponderador = PONDERADOR_LABERINTO_3

            self.tiempo_mov_lobo = (1 / VELOCIDAD_LOBO) * 1000 * ponderador
            self.timer_movimiento = QTimer(self)
            self.timer_movimiento.timeout.connect(self.actualizar_sprite_conejo)

            self.cargar_mapa()

    def eliminar_enemigos(self):
        # Detiene el movimiento y la generación zanahorias
        for lobo in self.lobos:
            lobo[-1].stop()  
            lobo[7].hide()   
        self.lobos.clear()  # Limpia la lista de lobos

        for canon in self.canones:
            canon[-2].stop()  
            canon[6].hide()   
        self.canones.clear() # Limpia la lista de canones
        self.senal_borrar_enemigos.emit(self.tablero_actual)

    def anadir_item(self, item):
        # Verifica qué tipo de ítem es y asigna el texto correspondiente
        if item == "BM":
            texto_item = "Bomba de manzana"
        elif item == "BC":
            texto_item = "Bomba de congelación"
        else:
            texto_item = "Ítem desconocido"
        
        # Crea un QLabel con el texto y lo agrega al layout del inventario
        label_item = QLabel(texto_item)
        label_item.setStyleSheet("color: #FF1493; font-size: 14px;") 
        self.layout_inventario.addWidget(label_item)

    def reproducir_sonido_victoria(self):
        ruta_sonido = f'frontend/assets/sonidos/victoria.mp3'
        url_sonido = QUrl.fromLocalFile(ruta_sonido)
        self.player.setSource(url_sonido)
        self.player.play()
        
    def cerrar_programa(self):
        # Cierra el programa cuando se apreta el boton salir
        self.senal_guardar_puntaje.emit(self.nombre, 0, self.nivel - 1, self.vidas)
        self.close()  
        QApplication.instance().quit()  
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventanajuego()
    sys.exit(app.exec())
