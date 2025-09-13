# Personalización de Ejes y Títulos

Este documento describe las opciones de configuración para personalizar los ejes y el espaciado de títulos en las gráficas de ConDatos.

## Configuración de Ejes

La configuración de ejes permite controlar la visibilidad de ticks y etiquetas de manera independiente, tanto para el eje X como para el eje Y.

### Configuración de Eje X

```yaml
xaxis:
  show_ticks: true|false     # Controla la visibilidad de las marcas (ticks) del eje X
  show_labels: true|false    # Controla la visibilidad de las etiquetas del eje X
  show_grid: true|false      # Controla la visibilidad de las líneas de cuadrícula verticales
```

### Configuración de Eje Y

```yaml
yaxis:
  show_ticks: true|false     # Controla la visibilidad de las marcas (ticks) del eje Y
  show_labels: true|false    # Controla la visibilidad de las etiquetas del eje Y
  show_grid: true|false      # Controla la visibilidad de las líneas de cuadrícula horizontales
```

### Casos de Uso Comunes

- **Gráfico limpio sin marcas ni etiquetas**:

```yaml
xaxis:
  show_ticks: false
  show_labels: false
yaxis:
  show_ticks: false
  show_labels: false
```

- **Etiquetas sin ticks (útil para gráficos con banderas)**:

```yaml
yaxis:
  show_ticks: false
  show_labels: true
```

- **Solo líneas de cuadrícula sin etiquetas ni ticks**:

```yaml
xaxis:
  show_ticks: false
  show_labels: false
  show_grid: true
yaxis:
  show_ticks: false
  show_labels: false
  show_grid: true
```

## Espaciado de Títulos

La configuración `title_spacing` permite un control preciso del espaciado entre el título, subtítulo y el resto del gráfico.

```yaml
title_spacing:
  top_margin: 0.35           # Espacio entre borde superior y título (0-1)
  bottom_margin: 0.25        # Espacio entre título y subtítulo (0-1)
  subtitle_top_margin: 0.10  # Espacio adicional sobre el subtítulo (0-1)
  left_margin: 0.00          # Margen izquierdo para títulos (0-1)
  right_margin: 0.00         # Margen derecho para títulos (0-1)
```

### Ajustes Recomendados

- **Espaciado estándar**:

```yaml
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.20
  subtitle_top_margin: 0.05
```

- **Para títulos grandes**:

```yaml
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.25
  subtitle_top_margin: 0.10
```

- **Para gráficos sin subtítulo**:

```yaml
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.30
  subtitle_top_margin: 0.00
```

## Interacción con Otros Componentes

### Banderas en Gráficos de Barras Horizontales

Cuando se utilizan banderas en gráficos de barras horizontales con `flags.enabled: true`, la configuración de etiquetas del eje Y (`yaxis.show_labels`) tiene prioridad sobre la configuración de banderas.

```yaml
yaxis:
  show_ticks: false
  show_labels: true

flags:
  enabled: true
  position: end          # Posición de las banderas (start|end)
  size: 0.03             # Tamaño relativo de las banderas
  padding: 0.01          # Espacio adicional entre barras y banderas
```

## Ejemplos Completos

### Gráfico de Barras Horizontales Apiladas con Banderas

```yaml
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.25
  subtitle_top_margin: 0.10

xaxis:
  show_ticks: false
  show_labels: false
  show_grid: false

yaxis:
  show_ticks: false
  show_labels: true
  show_grid: false

flags:
  enabled: true
  position: end
  size: 0.03
  padding: 0.01
```

Este ejemplo configura un gráfico de barras horizontales apiladas con:

- Espaciado optimizado para título y subtítulo
- Eje X completamente oculto (sin ticks, etiquetas ni cuadrícula)
- Eje Y con etiquetas visibles pero sin ticks
- Banderas de países al final de cada barra
