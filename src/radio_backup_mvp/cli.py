from pathlib import Path
import escanear
import normalizar_nombre


def preguntar_ruta():
    print("Ingrese la ruta de la emisora a la carpeta Programas:")
    ruta = input("> ")
    return ruta


def menu_cli():
    print("---- MENU ----")
    print("1. Escanear")
    print("2. Normalizar archivos seleccionados")
    print("3. Salir")


def run_cli():

    programas_archivos = []

    while True:

        menu_cli()

        opcion = input("Seleccionar una opcion (Ejemplo: 1) > ")

        if opcion == "1":

            ruta = preguntar_ruta()

            programas_archivos = escanear.escaner(ruta)

            if programas_archivos:
                print(f"\nSe encontraron {len(programas_archivos)} archivos.\n")
            else:
                print("\nNo se encontraron archivos.\n")

        elif opcion == "2":

            if not programas_archivos:
                print("\nNo hay archivos escaneados.")
                print("Primero debes ejecutar la opcion 1.\n")
                continue

            print("\n" + "=" * 140)
            print(f"{'PROGRAMA':<30} {'ARCHIVO ORIGINAL':<50} {'NUEVO NOMBRE'}")
            print("=" * 140)

            for item in programas_archivos:

                programa = item["programa"]

                # Convertir a Path
                archivo = Path(item["archivo"])

                nombre_original = archivo.name

                nuevo_nombre = normalizar_nombre.normalizar_nombre(
                    archivo,
                    programa
                )

                print(
                    f"{str(programa)[:29]:<30} "
                    f"{nombre_original[:49]:<50} "
                    f"{nuevo_nombre}"
                )

            print("=" * 140 + "\n")

        elif opcion == "3":

            print("Saliendo...")
            break

        else:
            print("\nOpcion invalida.\n")