def obtener_estilos():
    style_label = """
        QLabel {
            color: #FF1493; 
            font-family: 'Arial';
            font-size: 20px;
            font-weight: bold; 
        }
        """
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
    return style_label, style_button, style_inventario

def obtener_imagenes_objetos():
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
    return imagenes

def obtener_imagenes_bloques():
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
    return imagenes