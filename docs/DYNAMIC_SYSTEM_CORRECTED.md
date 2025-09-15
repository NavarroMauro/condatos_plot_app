# Sistema Dinámico de ConDatos-Figs-App

Este documento explica el funcionamiento del sistema dinámico de ConDatos-Figs-App, que permite detectar automáticamente tipos de gráficos y generar un Makefile adaptado a las configuraciones disponibles.

## Componentes Principales

El sistema dinámico se compone de los siguientes elementos:

1. **`detect_chart_type.py`**: Script que analiza un archivo de configuración YAML y recomienda el tipo de visualización más adecuado.

2. **`generate_makefile.py`**: Script que genera un Makefile dinámico basado en los archivos de configuración disponibles y sus tipos de gráficos detectados.

3. **`Makefile.dynamic`**: Versión estática del Makefile dinámico que puede servir como base o respaldo.

4. **`Makefile.auto`**: Versión generada automáticamente por `generate_makefile.py`.

## Detección Automática de Tipos de Gráficos

El script `detect_chart_type.py` analiza la estructura de los archivos YAML de configuración para determinar el tipo de gráfico más adecuado. Utiliza varios criterios:

- Declaraciones explícitas como `chart_type` en el archivo YAML
- Presencia de secciones específicas como `linechart`, `bar`, etc.
- Estructura de datos y consultas SQL (para conexiones a PostgreSQL)
- Uso de elementos como banderas o flags para identificar gráficos específicos

### Uso del Detector de Tipos

Para detectar el tipo de gráfico para una configuración específica:

```bash
python scripts/detect_chart_type.py config/mi-config.yml
```

Esto mostrará el tipo de gráfico recomendado junto con una breve descripción.

## Generación del Makefile Dinámico

El script `generate_makefile.py` detecta automáticamente:

1. Los módulos de gráficos disponibles en `app/plots/`
2. Los archivos de configuración en `config/`
3. El tipo de gráfico recomendado para cada configuración

Con esta información, genera un Makefile completo con targets para:

- Renderizar todas las configuraciones con un tipo específico de gráfico
- Renderizar una configuración específica con un tipo específico de gráfico
- Renderizar automáticamente cada configuración con su tipo de gráfico detectado

### Uso del Generador de Makefiles

Para generar un nuevo Makefile dinámico:

```bash
python scripts/generate_makefile.py
```

Esto crea el archivo `Makefile.auto` con todos los targets configurados.

Para instalar el Makefile generado como el Makefile principal (haciendo una copia de seguridad del original):

```bash
python scripts/generate_makefile.py --install
```

## Makefile Dinámico

El Makefile dinámico proporciona una interfaz unificada para trabajar con diferentes tipos de visualizaciones y configuraciones. Algunos de los comandos disponibles son:

### Comandos Principales

- `make help`: Muestra ayuda sobre los comandos disponibles
- `make auto-detect`: Detecta automáticamente el tipo de gráfico para cada configuración
- `make auto-render`: Renderiza cada configuración con su tipo de gráfico detectado
- `make <tipo>`: Renderiza todas las configuraciones como el tipo especificado (ej. `make linechart`)
- `make <tipo>:<config>`: Renderiza una configuración específica como el tipo especificado (ej. `make linechart:mi-config`)
- `make <tipo> <config>`: Sintaxis alternativa para renderizar una configuración específica (ej. `make linechart mi-config`)

### Soporte para PostgreSQL

El sistema incluye soporte básico para detectar y configurar conexiones PostgreSQL en las configuraciones:

- Target `check-postgres-env`: Verifica que las variables de entorno necesarias están configuradas
- Detección automática de consultas SQL en las configuraciones
- Adaptación de los tipos de gráficos basada en la estructura de las consultas SQL

## Ejemplo de Uso

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

## Beneficios del Sistema Dinámico

1. **Flexibilidad**: Adaptación automática a los módulos y configuraciones disponibles
2. **Facilidad de uso**: Interfaz consistente para trabajar con diferentes tipos de gráficos
3. **Detección inteligente**: Selección del tipo de gráfico más adecuado para cada configuración
4. **Soporte para PostgreSQL**: Preparado para trabajar con datos de bases de datos
5. **Mantenibilidad**: Centralización de la lógica de generación de gráficos

## Personalización

Si necesitas añadir un nuevo tipo de gráfico:

1. Crea un nuevo módulo en `app/plots/`
2. Regenera el Makefile: `python scripts/generate_makefile.py --install`
3. El nuevo tipo de gráfico estará disponible automáticamente en el sistema dinámico.
