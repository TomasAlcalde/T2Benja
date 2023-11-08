def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item in inventario:
        inventario.remove(item)  #Elimina primera instancia del ítem en el inventario
        return True, inventario.copy()
    else:    
       return False, inventario.copy()