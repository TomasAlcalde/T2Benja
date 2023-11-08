import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from frontend.Ventanadeinicio import Ventanainicio
from frontend.Ventanadejuego import Ventanajuego
from backend.logica import LogicaLogin, LogicaJuego
from backend.cliente import Cliente



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_inicio = Ventanainicio()
    ventana_juego = Ventanajuego()

    logica_login = LogicaLogin()
    logica_juego = LogicaJuego()
    cliente = Cliente()

    ventana_inicio.senal_enviar_login.connect(logica_login.validacion_formato)
    logica_login.senal_resultado_login.connect(ventana_inicio.validacion_completa)
    logica_login.senal_revisar_usuario.connect(cliente.verificar)
    ventana_inicio.senal_ventana_juego.connect(ventana_juego.abrir_ventana)
    ventana_juego.senal_tecla_movimiento.connect(logica_juego.validar_direccion)
    ventana_juego.senal_guardar_puntaje.connect(cliente.guardar_puntaje)
    logica_juego.senal_resultado_movimiento.connect(ventana_juego.mover_conejo)
    ventana_juego.senal_movimiento_lobo.connect(logica_juego.movimiento_lobo)
    logica_juego.senal_resultado_movimiento_lobo.connect(ventana_juego.mover_lobo)
    ventana_juego.senal_movimiento_zanahoria.connect(logica_juego.movimiento_zanahoria)
    cliente.senal_cerrar_ventana_inicio.connect(logica_login.validacion_usuario)
    sys.exit(app.exec())