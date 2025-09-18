#!/usr/bin/env python3
"""
Script para demostrar el uso de SVGs coloreables en las leyendas de ConDatos-Figs-App.
Este script crea un archivo de configuración temporal que usa un único SVG de medalla
y lo colorea con los colores específicos para oro, plata y bronce.
"""

import os
import sys
import yaml
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba

# Añadir el directorio raíz del proyecto al path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Crear un directorio para los archivos de ejemplo si no existe
assets_dir = root_dir / "assets" / "icons"
assets_dir.mkdir(parents=True, exist_ok=True)

# Archivo de configuración temporal
config_path = root_dir / "config" / "ejemplo-medalla-svg-coloreable.yml"

# Definir colores para las medallas
MEDAL_COLORS = {
    "oro": "#E5B13A",    # Dorado
    "plata": "#A8A9AD",  # Plateado
    "bronce": "#CD7F32"  # Bronce
}

def create_sample_svg_medal():
    """Crea un archivo SVG simple de una medalla que puede ser coloreado."""
    svg_path = assets_dir / "medal_template.svg"
    
    if svg_path.exists():
        print(f"✅ SVG de medalla ya existe: {svg_path}")
        return svg_path
        
    # Crear un SVG simple de una medalla
    svg_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- La medalla con color personalizable -->
  <circle cx="50" cy="50" r="40" fill="currentColor" stroke="black" stroke-width="2"/>
  <!-- Detalles internos también coloreables -->
  <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <!-- Brillo/reflejo de la medalla -->
  <ellipse cx="35" cy="35" rx="15" ry="12" fill="white" fill-opacity="0.4" />
  <!-- Número 1 en el centro -->
  <text x="50" y="58" text-anchor="middle" font-family="Arial" font-size="30" font-weight="bold" fill="black">1</text>
  <!-- Cinta de la medalla -->
  <rect x="45" y="5" width="10" height="15" fill="currentColor" fill-opacity="0.8"/>
  <!-- Conexión entre la cinta y la medalla -->
  <path d="M45,20 L43,30 A8,5 0 0,0 57,30 L55,20 Z" fill="currentColor" stroke="black" stroke-width="1"/>
</svg>
"""
    
    with open(svg_path, "w") as f:
        f.write(svg_content)
        
    print(f"✅ SVG de medalla creado en: {svg_path}")
    return svg_path

def create_config_file(medal_svg_path):
    """Crea un archivo de configuración que usa el SVG coloreado."""
    config = {
        "template": "templates/stackedbar-horizontal-template.yml",
        "outfile": "out/medallas-svg-ejemplo",
        "data": {
            "inline": {
                "pais": ["Chile", "Argentina", "Perú", "Colombia", "Brasil"],
                "oro": [15, 12, 8, 10, 20],
                "plata": [10, 14, 9, 11, 18],
                "bronce": [12, 15, 10, 12, 15]
            }
        },
        "title": "Medallero usando SVG Coloreado",
        "subtitle": "Ejemplo de uso de una única plantilla SVG",
        "legend_config": {
            "loc": "upper right",
            "bbox_to_anchor": [0.98, 0.15],
            "ncol": 3,
            "fontsize": 12,
            "frameon": True,
            "facecolor": "#f8f8f8",
            "title": "Tipos de medallas",
            "colorable_svg": True,  # Nueva opción para activar SVG coloreable
            "icons": [
                {
                    "label": "Oro",
                    "svg_template": str(medal_svg_path),
                    "color": MEDAL_COLORS["oro"],
                    "zoom": 0.15
                },
                {
                    "label": "Plata",
                    "svg_template": str(medal_svg_path),
                    "color": MEDAL_COLORS["plata"],
                    "zoom": 0.15
                },
                {
                    "label": "Bronce",
                    "svg_template": str(medal_svg_path),
                    "color": MEDAL_COLORS["bronce"],
                    "zoom": 0.15
                }
            ]
        }
    }
    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"✅ Archivo de configuración creado: {config_path}")
    return config_path

def main():
    """Ejecutar la prueba de SVG coloreable para medallas."""
    print("\n🧪 Iniciando prueba de SVG coloreable para medallas...\n")
    
    # Crear SVG de ejemplo
    medal_svg_path = create_sample_svg_medal()
    
    # Crear configuración
    config_path = create_config_file(medal_svg_path)
    
    # Verificar si existe la clase ColorableSVGHandler
    try:
        from app.plot_helpers import ColorableSVGHandler
        print("✅ ColorableSVGHandler está disponible en la aplicación")
    except ImportError:
        print("⚠️ ColorableSVGHandler no está implementado aún. Se requiere añadir esta funcionalidad.")
        print("  Siga las instrucciones para implementar el soporte para SVG coloreables.")
        return 1
    
    # Importar la función necesaria para renderizar
    try:
        from app.plots.stackedbarh import StackedHorizontalBarChart
        from app.chart_utils import render_chart
        print("✅ Componentes de gráficos encontrados")
    except ImportError as e:
        print(f"❌ Error al importar componentes: {e}")
        return 1
    
    # Renderizar el gráfico
    try:
        print(f"\n📊 Renderizando gráfico con SVG coloreable...\n")
        chart = render_chart(StackedHorizontalBarChart, config_path)
        print("✅ Gráfico renderizado correctamente")
        
        # Verificar que la imagen de salida existe
        outfile = root_dir / "out" / "medallas-svg-ejemplo.png"
        if outfile.exists():
            print(f"✅ Archivo de salida generado correctamente: {outfile}")
            print(f"   Tamaño: {outfile.stat().st_size / 1024:.2f} KB")
        else:
            print(f"❌ No se encontró el archivo de salida esperado: {outfile}")
            return 1
            
        print("\n🎉 Prueba completada con éxito!\n")
        return 0
        
    except Exception as e:
        print(f"❌ Error al renderizar el gráfico: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())