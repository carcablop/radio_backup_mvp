'''Definir la funcion normalizar_nombre que reciba un string con un nombre de archivo y devuelva el mismo archivo normalizado.'''

def normalizar_nombre(programa_archivo: list):
    for prog_arch in programa_archivo:
        n_archivo_normalizado = prog_arch["archivo"].strip().lower().replace(" ", "_").replace(",","_")
        n_prog_normalizado = prog_arch['programa'].strip().lower().replace(" ","_").replace(",","_")
        #imprimir el archivo normalizado (n_archivo_normalizado)
        print(f"Archivo normalizado: {n_prog_normalizado}_{n_archivo_normalizado}")
    return n_prog_normalizado + "_" + n_archivo_normalizado
