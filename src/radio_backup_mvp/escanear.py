from pathlib import Path
import catalogo

CARPETAS_EXCLUIDAS = ["MUSICA", "PRODUCCION", "PRODUC", "ARCHIVOS AUDIO", "VISUALES", "MUSIC", "IMAGENES"]

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
    print(f"Escaneando {ruta_a_escanear}")

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

    if dir_path.exists():
        pass
    else:
        print(f"No existe la ruta {ruta_a_escanear}")
        return
    for archivo in dir_path.rglob("*.mp3"):
        ruta_relativa_archivo= archivo.relative_to(dir_path)
        programa_archivo=detectar_programa(ruta_relativa_archivo)
         
        if programa_archivo is None:
            continue
        archivos_encontrados.append(programa_archivo)
    return archivos_encontrados

def detectar_programa(archivo: Path):
    """
    Detecta el programa a partir de la carpeta 'padre' del archivo
    Args:
        archivo (Path): Archivo a detectar el programa

    Returns:
        dict: Diccionario con el programa, el conductor y nombre de el archivo

    """   
    #Primero: recorrer los directorios y subdirectorio de cada archivo, para encontrar el nombre del programa
    #obtener el directorio padre al que pertenece el archivo
    programa_encontrado = None
    conductor_encontrado = None
    nombre_archivo= archivo.stem
    CATALOGO_PROGRAMAS_CONDUCTORES = catalogo.leer_catalogo_programas(catalogo.RUTA_A_CATALOGO)
    for c_partes in archivo.parents:
        nombre_carpeta_padre= c_partes.name.upper()
        #Primer caso: que la carpeta padre se encuentra dentro del catalogo  de programas válidos de la radio y su conductor. 
        if nombre_carpeta_padre in CATALOGO_PROGRAMAS_CONDUCTORES:
            print(f'El programa encontrado es {c_partes.name} y el conductor es:{CATALOGO_PROGRAMAS_CONDUCTORES[nombre_carpeta_padre]}')
            programa_encontrado = nombre_carpeta_padre
            conductor_encontrado = CATALOGO_PROGRAMAS_CONDUCTORES[nombre_carpeta_padre]
            break
        #validar si no es el nombre de un progrma si no el nombr de un conductor pero no se sabe a que programa asociado. 
        elif nombre_carpeta_padre in CATALOGO_PROGRAMAS_CONDUCTORES.values():
            conductor_encontrado = nombre_carpeta_padre
            programa_encontrado = "desconocido"
            #caso en el que es el nombre de un conductor y no tienen programa asociado
            print(f"Es conductor: {c_partes.name}, validar el programa asociado.")
            
    if programa_encontrado is not None:
        return {"programa": programa_encontrado, "conductor": conductor_encontrado, "archivo": nombre_archivo} 
    elif conductor_encontrado is not None:
        print({"programa": programa_encontrado, "conductor": conductor_encontrado, "archivo": nombre_archivo})
        return {"programa": programa_encontrado, "conductor": conductor_encontrado, "archivo": nombre_archivo} 
    else:
        print(f"No se detectó programa ni conductor para {archivo}")
        return None

