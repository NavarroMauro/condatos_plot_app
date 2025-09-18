# app/plots/__init__.py
# Permite importar los módulos de graficación directamente desde app.plots

# Registramos todos los gráficos disponibles en el paquete
# Esto permite que se registren los comandos cuando se importan en main.py

# Evitar importación circular cuando se ejecuta directamente como módulo
import sys
import os

# Estos imports registran los comandos en la CLI
# Importación condicional para evitar advertencias cuando se ejecuta directamente
if not (len(sys.argv) > 0 and sys.argv[0].endswith('__main__.py') and 
        os.path.basename(sys.argv[0].replace('__main__.py', '')) in ['barv', 'stackedbarh', 'linechart']):
    import app.plots.barv
    import app.plots.stackedbarh
    import app.plots.linechart
