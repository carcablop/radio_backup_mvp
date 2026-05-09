# normalizacion.py — Oriente Estéreo | Python Schools 2026
# ─────────────────────────────────────────────────────────────────────────────
# Módulo de normalización de nombres de archivos de audio.
# Dependencias: SOLO pathlib.Path y operaciones nativas de str.
# ─────────────────────────────────────────────────────────────────────────────

from pathlib import Path

# ═════════════════════════════════════════════════════════════════════════════
# CONSTANTES GLOBALES
# ═════════════════════════════════════════════════════════════════════════════

MAX_CHARS_CUERPO: int = 100
# Límite del cuerpo del nombre final (sin extensión).
# Ajustar según necesidades del sistema de archivos destino.

# ── Normalización de diacríticos ─────────────────────────────────────────────
# str.maketrans exige que _SRC y _DST tengan exactamente la misma longitud
# (46 caracteres).  Se cubre el rango latino extendido relevante al español.
# Decisión: implementación manual en lugar de unicodedata.normalize() para
# respetar la restricción de "solo pathlib + string nativo".
_SRC_ACEN = "áéíóúüàèìòùâêîôûãõñäëïöÁÉÍÓÚÜÀÈÌÒÙÂÊÎÔÛÃÕÑÄËÏÖ"
_DST_ACEN = "aeiouuaeiouaeiouaonaeioAEIOUUAEIOUAEIOUAONAEIO"
TABLA_ACENTOS: dict = str.maketrans(_SRC_ACEN, _DST_ACEN)

# ── Meses ─────────────────────────────────────────────────────────────────────
NOMBRES_MESES = [
    ("enero",      "ene"), ("febrero",    "feb"), ("marzo",      "mar"),
    ("abril",      "abr"), ("mayo",       "may"), ("junio",      "jun"),
    ("julio",      "jul"), ("agosto",     "ago"), ("septiembre", "sep"),
    ("octubre",    "oct"), ("noviembre",  "nov"), ("diciembre",  "dic"),
]

MESES: dict[str, str] = {}
for _n, (_largo, _abrev) in enumerate(NOMBRES_MESES, start=1):
    _ns = str(_n).zfill(2)
    MESES[_largo]      = _ns   # nombre completo
    MESES[_abrev]      = _ns   # abreviatura oficial
    MESES[_largo[:4]]  = _ns   # primeras 4 letras
    MESES[_largo[:3]]  = _ns   # primeras 3 letras (puede solapar con abrev)

# ── Palabras de ruido ─────────────────────────────────────────────────────────
# DECISIÓN: se eliminaron preposiciones ("de","del","la","en","y","el") que
# estaban en la versión anterior.  Motivo: forman parte de títulos creativos
# y de nombres de programa ("en la raya", "del amanecer", "radio y pueblo").
# Solo se conservan los días de semana porque son metadatos de transmisión
# sin valor semántico en el nombre del archivo final.
PALABRAS_RUIDO: set[str] = {
    "sabado", "domingo", "lunes", "martes",
    "miercoles", "jueves", "viernes",
}


# ═════════════════════════════════════════════════════════════════════════════
# UTILIDADES DE TEXTO
# ═════════════════════════════════════════════════════════════════════════════

def _quitar_acentos(texto: str) -> str:
    """Transliteración de diacríticos → ASCII puro mediante TABLA_ACENTOS."""
    return texto.translate(TABLA_ACENTOS)


def _limpiar_stem(stem: str) -> str:
    """
    Normaliza el stem de un archivo a una lista de tokens en minúsculas
    separados por espacios simples.

    Pasos (en orden, cada uno con su justificación):
    ──────────────────────────────────────────────────
    1. Quitar acentos → garantiza que comparaciones posteriores no fallen
       por diferencias de codificación entre sistemas operativos.
    2. Convertir a minúsculas → unifica capitalización.
    3. Eliminar la cadena literal 'mp3' ANTES de tokenizar.
       DECISIÓN CLAVE: si se hace después, '2025mp3' ya fue separado en
       ['2025', 'mp3'] y el token basura persiste.  Haciéndolo aquí,
       '2025mp3' → '2025 ' y se tokeniza correctamente como ['2025'].
    4. Guiones y guiones bajos → espacios para tratar ambos como separadores.
    5. Insertar espacio en transiciones dígito↔letra: '15oct2024' → '15 oct 2024'.
       Esto unifica expresiones compactas con las escritas con separadores.
    6. Todo carácter no alfanumérico → espacio; colapsar espacios múltiples.
    """
    s = _quitar_acentos(stem.lower())
    s = s.replace("mp3", " ")                      # paso 3: extensión incrustada
    s = s.replace("-", " ").replace("_", " ")       # paso 4

    resultado = ""
    prev = ""
    for c in s:                                     # paso 5: split dígito↔letra
        if c.isalnum():
            if prev and (
                (prev.isdigit() and c.isalpha()) or
                (prev.isalpha() and c.isdigit())
            ):
                resultado += " "
            resultado += c
        else:
            resultado += " "
        prev = c

    return " ".join(resultado.split())              # paso 6: colapsar espacios


def _texto_a_snake(texto: str, filtrar_ruido: bool = True) -> str:
    """
    Convierte texto libre a snake_case.

    filtrar_ruido=True  → elimina días de semana (uso en títulos).
    filtrar_ruido=False → conserva todos los tokens (uso en nombre de programa,
                          porque el programa podría llamarse "EL PROGRAMA DEL
                          VIERNES" y 'viernes' sería significativo allí).
    """
    partes = [
        tok for tok in _limpiar_stem(texto).split()
        if tok and (not filtrar_ruido or tok not in PALABRAS_RUIDO)
    ]
    return "_".join(partes)


# ═════════════════════════════════════════════════════════════════════════════
# DETECCIÓN DE FECHA
# ═════════════════════════════════════════════════════════════════════════════

def _construir_fecha(dia: str, mes: str, anio: str) -> str | None:
    """
    Valida y ensambla una fecha ISO parcial.

    Retorna:
    • "YYYY-MM-DD"  si dia es válido
    • "YYYY-MM"     si dia es vacío ""
    • None          si algún componente es inválido

    Nunca lanza excepción: usa None como señal de fallo para que el
    llamador pueda continuar probando otros patrones.
    """
    if not anio.isdigit():
        return None
    if len(anio) == 2:
        anio = "20" + anio
    if len(anio) != 4 or not (1900 <= int(anio) <= 2100):
        return None

    m = int(mes)
    if not (1 <= m <= 12):
        return None

    if dia:
        d = int(dia)
        if not (1 <= d <= 31):
            return None
        return f"{anio}-{m:02d}-{d:02d}"

    return f"{anio}-{m:02d}"


def detectar_fecha(nombre: str) -> str:
    """
    Detecta la fecha más específica posible en el nombre de archivo.

    Jerarquía de formatos producidos:
    • "YYYY-MM-DD"   fecha completa
    • "YYYY-MM"      mes + año
    • "sin_fecha"    no se encontró fecha válida

    DECISIÓN IMPORTANTE: los años aislados (p. ej. solo '2024' en el nombre)
    ya NO se aceptan como fecha.
    Motivo: un número de 4 dígitos como '2001' puede ser parte del título
    ('2001_odisea') y su interpretación como año generaría un falso positivo
    que contamina el nombre final con una fecha inexistente.
    Si el año aparece junto a un mes o un día se acepta normalmente.

    Estrategias de detección (en orden):
    1. Tripleta numérica: AAAA MM DD  o  DD MM AA[AA]
    2. Mes textual + año numérico en ventana de ±3 tokens.
    """
    stem = _limpiar_stem(Path(nombre).stem)
    palabras = stem.split()

    # ── 1. Tripletas numéricas ────────────────────────────────────────────────
    for i in range(len(palabras) - 2):
        a, b, c = palabras[i], palabras[i + 1], palabras[i + 2]
        if a.isdigit() and b.isdigit() and c.isdigit():
            # AAAA-MM-DD
            if len(a) == 4:
                f = _construir_fecha(c, b, a)
            else:
                # DD-MM-AAAA  o  DD-MM-AA
                f = _construir_fecha(a, b, c)
            if f:
                return f

    # ── 2. Mes textual ────────────────────────────────────────────────────────
    for i, tok in enumerate(palabras):
        num_mes = MESES.get(tok)
        if not num_mes:
            continue

        dia = anio = None
        ventana = palabras[max(0, i - 3): i + 4]

        for cand in ventana:
            if not cand.isdigit():
                continue
            v, n = int(cand), len(cand)
            if n == 4 and 1900 <= v <= 2100:
                anio = cand
            elif n == 2 and v > 31:
                anio = "20" + cand
            elif 1 <= v <= 31 and dia is None:
                dia = cand.zfill(2)

        if anio:
            f = _construir_fecha(dia or "", num_mes, anio)
            if f:
                return f

    return "sin_fecha"


# ═════════════════════════════════════════════════════════════════════════════
# DETECCIÓN DE EPISODIO / SECUENCIA
# ═════════════════════════════════════════════════════════════════════════════

def detectar_episodio(nombre: str) -> str | None:
    """
    Detecta número de episodio o identificador de secuencia.

    Formato de salida siempre unificado: 'epNNN' (3 dígitos, cero-relleno).

    DECISIÓN: unificar 'ep001', 'parte 1', 'prog 5' bajo un único formato
    resuelve la inconsistencia detectada en las pruebas donde coexistían
    representaciones distintas para el mismo concepto.

    DECISIÓN sobre prefijos de orden ('01_PRIMERA_LINEA.mp3'):
    El número inicial SE PRESERVA como episodio ('ep001') en vez de
    eliminarse silenciosamente.  En contextos radiales y de producción
    estos prefijos representan el orden de bloques o segmentos; perderlos
    destruye información relevante para la organización de la pauta.

    Patrones reconocidos (en orden de prioridad):
    1. Palabra clave seguida de número:
       'episodio 3', 'ep 3', 'programa 3', 'prog 3'
    2. Número entero al inicio del stem, separado con '-' o '_':
       '001-entrevista', '03_tema_del_dia'
    """
    stem = Path(nombre).stem
    texto = _limpiar_stem(stem)
    palabras = texto.split()

    # Patrón 1: palabra clave + número
    claves = {"episodio", "programa", "prog", "ep"}
    for i, pal in enumerate(palabras):
        if pal in claves and i + 1 < len(palabras):
            sig = palabras[i + 1]
            if sig.isdigit():
                return "ep" + str(int(sig)).zfill(3)

    # Patrón 2: número al inicio del stem ORIGINAL (antes de limpiar).
    # Se usa el stem original para respetar la posición exacta del separador.
    original = stem.strip()
    if original and original[0].isdigit():
        primer_token = original.replace("_", "-").split("-", 1)[0]
        if primer_token.isdigit():
            n = int(primer_token)
            if 1 <= n <= 999:
                return "ep" + str(n).zfill(3)

    return None


# ═════════════════════════════════════════════════════════════════════════════
# LIMPIEZA DE TÍTULO
# ═════════════════════════════════════════════════════════════════════════════

def _eliminar_tokens_programa(titulo_tokens: list[str],
                               prog_tokens: list[str]) -> list[str]:
    """
    Elimina del inicio del título los tokens que pertenezcan al programa.

    Algoritmo: se construye un conjunto con los tokens del programa (prog_set)
    y se consumen tokens del inicio del título mientras el primero de ellos
    pertenezca al conjunto.

    DECISIÓN DE CONSISTENCIA: usar un conjunto en vez de comparación de
    prefijo exacto resuelve el problema de 'EN LA RAYA' donde algunos archivos
    venían como 'raya_deportes_...' (sin "en la") y la eliminación por prefijo
    exacto solo quitaba nada o poco.  Con el conjunto, "raya" se elimina del
    inicio aunque no venga acompañado de "en" y "la".

    Límite: solo se eliminan tokens DESDE EL INICIO, no de cualquier posición,
    para no borrar palabras del programa que aparezcan de forma legítima en el
    cuerpo del título (p. ej. un programa llamado "radio" no debería borrar
    "radio" si aparece dentro de "historia_de_la_radio").
    """
    if not prog_tokens:
        return titulo_tokens

    prog_set = set(prog_tokens)
    resultado = list(titulo_tokens)

    while resultado and resultado[0] in prog_set:
        resultado = resultado[1:]

    return resultado


def limpiar_titulo(nombre: str, fecha: str, episodio: str | None,
                   prog_tokens: list[str]) -> str:
    """
    Extrae el título del archivo eliminando programa, fecha y episodio.

    QUÉ SE ELIMINA:
    • Tokens numéricos y textuales de la fecha detectada.
    • Número y palabras clave del episodio ('ep', 'programa', etc.).
    • Días de semana (PALABRAS_RUIDO).
    • Tokens iniciales del programa (_eliminar_tokens_programa).

    QUÉ SE CONSERVA (decisión):
    • Preposiciones y artículos: permiten títulos como "en_la_raya" o
      "del_amanecer" que perderían su sentido sin esas palabras.
    • Números no relacionados con fecha ni episodio: permite conservar
      expresiones como "parte_1", "parte_2" en el título.
    • Duplicados consecutivos se colapsan (limpieza defensiva).
    """
    texto = _limpiar_stem(Path(nombre).stem)
    tokens = texto.split()

    # Conjunto de tokens a eliminar
    eliminar: set[str] = set(PALABRAS_RUIDO)

    if fecha != "sin_fecha":
        for parte in fecha.split("-"):
            eliminar.add(parte)
            if parte.isdigit():
                eliminar.add(str(int(parte)))   # sin ceros iniciales
        # eliminar también el nombre textual del mes si aplica
        for nom_mes, num_mes in MESES.items():
            if len(fecha) >= 7 and num_mes == fecha[5:7]:
                eliminar.add(nom_mes)

    if episodio:
        num_str = str(int(episodio[2:]))         # "ep003" → "3"
        eliminar.add(num_str)
        eliminar.update({"episodio", "programa", "prog", "ep"})

    tokens_filtrados = [t for t in tokens if t not in eliminar]
    tokens_filtrados = _eliminar_tokens_programa(tokens_filtrados, prog_tokens)

    # Colapsar duplicados consecutivos
    dedup: list[str] = []
    for t in tokens_filtrados:
        if not dedup or dedup[-1] != t:
            dedup.append(t)

    return "_".join(dedup)


# ═════════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

def normalizar_nombre(archivo: Path, programa: str = "") -> str:
    """
    Normaliza el nombre de un archivo de audio al formato:

        [programa_]titulo[_YYYY-MM-DD][_epNNN].ext

    Parámetros
    ──────────
    archivo : Path
        Ruta al archivo.  La extensión se conserva en minúsculas.

    programa : str, opcional
        Nombre del programa proveniente de la carpeta padre del archivo.

        DECISIÓN ARQUITECTÓNICA: el programa se pasa como parámetro
        explícito en vez de deducirse internamente de archivo.parent.name.
        Razones:
        (a) Desacoplamiento: la función no asume ninguna estructura de
            carpetas específica.
        (b) Consistencia: todos los archivos del mismo programa reciben
            exactamente el mismo prefijo, sin variaciones por cómo venga
            nombrado cada archivo.
        (c) Testeabilidad: se puede probar la función con cualquier
            combinación de archivo/programa sin necesidad de crear
            directorios reales.
        (d) Separación de responsabilidades: quién llama a esta función
            es quien mejor sabe cómo obtener el nombre del programa
            (de la carpeta, de una base de datos, de metadatos, etc.).

    Límite de caracteres (MAX_CHARS_CUERPO)
    ────────────────────────────────────────
    El cuerpo (sin extensión) se trunca a MAX_CHARS_CUERPO caracteres.
    DECISIÓN: el truncado busca el último '_' dentro del límite y corta
    ahí (en vez de cortar en posición exacta) para no partir tokens a la
    mitad, produciendo nombres más legibles.  Si el último '_' está en la
    primera mitad del límite (token muy largo), se corta en posición exacta
    para no desperdiciar demasiado espacio.

    Retorna
    ───────
    str — nombre normalizado con extensión en minúsculas.
    """

    ext = archivo.suffix.lower()

    # ── 1. Normalizar nombre del programa ─────────────────────────────────────
    # filtrar_ruido=False: el programa viene curado de la carpeta padre;
    # se conservan TODOS sus tokens incluyendo días de semana si los hubiera.
    nombre_prog = _texto_a_snake(programa, filtrar_ruido=False) if programa.strip() else ""
    prog_tokens = nombre_prog.split("_") if nombre_prog else []

    # ── 2. Detectar metadatos del archivo ─────────────────────────────────────
    fecha    = detectar_fecha(archivo.name)
    episodio = detectar_episodio(archivo.name)

    # ── 3. Construir título limpio ────────────────────────────────────────────
    titulo = limpiar_titulo(archivo.name, fecha, episodio, prog_tokens)

    # ── 4. Ensamblar partes ───────────────────────────────────────────────────
    partes: list[str] = []

    if nombre_prog:
        partes.append(nombre_prog)

    # Se agrega el título solo si aporta información nueva respecto al programa
    if titulo and titulo != nombre_prog:
        partes.append(titulo)

    if fecha != "sin_fecha":
        partes.append(fecha)

    if episodio:
        partes.append(episodio)

    # Nombre de emergencia si ninguna parte tiene contenido
    if not partes:
        partes.append("audio")

    cuerpo = "_".join(p for p in partes if p)

    # ── 5. Limpiar dobles guiones bajos residuales ────────────────────────────
    while "__" in cuerpo:
        cuerpo = cuerpo.replace("__", "_")
    cuerpo = cuerpo.strip("_")

    # ── 6. Aplicar límite de caracteres ──────────────────────────────────────
    if len(cuerpo) > MAX_CHARS_CUERPO:
        cuerpo = cuerpo[:MAX_CHARS_CUERPO]
        ultimo_sep = cuerpo.rfind("_")
        # Cortar en '_' solo si no retrocedemos más del 50% del límite
        if ultimo_sep > MAX_CHARS_CUERPO // 2:
            cuerpo = cuerpo[:ultimo_sep]

    return cuerpo + ext
