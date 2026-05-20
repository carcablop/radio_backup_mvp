from pathlib import Path
import normalizar_nombre
import escanear
import sys
import io


def preguntar_ruta():
    print("Ingrese la ruta de la emisora a la carpeta Programas:")
    return input("> ").strip()


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

            buffer = io.StringIO()
            sys.stdout = buffer
            programas_archivos = escanear.escaner(ruta)
            sys.stdout = sys.__stdout__

            if not programas_archivos:
                print("\nNo se encontraron archivos.\n")
                continue

            C1, C2, C3 = 45, 25, 30
            sep = "-" * (C1 + C2 + C3 + 6)

            print()
            print(sep)
            print(f"  {'ARCHIVO':<{C1}} {'PROGRAMA':<{C2}} {'CONDUCTOR':<{C3}}")
            print(sep)

            programa_actual = None
            for item in sorted(programas_archivos, key=lambda x: x["programa"]):
                prog = item["programa"]
                cond = item.get("conductor", "—") or "—"
                arch = Path(item["archivo"]).name
                arch = arch[:C1-1] if len(arch) >= C1 else arch

                if prog != programa_actual:
                    if programa_actual is not None:
                        print(f"  {'-' * (C1 + C2 + C3 + 2)}")
                    programa_actual = prog

                etiqueta = prog if prog != "desconocido" else "( sin programa )"
                print(f"  {arch:<{C1}} {etiqueta:<{C2}} {cond:<{C3}}")

            print(sep)

            total       = len(programas_archivos)
            reconocidos = sum(1 for i in programas_archivos if i["programa"] != "desconocido")
            print(f"\nEscaneo completado : {total} archivos")
            print(f"  con programa     : {reconocidos}")
            print(f"  sin programa     : {total - reconocidos}\n")

        elif opcion == "2":

            if not programas_archivos:
                print("\nNo hay archivos escaneados.")
                print("Primero debes ejecutar la opcion 1.\n")
                continue

            C1, C2 = 30, 50
            filas  = []

            for item in sorted(programas_archivos, key=lambda x: x["programa"]):
                programa = item["programa"]
                archivo  = Path(item["archivo"])
                original = archivo.stem
                nuevo    = normalizar_nombre.normalizar_nombre(archivo, programa)  # FIX
                filas.append((programa, original, nuevo))

            C3  = max(len(f[2]) for f in filas) + 2
            sep = "=" * (C1 + C2 + C3 + 4)

            print("\n" + sep)
            print(f"{'PROGRAMA':<{C1}} {'ARCHIVO ORIGINAL':<{C2}} {'NUEVO NOMBRE':<{C3}}")
            print(sep)

            programa_actual = None
            for programa, original, nuevo in filas:

                if programa != programa_actual:
                    if programa_actual is not None:
                        print(f"  {'-' * (C1 + C2 + C3 + 2)}")
                    programa_actual = programa

                etiqueta   = programa if programa != "desconocido" else "( sin programa )"
                orig_corto = original[:C2-1] if len(original) >= C2 else original

                print(
                    f"{etiqueta[:C1-1]:<{C1}} "
                    f"{orig_corto:<{C2}} "
                    f"{nuevo:<{C3}}"
                )

            print(sep + "\n")

        elif opcion == "3":
            print("Saliendo...")
            break

        else:
            print("\nOpcion invalida.\n")