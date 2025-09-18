#!/usr/bin/env python
"""
Módulo ejecutable principal para todos los tipos de gráficos.
Este módulo evita los problemas de importación circular al ejecutar cualquier
tipo de gráfico desde la línea de comandos.

Uso:
    python -m app.plots.run [tipo_grafico] [ruta_config]

Ejemplo:
    python -m app.plots.run stackedbarh config/mi-config.yml
"""
import sys
from pathlib import Path

AVAILABLE_TYPES = {
    "stackedbarh": "Gráfico de barras horizontales apiladas",
    "barv": "Gráfico de barras verticales",
    "linechart": "Gráfico de líneas",
}

def show_help():
    """Muestra información de ayuda sobre el uso del módulo."""
    print("Uso: python -m app.plots.run [tipo_grafico] [ruta_config]")
    print("\nTipos de gráficos disponibles:")
    for tipo, desc in AVAILABLE_TYPES.items():
        print(f"  - {tipo}: {desc}")
    print("\nEjemplo:")
    print("  python -m app.plots.run stackedbarh config/mi-config.yml")

def main():
    """Función principal para ejecutar el tipo de gráfico solicitado."""
    if len(sys.argv) < 3 or sys.argv[1] in ["-h", "--help"]:
        show_help()
        return
    
    chart_type = sys.argv[1]
    config_path = Path(sys.argv[2])
    
    if chart_type not in AVAILABLE_TYPES:
        print(f"Error: Tipo de gráfico '{chart_type}' no reconocido.")
        show_help()
        return
    
    if not config_path.exists():
        print(f"Error: El archivo de configuración '{config_path}' no existe.")
        return
    
    # Importar la función correspondiente según el tipo de gráfico
    try:
        if chart_type == "stackedbarh":
            from app.plots.stackedbarh import stackedbarh
            stackedbarh(config_path)
        elif chart_type == "barv":
            from app.plots.barv import barv
            barv(config_path)
        elif chart_type == "linechart":
            from app.plots.linechart import linechart
            linechart(config_path)
    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
        raise

if __name__ == "__main__":
    main()