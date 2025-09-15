# Condatos-figs - Guía de Uso

Este proyecto proporciona herramientas para generar gráficos con estilos preestablecidos para Condatos.

## Estructura del Proyecto

```plaintext
condatos-figs/
├── app/                      # Código de la aplicación
│   ├── __init__.py
│   ├── branding.py           # Manejo de fuentes y estilos corporativos
│   ├── plots/                # Implementaciones de diferentes tipos de gráficos
│   │   ├── __init__.py
│   │   ├── base_chart.py     # Clase base para todos los gráficos
│   │   └── stackedbarh.py    # Implementación de gráfico de barras horizontales apiladas
│   └── styling.py            # Utilidades para aplicar estilos a gráficos
├── assets/                   # Recursos como imágenes
│   ├── flags/                # Banderas de países
│   └── logos/                # Logos corporativos
├── config/                   # Configuraciones YAML para los gráficos
│   └── ejemplo-stackedbarh.yml  # Ejemplo para gráfico de barras horizontales
├── data/                     # Archivos de datos para los gráficos
│   └── medallas-juegos-panamericanos-junior-2025.csv
├── fonts/                    # Fuentes personalizadas
├── main.py                   # Punto de entrada principal
├── output/                   # Directorio donde se guardan los gráficos generados
├── scripts/                  # Scripts auxiliares
│   └── create_logo.py        # Script para crear logo temporal
└── styles/                   # Estilos de matplotlib (.mplstyle)
    └── condatos.mplstyle     # Estilo para gráficos de Condatos
```

## Instalación

1. Clona el repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso Básico

Para generar un gráfico de barras horizontales apiladas:

```bash
python main.py config/ejemplo-stackedbarh.yml
```

## Creación de Configuraciones YAML

Puedes crear tus propias configuraciones YAML basándote en los ejemplos proporcionados.

### Ejemplo para Gráfico de Barras Horizontales Apiladas

```yaml
# Datos de entrada
data:
  csv: "data/medallas-juegos-panamericanos-junior-2025.csv"
  category_col: "pais"  # Columna que contiene las categorías

# Configuración de estilos y dimensiones
style: "styles/condatos.mplstyle"
width_in: 12
height_in: 8

# Título y subtítulo
title: "Medallero Juegos Panamericanos Junior Cali 2025"
subtitle: "Top 10 países con más medallas"

# Colores para las series
colors:
  "oro": "#E5B13A"    # Dorado
  "plata": "#A8A9AD"  # Plateado
  "bronce": "#CD7F32" # Bronce

# Configuración de salida
outfile: "output/medallero-panamericanos-2025.png"
formats: ["png", "pdf"]
dpi: 300
```

## Personalización

### Estilos

Puedes crear tus propios estilos en archivos `.mplstyle` en el directorio `styles/`.

### Nuevos tipos de gráficos

Para implementar un nuevo tipo de gráfico:

1. Crea un nuevo archivo en `app/plots/` (ej: `line_chart.py`)
2. Implementa una clase que herede de `BaseChart`
3. Implementa los métodos abstractos `configure_axes()` y `draw_chart()`
4. Añade una función comando que use la clase
5. Registra la función en `main.py`

## Ejemplos

### Gráfico de barras horizontales apiladas

![Ejemplo de Gráfico](/output/medallero-panamericanos-2025.png)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue las guías de estilo y documenta adecuadamente tu código.
