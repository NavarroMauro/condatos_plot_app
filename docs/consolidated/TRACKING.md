# Sistema de Tracking y Monitoreo del Proyecto

Este documento consolida toda la información sobre el sistema de tracking y monitoreo implementado en el proyecto ConDatos-Figs-App. El objetivo es mantener la calidad del código, prevenir regresiones y asegurar que no se introduzcan cambios que quiebren la funcionalidad existente.

## Índice

1. [Introducción](#introducción)
2. [Herramientas Implementadas](#herramientas-implementadas)
   - [Pre-commit Hooks](#pre-commit-hooks)
   - [Tests Automatizados](#tests-automatizados)
   - [Cobertura de Código](#cobertura-de-código)
   - [Verificaciones de Seguridad](#verificaciones-de-seguridad)
   - [CI/CD con GitHub Actions](#cicd-con-github-actions)
   - [Dependabot](#dependabot)
   - [Health Checks](#health-checks)
   - [Verificación de Documentación](#verificación-de-documentación)
3. [Comandos Make para Desarrollo](#comandos-make-para-desarrollo)
4. [Flujo de Trabajo Recomendado](#flujo-de-trabajo-recomendado)
5. [Detalles de Implementación](#detalles-de-implementación)
   - [Sistema de Pre-commit Hooks](#sistema-de-pre-commit-hooks)
   - [Suite de Tests Ampliada](#suite-de-tests-ampliada)
   - [Monitoreo de Cobertura](#monitoreo-de-cobertura)
   - [Verificación de Seguridad](#verificación-de-seguridad)
   - [Health Check del Proyecto](#health-check-del-proyecto)
   - [Actualización Automática de Dependencias](#actualización-automática-de-dependencias)
   - [Documentación Centralizada](#documentación-centralizada)

## Introducción

El sistema de tracking y monitoreo implementado tiene como objetivos principales:

1. **Detectar problemas temprano:** Identificar errores, vulnerabilidades y problemas de calidad durante el desarrollo
2. **Mantener la calidad:** Asegurar que el código sigue los estándares definidos
3. **Prevenir regresiones:** Evitar que cambios nuevos rompan funcionalidades existentes
4. **Facilitar la contribución:** Proporcionar herramientas para que los desarrolladores verifiquen su código
5. **Automatizar verificaciones:** Reducir el trabajo manual de revisión

## Herramientas Implementadas

### Pre-commit Hooks

Los hooks de pre-commit verifican automáticamente que el código cumple con los estándares antes de permitir un commit.

#### Instalación

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks en el repositorio local
pre-commit install
```

#### Hooks disponibles

- **ruff**: Linter y formateador de Python
- **trailing-whitespace**: Elimina espacios en blanco al final de las líneas
- **end-of-file-fixer**: Asegura que los archivos terminen con una línea en blanco
- **check-yaml**: Valida archivos YAML
- **check-json**: Valida archivos JSON
- **poetry-check**: Valida el archivo pyproject.toml
- **bandit**: Análisis de seguridad de código
- **isort**: Ordena los imports
- **pytest-check**: Ejecuta los tests básicos
- **check-chart-detection**: Verifica el detector de tipos de gráficos
- **check-makefile-mini**: Verifica que el Makefile.mini funcione

#### Uso manual

```bash
# Ejecutar los hooks en todos los archivos
pre-commit run --all-files
```

### Tests Automatizados

El proyecto incluye varios niveles de tests automatizados:

#### Tests Unitarios

Tests básicos para verificar componentes individuales:

```bash
pytest tests/test_basic.py
```

Verifican:

- Carga de configuraciones
- Inicialización de gráficos
- Funciones auxiliares
- Procesamiento de datos

#### Tests de Integración

Tests que verifican la interacción entre componentes y la calidad visual de las gráficas:

```bash
pytest tests/test_integration.py
```

Verifican:

- Interacción entre componentes
- Generación correcta de visualizaciones
- Aplicación de estilos
- Configuración de elementos visuales

#### Tests End-to-End

Tests completos de flujo de trabajo, desde la configuración hasta la generación de visualizaciones:

```bash
pytest tests/test_end_to_end.py
```

Verifican:

- Flujo completo desde configuración hasta imagen final
- Generación de múltiples formatos de salida
- Validación de configuraciones
- Funcionamiento del sistema de detección de tipos de gráficos

#### Ejecución de todos los tests

```bash
pytest
# o usando make
make -f Makefile.dev dev-test
```

### Cobertura de Código

La cobertura de código mide qué porcentaje del código es ejecutado durante los tests:

#### Generación de reportes de cobertura

```bash
# Usando el script dedicado
python scripts/check_coverage.py

# o usando make
make -f Makefile.dev dev-coverage
```

El script generará:

- Un reporte en terminal
- Un reporte HTML en el directorio `coverage_html/`
- Un archivo XML `coverage.xml` para integración con servicios como Codecov

#### Visualización en GitHub

Los reportes de cobertura se envían a Codecov automáticamente en cada push a través de GitHub Actions. Puedes ver el badge de cobertura en el README y los reportes detallados en Codecov.

### Verificaciones de Seguridad

El proyecto incluye herramientas para detectar vulnerabilidades:

#### Análisis de seguridad local

```bash
# Usando el script dedicado
python scripts/security_scan.py

# o usando make
make -f Makefile.dev dev-security
```

El script realiza:

- Análisis de seguridad del código con Bandit
- Verificación de vulnerabilidades en dependencias con Safety
- Generación de reportes en el directorio `security_reports/`

#### Verificación automática en CI/CD

Cada push activa verificaciones de seguridad automáticas en GitHub Actions:

- Escaneo del código con Bandit
- Verificación de dependencias con Safety

### CI/CD con GitHub Actions

El workflow de CI/CD en `.github/workflows/ci.yml` ejecuta automáticamente:

1. **Tests en múltiples versiones de Python** (3.9, 3.10, 3.11)
2. **Linting** con ruff
3. **Tests** con pytest
4. **Cobertura de código** y envío a Codecov
5. **Análisis de seguridad** con Bandit y Safety
6. **Smoke tests** usando el Makefile.mini
7. **Verificación de la generación del Makefile**
8. **Detección de tipos de gráficos**

En el caso de pushes a `main` o `develop`, también:
9. **Generación de ejemplos** de visualizaciones
10. **Publicación de artefactos** para revisión

### Dependabot

Dependabot está configurado para mantener las dependencias actualizadas automáticamente:

- Actualiza dependencias de Python semanalmente (los lunes)
- Actualiza Actions de GitHub mensualmente
- Limita a 5 PRs abiertos simultáneamente para evitar ruido
- Aplica etiquetas para facilitar la identificación de PRs
- Ignora actualizaciones menores en dependencias críticas como matplotlib y pandas

La configuración se encuentra en `.github/dependabot.yml`.

### Health Checks

Los health checks verifican el estado general del proyecto:

```bash
# Usando el script dedicado
python scripts/project_health_check.py

# o usando make (pendiente de implementación)
make -f Makefile.dev dev-health-check
```

Verificaciones incluidas:

- Dependencias obsoletas
- TODOs pendientes
- Archivos que no siguen las convenciones
- Docstrings faltantes
- Componentes sin tests
- Cobertura de tests
- Análisis del historial de commits

### Verificación de Documentación

Se asegura que la documentación se mantiene actualizada:

```bash
# Usando el script dedicado
python scripts/check_docs.py

# o usando make
make -f Makefile.dev dev-check-docs
```

Verificaciones incluidas:

- Enlaces rotos
- Formatos Markdown correctos
- Docstrings completos
- Ejemplos YAML válidos
- Archivos referenciados existentes

## Comandos Make para Desarrollo

El archivo `Makefile.dev` incluye comandos para tareas comunes de desarrollo:

```bash
# Configurar entorno de desarrollo
make -f Makefile.dev dev-setup

# Ejecutar tests
make -f Makefile.dev dev-test

# Verificar cobertura de código
make -f Makefile.dev dev-coverage

# Ejecutar análisis de seguridad
make -f Makefile.dev dev-security

# Verificar documentación
make -f Makefile.dev dev-check-docs

# Ejecutar linting
make -f Makefile.dev dev-lint

# Formatear código
make -f Makefile.dev dev-format

# Verificar salud del proyecto
make -f Makefile.dev dev-health-check

# Verificación completa (lint, format, test)
make -f Makefile.dev dev-check-all

# Preparar un Pull Request (ejecuta todas las verificaciones)
make -f Makefile.dev dev-prepare-pr
```

## Flujo de Trabajo Recomendado

1. **Antes de comenzar a desarrollar**:

   ```bash
   make -f Makefile.dev dev-setup
   ```

2. **Durante el desarrollo**:

   ```bash
   make -f Makefile.dev dev-lint  # Verificar errores
   make -f Makefile.dev dev-format  # Formatear código
   make -f Makefile.dev dev-test  # Ejecutar tests
   ```

3. **Antes de hacer commit**:

   ```bash
   # Los hooks de pre-commit se ejecutarán automáticamente
   # También puedes ejecutarlos manualmente:
   pre-commit run --all-files
   ```

4. **Antes de enviar un Pull Request**:

   ```bash
   make -f Makefile.dev dev-prepare-pr
   ```

5. **Después de enviar el PR**:
   - Revisa los resultados de las Actions de GitHub
   - Verifica el reporte de cobertura en Codecov
   - Atiende cualquier issue detectado

Siguiendo este flujo de trabajo, asegurarás que el proyecto mantenga altos estándares de calidad y evitarás introducir cambios que quiebren la funcionalidad existente.

## Detalles de Implementación

### Sistema de Pre-commit Hooks

Se ha implementado un sistema completo de pre-commit hooks para verificar automáticamente el código antes de cada commit:

- **Archivo:** `.pre-commit-config.yaml`
- **Hooks implementados:**
  - **ruff**: Linter y formateador para código Python
  - **isort**: Ordenamiento de imports
  - **bandit**: Análisis de seguridad
  - **check-yaml/json**: Validación de archivos de configuración
  - **pytest-check**: Ejecución automática de tests básicos
  - **check-chart-detection**: Verificación del detector de tipos de gráficos
  - **check-makefile-mini**: Verificación del Makefile simplificado

### Suite de Tests Ampliada

Se han creado tres niveles de tests automatizados para verificar el funcionamiento correcto del sistema:

- **Tests unitarios** (`test_basic.py`): Verifican componentes individuales
- **Tests de integración** (`test_integration.py`): Verifican la interacción entre componentes y la calidad visual
- **Tests end-to-end** (`test_end_to_end.py`): Verifican el flujo completo desde la configuración hasta la generación de visualizaciones

Los tests incluyen verificaciones de:

- Carga de configuraciones
- Inicialización de gráficos
- Carga de datos
- Calidad visual de las imágenes generadas
- Generación de múltiples formatos de salida
- Validación de configuraciones
- Funcionamiento del sistema de detección de tipos de gráficos

### Monitoreo de Cobertura

Se ha implementado un sistema completo para monitorear la cobertura de código:

- **Script dedicado:** `scripts/check_coverage.py` para generación local de reportes
- **Integración en CI/CD:** Envío automático de datos de cobertura a Codecov
- **Badge en README:** Visualización del porcentaje de cobertura
- **Reportes visuales:** Generación de reportes HTML y XML

### Verificación de Seguridad

Se han integrado herramientas para detectar vulnerabilidades en el código y las dependencias:

- **Script dedicado:** `scripts/security_scan.py` para análisis local
- **Integración en CI/CD:** Verificación automática en cada push
- **Bandit:** Análisis estático de seguridad del código
- **Safety:** Verificación de dependencias con vulnerabilidades conocidas
- **Generación de reportes:** JSON y HTML para revisión detallada

### Health Check del Proyecto

Se ha desarrollado un sistema de verificación completa de la salud del proyecto:

- **Script dedicado:** `scripts/project_health_check.py` para análisis local
- **Verificaciones:**
  - Dependencias obsoletas
  - TODOs pendientes
  - Cobertura de tests
  - Docstrings faltantes
  - Convenciones de nomenclatura
  - Análisis del historial de commits
- **Generación de reportes:** Reportes detallados con recomendaciones

### Actualización Automática de Dependencias

Se ha configurado Dependabot para mantener las dependencias actualizadas:

- **Actualización semanal** de dependencias de Python
- **Actualización mensual** de GitHub Actions
- **Gestión de etiquetas** para PRs de actualización
- **Configuración de límites** para evitar ruido
- **Exclusiones** para dependencias críticas

### Documentación Centralizada

Se ha creado documentación detallada sobre todas las herramientas y procesos:

- **Archivo:** `docs/TRACKING.md` (este documento)
- **Contenido:**
  - Descripción de todas las herramientas implementadas
  - Guías de uso para cada herramienta
  - Flujo de trabajo recomendado
  - Referencias a configuraciones
  - Detalles de implementación

---

## Resumen de Herramientas de Tracking Implementadas

1. **Pre-commit Hooks** (`.pre-commit-config.yaml`): Verificación automática antes de cada commit
2. **Tests Automatizados** (`tests/`): Tests unitarios, de integración y end-to-end
3. **Cobertura de Código** (`scripts/check_coverage.py`): Monitoreo de la cobertura de tests
4. **Seguridad** (`scripts/security_scan.py`): Detección de vulnerabilidades
5. **Verificación de Documentación** (`scripts/check_docs.py`): Validación de documentación
6. **Health Check** (`scripts/project_health_check.py`): Verificación completa del proyecto
7. **CI/CD** (`.github/workflows/ci.yml`): Integración continua con GitHub Actions
8. **Dependabot** (`.github/dependabot.yml`): Actualización automática de dependencias
9. **Comandos Make** (`Makefile.dev`): Tareas de desarrollo simplificadas
10. **Documentación de Tracking** (`docs/TRACKING.md`): Guía detallada del sistema

Estas herramientas trabajan en conjunto para proporcionar un sistema robusto de tracking del proyecto.
