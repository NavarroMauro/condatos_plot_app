# Plan de Optimización de Documentación

Este documento describe el plan para optimizar y organizar la documentación del proyecto ConDatos-Figs-App.

## Objetivos

1. **Mejorar la accesibilidad de la documentación**: Hacer más fácil encontrar la información relevante
2. **Reducir la redundancia**: Consolidar documentos relacionados
3. **Estandarizar el formato**: Mantener un estilo consistente en toda la documentación
4. **Facilitar el mantenimiento**: Implementar procesos para mantener la documentación actualizada

## Análisis del Estado Actual

Actualmente, la documentación está organizada en múltiples archivos Markdown en el directorio `docs/`.
Ya se ha iniciado un proceso de consolidación con el directorio `docs/consolidated/`.

### Categorías actuales

1. **Conceptos fundamentales**: Arquitectura, estándares, formatos de datos, etc.
2. **Guías para contribuidores**: Cómo contribuir, uso de herramientas, tareas pendientes.
3. **Documentación técnica**: Personalización de componentes, sintaxis, etc.

### Problemas identificados

1. **Fragmentación excesiva**: Demasiados archivos pequeños sobre temas relacionados
2. **Redundancia**: Algunos temas se repiten en varios documentos
3. **Falta de estructura jerárquica**: La navegación entre documentos no es intuitiva
4. **Ausencia de sistema de generación de documentación**: No hay integración con docstrings del código

## Plan de Acción

### 1. Reorganización de la Estructura

Implementaremos una estructura basada en categorías claras:

```bash
docs/
├── index.md                     # Documento principal de entrada
├── getting-started/             # Primeros pasos
│   ├── index.md                 # Guía rápida de inicio
│   ├── installation.md          # Instrucciones de instalación
│   └── basic-usage.md           # Uso básico
├── user-guide/                  # Guía del usuario
│   ├── index.md                 # Índice de la guía de usuario
│   ├── configuration/           # Configuración
│   │   ├── index.md             # Introducción a la configuración
│   │   ├── visualization.md     # Configuración de visualizaciones
│   │   └── data-sources.md      # Configuración de fuentes de datos
│   └── customization/           # Personalización (consolidada)
│       ├── index.md             # Introducción a la personalización
│       ├── styles.md            # Personalización de estilos
│       ├── components.md        # Personalización de componentes
│       └── advanced.md          # Personalización avanzada
├── developer-guide/             # Guía para desarrolladores
│   ├── index.md                 # Índice para desarrolladores
│   ├── architecture.md          # Arquitectura del sistema
│   ├── contributing.md          # Cómo contribuir
│   └── standards/               # Estándares y prácticas
│       ├── index.md             # Introducción a los estándares
│       ├── code-style.md        # Estilo de código
│       ├── testing.md           # Pruebas
│       └── documentation.md     # Documentación
└── reference/                   # Referencia técnica
    ├── index.md                 # Índice de referencia
    ├── api/                     # Documentación de API
    │   └── index.md             # Índice de API
    ├── config-reference/        # Referencia de configuración
    │   └── index.md             # Índice de referencia de configuración
    └── examples/                # Ejemplos
        └── index.md             # Índice de ejemplos
```

### 2. Consolidación de Documentos Relacionados

Identificamos los siguientes grupos para consolidación:

#### Grupo 1: Personalización de Componentes

- AXIS_TITLE_CUSTOMIZATION.md
- LEGEND_CUSTOMIZATION.md
- ROTATED_LABELS.md
- VALUE_TOTAL_LABELS.md
- FOOTER_CUSTOMIZATION.md (ya consolidado en consolidated/FOOTER.md)

#### Grupo 2: Arquitectura y Diseño

- ARCHITECTURE.md
- DECISIONS.md
- DYNAMIC_SYSTEM.md
- DYNAMIC_SYSTEM_CORRECTED.md

#### Grupo 3: Estándares y Mejores Prácticas

- VISUALIZATIONS_STANDARDS.md
- BEST_PRACTICES.md
- STANDARDIZATION.md

#### Grupo 4: Guías de Desarrollo

- CONTRIBUTING.md
- TASKS.md
- COPILOT.md

### 3. Implementación de Sistema de Generación de Documentación

Implementaremos MkDocs con el tema Material para generar documentación a partir de los archivos Markdown:

1. **Instalación de herramientas**:

   ```bash
   pip install mkdocs mkdocs-material
   ```

2. **Configuración inicial**:

   ```bash
   mkdocs new .
   ```

3. **Personalización del tema y plugins**:
   Configurar `mkdocs.yml` para usar el tema Material y plugins relevantes.

4. **Integración con docstrings**:
   Usar mkdocstrings para generar documentación de API a partir de docstrings del código.

### 4. Cronograma de Implementación

1. **Fase 1: Preparación y Estructura**
   - Crear la nueva estructura de directorios
   - Configurar MkDocs
   - Desarrollar templates y estilos

2. **Fase 2: Migración y Consolidación**
   - Migrar documentos existentes a la nueva estructura
   - Consolidar documentos relacionados
   - Actualizar enlaces internos

3. **Fase 3: Generación de Documentación de API**
   - Configurar mkdocstrings
   - Mejorar docstrings en el código fuente
   - Generar documentación de API

4. **Fase 4: Revisión y Mejora**
   - Revisar toda la documentación para consistencia
   - Agregar ejemplos y casos de uso
   - Validar enlaces y referencias

### 5. Mantenimiento Continuo

1. **Automatización**:
   - Configurar GitHub Actions para construir y desplegar la documentación automáticamente
   - Validar enlaces rotos y formato Markdown en los CI checks

2. **Proceso de contribución**:
   - Actualizar las guías de contribución para incluir estándares de documentación
   - Requerir actualización de documentación en PRs que cambien funcionalidad

3. **Revisiones periódicas**:
   - Programar revisiones trimestrales de la documentación
   - Mantener una lista de mejoras pendientes

## Conclusión

Este plan proporcionará una documentación más organizada, accesible y mantenible para el proyecto ConDatos-Figs-App. La consolidación de documentos relacionados y la implementación de un sistema de generación de documentación mejorará significativamente la experiencia de los usuarios y desarrolladores.
