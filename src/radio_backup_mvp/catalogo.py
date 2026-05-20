from pathlib import Path
import pandas as pd
import settings

BASE_DIR = Path(__file__).resolve().parent
RUTA_A_CATALOGO = BASE_DIR / "catalogo_programas.csv"
RUTA_A_CATALOGO_ARCHIVOS_CSV = BASE_DIR / "catalogo_archivos.csv"
#RUTA_A_CATALOGO  = Path(r"C:\Users\ferne\OneDrive\Imágenes\Datos adjuntos\Desktop\radio_backup_mvp\catalogo_programas.csv")
#RUTA_A_CATALOGO_ARCHIVOS_CSV = Path(r"C:\Users\ferne\OneDrive\Imágenes\Datos adjuntos\Desktop\radio_backup_mvp\catalogo_archivos.csv")
"""
Funcion para leer el catalogo de programas validos de la radio de un archivo csv que contienen el nombre del programa y el conductor
Args:
    la ruta al catalogo de programas validos de tipo Path

Returns:
    Un diccionario de programas y conductores

"""
def leer_catalogo_programas(RUTA_A_CATALOGO: Path):
    print("leyendo el catalogo de programas", RUTA_A_CATALOGO)
    #valido si la ruta no existe:
    if RUTA_A_CATALOGO.exists():
        df= pd.read_csv(RUTA_A_CATALOGO)
        dicc_programa_conductor = dict(zip(df["programa"], df["conductor"]))
        return dicc_programa_conductor
    print("Aviso: no hay un catalogo de programaas")
    return {}

def obtener_catalogo_csv ():
    if RUTA_A_CATALOGO_ARCHIVOS_CSV.exists():
        print("El archivo catalgo csv ya existe")
        df= pd.read_csv(RUTA_A_CATALOGO_ARCHIVOS_CSV)
        return df
    else:
        df =pd.DataFrame(columns=settings.COLUMNAS_CATALOGO)
        df.to_csv(RUTA_A_CATALOGO_ARCHIVOS_CSV, index=False)
        return df
    
def agregar_filas(data_frame: pd.DataFrame, nueva_fila: dict):
    df_actualizado= pd.concat([data_frame, pd.DataFrame([nueva_fila])], ignore_index=True)
    df_actualizado.to_csv(RUTA_A_CATALOGO_ARCHIVOS_CSV, index=False)

    return df_actualizado




