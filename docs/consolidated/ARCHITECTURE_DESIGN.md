# Arquitectura y Diseño del Sistema ConDatos-Figs-App

Este documento consolida la información sobre la arquitectura, decisiones de diseño y el sistema dinámico implementado en ConDatos-Figs-App, una plataforma para la creación de visualizaciones estandarizadas y profesionales adaptada específicamente para representar datos del contexto chileno y latinoamericano.

## Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
   - [Módulos Principales](#módulos-principales)
   - [Flujo de Renderización](#flujo-de-renderización)
   - [Entradas del Sistema](#entradas-del-sistema)
   - [Principios de Diseño](#principios-de-diseño)

2. [Decisiones de Arquitectura (ADR)](#decisiones-de-arquitectura-adr)
   - [Configuración de Ejes](#configuración-de-ejes)
   - [Espaciado de Títulos](#espaciado-de-títulos)
   - [Posicionamiento de Leyendas](#posicionamiento-de-leyendas)
   - [Exportación Multi-Formato](#exportación-multi-formato)
   - [Estructura del Header](#estructura-del-header)

3. [Sistema Dinámico](#sistema-dinámico)
   - [Componentes Principales](#componentes-principales-del-sistema-dinámico)
   - [Detección Automática de Tipos de Gráficos](#detección-automática-de-tipos-de-gráficos)
   - [Generación del Makefile Dinámico](#generación-del-makefile-dinámico)
   - [Comandos Principales](#comandos-principales-del-sistema-dinámico)
   - [Ejemplo de Uso](#ejemplo-de-uso-del-sistema-dinámico)

---

## Arquitectura del Sistema

ConDatos-Figs-App sigue un diseño modular centrado en la separación entre configuración (YAML) y código, permitiendo la generación consistente y estandarizada de visualizaciones para datos chilenos y latinoamericanos.

### Módulos Principales

El sistema está organizado en los siguientes módulos principales:

- **app/plot.py**: CLI Typer que implementa los comandos de generación de gráficos (`line`, `bar`, `barh`, `stackedbar`, `stackedbarh`, `heatmap`). Se encarga de cargar plantillas y configuraciones (YAML), aplicar estilos y layout, y gestionar el guardado en múltiples formatos.

- **app/layout.py**: Gestiona el frame de la figura, incluyendo header (título/subtítulo), márgenes y el proceso `finish_and_save` que inserta branding y guarda la figura.

- **app/branding.py**: Controla el footer/branding, incluyendo íconos CC, logos, y textos de fuente/nota/fecha.

- **app/io_utils.py**: Implementa `save_fig_multi(fig, base, formats, …)` para guardar la figura en múltiples formatos (PNG/SVG/PDF/JPG/WEBP/AVIF).

- **app/styling.py**: Contiene `apply_style(...)` para aplicar estilos `.mplstyle` y registrar fuentes (Nunito).

- **app/plot_helpers.py**: Utilidades diversas como autosize por número de filas, inserción de banderas en barras apiladas, y labels de segmentos y totales.

- **app/cmd_choropleth.py**: Implementa el comando de mapa coroplético utilizando GeoPandas, con soporte para schemes opcionales vía mapclassify.

- **app/helpers.py**: Funciones auxiliares para normalización de leyendas, formatos de etiqueta y helpers para gráficos de barras.

### Flujo de Renderización

El flujo general para el renderizado de gráficos sigue estos pasos:

1. **Configuración**: Carga del YAML (template + overrides)
2. **Estilo**: Aplicación del estilo mediante `apply_style()`
3. **Creación**: Generación del gráfico base con `plt.subplots()`
4. **Framing**: Aplicación del frame mediante `apply_frame()` (header/márgenes)
5. **Plotting**: Generación del gráfico específico según el tipo
6. **Finalización**: Llamada a `finish_and_save()` para insertar branding y exportar

### Entradas del Sistema

El sistema acepta las siguientes entradas comunes:

- **Template**: Ruta al archivo YAML base con la configuración
- **Overrides**: Diccionario con valores que sobrescriben el template
- **Fuentes de datos**:
  - `data.csv`: Datos desde archivo CSV
  - `data.inline`: Datos definidos directamente en el YAML
  - `data.postgresql`: *(planificado)* Datos desde base de datos PostgreSQL
- **Estilo**: Uno o varios archivos `.mplstyle`
- **Formatos**: Lista de formatos de salida (ej. `["png", "svg", "pdf", "webp"]`)

### Principios de Diseño

La arquitectura de ConDatos-Figs-App está basada en los siguientes principios:

1. **Estandarización**: Garantizar la consistencia visual entre todas las figuras producidas.
2. **Configuración declarativa**: Separar la configuración (YAML) del código para facilitar ajustes sin modificar el código.
3. **Adaptabilidad regional**: Incluir características específicas para el contexto chileno y latinoamericano (banderas, formatos regionales, etc.).
4. **Extensibilidad**: Diseño modular que permite añadir nuevos tipos de gráficos manteniendo la coherencia del sistema.
5. **Calidad de exportación**: Priorizar formatos de exportación de alta calidad adecuados para publicaciones profesionales.
6. **Templates fijos**: Utilizar templates predefinidos que aceptan datos en formatos específicos para facilitar la creación estandarizada de visualizaciones.
7. **Flexibilidad en fuentes de datos**: Soportar múltiples fuentes de datos manteniendo la consistencia visual.

## Decisiones de Arquitectura (ADR)

A continuación se detallan las principales decisiones de arquitectura (Architecture Decision Records) que han moldeado el desarrollo del sistema:

### Configuración de Ejes

**Fecha**: 2025-09-13

**Decisión**: Implementar control independiente para la visibilidad de etiquetas y ticks de ejes, permitiendo mostrar etiquetas sin ticks.

**Motivación**: Esta flexibilidad es especialmente útil para gráficos con banderas de países latinoamericanos, donde las etiquetas son necesarias pero los ticks pueden crear ruido visual.

### Espaciado de Títulos

**Fecha**: 2025-09-13

**Decisión**: Implementar un sistema de espaciado personalizable para título y subtítulo a través de la configuración `title_spacing` con control individual de márgenes.

**Motivación**: Proporcionar un control preciso sobre la disposición de elementos clave del gráfico, especialmente importante para títulos largos en español o que contienen términos técnicos específicos del contexto latinoamericano.

### Posicionamiento de Leyendas

**Fecha**: 2025-09-13

**Decisión**: Mantener tanto `loc` como `bbox_to_anchor` para posicionamiento preciso de leyendas, documentando claramente su relación.

**Motivación**: Ofrecer flexibilidad total en el posicionamiento de leyendas, permitiendo tanto posiciones predefinidas como ubicaciones personalizadas exactas. Esto es importante para adaptarse a diferentes tipos de visualizaciones y distribuciones de datos regionales.

### Exportación Multi-Formato

**Fecha**: 2025-09-09

**Decisión**: Implementar un sistema de exportación multi-formato estandarizado con `save_fig_multi` que incluye soporte para SVG minificado con scour y formatos modernos como WEBP/AVIF vía Pillow-Heif.

**Motivación**: Garantizar que todas las visualizaciones puedan ser exportadas en formatos de alta calidad para diferentes medios, asegurando coherencia visual y portabilidad.

### Estructura del Header

**Fecha**: 2025-09-09

**Decisión**: Separar el header (título y subtítulo) del área de gráfico en `layout._draw_header`.

**Motivación**: Permitir una mejor gestión del espacio en gráficos con títulos largos, frecuentes en contextos técnicos o académicos al describir datos latinoamericanos.

## Sistema Dinámico

El sistema dinámico es un componente clave que permite detectar automáticamente tipos de gráficos y generar un Makefile adaptado a las configuraciones disponibles, simplificando el flujo de trabajo para los usuarios.

### Componentes Principales del Sistema Dinámico

1. **`detect_chart_type.py`**: Script que analiza un archivo de configuración YAML y recomienda el tipo de visualización más adecuado.

2. **`generate_makefile.py`**: Script que genera un Makefile dinámico basado en los archivos de configuración disponibles y sus tipos de gráficos detectados.

3. **`Makefile.dynamic`**: Versión estática del Makefile dinámico que puede servir como base o respaldo.

4. **`Makefile.auto`**: Versión generada automáticamente por `generate_makefile.py`.

### Detección Automática de Tipos de Gráficos

El script `detect_chart_type.py` analiza la estructura de los archivos YAML de configuración para determinar el tipo de gráfico más adecuado. Utiliza varios criterios:

- Declaraciones explícitas como `chart_type` en el archivo YAML
- Presencia de secciones específicas como `linechart`, `bar`, etc.
- Estructura de datos y consultas SQL (para conexiones a PostgreSQL)
- Uso de elementos como banderas o flags para identificar gráficos específicos

Para detectar el tipo de gráfico para una configuración específica:

```bash
python scripts/detect_chart_type.py config/mi-config.yml
```

### Generación del Makefile Dinámico

El script `generate_makefile.py` detecta automáticamente:

1. Los módulos de gráficos disponibles en `app/plots/`
2. Los archivos de configuración en `config/`
3. El tipo de gráfico recomendado para cada configuración

Con esta información, genera un Makefile completo con targets para:

- Renderizar todas las configuraciones con un tipo específico de gráfico
- Renderizar una configuración específica con un tipo específico de gráfico
- Renderizar automáticamente cada configuración con su tipo de gráfico detectado

Para generar un nuevo Makefile dinámico:

```bash
python scripts/generate_makefile.py
```

Para instalar el Makefile generado como el Makefile principal (haciendo una copia de seguridad del original):

```bash
python scripts/generate_makefile.py --install
```

### Comandos Principales del Sistema Dinámico

El Makefile dinámico proporciona una interfaz unificada para trabajar con diferentes tipos de visualizaciones y configuraciones:

- **`make help`**: Muestra ayuda sobre los comandos disponibles
- **`make auto-detect`**: Detecta automáticamente el tipo de gráfico para cada configuración
- **`make auto-render`**: Renderiza cada configuración con su tipo de gráfico detectado
- **`make <tipo>`**: Renderiza todas las configuraciones como el tipo especificado (ej. `make linechart`)
- **`make <tipo>:<config>`**: Renderiza una configuración específica como el tipo especificado (ej. `make linechart:mi-config`)
- **`make <tipo> <config>`**: Sintaxis alternativa para renderizar una configuración específica (ej. `make linechart mi-config`)

#### Soporte para PostgreSQL

El sistema incluye soporte básico para detectar y configurar conexiones PostgreSQL en las configuraciones:

- Target `check-postgres-env`: Verifica que las variables de entorno necesarias están configuradas
- Detección automática de consultas SQL en las configuraciones
- Adaptación de los tipos de gráficos basada en la estructura de las consultas SQL

### Ejemplo de Uso del Sistema Dinámico

1. **Crear una nueva configuración**: Crea un archivo YAML en el directorio `config/`

2. **Regenerar el Makefile**:

   ```bash
   python scripts/generate_makefile.py --install
   ```

3. **Verificar el tipo de gráfico detectado**:

   ```bash
   make auto-detect
   ```

4. **Renderizar la configuración**:

   ```bash
   make auto-render
   ```

   O si prefieres un tipo específico:

   ```bash
   make stackedbarh:mi-config
   ```

   O usando la sintaxis alternativa:

   ```bash
   make stackedbarh mi-config
   ```

### Beneficios del Sistema Dinámico

1. **Flexibilidad**: Adaptación automática a los módulos y configuraciones disponibles
2. **Facilidad de uso**: Interfaz consistente para trabajar con diferentes tipos de gráficos
3. **Detección inteligente**: Selección del tipo de gráfico más adecuado para cada configuración
4. **Soporte para PostgreSQL**: Preparado para trabajar con datos de bases de datos
5. **Mantenibilidad**: Centralización de la lógica de generación de gráficos

### Personalización del Sistema Dinámico

Si necesitas añadir un nuevo tipo de gráfico:

1. Crea un nuevo módulo en `app/plots/`
2. Regenera el Makefile: `python scripts/generate_makefile.py --install`
3. El nuevo tipo de gráfico estará disponible automáticamente en el sistema dinámico.

---

Esta arquitectura flexible y modular permite a ConDatos-Figs-App servir como una plataforma robusta para la creación de visualizaciones estandarizadas que representan efectivamente datos en el contexto chileno y latinoamericano, manteniendo una alta calidad visual y facilitando el proceso de generación.
