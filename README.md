# radio_backup_mvp
Sistema de gestion de archivos mp3 y mp4 de la emisora Oriente estereo de Cali con respaldo en la nube. 

Empezar (Setup en Windows):
1. Clonar repositorio:

    `git clone https://github.com/carcablop/radio_backup_mvp.git`

    `cd radio_backup_mvp`

2. Crear entorno virtual (venv):

    `python -m venv venv`

3. Activar un entorno virtual:

    `venv\Scripts\activate`

    Deberías ver algo así:
        
        (venv) C:\ruta\radio_backup_mvp>

4. Instalar dependencias. 
    
    `pip install -r requirements.txt`

5. Ejecutar el proyecto:

    `python main.py`


**Contribucción al proyecto**:
Si quieres contribuir al proyecto debes trabajar sobre la rama 'dev'

**Trabajando con Ramas:**

**Ramas principales**:

    main → producción
    dev  → desarrollo

Cambiar a rama dev
        git checkout dev

Crear nueva rama
        git checkout -b feature/nombre-tarea

Ejemplo:

    git checkout -b feature/normalizer

**Subir cambios:**
    git add .
    git commit -m "feat: agrega normalizador"
    git push origin feature/normalizer


**Crear Pull Request**

    Ir a GitHub → abrir PR hacia dev

Actualizar código desde repositorio:
Estar en la rama dev

    git checkout dev

Traer cambios:

        git pull origin dev

 Actualizar tu rama:

        git checkout feature/tu-rama
        git merge dev

⚠️ Reglas del equipo:

    ❌ No hacer push a main
    ❌ No hacer push directo a dev
    ✅ Usar Pull Request
    ✅ 1 tarea = 1 rama
    ✅ Código revisado antes de merge


Configuración de GitHub:

 Configurar usuario

        git config --global user.name "Tu Nombre"
        git config --global user.email "tu@email.com"

Autenticación

Usar token personal (no contraseña)

Guía:
https://docs.github.com/en/authentication

Referencias técnicas
Python venv

https://docs.python.org/3/library/venv.html

pip

https://pip.pypa.io/en/stable/

Git

 https://git-scm.com/docs

GitHub Docs

https://docs.github.com/