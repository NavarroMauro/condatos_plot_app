#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento de las leyendas personalizadas con imágenes
y logos en ConDatos-Figs-App.

Este script ejecuta un ejemplo de gráfico con leyenda personalizada y logo,
verificando que todos los componentes se rendericen correctamente.
"""

import os
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Importar las funciones necesarias
from app.chart_utils import render_chart
from app.plots.stackedbarh import StackedHorizontalBarChart

def main():
    """Ejecutar prueba de leyenda personalizada con imágenes y logo."""
    print("\n🧪 Iniciando prueba de leyenda personalizada con imágenes y logo...")
    
    # Ruta al archivo de configuración de ejemplo
    config_path = root_dir / "config" / "ejemplo-leyenda-custom.yml"
    
    if not config_path.exists():
        print(f"❌ Archivo de configuración no encontrado: {config_path}")
        return 1
    
    print(f"📄 Usando archivo de configuración: {config_path}")
    
    try:
        # Renderizar el gráfico
        chart = render_chart(StackedHorizontalBarChart, config_path)
        print("✅ Gráfico renderizado correctamente")
        
        # Verificar que la imagen de salida existe
        outfile = root_dir / "out" / "medallas-ejemplo.png"
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