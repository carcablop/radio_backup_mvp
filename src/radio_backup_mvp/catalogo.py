from pathlib import Path
import pandas as pd



print("Archivo actual:", __file__)
print("Parent:", Path(__file__).resolve().parent)

RUTA_A_CATALOGO = (
    Path(__file__).resolve().parent
    / "catalogo_programas.csv"
)

print("Ruta final:", RUTA_A_CATALOGO)
print("Existe:", RUTA_A_CATALOGO.exists())

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

