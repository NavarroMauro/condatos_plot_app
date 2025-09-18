# Estándares y Mejores Prácticas de ConDatos-Figs-App

Este documento consolida los estándares visuales, mejores prácticas de desarrollo y estandarización de implementaciones para el proyecto ConDatos-Figs-App, diseñado específicamente para visualizaciones de datos en el contexto chileno y latinoamericano.

## Índice

1. [Estándares de Visualización](#estándares-de-visualización)
   - [Principios Fundamentales](#principios-fundamentales)
   - [Paletas de Colores](#paletas-de-colores)
   - [Tipografía](#tipografía)
   - [Elementos de Identidad Regional](#elementos-de-identidad-regional)
   - [Adaptaciones por Tipo de Gráfico](#adaptaciones-por-tipo-de-gráfico)
   - [Consideraciones Bilingües](#consideraciones-bilingües)

2. [Mejores Prácticas para el Desarrollo](#mejores-prácticas-para-el-desarrollo)
   - [Control de Calidad](#control-de-calidad)
   - [Gestión de Versiones](#gestión-de-versiones)
   - [Documentación](#documentación)
   - [Manejo de Dependencias](#manejo-de-dependencias)
   - [Seguridad](#seguridad)
   - [Rendimiento](#rendimiento)
   - [Compatibilidad](#compatibilidad)

3. [Estandarización de Implementaciones](#estandarización-de-implementaciones)
   - [Análisis de Implementaciones Alternativas](#análisis-de-implementaciones-alternativas)
   - [Estandarización de Makefiles](#estandarización-de-makefiles)
   - [Configuración de Pre-commit](#configuración-de-pre-commit)
   - [Plan de Implementación](#plan-de-implementación)
   - [Beneficios de la Estandarización](#beneficios-de-la-estandarización)

---

## Estándares de Visualización

Los estándares visuales de ConDatos-Figs-App están diseñados para representar datos del contexto chileno y latinoamericano de manera clara, precisa y coherente.

### Principios Fundamentales

1. **Coherencia visual**: Todas las visualizaciones deben mantener una coherencia visual que refleje la identidad de ConDatos, similar al enfoque de Statista pero con adaptaciones regionales.

2. **Precisión y claridad**: La representación de datos debe ser precisa y clara, evitando distorsiones visuales o elementos decorativos que interfieran con la interpretación correcta.

3. **Contextualización regional**: Las visualizaciones deben considerar el contexto específico de Chile y Latinoamérica, utilizando referencias, símbolos y formatos familiares para la audiencia regional.

4. **Accesibilidad**: Los gráficos deben ser comprensibles para una amplia audiencia, incluyendo consideraciones para daltonismo y otros aspectos de accesibilidad.

### Paletas de Colores

#### Paleta Principal

La paleta principal de ConDatos está diseñada para representar datos chilenos y latinoamericanos con colores que reflejan tanto identidad visual profesional como elementos culturales regionales:

- **Azul ConDatos** (`#4ECDC4`): Color principal, representa confiabilidad y datos.
- **Rojo Chile** (`#FF6B6B`): Secundario, alude a elementos de la bandera chilena.
- **Amarillo Andino** (`#FFE66D`): Complementario, representa la diversidad regional.
- **Azul Profundo** (`#1A535C`): Para elementos estructurales y datos históricos.
- **Naranja Cálido** (`#FF9F1C`): Para destacar elementos clave o tendencias emergentes.

#### Paletas Temáticas

- **Económica**: Variaciones de azules y verdes para indicadores económicos regionales.
- **Social**: Gama de colores cálidos para indicadores sociales y demográficos.
- **Geográfica**: Paleta de verdes y marrones para representaciones territoriales.

### Tipografía

- **Principal**: Nunito, una tipografía clara y legible que funciona bien tanto en español como en inglés.
- **Alternativa**: Lato, para casos donde se necesita mayor densidad de información.

### Elementos de Identidad Regional

#### Banderas y Símbolos

- Incorporación de banderas nacionales y regionales en gráficos comparativos entre países.
- Uso consistente de símbolos monetarios regionales (CLP, USD, etc.).

#### Formatos Numéricos y Fechas

- Formato latinoamericano para fechas: DD/MM/AAAA
- Separador de miles: punto (1.000.000)
- Separador decimal: coma (1.234,56)

### Adaptaciones por Tipo de Gráfico

#### Mapas Coropléticos

- Nivel de detalle adaptado para regiones chilenas y división política latinoamericana.
- Escala de colores que considera las particularidades geográficas de la región.

#### Gráficos de Barras

- Incorporación de elementos visuales regionales (banderas, íconos) cuando sea relevante.
- Ordenamiento contextual: posibilidad de destacar Chile en comparativas regionales.

#### Gráficos de Líneas

- Marcadores de eventos relevantes para el contexto económico/social latinoamericano.
- Ajustes estacionales considerando patrones específicos del hemisferio sur.

### Consideraciones Bilingües

Para maximizar el alcance de las visualizaciones, se recomienda:

- Títulos y etiquetas principales en español con opción de versión en inglés.
- Notas metodológicas en ambos idiomas cuando sea posible.
- Nombres de países y regiones en el idioma principal del gráfico (evitar mezclas).

---

## Mejores Prácticas para el Desarrollo

Estas prácticas buscan mantener la calidad y estabilidad del proyecto ConDatos-Figs-App durante todo su ciclo de desarrollo.

### Control de Calidad

#### Pruebas Automatizadas

Todas las características nuevas y correcciones de errores deben incluir pruebas que cubran los cambios:

1. **Tests unitarios**: Para funciones y clases específicas
2. **Tests de integración**: Para verificar que los componentes funcionen juntos
3. **Smoke tests**: Para verificar rápidamente que la funcionalidad básica sigue funcionando

#### Revisión de Código

- Todo el código debe ser revisado por al menos un desarrollador antes de ser integrado
- Usar Pull Requests para facilitar la revisión
- Verificar que el código sigue las convenciones de estilo

#### CI/CD

El proyecto utiliza GitHub Actions para la integración continua:

- **Linting**: Verificación automática del formato del código
- **Tests**: Ejecución de la suite de pruebas
- **Build**: Generación de ejemplos de visualización

### Gestión de Versiones

#### Ramificación

Usar el flujo Git-Flow para el desarrollo:

1. `main`: Código en producción estable
2. `develop`: Rama de integración para nuevas características
3. `feature/*`: Ramas para nuevas características
4. `bugfix/*`: Ramas para corrección de errores
5. `release/*`: Ramas para preparar lanzamientos

#### Etiquetado

Usar versionado semántico (MAJOR.MINOR.PATCH):

- MAJOR: Cambios incompatibles con versiones anteriores
- MINOR: Nuevas funcionalidades manteniendo compatibilidad
- PATCH: Correcciones de errores manteniendo compatibilidad

### Documentación

#### Documentación de Código

- Incluir docstrings en todas las funciones, clases y métodos
- Documentar parámetros, tipos de retorno y excepciones
- Explicar lógica compleja con comentarios

#### Documentación de Proyecto

- Mantener la documentación actualizada con cada cambio
- Documentar decisiones de diseño importantes
- Incluir ejemplos de uso para nuevas funcionalidades

### Manejo de Dependencias

- Minimizar el número de dependencias externas
- Especificar rangos de versiones en lugar de versiones exactas cuando sea apropiado
- Revisar regularmente las actualizaciones de dependencias

### Seguridad

- No incluir credenciales en el código
- Usar variables de entorno para configuración sensible
- Mantener todas las dependencias actualizadas

### Rendimiento

- Optimizar el rendimiento de operaciones costosas
- Considerar el uso de memoria para conjuntos de datos grandes
- Usar perfilado para identificar cuellos de botella

### Compatibilidad

- Mantener compatibilidad con Python ≥3.10
- Asegurar que las visualizaciones funcionen en diferentes plataformas
- Probar con diferentes versiones de dependencias importantes

---

## Estandarización de Implementaciones

### Análisis de Implementaciones Alternativas

#### Múltiples Variantes de Makefile

El proyecto contiene dos implementaciones diferentes de Makefiles:

1. **Makefile principal** (`/Makefile`):
   - Contiene targets para operaciones comunes como `lint`, `fmt`, `test`, y renderización de gráficos
   - Usa `conda run` para ejecutar comandos en el entorno conda
   - Implementa smoke tests y targets específicos para diferentes tipos de gráficos

2. **Makefile de inicialización** (`/templates/init/Makefile`):
   - Versión simplificada para proyectos nuevos
   - No usa `conda run` explícitamente
   - Tiene una estructura diferente para invocar los scripts de generación de gráficos

### Problemas Identificados

1. **Inconsistencia en la invocación de scripts**:
   - El Makefile principal usa `python -m app.plots.[tipo_grafico]`
   - El Makefile de inicialización usa `python -m app.plot [tipo_grafico]`

2. **Diferencias en la gestión del entorno**:
   - El Makefile principal usa `conda run -n $(ENV_NAME)`
   - El Makefile de inicialización no especifica el entorno conda

3. **Potencial confusión para nuevos desarrolladores**:
   - Las diferencias entre los archivos pueden generar incertidumbre sobre cuál es la forma "correcta" de invocar los scripts

### Estandarización de Makefiles

Se propone estandarizar la estructura de los Makefiles mediante las siguientes acciones:

1. **Crear un Makefile base** con funcionalidad común:

   ```makefile
   SHELL := /bin/bash
   ENV_NAME        ?= condatos-figs-app
   PYTHON          ?= $(shell which python || which python3)
   CONFIG_DIR      ?= config
   OUT_DIR         ?= out

   # Targets básicos comunes...
   ```

2. **Modificar el Makefile principal** para incluir este base:

   ```makefile
   include Makefile.base
   
   # Targets específicos para desarrollo...
   ```

3. **Actualizar el Makefile de inicialización** para usar la misma estructura

4. **Adoptar un enfoque consistente** para invocar scripts:
   - Elegir entre `app.plots.[tipo_grafico]` y `app.plot [tipo_grafico]` y usarlo consistentemente
   - Documentar claramente la estructura de módulos y su invocación

5. **Estandarizar la gestión del entorno**:
   - Usar `conda run -n $(ENV_NAME)` consistentemente si ese es el método preferido
   - Alternativamente, asumir que el entorno ya está activado y usar `$(PYTHON)` directamente

### Configuración de Pre-commit

La revisión del proyecto no encontró configuraciones formales de pre-commit. Se propone:

1. **Implementar pre-commit hooks formalmente**:
   - Crear un archivo `.pre-commit-config.yaml` para gestionar hooks de pre-commit
   - Documentar su uso en la documentación de desarrollo

2. **Configurar hooks específicos para el proyecto**:

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

3. **Actualizar documentación**:
   - Revisar referencias a `.hooks/pre-commit` en la documentación
   - Actualizar el proceso de configuración para nuevos desarrolladores

### Plan de Implementación

#### Fase 1: Estandarización de Makefiles

1. Crear un `Makefile.base` con la funcionalidad compartida
2. Modificar el Makefile principal para incluir este base
3. Actualizar el Makefile de inicialización para usar la misma estructura

#### Fase 2: Implementación de Pre-commit

1. Crear el archivo `.pre-commit-config.yaml` con la configuración estándar
2. Documentar la instalación y uso de pre-commit en `docs/CONTRIBUTING.md`

#### Fase 3: Actualización de Documentación

1. Revisar toda la documentación para eliminar referencias a implementaciones obsoletas
2. Documentar claramente el flujo de trabajo recomendado

### Beneficios de la Estandarización

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

---

Estos estándares y prácticas buscan posicionar a ConDatos como referente en la visualización de datos para Chile y Latinoamérica, combinando rigor metodológico, identidad regional y calidad profesional comparable a estándares internacionales.
