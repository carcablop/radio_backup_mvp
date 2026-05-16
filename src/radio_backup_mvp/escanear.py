from pathlib import Path
import catalogo

CARPETAS_EXCLUIDAS = ["MUSICA", "PRODUCCION", "PRODUC", "ARCHIVOS AUDIO", "VISUALES", "MUSIC", "IMAGENES"]

def escaner(ruta_a_escanear):
    print(f"Escaneando {ruta_a_escanear}")
    archivos_encontrados = []
    dir_path= Path(ruta_a_escanear)

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