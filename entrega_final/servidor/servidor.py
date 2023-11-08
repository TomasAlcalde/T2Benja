import socket
import threading
import json
from random import randint
from leer_archivos import obtener_direccion

class Servidor:
    _id_cliente = 1
    def __init__(self, host, port):
        self.host = host
        self.port = port 
        self.clientes_conectados = {}
        self.clientes_sala_espera = {}
        self.jugadores_listos1 = 0
        self.apuestas1 = {}
        self.jugadores_listos2 = 0
        self.apuestas2 = {}
        self.contador1 = 1
        self.contador2 = 1
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()

    def bind_and_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host}:{self.port}...")
        self.accept_connections()
        print("Conectado")
    
    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread())
        thread.start()
    
    def accept_connections_thread(self):
        print("Servidor aceptando conexiones...")
        try:
            while True:
                client_socket, _ = self.socket_server.accept()
                listening_client_thread = threading.Thread(
                    target=self.thread_escuchar_cliente,
                    args=(client_socket, self._id_cliente),
                    daemon=True)
                listening_client_thread.start()
                self._id_cliente += 1
        except ConnectionError:
            print("Error de coneccion1")
            client_socket.close()
              
    def thread_escuchar_cliente(self, socket_cliente, id_cliente):
        try:
            print(f"Jugador con direccion {socket_cliente} se ha conectado")
            while True:
                    mensaje = self.recibir_mensaje(socket_cliente)
                    if len(mensaje) != 0:
                        self.manejar_comando(mensaje, socket_cliente)

        except ConnectionError:
            print(f"El jugador {id_cliente} se ha desconectado")
            socket_cliente.close()
                            
    def recibir_mensaje(self, socket_cliente):
        mensaje = socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(mensaje, byteorder = "big")
        respuesta = bytearray()

        while len(respuesta) < largo_mensaje:
            read_largo = min(4096, largo_mensaje - len(respuesta))
            respuesta.extend(socket_cliente.recv(read_largo))
        recibido = self.decodificar_mensaje(respuesta)
        return recibido

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

    def enviar(self, mensaje, sock_cliente):
        mensaje_cod = self.codificar_mensaje(mensaje)
        largo_mensaje = len(mensaje_cod).to_bytes(4, byteorder="big")
        sock_cliente.send(largo_mensaje + mensaje_cod)

    def manejar_comando(self, recibido, socket_cliente):
        comando = recibido["comando"]
        respuesta = {}
        if comando == "verificar":
            estado, nombre = self.verificar_usuario(recibido["argumento"])
            respuesta["comando"] = "verificacion"
            respuesta["argumento"] = estado
            respuesta["nombre"] = nombre
            if not estado:
                self.enviar(respuesta, socket_cliente)
                print(f"El nombre de usuario: {nombre} se encuentra bloqueado")
            else:
                nivel, puntaje, vidas = self.buscar_nivel_guardado(nombre)
                respuesta["nivel"] = nivel
                respuesta["puntaje"] = puntaje
                respuesta["vidas"] = vidas
                self.enviar(respuesta, socket_cliente)
                print(f"{nombre} es válido")
        if comando == "guardar":
            self.guardar_puntaje(recibido["argumento"])
        if comando == "puntajes":
            print("buscando puntajes")
            respuesta["comando"] = "puntajes"
            respuesta["argumento"] = self.mostrar_records()
            self.enviar(respuesta, socket_cliente)

    def verificar_usuario(self, info):
        nombre = info[0]
        with open("usuarios_bloqueados.txt", "r") as archivo:
            # Leer todas las líneas del archivo
            lineas = archivo.readlines()
        usuarios_bloqueados = [linea.strip() for linea in lineas]
        # Verificar si el nombre a verificar está en la lista de usuarios bloqueados
        if nombre in usuarios_bloqueados:
            return False, ""
        else:
            return True, nombre
    
    def guardar_puntaje(self, info):
        nombre = info[0]
        puntaje = info[1]
        nivel_superado = info[2]
        vidas_restantes = info[3]
        linea = f"{nombre} {puntaje} {nivel_superado} {vidas_restantes}"
        with open("puntajes.txt", "a") as archivo:
            archivo.write(linea + '\n')
        print(f"Se ha registrado el puntaje para el usuario {nombre}: {puntaje}")
    
    def mostrar_records(self):
        n = 5
        puntajes = self.leer_puntajes()
        if len(puntajes) < 5:
            n = len(puntajes)
        puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)
        mejores_puntajes = puntajes_ordenados[:n]
        if len(mejores_puntajes) < 5:
            mejores_puntajes += [("", 0)] * (5 - len(mejores_puntajes))
        return mejores_puntajes

    def buscar_nivel_guardado(self, nombre):
        with open("puntajes.txt", "r") as archivo:
            lineas = archivo.readlines()
        for linea in lineas:
            datos = linea.strip().split()
            if datos[0] == nombre and datos[2] < 3 and datos[3] > 0:
                return datos[2], datos[1], datos[3]
        return 1, 0, 3
    
    def leer_puntajes(self):
        puntajes = []
        with open("puntajes.txt", "r") as archivo:
            for linea in archivo:
                nombre, puntaje, nivel, vidas = linea.strip().split()
                puntajes.append((nombre, int(puntaje)))
        return puntajes

