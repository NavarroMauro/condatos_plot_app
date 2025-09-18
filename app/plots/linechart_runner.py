#!/usr/bin/env python
"""
Módulo auxiliar para ejecutar linechart sin warning de importación.
Este módulo evita el problema de importación circular cuando se ejecuta directamente 
como un módulo con python -m.
"""
from pathlib import Path
import sys

def main():
    # Importar directamente la función sin pasar por el sistema de módulos
    from app.plots.linechart import linechart
    
    if len(sys.argv) > 1:
        # Llamar a la función con el primer argumento como ruta de config
        linechart(Path(sys.argv[1]))
    else:
        print("Uso: python -m app.plots.linechart_runner ruta/al/config.yml")

if __name__ == "__main__":
    main()