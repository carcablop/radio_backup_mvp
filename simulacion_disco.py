from pathlib import Path
import os

# ============================================================
# Ruta base
# ============================================================

RUTA_BASE = Path(
    "sample_data/DISCO_PRUEBA/NUEVO ORIENTE ESTEREO/PROGRAMAS"
)

# ============================================================
# Función para soportar rutas largas en Windows
# ============================================================

def windows_long_path(path: Path) -> str:
    """
    Convierte una ruta normal en una ruta compatible
    con rutas largas de Windows.
    """

    ruta_absoluta = path.resolve()

    # En Windows usar prefijo \\?\
    if os.name == "nt":
        return f"\\\\?\\{ruta_absoluta}"

    return str(ruta_absoluta)

# ============================================================
# Carpetas
# ============================================================

carpetas = [
    "A PRENDER LA ONDA",
    "AFRO ESTEREO/ARCHIVOS AUDIOS",
    "AFRO ESTEREO/MUSICA",
    "AFRO ESTEREO/PROGRAMAS",
    "BARRIO ADENTRO/DOCU BRYAN",
    "CESAR PAGANO/SONGOROCOSONGO",
    "CESAR PAGANO/PAGANO BOLERO/PAGANO BOLERO",
    "CESAR PAGANO/PAGANO BOLERO/2025",
    "DEJAME SER ARTE/PRODUCCION DSA",
    "DEJAME SER ARTE/PROGRAMAS",
    "DEJAME SER ARTE/MUSICA",
    "DIANA URIBE",
    "EN LA RAYA",
    "ENTRE NOSOTROS/2025",
    "ENTRE NOSOTROS/PROGRAMA 290 ENTRE NOSOTROS DE KAREN ARRANZ SABADO 24 DE FEBRERO DE 2026",
    "ENTRE NOSOTROS/PROGRAMA 289 ENTRE NOSOTROS DE KAREN ARRANZ SABADO 17 DE FEBRERO DE 2026",
    "ENTRE NOSOTROS/PROGRAMA 287 ENTRE NOSOTROS DE KAREN ARRANZ SABADO DE 14 MARZO DE 2026",
    "LA CHICHARRA/ARCHIVOS AUDIO",
    "LA CHICHARRA/PROGRAMAS",
    "LA CHICHARRA/INFORMES",
    "FRECUENCIA UMBRELLA/MUSICA",
    "FRECUENCIA UMBRELLA/VISUALES",
    "FREDY CORTES/CITA BOLERO",
    "FREDY CORTES/HORA SONORA",
    "HUMO EN LA RADIO/CARPETAS RAP/13-09-25",
    "HUMO EN LA RADIO/CARPETAS RAP/HUMO 8 NOV 2025",
    "LA CHICHARRA",
    "LAS 20+",
    "LATINOAMERICA",
    "LAURA SOTELO",
    "LENGUAJE ROCK",
    "MERIDIANO MUSICAL",
    "NOVENAS",
    "PACIFICO AL BARRIO",
    "PALABRAS DE EQUIDAD",
    "RADIO ESQUINA",
    "RADIO GUAYABA",
    "RADIO VILLAMAGA",
    "ROCK CINEFILIA",
    "SALSA GORDA",
    "SALSA, CAFE Y LETRAS",
    "SOY DE AQUI",
    "VICTORIA CON LAS ESTRELLAS",
    "VIVA LA GENTE",
    "VIVE VILLANCICOS",
    "VOCES VIAJERAS",
]

# ============================================================
# Archivos sonoros
# ============================================================

archivos_sonoros = [

    "A PRENDER LA ONDA/EPISODIO 24-2025.mp3",
    "A PRENDER LA ONDA/Episodio 35 2025.mp3",
    "A PRENDER LA ONDA/Episodio 125.mp3",
    "A PRENDER LA ONDA/Episodio 122 2023(1).mp3",

    "BARRIO ADENTRO/PROGRAMAS/BARRIO ADENTRO 06-06-25.mp3",

    "CESAR PAGANO/SONGOROCOSONGO/SONGORO - leonor gonzalez mina la negra grande colombia.mp3",
    "CESAR PAGANO/SONGOROCOSONGO/SONGORO - exotismos sonoros brasil.mp3",
    "CESAR PAGANO/SONGOROCOSONGO/SONGORO - gerardo rosales su salsagenuina venezuela PARTE 1.mp3",
    "CESAR PAGANO/SONGOROCOSONGO/SONGORO - gerardo rosales su salsagenuina venezuela PARTE 2.mp3",
    "CESAR PAGANO/SONGOROCOSONGO/SONGOROCOSONGO - luis perico ortiz artista multifacetico PARTE 2.mp3",
    "CESAR PAGANO/PAGANO BOLERO/PAGANO BOLERO - mujeres bolero parte2.mp3",

    "DEJAME SER ARTE/PRODUCCION DSA/CABEZOTE DSA.mp3",
    "DEJAME SER ARTE/PRODUCCION DSA/PISADOR DSA 1.mp3",
    "DEJAME SER ARTE/PROGRAMAS/DEJAME SER ARTE 03-07-25.mp3",
    "DEJAME SER ARTE/PROGRAMAS/DEJAME SER ARTE17-07-25.mp3",
    "DEJAME SER ARTE/PROGRAMAS/DSA 02-10-25.mp4",
    "DEJAME SER ARTE/MUSICA/insaic cancion 1.mp3",

    "DIANA URIBE/1 - La historia de la radio y la radio en la historia.mp3",
    "DIANA URIBE/2 - La radio en las guerras.mp3",
    "DIANA URIBE/3 - una radio diferente.mp3",
    "DIANA URIBE/7- Comienzos de la radio en Colombia.mp3",

    "EN LA RAYA/EN LA RAYA DEPORTES 03 DE DIC DE 2025.mp3",
    "EN LA RAYA/EN LA RAYA DEPORTES- AGOSTO 25 DE 2025.mp3",
    "EN LA RAYA/EN LA RAYA DEPORTES- OCT 1 DE 2025.mp3",
    "EN LA RAYA/EN LA RAYA DEPORTES- OCT 03 DE 2025.mp3",
    "EN LA RAYA/EN LA RAYA DEPORTES OCT 27 DE 2025.mp3",
    "EN LA RAYA/EN LA RAYA DEPORTES- SEPTIEMBRE 15 DE 2025mp3.mp3",
    "EN LA RAYA/En la Raya Deportes- Septiembre 29 de 2025.mp3",

    "ENTRE NOSOTROS/PROGRAMA 290 ENTRE NOSOTROS DE KAREN ARRANZ SABADO 24 DE FEBRERO DE 2026/PROG.290 ENTRE NOSOTROS, SABADO 21 DE FEBRERO 2026 1RA MEDIA HORA.mp3",

    "ENTRE NOSOTROS/PROGRAMA 289 ENTRE NOSOTROS DE KAREN ARRANZ SABADO 17 DE FEBRERO DE 2026/PROG.289 ENTRE NOSOTROS, SABADO 17 DE FEBRERO 2026 4TA MEDIA HORA.mp3",

    "ENTRE NOSOTROS/Cuando Pase El Temblor - Remasterizado 2007.mp3",

    "ENTRE NOSOTROS/Via Lactea_spotdown.org.mp3",

    "LA CHICHARRA/CAVASA 02-03-2026.mp3",
    "LA CHICHARRA/INFORMES/VOCES DEL PACIFICO.mp4",
    "LA CHICHARRA/INFORMES/vanesa calle_mezcla.mp3",
    "LA CHICHARRA/INFORMES/vanesa - 4-08-2025_mezcla.mp3",
    "LA CHICHARRA/INFORMES/VOCES DEL PACIFICO (online-audio-converter.com).mp3",

    "FRECUENCIA UMBRELLA/Cancion de Tetris Original.mp3",
    "FRECUENCIA UMBRELLA/MOMENTOS TENSOS.mp3",
    "FRECUENCIA UMBRELLA/FONDO UMBRELLA 2.mp4",

    "FREDY CORTES/BLOQUE FINAL SONORA 29 MARZO.mp3",
    "FREDY CORTES/BLOQUE FINAL CITA 29 MARZO 2026.mp3",

    "HUMO EN LA RADIO/COMO UN HUMO EN LA RADIO.mp3",
    "HUMO EN LA RADIO/CARPETAS RAP/13-09-25/01 - PRIMERA LINEA.mp3",
    "HUMO EN LA RADIO/CARPETAS RAP/13-09-25/02- NO LOS LEO.mp3",
    "HUMO EN LA RADIO/CARPETAS RAP/13-09-25/003--MI RAP.mp3",
    "HUMO EN LA RADIO/CARPETAS RAP/13-09-25/04-A UD SEÑOR tema.mp3",
]

# ============================================================
# Crear carpetas
# ============================================================

for carpeta in carpetas:

    ruta_carpeta = RUTA_BASE / carpeta

    ruta_larga = windows_long_path(ruta_carpeta)

    os.makedirs(ruta_larga, exist_ok=True)

    print(f"[CARPETA] {ruta_carpeta}")

# ============================================================
# Crear archivos
# ============================================================

for ruta_archivo in archivos_sonoros:

    ruta = RUTA_BASE / ruta_archivo

    # Crear carpeta padre
    ruta_padre = windows_long_path(ruta.parent)

    os.makedirs(ruta_padre, exist_ok=True)

    # Ruta larga del archivo
    ruta_archivo_windows = windows_long_path(ruta)

    # Crear archivo vacío
    with open(ruta_archivo_windows, "a", encoding="utf-8"):
        pass

    print(f"[ARCHIVO] {ruta}")

# ============================================================
# Resumen
# ============================================================

print("\n==================================================")
print(f"Carpetas creadas: {len(carpetas)}")
print(f"Archivos creados: {len(archivos_sonoros)}")
print(f"Ruta base: {RUTA_BASE}")
print("==================================================")