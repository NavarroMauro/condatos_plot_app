# Configuración de Etiquetas de Valores y Totales

Este documento describe las opciones para configurar las etiquetas de valores en los segmentos de las barras y los totales al final de las barras en los gráficos de ConDatos, con enfoque en visualizaciones de datos chilenos y comparativas regionales latinoamericanas.

## Etiquetas de Valores en Segmentos

Las etiquetas de valores muestran el valor numérico dentro de cada segmento de las barras apiladas. Se configuran con los siguientes parámetros:

```yaml
# Activar/desactivar etiquetas de valores dentro de las barras
value_labels: true|false

# Formato para las etiquetas de valores (usando sintaxis de Python)
value_format: "{:.0f}"  # Entero sin decimales
# Otros ejemplos de formatos:
# value_format: "{:.1f}" # Un decimal
# value_format: "{:,.0f}" # Entero con separador de miles

# Configuración avanzada de las etiquetas de valores
value_labels_config:
  font_size: 10           # Tamaño de fuente para las etiquetas
  font_weight: "bold"     # Peso de la fuente: normal, bold
  # color: "auto"         # Por defecto determina el color automáticamente para contraste
```

### Ejemplos de Configuración

```yaml
# Mostrar etiquetas con valores enteros (sin decimales)
value_labels: true
value_format: "{:.0f}"

# Mostrar etiquetas con un decimal
value_labels: true
value_format: "{:.1f}"

# Mostrar etiquetas con separador de miles
value_labels: true
value_format: "{:,.0f}"

# Configuración completa con tamaño de fuente y peso personalizados
value_labels: true
value_format: "{:.0f}"
value_labels_config:
  font_size: 12
  font_weight: "bold"
```

## Etiquetas de Totales al Final de las Barras

Las etiquetas de totales muestran la suma total de cada barra al final de la misma. Se configuran con los siguientes parámetros:

```yaml
# Configuración de etiquetas de totales
total_labels:
  enabled: true|false         # Activar/desactivar etiquetas de totales
  x_offset: 4                 # Distancia desde el final de la barra (en puntos)
  font_size: 12               # Tamaño de fuente para las etiquetas
  font_weight: "bold"         # Peso de la fuente: normal, bold
  color: "#333333"            # Color del texto para las etiquetas de totales
  format: "{:.0f}"            # Formato para los valores totales (similar a value_format)
```

### Ejemplos de Totales

```yaml
# Configuración básica para mostrar totales
total_labels:
  enabled: true
  x_offset: 4
  font_size: 12
  font_weight: "bold"

# Configuración con mayor espacio y fuente más grande
total_labels:
  enabled: true
  x_offset: 8
  font_size: 14
  font_weight: "bold"

# Configuración con fuente normal (no negrita)
total_labels:
  enabled: true
  x_offset: 4
  font_size: 12
  font_weight: "normal"
```

## Combinando Configuraciones

Es posible usar tanto etiquetas de valores como etiquetas de totales simultáneamente para crear gráficos más informativos:

```yaml
# Mostrar tanto valores en segmentos como totales
value_labels: true
value_format: "{:.0f}"

total_labels:
  enabled: true
  x_offset: 6
  font_size: 12
  font_weight: "bold"
```

## Recomendaciones Específicas para Datos Regionales

### Formato Numérico para Indicadores Chilenos

En Chile y gran parte de Latinoamérica se utiliza la coma como separador decimal y el punto como separador de miles. Para adaptar las etiquetas a estos formatos:

```yaml
# Para valores monetarios en pesos chilenos
value_format: "${:,.0f}"  # Ejemplo: $1.234.567

# Para valores decimales con la coma como separador decimal
value_format_cl: "{:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
# Esto producirá formato como: 1.234,5
```

### Etiquetas para Comparativas Regionales

Cuando se comparan datos entre países de Latinoamérica, considere estas configuraciones:

```yaml
# Destacar visualmente a Chile en las comparativas
total_labels:
  enabled: true
  x_offset: 6
  font_size: 12
  font_weight: "bold"
  color_map:
    "Chile": "#D22730"  # Color rojo para los totales de Chile
    "default": "#333333"  # Color por defecto para los demás países
```

## Ejemplos Completos para Casos de Uso Regional

### Comparativa de Indicadores Económicos de Países Latinoamericanos

```yaml
# Gráfico con etiquetas de valores y totales destacando a Chile
title: "PIB per cápita en Latinoamérica (2023)"
subtitle: "En miles de dólares estadounidenses"

# Configuración de barras
bar:
  height: 0.9
  edgecolor: "#ffffff"
  linewidth: 0.5
  gap: 0.1

# Colores por serie con esquema que destaca a Chile
colors:
  Agricultura: "#4E79A7"
  Industria: "#F28E2B"
  Servicios: "#76B7B2"
  highlight_country: "Chile"  # País a destacar con colores más intensos

# Etiquetas de valores en segmentos
value_labels: true
value_format: "{:.1f}"  # Un decimal para PIB per cápita
value_labels_config:
  font_size: 9  # Tamaño reducido para no sobrecargar
  font_weight: "normal"

# Etiquetas de totales
total_labels:
  enabled: true
  x_offset: 8
  font_size: 11
  font_weight: "bold"
  color_map:
    "Chile": "#D22730"  # Destacar Chile con color rojo
    "default": "#333333"
  format: "{:.1f}"

# Configuración de ejes
yaxis:
  show_ticks: false
  show_labels: true
  font:
    size: 11
  
# Banderas para identificación visual
flags:
  enabled: true
  position: "start"
  size: 0.03
```

### Datos Socioeconómicos por Región de Chile

```yaml
# Gráfico con etiquetas de valores y totales para regiones de Chile
title: "Ingreso medio por hogar según región (2023)"
subtitle: "En miles de pesos chilenos"

# Configuración de barras
bar:
  height: 0.85
  edgecolor: "#ffffff"
  linewidth: 0.5
  gap: 0.12

# Colores por serie para fuentes de ingreso
colors:
  Trabajo: "#4E79A7"
  Jubilación: "#F28E2B"
  Subsidios: "#76B7B2"
  Otros: "#A0CBE8"

# Etiquetas de valores en segmentos
value_labels: true
value_format: "${:,.0f}"  # Formato monetario chileno
value_labels_config:
  font_size: 8  # Tamaño reducido por la cantidad de datos
  font_weight: "normal"

# Etiquetas de totales
total_labels:
  enabled: true
  x_offset: 8
  font_size: 10
  font_weight: "bold"
  color: "#333333"
  format: "${:,.0f}"

# Configuración de ejes
yaxis:
  show_ticks: false
  show_labels: true
  font:
    size: 10
  
# Configuración para destacar la Región Metropolitana
highlight:
  bars: ["Región Metropolitana"]
  color: "#FFA07A"  # Color ligeramente diferente
```

Estos ejemplos muestran configuraciones completas para:

1. **Comparativa regional**: Gráfico que compara indicadores entre países latinoamericanos con destaque especial para Chile
2. **Análisis nacional**: Gráfico que muestra datos por región dentro de Chile, con formato monetario chileno

Las configuraciones incluyen:

- Formatos numéricos adaptados a las convenciones regionales
- Esquemas de colores que destacan a Chile o a regiones específicas
- Banderas para identificación rápida en comparativas internacionales
- Tamaños de fuente ajustados para la cantidad de datos típica en estos análisis
