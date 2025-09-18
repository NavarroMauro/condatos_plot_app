# Análisis y Estandarización de Implementaciones Alternativas

Este documento analiza las implementaciones alternativas identificadas en el proyecto ConDatos-Figs-App y proporciona recomendaciones para estandarizar y reducir la redundancia en el código.

## 1. Múltiples Variantes de Makefile

### Situación Actual

El proyecto contiene dos implementaciones diferentes de Makefiles:

1. **Makefile principal** (`/Makefile`):
   - Contiene targets para operaciones comunes como `lint`, `fmt`, `test`, y renderización de gráficos
   - Usa `conda run` para ejecutar comandos en el entorno conda
   - Implementa smoke tests y targets específicos para diferentes tipos de gráficos

2. **Makefile de inicialización** (`/templates/init/Makefile`):
   - Versión simplificada para proyectos nuevos
   - No usa `conda run` explícitamente
   - Tiene una estructura diferente para invocar los scripts de generación de gráficos

Los archivos `Makefile.mini` y `Makefile.dynamic` mencionados en la solicitud no se encuentran actualmente en el proyecto, pero pueden haber existido en versiones anteriores o pueden estar referenciados en la documentación.

### Problemas Identificados

1. **Inconsistencia en la invocación de scripts**:
   - El Makefile principal usa `python -m app.plots.[tipo_grafico]`
   - El Makefile de inicialización usa `python -m app.plot [tipo_grafico]`

2. **Diferencias en la gestión del entorno**:
   - El Makefile principal usa `conda run -n $(ENV_NAME)`
   - El Makefile de inicialización no especifica el entorno conda

3. **Potencial confusión para nuevos desarrolladores**:
   - Las diferencias entre los archivos pueden generar incertidumbre sobre cuál es la forma "correcta" de invocar los scripts

### Recomendaciones

1. **Estandarizar la estructura de los Makefiles**:
   - Crear un Makefile base con funcionalidad común
   - Extender este base para casos específicos (desarrollo, producción, inicialización)

2. **Adoptar un enfoque consistente para invocar scripts**:
   - Elegir entre `app.plots.[tipo_grafico]` y `app.plot [tipo_grafico]` y usarlo consistentemente
   - Documentar claramente la estructura de módulos y su invocación

3. **Estandarizar la gestión del entorno**:
   - Usar `conda run -n $(ENV_NAME)` consistentemente si ese es el método preferido
   - Alternativamente, asumir que el entorno ya está activado y usar `$(PYTHON)` directamente

4. **Eliminar referencias a implementaciones obsoletas**:
   - Revisar la documentación para eliminar referencias a `Makefile.mini` o `Makefile.dynamic`
   - Actualizar cualquier guía o tutorial que mencione estas variantes

## 2. Configuración de Pre-commit

### Estado Actual

La revisión del proyecto no encontró múltiples configuraciones de pre-commit. No se encontraron:

- Archivo `.pre-commit-config.yaml`
- Directorio `.hooks/pre-commit`

Sólo se encontró el archivo de ejemplo de git hooks en `.git/hooks/pre-commit.sample`, que es estándar en cualquier repositorio git y no está activado.

### Acciones Recomendadas

1. **Implementar pre-commit hooks formalmente**:
   - Crear un archivo `.pre-commit-config.yaml` para gestionar hooks de pre-commit
   - Documentar su uso en la documentación de desarrollo

2. **Configurar hooks específicos para el proyecto**:
   - Agregar hooks para validar YAML
   - Agregar hooks para formateo de código con ruff
   - Agregar hooks para verificar sintaxis de Python
   - Considerar hooks para tests básicos

3. **Actualizar documentación**:
   - Revisar referencias a `.hooks/pre-commit` en la documentación
   - Actualizar el proceso de configuración para nuevos desarrolladores

## 3. Plan de Implementación

### Fase 1: Estandarización de Makefiles

1. Crear un `Makefile.base` con la funcionalidad compartida:

   ```makefile
   SHELL := /bin/bash
   ENV_NAME        ?= condatos-figs-app
   PYTHON          ?= $(shell which python || which python3)
   CONFIG_DIR      ?= config
   OUT_DIR         ?= out

   # Targets básicos comunes...
   ```

2. Modificar el Makefile principal para incluir este base:

   ```makefile
   include Makefile.base
   
   # Targets específicos para desarrollo...
   ```

3. Actualizar el Makefile de inicialización para usar la misma estructura

### Fase 2: Implementación de Pre-commit

1. Crear el archivo `.pre-commit-config.yaml` con configuración estándar:

   ```yaml
   repos:
   - repo: https://github.com/astral-sh/ruff-pre-commit
     rev: v0.0.287
     hooks:
     - id: ruff
       args: [--fix, --exit-non-zero-on-fix]
     - id: ruff-format
   - repo: https://github.com/pre-commit/pre-commit-hooks
     rev: v4.4.0
     hooks:
     - id: trailing-whitespace
     - id: end-of-file-fixer
     - id: check-yaml
   ```

2. Documentar la instalación y uso de pre-commit en `docs/CONTRIBUTING.md`

### Fase 3: Actualización de Documentación

1. Revisar toda la documentación para eliminar referencias a implementaciones obsoletas
2. Documentar claramente el flujo de trabajo recomendado

## 4. Beneficios de la Estandarización

1. **Mantenibilidad mejorada**:
   - Código más consistente y predecible
   - Menos confusión para nuevos desarrolladores

2. **Reducción de errores**:
   - Una única forma "correcta" de hacer las cosas
   - Validación automatizada mediante hooks de pre-commit

3. **Onboarding más rápido**:
   - Documentación clara y consistente
   - Configuración automatizada del entorno de desarrollo

4. **Base para CI/CD**:
   - Hooks de pre-commit como primera línea de defensa
   - Makefiles estandarizados para facilitar la integración con CI/CD
