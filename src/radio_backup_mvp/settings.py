from escanear import detectar_programa

CARPETAS = {
    #Creo el diccionario con los conductores y sus programas, si es desconocido lo asigno a "Desconocido", con el fin de
    #poder asignar los programas a sus conductores posteriormente, ya que algunos programas no tienen el nombre del conductor en la carpeta, 
    #o no se puede deducir el conductor a partir del nombre del programa.

    "A PRENDER LA ONDA" : "DESCONOCIDO",
    "AFRO ESTEREO" : "DESCONOCIDO",
    "BARRIO ADENTRO" : "DESCONOCIDO",
    "SONGOROCOSONGO" : "CESAR PAGANO",
    "PAGANO BOLERO" : "CESAR PAGANO",
    "DEJAME SER ARTE" : "DESCONOCIDO",
    "DESCONOCIDO" : "DIANA URIBE",
    "EN LA RAYA" : "DESCONOCIDO",   
    "ENTRE NOSOTROS" : "KAREN ARRANZ",
    "LA CHICHARRA" : "DESCONOCIDO",
    "FRECUENCIA UMBRELLA" : "DESCONOCIDO",
    "CITA BOLERO" : "FREDY CORTES",
    "HORA SONORA" : "FREDY CORTES",
    "HUMO EN LA RADIO" : "DESCONOCIDO",
    "LAS 20+" : "DESCONOCIDO",
    "LATINOAMERICA" : "DESCONOCIDO",
    "DESCONOCIDO" : "LAURA SOTELO",
    "LENGUAJE ROCK" : "DESCONOCIDO",
    "MERIDIANO MUSICAL" : "DESCONOCIDO",
    "NOVENAS" : "DESCONOCIDO",
    "PACIFICO AL BARRIO" : "DESCONOCIDO",
    "PALABRAS DE EQUIDAD" : "DESCONOCIDO",
    "RADIO ESQUINA" : "DESCONOCIDO",
    "RADIO GUAYABA" : "DESCONOCIDO",
    "RADIO VILLAMAGA" : "DESCONOCIDO",
    "ROCK CINEFILIA" : "DESCONOCIDO",
    "SALSA GORDA" : "DESCONOCIDO",
    "SALSA, CAFE Y LETRAS" : "DESCONOCIDO",
    "SOY DE AQUI" : "DESCONOCIDO",
    "VICTORIA CON LAS ESTRELLAS" : "DESCONOCIDO",
    "VIVA LA GENTE" : "DESCONOCIDO",
    "VIVE VILLANCICOS" : "DESCONOCIDO",
    "VOCES VIAJERAS" : "DESCONOCIDO"
}