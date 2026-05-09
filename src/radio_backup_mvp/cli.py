import escanear
import normalizar_nombre
from pathlib import Path

def preguntar_ruta():
    print("Ingrese la ruta de la emisora a la carpetas Programas:")
    ruta = input("> ")
    return ruta

def menu_cli():
    print("----Menu----")
    print("1. Escanear")
    print("2. Normalizar archivos seleccionados")
    print("3. Salir")

def run_cli():
    programa_archivo = []

    while True:
        menu_cli()
        opcion = input("Seleccionar una opcion: Ejmplo: 1 > ")

        if opcion == "1":
            ruta = preguntar_ruta()
            programa_archivo = escanear.escaner(ruta)

        elif opcion == "2":
            print(f"Programa Archivo opcion 2: {programa_archivo}")

            for item in programa_archivo:
                programa = item["programa"]
                archivo = item["archivo"]

                archivo_path = Path(programa) / f"{archivo}.mp3"
                nuevo_nombre = normalizar_nombre.normalizar_nombre(archivo_path)
                print(f"{archivo}.mp3 -> {nuevo_nombre}")

        elif opcion == "3":
            break
        else:            print("Opcion no valida, intente nuevamente.")