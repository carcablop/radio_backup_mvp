from pathlib import Path

def escaner(ruta_a_escanear):
    archivos_encontrados = []
    dir_path= Path(ruta_a_escanear)

    for archivo in dir_path.rglob("*.mp4"):
        print ("Archivo Encontrado: " + archivo.stem)
        archivos_encontrados.append(archivo.stem)
    return archivos_encontrados