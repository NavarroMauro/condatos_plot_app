#!/usr/bin/env python
# Prueba de estilos para el gráfico de medallas de los Juegos Panamericanos Junior 2025
# Este script genera el mismo gráfico con diferentes estilos para comparar

import os
import sys
import shutil
from pathlib import Path
import yaml

# Obtener el directorio del proyecto
project_dir = Path(__file__).parent.parent
print(f"Directorio del proyecto: {project_dir}")

# Estilos disponibles
styles = [
    "condatos",    # El estilo predeterminado
    "minimal",     # Estilo minimalista moderno
    "dark",        # Estilo oscuro/nocturno
    "vibrant",     # Estilo colorido y vibrante
]

# Paletas de colores específicas para cada estilo
color_palettes = {
    "condatos": {  # Mantiene los colores originales
        "oro": "#B6862C",
        "plata": "#7D7D7D",
        "bronce": "#8C5A2B"
    },
    "minimal": {
        "oro": "#F28E2B",
        "plata": "#4E79A7",
        "bronce": "#E15759"
    },
    "dark": {
        "oro": "#e5c07b",
        "plata": "#61afef",
        "bronce": "#e06c75"
    },
    "vibrant": {
        "oro": "#FFE66D",
        "plata": "#4ECDC4",
        "bronce": "#FF6B6B"
    }
}

# Nombre del archivo de configuración
config_file = "config/medallas-juegos-panamericanos-junior-2025-stacked-horizontal.yml"
config_path = project_dir / config_file

# Cargar la configuración actual
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Crear copia de seguridad del archivo original
backup_path = config_path.with_suffix(".yml.bak")
shutil.copy2(config_path, backup_path)
print(f"✅ Se ha creado una copia de seguridad en: {backup_path}")

# Directorio para guardar las diferentes versiones
output_dir = project_dir / "out"
output_dir.mkdir(exist_ok=True)

# Generar versiones con diferentes estilos
for style_name in styles:
    print(f"\n🎨 Generando versión con estilo: {style_name}")
    
    # Actualizar configuración para este estilo
    style_path = f"styles/{style_name}.mplstyle"
    config["style"] = style_path
    
    # Actualizar la paleta de colores
    config["colors"] = color_palettes[style_name]
    
    # Actualizar nombre de archivo de salida para incluir el estilo
    original_outfile = config["outfile"]
    config["outfile"] = f"{original_outfile}-{style_name}"
    
    # Guardar la configuración modificada
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Ejecutar el script de generación del gráfico
    print(f"⚙️  Ejecutando: make stackedbarh")
    os.system("make stackedbarh")
    
    print(f"✅ Gráfico generado: {config['outfile']}")

# Restaurar la configuración original
shutil.copy2(backup_path, config_path)
print(f"\n✅ Configuración original restaurada")
print(f"🎉 Se han generado {len(styles)} versiones del gráfico con diferentes estilos")
print(f"📁 Revisa los archivos generados en el directorio: {output_dir}")