# Configuración de Etiquetas de Valores y Totales

Este documento describe las opciones para configurar las etiquetas de valores en los segmentos de las barras y los totales al final de las barras en los gráficos de ConDatos.

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

## Ejemplo Completo con Otras Configuraciones

```yaml
# Gráfico con etiquetas de valores y totales
title: "Medallas por país - Juegos Panamericanos Junior 2025"
subtitle: "Total de preseas ganadas (oro, plata y bronce)"

# Configuración de barras
bar:
  height: 1.0
  edgecolor: "#ffffff"
  linewidth: 0.5
  gap: 0.08

# Colores por serie
colors:
  oro: "#F28E2B"
  plata: "#4E79A7" 
  bronce: "#E15759"

# Etiquetas de valores en segmentos
value_labels: true
value_format: "{:.0f}"

# Etiquetas de totales
total_labels:
  enabled: true
  x_offset: 8
  font_size: 12
  font_weight: "bold"

# Configuración de ejes
yaxis:
  show_ticks: false
  show_labels: true
  font:
    size: 18
```

Este ejemplo muestra un gráfico completo con:

- Barras con espaciado (gap) del 8%
- Etiquetas de valores dentro de cada segmento con formato entero
- Totales al final de cada barra con fuente en negrita
- Etiquetas de categorías visibles en el eje Y (sin ticks)
