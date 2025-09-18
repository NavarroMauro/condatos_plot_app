# Personalización de Componentes Visuales

Este documento consolida toda la información sobre la personalización de componentes visuales en las gráficas de ConDatos-Figs-App. Incluye opciones detalladas para ejes, títulos, leyendas, etiquetas rotadas y etiquetas de valores, con enfoque en visualizaciones de datos chilenos y comparativas regionales latinoamericanas.

## Índice

1. [Ejes y Títulos](#ejes-y-títulos)
   - [Configuración de Ejes](#configuración-de-ejes)
   - [Espaciado de Títulos](#espaciado-de-títulos)
   - [Interacción con Banderas](#interacción-con-banderas)

2. [Leyendas](#leyendas)
   - [Configuración Básica](#configuración-básica-de-leyendas)
   - [Configuración Avanzada](#configuración-avanzada-de-leyendas)
   - [Posicionamiento](#posicionamiento-avanzado-de-leyendas)
   - [Recomendaciones Regionales](#recomendaciones-para-leyendas-regionales)

3. [Etiquetas Rotadas](#etiquetas-rotadas)
   - [Configuración Básica](#configuración-básica-de-etiquetas-rotadas)
   - [Configuración Avanzada](#configuración-avanzada-de-etiquetas-rotadas)
   - [Recomendaciones para Datos Regionales](#recomendaciones-para-etiquetas-rotadas-regionales)

4. [Etiquetas de Valores y Totales](#etiquetas-de-valores-y-totales)
   - [Etiquetas de Valores en Segmentos](#etiquetas-de-valores-en-segmentos)
   - [Etiquetas de Totales](#etiquetas-de-totales)
   - [Formatos para Datos Regionales](#formatos-para-datos-regionales)

5. [Ejemplos Completos](#ejemplos-completos)
   - [Comparativa de Países Latinoamericanos](#comparativa-de-países-latinoamericanos)
   - [Indicadores por Región en Chile](#indicadores-por-región-en-chile)
   - [Indicadores Económicos Temporales](#indicadores-económicos-temporales)

---

## Ejes y Títulos

### Configuración de Ejes

La configuración de ejes permite controlar la visibilidad de ticks y etiquetas de manera independiente, tanto para el eje X como para el eje Y.

#### Configuración de Eje X

```yaml
xaxis:
  show_ticks: true|false     # Controla la visibilidad de las marcas (ticks) del eje X
  show_labels: true|false    # Controla la visibilidad de las etiquetas del eje X
  show_grid: true|false      # Controla la visibilidad de las líneas de cuadrícula verticales
```

#### Configuración de Eje Y

```yaml
yaxis:
  show_ticks: true|false     # Controla la visibilidad de las marcas (ticks) del eje Y
  show_labels: true|false    # Controla la visibilidad de las etiquetas del eje Y
  show_grid: true|false      # Controla la visibilidad de las líneas de cuadrícula horizontales
```

#### Casos de Uso Comunes

- **Gráfico limpio sin marcas ni etiquetas** (ideal para comparaciones simples de datos entre países de Latinoamérica):

```yaml
xaxis:
  show_ticks: false
  show_labels: false
yaxis:
  show_ticks: false
  show_labels: false
```

- **Etiquetas sin ticks** (recomendado para gráficos con banderas de países latinoamericanos):

```yaml
yaxis:
  show_ticks: false
  show_labels: true
```

- **Solo líneas de cuadrícula sin etiquetas ni ticks** (útil para mostrar tendencias regionales):

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

- **Formato para comparación regional Chile-Latinoamérica** (destaca Chile entre los demás países):

```yaml
yaxis:
  show_ticks: false
  show_labels: true
  highlight_labels: ["Chile"]  # Destacar Chile en las etiquetas
```

### Espaciado de Títulos

La configuración `title_spacing` permite un control preciso del espaciado entre el título, subtítulo y el resto del gráfico.

```yaml
title_spacing:
  top_margin: 0.35           # Espacio entre borde superior y título (0-1)
  bottom_margin: 0.25        # Espacio entre título y subtítulo (0-1)
  subtitle_top_margin: 0.10  # Espacio adicional sobre el subtítulo (0-1)
  left_margin: 0.00          # Margen izquierdo para títulos (0-1)
  right_margin: 0.00         # Margen derecho para títulos (0-1)
```

#### Ajustes Recomendados

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

### Interacción con Banderas

Cuando se utilizan banderas en gráficos de barras horizontales con `flags.enabled: true`, la configuración de etiquetas del eje Y (`yaxis.show_labels`) tiene prioridad sobre la configuración de banderas. Esto es particularmente útil para visualizaciones comparativas entre países latinoamericanos.

```yaml
yaxis:
  show_ticks: false
  show_labels: true

flags:
  enabled: true
  position: end          # Posición de las banderas (start|end)
  size: 0.03             # Tamaño relativo de las banderas
  padding: 0.01          # Espacio adicional entre barras y banderas
  highlight: ["CL"]      # Opcional: Destacar bandera de Chile
```

#### Recomendaciones para Visualizaciones Regionales

Para visualizaciones que comparan Chile con otros países de Latinoamérica, recomendamos:

1. Utilizar banderas al inicio (`position: start`) para facilitar la identificación rápida de países
2. Aumentar ligeramente el tamaño de la bandera de Chile (`size: 0.035`) cuando aparece en la comparativa
3. Ordenar los países de forma que Chile aparezca en una posición destacada (primero o último de la lista)

---

## Leyendas

### Configuración Básica de Leyendas

Para mantener compatibilidad con versiones anteriores, se pueden seguir utilizando las opciones básicas:

```yaml
# Configuración de leyenda - modo básico
legend: true             # Habilita/deshabilita la leyenda
legend_loc: "upper right"  # Posición de la leyenda
legend_fontsize: 12      # Tamaño de fuente para las etiquetas
```

### Configuración Avanzada de Leyendas

Para una personalización más detallada, se puede utilizar el bloque `legend_config` con las siguientes opciones:

```yaml
# Configuración avanzada de leyenda
legend_config:
  # Posición y estructura
  loc: "upper right"     # Posición: upper/lower right/left/center, best, etc.
  ncol: 3                # Número de columnas para los elementos de la leyenda
  bbox_to_anchor: [1.02, 1]  # Posición personalizada [x, y] o [x, y, width, height]
  
  # Tipografía y aspecto general
  fontsize: 12           # Tamaño de fuente para las etiquetas
  frameon: true          # Mostrar borde alrededor de la leyenda
  
  # Título de la leyenda
  title: "Tipo de Medalla"  # Título para la leyenda
  title_fontsize: 14     # Tamaño de fuente para el título
  title_fontweight: "bold" # Peso de la fuente para el título
  title_color: "#333333" # Color del título
  
  # Propiedades de espaciado
  borderpad: 0.4         # Padding entre el contenido y el borde
  labelspacing: 0.5      # Espacio vertical entre etiquetas
  handlelength: 1.8      # Longitud de los marcadores
  handleheight: 0.7      # Altura de los marcadores
  handletextpad: 0.6     # Espacio entre marcador y texto
  borderaxespad: 0.5     # Padding entre la leyenda y los ejes
  columnspacing: 1.5     # Espacio entre columnas
  
  # Apariencia de la caja
  facecolor: "#f8f8f8"   # Color de fondo
  edgecolor: "#dddddd"   # Color del borde
  framealpha: 0.9        # Transparencia del fondo (0-1)
  shadow: false          # Sombra para la leyenda
  fancybox: true         # Bordes redondeados
  
  # Configuración específica de fuente para las etiquetas
  font:
    color: "#333333"     # Color del texto
    family: "Nunito"     # Familia de fuente
    style: "normal"      # Estilo: normal, italic
    weight: "normal"     # Peso: normal, bold
```

#### Posiciones de Leyenda

El sistema acepta tanto nombres técnicos de Matplotlib como nombres más "humanos" para la posición de la leyenda:

| Nombre técnico | Nombres alternativos |
|---------------|---------------------|
| `upper left`   | `top left`          |
| `upper right`  | `top right`         |
| `lower left`   | `bottom left`       |
| `lower right`  | `bottom right`      |
| `upper center` | `top`               |
| `lower center` | `bottom`            |
| `center left`  | `left`              |
| `center right` | `right`             |
| `center`       | -                   |

### Posicionamiento Avanzado de Leyendas

#### Combinando `loc` y `bbox_to_anchor`

El posicionamiento preciso de la leyenda se puede lograr combinando `loc` y `bbox_to_anchor`. Estos parámetros funcionan juntos de la siguiente manera:

- **`loc`**: Define qué punto de la leyenda se alineará con las coordenadas especificadas en `bbox_to_anchor`
- **`bbox_to_anchor`**: Define las coordenadas precisas [x, y] donde se anclará la leyenda

Por ejemplo:

```yaml
legend_config:
  loc: "lower right"      # La esquina inferior derecha de la leyenda...
  bbox_to_anchor: [0.98, 0.02]  # ...se colocará en estas coordenadas (cerca de la esquina inferior derecha)
```

#### Sistema de Coordenadas

El sistema de coordenadas para `bbox_to_anchor` va de 0 a 1 en ambos ejes:

- Eje X: 0 = extremo izquierdo, 1 = extremo derecho
- Eje Y: 0 = extremo inferior, 1 = extremo superior

#### Ejemplos Comunes de Posicionamiento

| Objetivo | `loc` | `bbox_to_anchor` | Resultado |
|---------|------|----------------|---------|
| Leyenda en esquina superior derecha | `"upper right"` | `[0.98, 0.98]` | Esquina superior derecha de la leyenda anclada cerca del borde superior derecho |
| Leyenda en esquina inferior derecha | `"lower right"` | `[0.98, 0.02]` | Esquina inferior derecha de la leyenda anclada cerca del borde inferior derecho |
| Leyenda fuera del gráfico a la derecha | `"upper left"` | `[1.05, 1]` | Esquina superior izquierda de la leyenda anclada fuera del gráfico a la derecha |
| Leyenda centrada arriba | `"lower center"` | `[0.5, 1.02]` | Centro inferior de la leyenda anclado encima del gráfico |
| Leyenda en el centro del gráfico | `"center"` | `[0.5, 0.5]` | Centro de la leyenda anclado en el centro del gráfico |

### Recomendaciones para Leyendas Regionales

#### Para Gráficos con Múltiples Países

Para visualizaciones que comparan a Chile con otros países latinoamericanos, recomendamos:

- Usar una leyenda clara con todos los países listados en una sola columna
- Destacar a Chile con un formato distintivo (color especial o marca)
- Ordenar los países en la leyenda de forma consistente (alfabético o por valor)

```yaml
legend_config:
  loc: "best"  # Posicionamiento automático para evitar superposición
  ncol: 1      # Una columna para facilitar la lectura
  fontsize: 12
  title: "Países"
  title_fontweight: "bold"
  handlelength: 2.0  # Marcadores más largos para mejor visibilidad
```

#### Para Visualizaciones de Indicadores Regionales

Para visualizaciones que muestran múltiples indicadores económicos o sociales:

- Usar una leyenda con título descriptivo
- Dividir los indicadores en columnas si son muchos
- Usar colores contrastantes para facilitar la identificación

```yaml
legend_config:
  loc: "lower center"
  ncol: 3        # Múltiples columnas para indicadores
  fontsize: 10
  columnspacing: 1.2
  title: "Indicadores Socioeconómicos"
  title_fontsize: 12
  handletextpad: 0.8  # Mayor espacio entre marcador y texto
```

#### Estándares para Visualizaciones de ConDatos

Para mantener la consistencia en todas las visualizaciones de datos chilenos y latinoamericanos, se recomienda seguir estos estándares para las leyendas:

1. **Fuente y tamaño**: Usar la familia de fuentes "Nunito" con tamaño 10-12pt para etiquetas y 12-14pt para títulos.

2. **Colores**: Utilizar colores de texto #333333 (gris oscuro) para mejor legibilidad y colores de fondo #f8f8f8 (gris muy claro) cuando se requiera un marco.

3. **Posicionamiento**: Preferir las posiciones "upper right", "lower right" o "best" para visualizaciones estándar.

4. **Destacado de Chile**: En comparativas regionales, resaltar siempre a Chile con un color distintivo (#D22730 - rojo) o un estilo de línea más prominente.

5. **Idioma**: Todas las leyendas deben estar en español, utilizando la terminología correcta para los conceptos económicos y sociales según los estándares chilenos.

---

## Etiquetas Rotadas

### Configuración Básica de Etiquetas Rotadas

Para rotar las etiquetas del eje X, utiliza el parámetro `rotate_xticks` en tu archivo de configuración YAML:

```yaml
rotate_xticks: 45  # Ángulo de rotación en grados
```

### Configuración Avanzada de Etiquetas Rotadas

Para un control más preciso sobre las etiquetas rotadas, utiliza la sección `xtick_config`:

```yaml
# Rotación básica
rotate_xticks: 45

# Configuración avanzada
xtick_config:
  ha: "right"         # Alineación horizontal: "right", "center", o "left"
  bottom_space: 0.24  # Espacio inferior para etiquetas rotadas (0-1)
```

#### Parámetros para Etiquetas Rotadas

- **ha**: Alineación horizontal de las etiquetas. Opciones:
  - `"right"`: Alinea el extremo derecho de la etiqueta (predeterminado para etiquetas rotadas)
  - `"center"`: Alinea el centro de la etiqueta
  - `"left"`: Alinea el extremo izquierdo de la etiqueta

- **bottom_space**: Espacio entre el borde inferior de la figura y el área del gráfico (valor de 0 a 1). Un valor mayor proporciona más espacio para las etiquetas largas o con rotación pronunciada. El valor predeterminado es 0.24.

### Recomendaciones para Etiquetas Rotadas Regionales

#### Para Nombres de Países Latinoamericanos

Los nombres de países latinoamericanos suelen requerir configuraciones específicas para garantizar su correcta visualización:

```yaml
rotate_xticks: 45
xtick_config:
  ha: "right"
  bottom_space: 0.26  # Valor recomendado para nombres de países
```

#### Para Regiones de Chile

Cuando se visualizan las 16 regiones de Chile:

```yaml
rotate_xticks: 60  # Mayor rotación para nombres más largos
xtick_config:
  ha: "right"
  bottom_space: 0.30  # Mayor espacio para nombres largos como "Región de Valparaíso"
```

#### Para Datos Temporales (Series Trimestrales o Mensuales)

Para visualizaciones con períodos de tiempo (común en indicadores económicos chilenos):

```yaml
rotate_xticks: 45
xtick_config:
  ha: "right"
  bottom_space: 0.24
  fontsize: 9  # Tamaño de fuente más pequeño para muchas etiquetas
```

---

## Etiquetas de Valores y Totales

### Etiquetas de Valores en Segmentos

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

#### Ejemplos de Configuración de Valores

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

### Etiquetas de Totales

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

#### Ejemplos de Configuración de Totales

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
```

#### Combinando Configuraciones

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

### Formatos para Datos Regionales

#### Formato Numérico para Indicadores Chilenos

En Chile y gran parte de Latinoamérica se utiliza la coma como separador decimal y el punto como separador de miles. Para adaptar las etiquetas a estos formatos:

```yaml
# Para valores monetarios en pesos chilenos
value_format: "${:,.0f}"  # Ejemplo: $1.234.567

# Para valores decimales con la coma como separador decimal
value_format_cl: "{:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
# Esto producirá formato como: 1.234,5
```

#### Etiquetas para Comparativas Regionales

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

---

## Ejemplos Completos

### Comparativa de Países Latinoamericanos

Configuración completa para un gráfico de barras horizontales apiladas que compara indicadores entre países latinoamericanos:

```yaml
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

# Configuración de leyenda
legend_config:
  loc: "lower right"
  ncol: 3
  fontsize: 10
  title: "Sectores Económicos"
  title_fontsize: 12
  title_fontweight: "bold"
  
# Configuración de espaciado de título
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.25
  subtitle_top_margin: 0.10
  
# Configuración de footer
footer:
  source: "Fuente: Banco Mundial, 2023"
  source_config:
    y_position: 0.08
```

### Indicadores por Región en Chile

Configuración completa para un gráfico de barras verticales que muestra indicadores por región en Chile:

```yaml
title: "Tasa de Desempleo por Región"
subtitle: "Porcentaje, Primer trimestre 2023"

# Configuración de rotación de etiquetas
rotate_xticks: 60
xtick_config:
  ha: "right"
  bottom_space: 0.30
  fontsize: 9  # Tamaño reducido para nombres largos de regiones

# Configuración de márgenes
margins:
  bottom: 0.28
  left: 0.12
  right: 0.05

# Configuración de ejes
xaxis:
  show_ticks: false
  show_labels: true
  show_grid: false
  
yaxis:
  show_ticks: true
  show_labels: true
  show_grid: true
  title: "Tasa (%)"

# Etiquetas de valores
value_labels: true
value_format: "{:.1f}%"
value_labels_config:
  font_size: 10
  font_weight: "bold"

# Configuración de destacados
highlight:
  bars: ["Región Metropolitana"]  # Destacar RM
  color: "#D22730"  # Color rojo para destacar

# Configuración de título
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.25
  subtitle_top_margin: 0.10

# Configuración de footer
footer:
  source: "Fuente: INE Chile, 2023"
  source_config:
    y_position: 0.11
  logos:
    - path: "assets/logos/logo_condatos.png"
      y_position: 0.11
```

### Indicadores Económicos Temporales

Configuración completa para un gráfico de líneas que muestra la evolución temporal de indicadores económicos para países latinoamericanos:

```yaml
title: "Evolución del PIB en América Latina"
subtitle: "Variación porcentual anual, 2010-2023"

# Configuración de ejes
xaxis:
  show_ticks: true
  show_labels: true
  show_grid: true
  title: "Años"

yaxis:
  show_ticks: true
  show_labels: true
  show_grid: true
  title: "Variación del PIB (%)"
  
# Configuración de líneas
line:
  linewidth: 2.0
  markersize: 6
  
# Destacar Chile
highlight:
  series: ["Chile"]
  color: "#D22730"
  width: 3.0
  
# Leyenda
legend_config:
  loc: "lower right"
  ncol: 2
  fontsize: 10
  title: "Países"
  title_fontsize: 12
  
# Espaciado de títulos
title_spacing:
  top_margin: 0.35
  bottom_margin: 0.20
  subtitle_top_margin: 0.05
  
# Configuración del footer
footer:
  source: "Fuente: CEPAL, 2023"
  source_config:
    y_position: 0.07
  note: "Datos 2023: Proyecciones"
  note_config:
    y_position: 0.03
```

Estos ejemplos muestran configuraciones completas optimizadas para visualizaciones que representan datos chilenos y latinoamericanos, con las mejores prácticas para cada tipo de componente visual y escenario de datos.
