import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap

class Ventanainicio(QWidget):

    senal_enviar_login = pyqtSignal(str)
    senal_ventana_juego = pyqtSignal(str, int)
    senal_actualizar_puntajes = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.inicializarUI()

    def inicializarUI(self):
        self.setGeometry(300, 100, 700, 700)
        self.setWindowTitle("DCConejoChico")
        self.setStyleSheet("background-color: pink;")

        # Estilo para QLabel
        style_label = """
        QLabel {
            color: #FF1493; 
            font-family: 'Arial';
            font-size: 20px;
            font-weight: bold; 
        }
        """

        # Estilo para QLabel2
        style_label2 = """
        QLabel {
            color: #FF1493; 
            font-family: 'Arial';
            font-size: 16px;
            font-weight: bold; 
        }
        """

        # Estilo para Nombre de Usuario
        style_user = """
        QLineEdit {
            border: 2px solid #FF1493;
            border-radius: 15px; 
            padding: 5px;
            background-color: white;
            color: black;
        }

        QLineEdit::placeholder {
            color: rgba(255, 20, 147, 0.5); 
        }
        """

        # Estilo para Boton de comienzo
        style_start = """
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

        # Estilo para Cuadrado de Salon de la fama
        style_frame = """
            QFrame {
                border: 4px solid #FF1493;  
                border-radius: 15px;
            }
        """

        # Logo de DCConejoChico
        self.logo = QLabel(self)
        self.pixmap = QPixmap('frontend/assets/sprites/logo.png')
        self.logo.setPixmap(self.pixmap)
        self.logo.move(0, 80)

        # Línea de texto editable para ingresar el nombre de usuario
        self.nombre_usuario = QLineEdit(self)
        self.nombre_usuario.setGeometry(250, 200, 200, 30)
        self.nombre_usuario.setPlaceholderText("Ingrese nombre de usuario")
        self.nombre_usuario.setStyleSheet(style_user)

        # Botón para comenzar la partida
        self.boton_comenzar = QPushButton('Comenzar partida', self)
        self.boton_comenzar.move(200, 250)
        self.boton_comenzar.clicked.connect(self.comenzar_partida)
        self.boton_comenzar.setStyleSheet(style_start)

        # Marco para el "Salón de la Fama"
        self.marco_fama = QFrame(self)
        self.marco_fama.setGeometry(200, 300, 300, 200)  
        self.marco_fama.setStyleSheet(style_frame)

        
        # Sección para el "Salón de la Fama"
        self.salon_fama = QLabel(self.marco_fama)
        self.salon_fama.setText('Salón de la Fama')
        self.salon_fama.move(55, 20)
        self.salon_fama.setStyleSheet(style_label)

        # Lista de puntajes
        self.puntajes = QLabel(self.marco_fama)
        self.puntajes.setText('1. Usuario1 - 100\n2. Usuario2 - 90\n3. Usuario3 - 80\n4. Usuario4 - 70\n5. Usuario5 - 60')
        self.puntajes.move(75, 70)
        self.puntajes.setStyleSheet(style_label2)

        # Botón para salir del programa
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.move(450, 250)
        self.boton_salir.setStyleSheet(style_start)
        self.boton_salir.clicked.connect(self.cerrar_programa)

        self.show()

    #Funcion para el boton comenzar partida
    def comenzar_partida(self):
        # Obtiene el nombre de usuario de el QLineEdit para comprobarlo
        self.nombre = self.nombre_usuario.text()
        self.senal_enviar_login.emit(self.nombre)
    
    def actualizar_puntajes(self, puntajes):
        punt1 = f"1. {puntajes[0][0]} - {puntajes[0][1]}\n"
        punt2 = f"2. {puntajes[1][0]} - {puntajes[1][1]}\n"
        punt3 = f"3. {puntajes[2][0]} - {puntajes[2][1]}\n"
        punt4 = f"4. {puntajes[3][0]} - {puntajes[3][1]}\n"
        punt5 = f"5. {puntajes[4][0]} - {puntajes[4][1]}\n"
        print("ACTUALIZADO")
        self.puntajes.setText(punt1 + punt2 + punt3 + punt4 + punt5)

    def validacion_completa(self, confirmacion):
        # Llama a la función de validación con el nombre de usuario (logica.py --> backend)
        if confirmacion == True:
            self.close()  # Cierra la ventana actual
            self.senal_ventana_juego.emit(self.nombre, 1)
        else:
            # Muestra un QMessageBox informando que el usuario no es válido, y lo pide denuevo
            QMessageBox.warning(self, "Error de validación", 
                                "El formato del nombre de usuario no es válido.\n"
                                "Asegúrate de que tenga al menos una mayúscula, "
                                "un dígito y entre 3 y 16 caracteres.")
    
    #Funcion para el boton salir
    def cerrar_programa(self):
        self.close()  
        QApplication.instance().quit()  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventanainicio()
    sys.exit(app.exec())
