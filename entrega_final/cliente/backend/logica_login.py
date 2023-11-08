from PyQt6.QtCore import pyqtSignal, QObject

class LogicaLogin(QObject):

    senal_resultado_login = pyqtSignal(bool)
    senal_revisar_usuario = pyqtSignal(str)
    senal_pasar_datos_juego = pyqtSignal(str, int, int, int)

    def __init__(self):
        super().__init__()

    def validacion_formato(self, nombre:str) -> bool:
        self.nombre = nombre
        countador_mayusculas = 0
        countador_digitos = 0

        # Verificamos cada carácter en el nombre
        for caracter in nombre:
            
            if caracter.isupper():
                countador_mayusculas += 1
                
            if caracter.isdigit():
                countador_digitos += 1

        # Verificar condiciones de mayúsculas, dígitos y longitud
        if countador_mayusculas >= 1 and countador_digitos >= 1 and len(nombre) >= 3 and \
            len(nombre) <= 16:
            self.senal_revisar_usuario.emit(nombre)
        else:
            self.senal_resultado_login.emit(False)
    
    def validacion_user_existente(self, valido: bool, nombre: str, nivel: int, puntaje: int, 
                                  vidas: int) -> bool:
        if valido:
            self.senal_resultado_login.emit(True)
            self.senal_pasar_datos_juego.emit(nombre, nivel, puntaje, vidas)
    