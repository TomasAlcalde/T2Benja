from PyQt6.QtCore import pyqtSignal, QObject
import socket
import os
import json
import threading

class Cliente(QObject):

    senal_verificar_identidad = pyqtSignal(str, str)
    senal_retar = pyqtSignal(str)
    senal_rechazo = pyqtSignal()
    senal_aceptar = pyqtSignal(str)
    senal_j1_listo = pyqtSignal(int, str)
    senal_fin = pyqtSignal(str)
    senal_cerrar_ventana_inicio = pyqtSignal(bool)
    senal_error_verificacion = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.senal_verificar_identidad.connect(self.verificar)
        
        self.senal_abrir_sala_principal = None
        self.actualizar_sala = None
        self.senal_abrir_invitacion = None
        self.senal_desabilitar = None
        self.senal_habilitar = None
        self.senal_abrir_ventana_juego = None
        self.senal_quitar_nombres = None
        self.senal_cerrar_sala_principal = None 
        self.senal_iniciar_jugada = None
        self.senal_resultados = None 
        self.senal_cerrar_juego = None 
        self.senal_abrir_ventana_fin = None 
        try:
            self.conectar_con_servidor()
            self.escuchar()
        except:
            print("Error coneccion")
    
    def conectar_con_servidor(self):
        with open(os.path.join("parametros.json"), "rt", encoding="utf-8") as datos:
            data = json.load(datos)
        self.host = data["host"]
        self.port = data["port"]
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect((self.host, self.port))
        print("Conectado")
    
    def verificar(self, nombre):
        print(nombre)
        msg = {}
        msg["comando"] = "verificar"
        msg["argumento"] = [nombre]
        mensaje_bytes = self.codificar_mensaje(msg)
        largo_mensaje = len(mensaje_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.sendall(largo_mensaje + mensaje_bytes)
    
    def guardar_puntaje(self, nombre, puntaje, nivel, vidas):
        msg = {}
        msg["comando"] = "guardar"
        msg["argumento"] = [nombre, puntaje, nivel, vidas]
        mensaje_bytes = self.codificar_mensaje(msg)
        largo_mensaje = len(mensaje_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.sendall(largo_mensaje + mensaje_bytes)

    def escuchar(self):
        thread = threading.Thread(target=self.thread_escuchar, daemon=True)
        thread.start()

    def thread_escuchar(self):
        try:
            while True:
                largo_bytes = self.socket_cliente.recv(4)
                largo_respuesta = int.from_bytes(largo_bytes, byteorder="big")
                respuesta = bytearray()

                while len(respuesta) < largo_respuesta:
                    read_largo = min(4096, largo_respuesta - len(respuesta))
                    respuesta.extend(self.socket_cliente.recv(read_largo))
                
                mensaje_decod = self.decodificar_mensaje(respuesta)
                self.manejar_comando(mensaje_decod)

        except ConnectionError:
            pass

    @staticmethod
    def codificar_mensaje(mensaje):
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode()
            return mensaje_bytes
        except json.JSONDecodeError:
            print('No se pudo codificar el mensaje.')

    @staticmethod
    def decodificar_mensaje(msg_bytes):
        try:
            mensaje = json.loads(msg_bytes)
            return mensaje
        except json.JSONDecodeError:
            print('No se pudo decodificar el mensaje.')
            return dict()
    
    def manejar_comando(self, recibido):
        comando = recibido["comando"]
        if comando == "verificacion":
            if recibido["argumento"]:
                nombre = recibido["nombre"]
                self.senal_cerrar_ventana_inicio.emit(True)
            else:
                self.senal_error_verificacion.emit()