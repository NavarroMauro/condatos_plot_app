# Refactorización y Reorganización del Proyecto ConDatos-Figs-App

Este documento describe las mejoras de organización y las refactorizaciones realizadas en el proyecto ConDatos-Figs-App para mejorar su mantenibilidad, reducir la redundancia y facilitar su uso.

## Refactorización del Script de Configuración

### Problema

El script `setup_condatos_figs.sh` original contenía código embebido para crear varios archivos (Python, YAML, Makefile, etc.) lo que hacía difícil su mantenimiento y actualización.

### Solución

1. Se extrajo todo el contenido embebido a archivos individuales en la estructura `templates/init/`.
2. Se refactorizó el script para que copie estos archivos en lugar de contenerlos directamente.
3. Se reorganizaron las funciones para mejorar la legibilidad y facilitar futuras modificaciones.

### Beneficios

- Mayor facilidad para actualizar los templates sin modificar el script principal
- Mejor organización del código fuente
- Mayor facilidad para revisar, modificar y mantener tanto el script como los templates
- Se mantiene la misma funcionalidad desde la perspectiva del usuario

### Estructura del Directorio `templates/init/`

```bash
templates/init/
├── environment.yml      # Configuración del entorno Conda
├── Makefile             # Makefile inicial
├── README.md            # README inicial
├── app/                 # Código Python inicial
│   ├── __init__.py
│   ├── io_utils.py
│   ├── plot.py
│   └── styling.py
├── config/              # Ejemplos de configuraciones YAML
│   ├── bar-ejemplo.yml
│   ├── barh-ejemplo.yml
│   ├── heatmap-ejemplo.yml
│   └── line-ejemplo.yml
├── styles/              # Estilos de matplotlib
│   └── condatos.mplstyle
└── templates/           # Templates YAML para diferentes tipos de gráficos
    ├── bar-condatos.yml
    ├── barh-condatos.yml
    ├── heatmap-condatos.yml
    └── line-condatos.yml
```

## Consolidación de Documentación

### Problema de Documentación

La documentación estaba fragmentada con archivos que contenían información redundante o estrechamente relacionada, lo que dificultaba encontrar la información necesaria y mantenerla actualizada.

### Solución para la Documentación

1. Se creó una estructura de `docs/consolidated/` para contener documentos consolidados.
2. Se combinaron documentos relacionados para crear guías completas y coherentes sobre temas específicos.
3. Se actualizó el índice de documentación para reflejar estos cambios.

### Documentos Consolidados

1. **Sistema de Tracking y Monitoreo** (`TRACKING.md`)
   - Combina `TRACKING_TOOLS.md` y `TRACKING_IMPLEMENTATION.md`
   - Proporciona una guía completa sobre las herramientas de tracking del proyecto

2. **Configuración y Personalización del Footer** (`FOOTER.md`)
   - Combina `FOOTER_CONFIGURATION.md` y `FOOTER_CUSTOMIZATION.md`
   - Proporciona una guía completa para configurar y personalizar los footers de las visualizaciones

### Beneficios de la Consolidación

- Documentación más coherente y completa
- Menos redundancia y contradicciones
- Mayor facilidad para encontrar información relevante
- Mantenimiento simplificado de la documentación

## Mejoras en la Estructura de Scripts

### Problema de Estructura de Scripts

Algunos scripts tenían múltiples responsabilidades y no seguían el principio de responsabilidad única.

### Solución para los Scripts

1. Se separaron las funcionalidades en scripts más específicos.
2. Se crearon scripts dedicados para tareas como pruebas de humo, configuración del entorno, etc.
3. Se actualizaron las referencias y la documentación.

### Scripts Mejorados

- `setup_conda_env.sh`: Configuración específica del entorno Conda
- `smoke.sh`: Script simplificado para pruebas de humo
- `run_smoke_test.sh`: Script para ejecutar todas las pruebas de humo

## Proceso de Desarrollo Futuro

Para mantener estas mejoras en futuros desarrollos:

1. **Mantener la separación de responsabilidades**:
   - Evitar scripts monolíticos con múltiples responsabilidades
   - Preferir extraer configuraciones a archivos dedicados

2. **Consolidar documentación relacionada**:
   - Identificar documentos que traten temas similares
   - Consolidarlos en guías completas y coherentes
   - Actualizar referencias y enlaces

3. **Actualizar los templates**:
   - Modificar los archivos en `templates/init/` en lugar del script de configuración
   - Verificar la coherencia con el resto del sistema

4. **Mantener el índice de documentación actualizado**:
   - Asegurar que el índice refleje la estructura actual de la documentación
   - Proporcionar descripciones claras para cada documento

5. **Estandarizar implementaciones alternativas**:
   - Revisar y estandarizar diferentes implementaciones de la misma funcionalidad
   - Consultar [docs/STANDARDIZATION.md](docs/STANDARDIZATION.md) para recomendaciones detalladas
   - Preferir un enfoque unificado para tareas comunes

## Gestión de Artefactos de Desarrollo

Se identificaron varios artefactos de desarrollo y prueba que podrían no ser necesarios en el repositorio principal:

### Artefactos Identificados

1. **Scripts de prueba específicos**:
   - `scripts/test_styles.py`: Script específico para probar estilos en el gráfico de medallas de los Juegos Panamericanos Junior 2025.

2. **Directorios de caché**:
   - `.pytest_cache/`: Caché generado por pytest durante la ejecución de tests
   - `.ruff_cache/`: Caché generado por el linter ruff

3. **Archivos temporales**:
   - `setup_condatos_figs.sh.new`: Versión alternativa del script de configuración

### Recomendaciones

1. **Actualizar el archivo `.gitignore`**:
   - Incluir patrones para directorios de caché como `.pytest_cache/` y `.ruff_cache/`
   - Incluir patrones para archivos temporales y de respaldo (como `*.bak`, `*.new`)
   - Incluir directorios de salida (`out/` si solo contiene resultados generados)

2. **Mover scripts específicos de prueba**:
   - Reubicar scripts como `test_styles.py` dentro de una carpeta dedicada como `scripts/dev/` o `tests/utils/`
   - Documentar su propósito específico y cuándo utilizarlos

3. **Normalizar archivos temporales**:
   - Eliminar archivos con extensiones `.new` o `.bak` si no son necesarios
   - Establecer una convención para archivos de trabajo en desarrollo

## Conclusión

Estas refactorizaciones y reorganizaciones han mejorado significativamente la mantenibilidad del proyecto ConDatos-Figs-App, sin modificar su funcionalidad desde la perspectiva del usuario. Las mejoras facilitan futuras extensiones y modificaciones, siguiendo principios de diseño como la separación de responsabilidades y la reducción de la redundancia. Las recomendaciones adicionales sobre la gestión de artefactos de desarrollo ayudarán a mantener el repositorio limpio y enfocado en los componentes esenciales del proyecto.
