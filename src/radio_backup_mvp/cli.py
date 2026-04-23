import escanear

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
            archivos_encontrados = escanear.escaner(ruta)
            print("Archivos encontrados:")
            for archivo in archivos_encontrados[:10]:
                print(f'{archivo}')
        elif opcion == "2":
            pass
        elif opcion == "3":
            break