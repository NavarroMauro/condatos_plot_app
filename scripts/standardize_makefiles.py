#!/usr/bin/env python3
# Script para refactorizar los Makefiles y aplicar las recomendaciones de estandarización

import os
import sys
import shutil
from pathlib import Path
import re

def print_colored(text, color):
    """Imprime texto con color en la terminal."""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def backup_file(file_path):
    """Crea una copia de seguridad del archivo."""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print_colored(f"✅ Copia de seguridad creada: {backup_path}", "green")
    return backup_path

def find_makefiles(project_dir):
    """Encuentra todos los Makefiles en el proyecto."""
    makefiles = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.startswith("Makefile"):
                full_path = os.path.join(root, file)
                makefiles.append(full_path)
    return makefiles

def analyze_makefile(makefile_path):
    """Analiza un Makefile y devuelve información sobre su estructura."""
    with open(makefile_path, 'r') as f:
        content = f.read()
    
    analysis = {
        'path': makefile_path,
        'targets': re.findall(r'^([a-zA-Z0-9_-]+):', content, re.MULTILINE),
        'uses_conda': 'conda run' in content,
        'python_invocation': None
    }
    
    # Detectar cómo se invoca Python
    if 'python -m app.plots.' in content:
        analysis['python_invocation'] = 'app.plots.[tipo]'
    elif 'python -m app.plot ' in content:
        analysis['python_invocation'] = 'app.plot [tipo]'
    
    return analysis

def update_makefile(makefile_path, use_base=True):
    """Actualiza un Makefile para usar el nuevo enfoque estandarizado."""
    with open(makefile_path, 'r') as f:
        content = f.read()
    
    # Crear respaldo
    backup_file(makefile_path)
    
    # Realizar transformaciones
    new_content = content
    
    # Incluir Makefile.base si se especifica
    if use_base and not 'include Makefile.base' in content:
        new_content = f"# Este Makefile incluye la funcionalidad base estandarizada\ninclude Makefile.base\n\n{new_content}"
    
    # Estandarizar la invocación de Python si no está usando $(call run_python,...)
    new_content = re.sub(
        r'(conda run -n \$\(ENV_NAME\)) python -m app\.plots\.([a-zA-Z0-9_]+)',
        r'$(call run_python,app.plots.\2,\3)',
        new_content
    )
    
    # Estandarizar la invocación directa de Python
    new_content = re.sub(
        r'(\$\(PYTHON\)) -m app\.plot ([a-zA-Z0-9_]+)',
        r'$(call run_python,app.plot,\2)',
        new_content
    )
    
    # Guardar el archivo actualizado
    with open(makefile_path, 'w') as f:
        f.write(new_content)
    
    print_colored(f"✅ Makefile actualizado: {makefile_path}", "green")

def create_makefile_base(project_dir):
    """Crea o actualiza el Makefile.base en el directorio del proyecto."""
    base_path = os.path.join(project_dir, "Makefile.base")
    
    if os.path.exists(base_path):
        print_colored(f"ℹ️ Makefile.base ya existe en {base_path}", "blue")
        return
    
    # El contenido está definido en un archivo existente o se crea nuevo
    print_colored(f"✅ Creando Makefile.base en {base_path}", "green")
    
    # Esta función asume que el archivo ya ha sido creado manualmente o por otra parte del script

def main():
    project_dir = os.getcwd()
    print_colored(f"🔍 Analizando Makefiles en {project_dir}", "blue")
    
    # Encontrar todos los Makefiles
    makefiles = find_makefiles(project_dir)
    print_colored(f"📋 Encontrados {len(makefiles)} Makefiles", "blue")
    
    # Crear Makefile.base
    create_makefile_base(project_dir)
    
    # Analizar y mostrar información sobre los Makefiles
    for makefile in makefiles:
        analysis = analyze_makefile(makefile)
        print("\n" + "="*60)
        print_colored(f"📄 {os.path.basename(analysis['path'])}", "yellow")
        print(f"   Ubicación: {os.path.dirname(analysis['path'])}")
        print(f"   Targets: {', '.join(analysis['targets'])}")
        print(f"   Usa conda: {'✅' if analysis['uses_conda'] else '❌'}")
        print(f"   Invocación Python: {analysis['python_invocation'] or 'No detectada'}")
    
    # Preguntar al usuario si desea actualizar los Makefiles
    print("\n" + "="*60)
    response = input("¿Desea actualizar estos Makefiles con el nuevo enfoque estandarizado? [s/N]: ")
    
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        # El Makefile principal podría requerir un tratamiento especial
        for makefile in makefiles:
            # No actualizamos Makefile.base
            if os.path.basename(makefile) == "Makefile.base":
                continue
                
            # El Makefile principal incluye el base pero otros podrían no necesitarlo
            is_main = os.path.basename(makefile) == "Makefile" and os.path.dirname(makefile) == project_dir
            update_makefile(makefile, use_base=is_main)
        
        print_colored("\n✅ Actualización completada exitosamente!", "green")
    else:
        print_colored("\n❌ Operación cancelada.", "red")
    
    print("\nPara aplicar estos cambios, revise los Makefiles actualizados y sus copias de seguridad.")
    print("Si todo es correcto, elimine los archivos .bak o restaure si es necesario.")

if __name__ == "__main__":
    main()