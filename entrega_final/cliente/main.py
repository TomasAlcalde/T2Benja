import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from frontend.Ventanadeinicio import Ventanainicio
from frontend.Ventanadejuego import Ventanajuego
from backend.logica import LogicaJuego
from backend.logica_login import LogicaLogin
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
    logica_login.senal_pasar_datos_juego.connect(ventana_juego.recibir_datos)
    logica_login.senal_revisar_usuario.connect(cliente.verificar)
    ventana_inicio.senal_ventana_juego.connect(ventana_juego.abrir_ventana)
    ventana_juego.senal_tecla_movimiento.connect(logica_juego.validar_direccion)
    ventana_juego.senal_guardar_puntaje.connect(cliente.guardar_puntaje)
    logica_juego.senal_resultado_movimiento.connect(ventana_juego.mover_conejo)
    ventana_juego.senal_movimiento_lobo.connect(logica_juego.movimiento_lobo)
    logica_juego.senal_resultado_movimiento_lobo.connect(ventana_juego.mover_lobo)
    ventana_juego.senal_movimiento_zanahoria.connect(logica_juego.movimiento_zanahoria)
    logica_juego.senal_resultado_movimiento_zanahoria.connect(ventana_juego.mover_zanahoria)
    logica_juego.senal_nuevo_nivel.connect(ventana_juego.iniciar_nuevo_nivel)
    ventana_juego.senal_borrar_enemigos.connect(logica_juego.borrar_enemigos)
    logica_juego.senal_resultado_borrar.connect(ventana_juego.actualizar_tablero)
    ventana_juego.senal_recoger.connect(logica_juego.recoger_item)
    logica_juego.senal_resultado_recoger.connect(ventana_juego.anadir_item)
    ventana_juego.senal_puntaje.connect(logica_juego.calcular_puntaje)
    logica_juego.senal_resultado_puntaje.connect(ventana_juego.iniciar_nuevo_nivel)
    cliente.senal_cerrar_ventana_inicio.connect(logica_login.validacion_user_existente)
    ventana_inicio.senal_actualizar_puntajes.connect(cliente.actualizar_puntajes)
    cliente.senal_actualizar_puntajes.connect(ventana_inicio.actualizar_puntajes)
    sys.exit(app.exec())