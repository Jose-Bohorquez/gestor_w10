# gestor_w10

---

## estructura:

proyecto/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── files.py  # Manejo de archivos
│   │   └── auth.py   # Registro y login
│   ├── static/
│   ├── templates/
│   ├── utils.py      # Funciones auxiliares
│   └── models.py     # Modelos y lógica de datos
├── config.py         # Configuración
├── run.py            # Punto de entrada
└── requirements.txt  # Dependencias


# instrucciones

## 1. Verifica la política actual en (consola)(powerShell) con:
---
Get-ExecutionPolicy
---
Probablemente obtendrás algo como Restricted, lo que impide la ejecución de scripts.
---

## 2. Cambia la política de ejecución (consola)(powerShell)(como Admin) con
---
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
---
Esto permitirá ejecutar scripts solo durante esta sesión de PowerShell.
---

## 3. Activa el entorno virtual
---
Intenta nuevamente activar el entorno virtual con:
---
.\venv\Scripts\Activate
---
Deberías ver algo como:
---
(venv) PS C:\laragon\www\gestor_w10>
---

## 4. Desactivar el entorno en (consola)(powerShell) con:
---
deactivate
---

## 5. Cambiar la política de ejecución de manera permanente (opcional)
---
Si prefieres no tener que cambiar la política en cada sesión, puedes configurarla globalmente con:
---
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
---
Esto permitirá ejecutar scripts locales, pero seguirá bloqueando scripts descargados de internet a menos que estén firmados.



## 6 Crea un entorno virtual o aativa el existente para el proyecto:
Esto asegura que las dependencias del proyecto no interfieran con otros proyectos
---
python -m venv venv
---

## 7 Activa el entorno virtual:
En Windows:
---
venv\Scripts\activate
---
en git bash:_
---
source venv/Scripts/activate
---
Alternativa: Usa PowerShell:
---
.\venv\Scripts\Activate
---

## 8 instala las dependencias con:
---
pip install -r requirements.txt
---

## 9 si se instalan librerias nuevas se recomienda congelarlas con:
---
pip freeze > requirements.txt
---