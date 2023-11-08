import json 

"""mensaje = "5e" #mensaje original
mensaje_json = json.dumps(mensaje) #Formato json (str) serializado
mensaje_bytes = mensaje_json.encode("utf-8") #Va ser lo mismo pq mensaje_json es str
largo_mensaje = len(mensaje_bytes).to_bytes(4, byteorder="little") 
print(bytes(mensaje_bytes))
a = bytearray()
b = bytearray()
c = bytearray()
for i in range (0, len(mensaje_bytes), 3): #Separo el mensaje en tres arreglos de bytes
    a.extend(mensaje_bytes[i:i+1])
    b.extend(mensaje_bytes[i+1:i+2])
    c.extend(mensaje_bytes[i+2:i+3])
print(b"\x05" in mensaje_bytes)

if b[0:1] < c[0:1]: #Voy del [0:1] para que no sea un int y sea un byte 
    for i in range(0, len(b)):
        if b[i:i+1] == b"x\05": #Nunca va a haber un \x05 en b ya que ese byte es de un numero 5 en formato int y no en str
            pass"""
def codificacion(mensaje):
    mensaje_json = json.dumps(mensaje)
    mensaje_bytes = mensaje_json.encode("utf-8")
    largo_mensaje = len(mensaje_bytes).to_bytes(4, byteorder="big")
    print(mensaje_json)
    msg_oficial = bytearray()
    a = 0
    for i in range(0, len(mensaje_bytes), 80):
        chunck = mensaje_bytes[i:i+80]
        if len(chunck) < 80:
            falta = 80 - len(chunck)
            chunck += b'\x00' * falta
        numero = a.to_bytes(4, byteorder="big")
        msg_oficial.extend(numero)
        msg_oficial.extend(chunck)
        a+=1
        print(chunck[1:2])
        print(type(chunck))
    print(msg_oficial)
    return msg_oficial

def encriptacion(mensaje):
    mensaje_json = json.dumps(mensaje) #Formato json (str) serializado
    mensaje_bytes = mensaje_json.encode("utf-8") #Va ser lo mismo pq mensaje_json es str
    largo_mensaje = len(mensaje_bytes).to_bytes(4, byteorder="big") 
    print(bytes(mensaje_bytes))
    a = bytearray()
    b = bytearray()
    c = bytearray()
    msg = bytearray()
    for i in range (0, len(mensaje_bytes), 3): #Separo el mensaje en tres arreglos de bytes
        a.extend(mensaje_bytes[i:i+1])
        b.extend(mensaje_bytes[i+1:i+2])
        c.extend(mensaje_bytes[i+2:i+3])
    print(b"\x05" in mensaje_bytes)

    if b[0:1] > c[0:1]: #Voy del [0:1] para que no sea un int y sea un byte 
        for i in range(0, len(a)):
            if a[i:i+1] == b"x\05": #Nunca va a haber un \x05 en b
                a[i:i+1] = b"x\03"
            elif a[i:i+1] == b"\x03":
                a[i:i+1] = b"\x03"

        for i in range(0, len(b)):
            if b[i:i+1] == b"x\05": #Nunca va a haber un \x05 en b
                b[i:i+1] = b"x\03"
            elif b[i:i+1] == b"\x03":
                b[i:i+1] = b"\x03"

        for i in range(0, len(c)):
            if c[i:i+1] == b"x\05": #Nunca va a haber un \x05 en b
                c[i:i+1] = b"x\03"
            elif c[i:i+1] == b"\x03":
                c[i:i+1] = b"\x03"
        n = b"\x00"
        msg.extend(a)
        msg.extend(b)
        msg.extend(c)

    else:
        msg.extend(b)
        msg.extend(a)
        msg.extend(c)
        n = b"\x01"
    msg.extend(n)
        
    print(a)
    print(b)
    print(c)
    print(msg)
    return msg

def encriptar(mensaje):
        A = bytearray()
        B = bytearray()
        mensaje_final = bytearray
        bytes_entregados = 0
        bytes_a_entregar = 1
        while bytes_entregados < len(mensaje):
            chunk_A = mensaje[bytes_entregados : bytes_entregados + 
                                min(len(mensaje[bytes_entregados:]), bytes_a_entregar)]
            if len(mensaje[bytes_entregados:]) > bytes_a_entregar:
                bytes_entregados += bytes_a_entregar
                chunk_B = mensaje[bytes_entregados : bytes_entregados + 
                                min(len(mensaje[bytes_entregados:]), bytes_a_entregar)]
                bytes_entregados += min(len(mensaje[bytes_entregados:]), bytes_a_entregar)
            else:
                bytes_entregados += len(mensaje[bytes_entregados:])
                chunk_B = b""
            A.extend(chunk_A)
            B.extend(chunk_B)
            if bytes_a_entregar == 1:
                bytes_a_entregar = 2
            else:
                bytes_a_entregar = 1
        largo_A = len(A)
        largo_B = len(B)
        print(A)
        print(B)
        if largo_A % 2 == 0:
            central_1_A = A[largo_A // 2]
            central_2_A = A[(largo_A // 2) - 1]
            suma_A = central_1_A + central_2_A
        else:
            central_1_A = A[largo_A // 2]
            central_2_A = A[(largo_A // 2) + 1]
            central_3_A = A[(largo_A // 2) - 1]
            suma_A = central_1_A + (central_2_A + central_3_A) / 2
        if largo_B % 2 == 0:
            central_1_B = B[largo_B // 2]
            central_2_B = B[(largo_B // 2) - 1]
            suma_B = central_1_B + central_2_B
        else:
            central_1_B = B[largo_B // 2]
            central_2_B = B[(largo_B // 2) + 1]
            central_3_B = B[(largo_B // 2) - 1]
            suma_B = central_1_B + (central_2_B + central_3_B) / 2
        if suma_A < suma_B:
            mensaje_final = b"\x01" + A + B
        else:
            mensaje_final = b"\x00" + B + A
        return mensaje_final
    
def desencriptar(mensaje):
    mensaje_final = bytearray()
    orden = mensaje[0]
    mensaje_enc = mensaje[1:]
    if len(mensaje_enc) % 2 == 1:
        largo_A = len(mensaje_enc) // 2 + 1
        largo_B = len(mensaje_enc) // 2
    else:
        if len(mensaje_enc) % 6 == 4:
            largo_A = len(mensaje_enc) // 2 + 1
            largo_B = len(mensaje_enc) // 2 - 1
        else:
            largo_A = len(mensaje_enc) // 2
            largo_B = len(mensaje_enc) // 2
    if orden == 1:
        A = mensaje_enc[0 : largo_A]
        B = mensaje_enc[largo_A : ]
    elif orden == 0:
        B = mensaje_enc[0 : largo_B]
        A = mensaje_enc[largo_B : ]
    print(A)
    print(B)
    bytes_entregados_A = 0
    bytes_entregados_B = 0
    bytes_a_entregar = 1
    while bytes_entregados_A + bytes_entregados_B < len(mensaje_enc):
        if bytes_entregados_A < len(A):
            chunk_A = A[bytes_entregados_A : bytes_entregados_A + min(len(A[bytes_entregados_A : ]), bytes_a_entregar)]
            mensaje_final += chunk_A
            bytes_entregados_A += min(len(A[bytes_entregados_A : ]), bytes_a_entregar)
        if bytes_entregados_B < len(B):
            chunk_B = B[bytes_entregados_B : bytes_entregados_B + min(len(B[bytes_entregados_B : ]), bytes_a_entregar)]
            mensaje_final += chunk_B
            bytes_entregados_B += min(len(B[bytes_entregados_B : ]), bytes_a_entregar)
        if bytes_a_entregar == 1:
            bytes_a_entregar = 2
        else:
            bytes_a_entregar = 1
    return mensaje_final

a = b"\x05\x08\x03\x02\x04\x03\x05\x09\x04"
b = encriptar(a)
c = desencriptar(b)
print(c)

