# normalizacion.py — Oriente Estéreo | Python Schools 2026
# Módulo de normalización de nombres de archivos de audio.
# Sin expresiones regulares, solo string operations.

from pathlib import Path

# ============================================================
# CONSTANTES
# ============================================================
MAX_CHARS_CUERPO = 75
MAX_TOKENS_TITULO = 8

# Transliteración de acentos
_SRC_ACEN = "áéíóúüàèìòùâêîôûãõñäëïöÁÉÍÓÚÜÀÈÌÒÙÂÊÎÔÛÃÕÑÄËÏÖ"
_DST_ACEN = "aeiouuaeiouaeiouaonaeioAEIOUUAEIOUAEIOUAONAEIO"

# Meses
NOMBRES_MESES = [
    ("enero", "ene"),
    ("febrero", "feb"),
    ("marzo", "mar"),
    ("abril", "abr"),
    ("mayo", "may"),
    ("junio", "jun"),
    ("julio", "jul"),
    ("agosto", "ago"),
    ("septiembre", "sep"),
    ("octubre", "oct"),
    ("noviembre", "nov"),
    ("diciembre", "dic"),
]

MESES = {}

for n, (largo, abrev) in enumerate(NOMBRES_MESES, 1):
    ns = str(n).zfill(2)
    MESES[largo] = ns
    MESES[abrev] = ns
    MESES[largo[:4]] = ns
    MESES[largo[:3]] = ns

# Stopwords para títulos
PALABRAS_RUIDO_TITULO = {
    "lunes", "martes", "miercoles", "jueves", "viernes",
    "sabado", "domingo",
    "de", "del", "y", "con", "para", "por",
    "la", "el", "los", "las", "en", "a",
    "un", "una", "entre", "lo",
    "su", "sus", "mi", "tu", "mis", "tus",
    "nuestro", "nuestra", "nuestros", "nuestras",
    "este", "esta", "estos", "estas",
    "aquel", "aquella", "aquellos", "aquellas",
    "ese", "esa", "esos", "esas",
    "ante", "bajo", "cabe", "contra",
    "desde", "durante", "hacia", "hasta",
    "mediante", "segun", "sin", "sobre",
    "tras", "via",
    "que", "cual", "quien", "donde",
    "cuando", "como", "mas", "pero", "sino"
}

PALABRAS_RUIDO_PROGRAMA = {
    "lunes", "martes", "miercoles",
    "jueves", "viernes", "sabado", "domingo"
}

CLAVES_EPISODIO = {
    "episodio",
    "ep",
    "parte",
    "capitulo",
    "cap",
    "programa",
    "prog"
}

CARPETAS_GENERICAS = {
    "musica",
    "programas",
    "produccion dsa",
    "audio",
    "varios"
}

# ============================================================
# UTILIDADES
# ============================================================
def _quitar_acentos(texto):
    return texto.translate(str.maketrans(_SRC_ACEN, _DST_ACEN))


def _es_ordinal(token):
    """Detecta tokens como '4ta', '1ra', '2do', '3er', '21avo', etc."""
    sufijos = ("ra", "ro", "ta", "to", "er", "do", "va", "da", "avo", "ava")
    for suf in sufijos:
        if token.endswith(suf):
            base = token[:-len(suf)]
            if base.isdigit() and len(base) >= 1:
                return True
    return False


def _separar_numeros(texto):
    resultado = []
    for palabra in texto.split():
        if palabra.isalpha() or palabra.isdigit():
            resultado.append(palabra)
            continue
        if _es_ordinal(palabra):
            resultado.append(palabra)
            continue
        subtokens = []
        actual = ""
        for c in palabra:
            if not actual:
                actual = c
                continue
            previo = actual[-1]
            cambia_tipo = (
                (previo.isalpha() and c.isdigit()) or
                (previo.isdigit() and c.isalpha())
            )
            if cambia_tipo:
                subtokens.append(actual)
                actual = c
            else:
                actual += c
        if actual:
            subtokens.append(actual)
        fusionados = []
        i = 0
        while i < len(subtokens):
            if i + 1 < len(subtokens):
                candidato = subtokens[i] + subtokens[i + 1]
                if _es_ordinal(candidato):
                    fusionados.append(candidato)
                    i += 2
                    continue
            fusionados.append(subtokens[i])
            i += 1
        resultado.extend(fusionados)
    return " ".join(resultado)


def _limpiar_stem(stem, separar_numeros=True):
    s = _quitar_acentos(stem.lower())
    for sep in ["-", "_", ".", "(", ")", "[", "]", ",", ";", "!"]:
        s = s.replace(sep, " ")
    while "  " in s:
        s = s.replace("  ", " ")
    s = s.strip()
    if separar_numeros:
        s = _separar_numeros(s)
    return s


def _texto_a_snake(
    texto,
    filtrar_ruido_titulo=True,
    filtrar_ruido_programa=False
):
    texto_limpio = _limpiar_stem(texto)
    partes = []
    for tok in texto_limpio.split():
        if not tok:
            continue
        if filtrar_ruido_titulo and tok in PALABRAS_RUIDO_TITULO:
            continue
        if filtrar_ruido_programa and tok in PALABRAS_RUIDO_PROGRAMA:
            continue
        partes.append(tok)
    return "_".join(partes)


# ============================================================
# FECHAS
# ============================================================
def _construir_fecha(dia, mes, anio, solo_mes=False):
    if not anio.isdigit():
        return None
    if len(anio) == 2:
        anio = "20" + anio
    if len(anio) != 4:
        return None
    anio_int = int(anio)
    if not (1900 <= anio_int <= 2100):
        return None
    mes_int = int(mes)
    if not (1 <= mes_int <= 12):
        return None
    if solo_mes:
        return f"{anio}-{mes_int:02d}"
    if dia:
        dia_int = int(dia)
        if not (1 <= dia_int <= 31):
            return None
        return f"{anio}-{mes_int:02d}-{dia_int:02d}"
    return f"{anio}-{mes_int:02d}"


def detectar_fecha(nombre):
    stem = _limpiar_stem(Path(nombre).stem)
    palabras = stem.split()
    tokens_usados = set()

    for i in range(len(palabras) - 2):
        a = palabras[i]
        b = palabras[i + 1]
        c = palabras[i + 2]
        if a.isdigit() and b.isdigit() and c.isdigit():
            if len(a) == 4:
                fecha = _construir_fecha(c, b, a)
                if fecha:
                    tokens_usados.update([a, b, c])
                    return fecha, tokens_usados
            if len(c) == 4:
                fecha = _construir_fecha(a, b, c)
                if fecha:
                    tokens_usados.update([a, b, c])
                    return fecha, tokens_usados
            if len(c) == 2:
                fecha = _construir_fecha(a, b, c)
                if fecha:
                    tokens_usados.update([a, b, c])
                    return fecha, tokens_usados

    for i, tok in enumerate(palabras):
        num_mes = MESES.get(tok)
        if not num_mes:
            continue
        dia = None
        anio = None
        inicio = max(0, i - 3)
        fin = min(len(palabras), i + 4)
        ventana = palabras[inicio:fin]
        for cand in ventana:
            if not cand.isdigit():
                continue
            v = int(cand)
            if len(cand) == 4 and 1900 <= v <= 2100:
                anio = cand
            elif len(cand) == 2 and v > 31:
                anio = "20" + cand
            elif 1 <= v <= 31 and dia is None:
                dia = cand.zfill(2)
        if anio:
            fecha = _construir_fecha(
                dia or "",
                num_mes,
                anio,
                solo_mes=(dia is None)
            )
            if fecha:
                tokens_usados.add(tok)
                if dia:
                    tokens_usados.add(dia)
                    tokens_usados.add(str(int(dia)))
                tokens_usados.add(anio)
                if len(anio) == 4:
                    tokens_usados.add(anio[2:])
                return fecha, tokens_usados

    return "sin_fecha", set()


# ============================================================
# EPISODIOS
# ============================================================
def detectar_episodio(nombre):
    texto = _limpiar_stem(Path(nombre).stem)
    palabras = texto.split()
    for i, pal in enumerate(palabras):
        if (
            pal in CLAVES_EPISODIO and
            i + 1 < len(palabras) and
            palabras[i + 1].isdigit()
        ):
            n = int(palabras[i + 1])
            if 1 <= n <= 999:
                return f"ep{n:03d}"
    for pal in palabras:
        for clave in CLAVES_EPISODIO:
            if pal.startswith(clave):
                resto = pal[len(clave):]
                if resto.isdigit():
                    n = int(resto)
                    if 1 <= n <= 999:
                        return f"ep{n:03d}"
    return None


# ============================================================
# LIMPIEZA DE TITULO
# ============================================================
def _eliminar_tokens_programa(titulo_tokens, prog_tokens):
    if not prog_tokens:
        return titulo_tokens
    n = len(prog_tokens)
    resultado = list(titulo_tokens)
    i = 0
    while i <= len(resultado) - n:
        if resultado[i:i + n] == prog_tokens:
            del resultado[i:i + n]
        else:
            i += 1
    return resultado


def limpiar_titulo(nombre, fecha, tokens_fecha, episodio, prog_tokens):
    texto = _limpiar_stem(Path(nombre).stem)
    tokens = texto.split()
    tokens = _eliminar_tokens_programa(tokens, prog_tokens)
    eliminar = set(PALABRAS_RUIDO_TITULO)
    if fecha != "sin_fecha":
        eliminar.update(tokens_fecha)
        for parte in fecha.split("-"):
            eliminar.add(parte)
            if parte.isdigit():
                eliminar.add(str(int(parte)))
    if episodio:
        eliminar.update(CLAVES_EPISODIO)
        numero = str(int(episodio[2:]))
        eliminar.add(numero)
        eliminar.add(episodio[2:])
    filtrados = []
    vistos = set()
    for tok in tokens:
        if tok in eliminar:
            continue
        if tok in vistos:
            continue
        if tok.isdigit() and len(tok) == 1:
            continue
        vistos.add(tok)
        filtrados.append(tok)
    filtrados = filtrados[:MAX_TOKENS_TITULO]
    if not filtrados:
        return "audio"
    return "_".join(filtrados)


# ============================================================
# VALIDACIÓN PROGRAMA
# ============================================================
def _es_programa_valido(nombre_programa):
    nombre_clean = nombre_programa.strip().lower()
    if nombre_clean in CARPETAS_GENERICAS:
        return False
    test = nombre_clean.replace("_", "-")
    partes = test.split("-")
    if len(partes) == 3:
        d, m, a = partes
        if d.isdigit() and m.isdigit() and a.isdigit():
            if 1 <= int(d) <= 31 and 1 <= int(m) <= 12:
                if len(a) in (2, 4):
                    return False
    return True


def _convertir_fecha_programa(fecha_str):
    fecha_clean = fecha_str.replace("_", "-")
    partes = fecha_clean.split("-")
    if len(partes) != 3:
        return None
    d, m, a = partes
    if not (d.isdigit() and m.isdigit() and a.isdigit()):
        return None
    if len(a) == 2:
        a = "20" + a
    if len(a) != 4:
        return None
    return f"{a}-{int(m):02d}-{int(d):02d}"


# ============================================================
# NORMALIZACIÓN PRINCIPAL
# ============================================================
def normalizar_nombre(archivo, programa=""):
    # FIX: acepta string (stem sin extensión) o Path completo
    if isinstance(archivo, str):
        archivo = Path(archivo)

    ext = archivo.suffix.lower() if archivo.suffix else ".mp3"
    programa_fecha = None

    if programa.strip() and not _es_programa_valido(programa):
        programa_fecha = _convertir_fecha_programa(programa)
        if programa_fecha:
            programa = ""
        else:
            programa = ""

    nombre_prog = ""
    if programa:
        nombre_prog = _texto_a_snake(
            programa,
            filtrar_ruido_titulo=False,
            filtrar_ruido_programa=True
        )

    prog_tokens = nombre_prog.split("_") if nombre_prog else []
    fecha, tokens_fecha = detectar_fecha(archivo.name)

    if programa_fecha and fecha == "sin_fecha":
        fecha = programa_fecha
        tokens_fecha = set(programa_fecha.split("-"))

    episodio = detectar_episodio(archivo.name)
    titulo = limpiar_titulo(
        archivo.name,
        fecha,
        tokens_fecha,
        episodio,
        prog_tokens
    )

    partes = []
    if nombre_prog:
        partes.append(nombre_prog)
    if titulo and titulo != "audio":
        if titulo != nombre_prog:
            partes.append(titulo)
    if fecha != "sin_fecha":
        partes.append(fecha)
    if episodio:
        partes.append(episodio)
    if not partes:
        partes.append("audio")

    cuerpo = "_".join(partes)
    while "__" in cuerpo:
        cuerpo = cuerpo.replace("__", "_")
    cuerpo = cuerpo.strip("_")

    # FIX: quitar prefijo 'desconocido_' cuando no hay programa
    if cuerpo.startswith("desconocido_"):
        cuerpo = cuerpo[len("desconocido_"):]

    if len(cuerpo) > MAX_CHARS_CUERPO:
        corto = cuerpo[:MAX_CHARS_CUERPO]
        ultimo = corto.rfind("_")
        if ultimo > MAX_CHARS_CUERPO // 2:
            cuerpo = corto[:ultimo]
        else:
            cuerpo = corto

    # FIX: no incluir extensión en el cuerpo — solo retornar el nombre limpio
    return cuerpo