#!/bin/bash
# Script para reorganizar los artefactos de desarrollo y mejorar la estructura del proyecto

echo "🧹 Reorganización de artefactos de desarrollo"
echo "============================================="

# Directorio base del proyecto
PROJECT_DIR=$(pwd)
echo "📁 Directorio del proyecto: $PROJECT_DIR"

# Crear estructura para scripts de desarrollo si no existe
if [ ! -d "$PROJECT_DIR/scripts/dev" ]; then
  echo "📁 Creando directorio para scripts de desarrollo..."
  mkdir -p "$PROJECT_DIR/scripts/dev"
fi

# Mover scripts específicos de desarrollo
if [ -f "$PROJECT_DIR/scripts/test_styles.py" ]; then
  echo "🔄 Moviendo test_styles.py a scripts/dev/..."
  cp "$PROJECT_DIR/scripts/test_styles.py" "$PROJECT_DIR/scripts/dev/"
  echo "✅ Script copiado correctamente"
fi

# Actualizar gitignore
echo "📝 Actualizando .gitignore..."
if [ -f "$PROJECT_DIR/.gitignore.new" ]; then
  echo "🔄 Encontrado .gitignore.new, aplicando cambios..."
  mv "$PROJECT_DIR/.gitignore.new" "$PROJECT_DIR/.gitignore"
  echo "✅ .gitignore actualizado correctamente"
else
  echo "⚠️ No se encontró .gitignore.new, creando uno nuevo..."
  cat > "$PROJECT_DIR/.gitignore" << EOF
# Archivos temporales del sistema
*.swp
*.swo
*~
.DS_Store

# Caché y directorios de compilación
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.ruff_cache/
*.so
.coverage
htmlcov/
coverage.xml

# Directorios y archivos de entorno
env/
venv/
ENV/
.env
.venv
.Python
.python-version

# Configuración del editor
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
.idea/

# Archivos de proyecto y dependencias
*.egg-info/
.installed.cfg
*.egg

# Archivos temporales y de respaldo
*.bak
*.new
*.tmp
netlog.json

# Directorios de salida (si solo contienen resultados generados)
# out/

# Archivos específicos del proyecto
# setup_condatos_figs.sh.new
EOF
  echo "✅ .gitignore creado correctamente"
fi

# Limpiar archivos temporales y de respaldo
echo "🧹 Buscando archivos temporales y de respaldo para limpiar..."
BACKUP_FILES=$(find "$PROJECT_DIR" -type f -name "*.bak" -o -name "*.tmp")
if [ -n "$BACKUP_FILES" ]; then
  echo "📋 Archivos de respaldo encontrados:"
  echo "$BACKUP_FILES"
  echo "⚠️ Los siguientes archivos son copias de seguridad que podrían eliminarse:"
  echo "$BACKUP_FILES"
  echo "Para eliminarlos, ejecuta: find \"$PROJECT_DIR\" -type f -name \"*.bak\" -o -name \"*.tmp\" -delete"
else
  echo "✅ No se encontraron archivos temporales o de respaldo"
fi

# Verificar archivos .new
NEW_FILES=$(find "$PROJECT_DIR" -type f -name "*.new")
if [ -n "$NEW_FILES" ]; then
  echo "📋 Archivos .new encontrados:"
  echo "$NEW_FILES"
  echo "⚠️ Los siguientes archivos tienen extensión .new y podrían requerir revisión:"
  echo "$NEW_FILES"
  echo "Revisa estos archivos y decide si deben reemplazar a sus versiones originales"
else
  echo "✅ No se encontraron archivos con extensión .new"
fi

echo "✅ Reorganización de artefactos de desarrollo completada"
echo "📘 Consulta REFACTORING.md para más detalles sobre la organización del proyecto"