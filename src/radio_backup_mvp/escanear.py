from pathlib import Path

CARPETAS_EXCLUIDAS = ["MUSICA", "PRODUCCION", "PRODUC", "ARCHIVOS AUDIO", "VISUALES"]

from pathlib import Path

def escaner(ruta_a_escanear):
    """
    Escanea un directorio en busca de archivos multimedia (.mp3, .mp4),
    filtrando carpetas excluidas y detectando el programa asociado.

    Args:
        ruta_a_escanear (str): La ruta de la carpeta que se desea inspeccionar.

    Returns:
        list: Una lista de objetos o datos de los programas encontrados. 
              Retorna una lista vacía si la ruta no es válida.
    """
    archivos_encontrados = []
    dir_path = Path(ruta_a_escanear)

    # Verificación de existencia de la ruta
    # Corrección: Se cambió 'ruta_a_escaner' por 'ruta_a_escanear' para corregir el typo
    if not dir_path.exists():
        print(f"Error: La ruta '{ruta_a_escanear}' no existe.")
        return []

    # Búsqueda recursiva de archivos en la ruta proporcionada
    for archivo in dir_path.rglob("*"):
        # Filtrar solo archivos con extensiones .mp3 y .mp4
        if archivo.suffix.lower() in ['.mp3', '.mp4']:
            
            # Omitir el archivo si pertenece a alguna de las carpetas excluidas
            if any(excluida in archivo.parts for excluida in CARPETAS_EXCLUIDAS):
                continue

            # Intentar detectar el programa basado en el archivo encontrado
            programa_archivo = detectar_programa(archivo)
            
            # Si se detecta un programa válido, se añade a la lista de resultados
            if programa_archivo is not None:
                archivos_encontrados.append(programa_archivo)

    return archivos_encontrados

def detectar_programa(archivo: Path):
    dict_programas_conductor_archivo = {}
    programa_encontrado= archivo.parent.name
    print(f"Programa Encontrado: {programa_encontrado}")
    if programa_encontrado == "Programas" or programa_encontrado == "PROGRAMAS":
        p_encontrado = archivo.parent.parent.name
        print(f"Programa Encontrado del padre: {p_encontrado}")
        dict_programas_conductor_archivo["programa"] = p_encontrado
        dict_programas_conductor_archivo["archivo"] = archivo
    elif any(c_excluida in programa_encontrado.upper() for c_excluida in CARPETAS_EXCLUIDAS):
        return None
    else:
        dict_programas_conductor_archivo["programa"] = programa_encontrado
        dict_programas_conductor_archivo["archivo"] = archivo
    print (dict_programas_conductor_archivo)
    return dict_programas_conductor_archivo