import escanear
import normalizar_nombre

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
    while True:
        menu_cli()
        opcion = input("Seleccionar una opcion: Ejmplo: 1 > ")

        if opcion == "1":
            ruta = preguntar_ruta()
            programa_archivo = escanear.escaner(ruta)   
        elif opcion == "2":
            print(f"Programa Archivo opecion 2: {programa_archivo}")
            normalizar_nombre.normalizar_nombre(programa_archivo)

        elif opcion == "3":
            break