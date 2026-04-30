from pathlib import Path

CARPETAS_EXCLUIDAS = ["MUSICA", "PRODUCCION", "PRODUC", "ARCHIVOS AUDIO", "VISUALES"]

def escaner(ruta_a_escanear):
    archivos_encontrados = []
    dir_path= Path(ruta_a_escanear)

    for archivo in dir_path.rglob("*.mp3"):
        programa_archivo=detectar_programa(archivo)
        if programa_archivo is None:
            continue
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
        dict_programas_conductor_archivo["archivo"] = archivo.stem
    elif any(c_excluida in programa_encontrado.upper() for c_excluida in CARPETAS_EXCLUIDAS):
        return None
    else:
        dict_programas_conductor_archivo["programa"] = programa_encontrado
        dict_programas_conductor_archivo["archivo"] = archivo.stem
    print (dict_programas_conductor_archivo)
    return dict_programas_conductor_archivo