# Personalización de Leyendas en Condatos-Figs

Este documento describe las opciones de personalización disponibles para las leyendas en los gráficos generados con Condatos-Figs, optimizadas para visualizaciones de datos centrados en Chile y el contexto latinoamericano.

## Configuración Básica

Para mantener compatibilidad con versiones anteriores, se pueden seguir utilizando las opciones básicas:

```yaml
# Configuración de leyenda - modo básico
legend: true             # Habilita/deshabilita la leyenda
legend_loc: "upper right"  # Posición de la leyenda
legend_fontsize: 12      # Tamaño de fuente para las etiquetas
```

## Configuración Avanzada

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

## Posiciones de Leyenda

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

## Posicionamiento Avanzado

### Combinando `loc` y `bbox_to_anchor`

El posicionamiento preciso de la leyenda se puede lograr combinando `loc` y `bbox_to_anchor`. Estos parámetros funcionan juntos de la siguiente manera:

- **`loc`**: Define qué punto de la leyenda se alineará con las coordenadas especificadas en `bbox_to_anchor`
- **`bbox_to_anchor`**: Define las coordenadas precisas [x, y] donde se anclará la leyenda

Por ejemplo:

```yaml
legend_config:
  loc: "lower right"      # La esquina inferior derecha de la leyenda...
  bbox_to_anchor: [0.98, 0.02]  # ...se colocará en estas coordenadas (cerca de la esquina inferior derecha)
```

En este caso, la esquina inferior derecha de la leyenda se posicionará en el punto (0.98, 0.02) del gráfico, que está cerca del borde inferior derecho.

### Sistema de Coordenadas

El sistema de coordenadas para `bbox_to_anchor` va de 0 a 1 en ambos ejes:

- Eje X: 0 = extremo izquierdo, 1 = extremo derecho
- Eje Y: 0 = extremo inferior, 1 = extremo superior

### Ejemplos Comunes

| Objetivo | `loc` | `bbox_to_anchor` | Resultado |
|---------|------|----------------|---------|
| Leyenda en esquina superior derecha | `"upper right"` | `[0.98, 0.98]` | Esquina superior derecha de la leyenda anclada cerca del borde superior derecho |
| Leyenda en esquina inferior derecha | `"lower right"` | `[0.98, 0.02]` | Esquina inferior derecha de la leyenda anclada cerca del borde inferior derecho |
| Leyenda fuera del gráfico a la derecha | `"upper left"` | `[1.05, 1]` | Esquina superior izquierda de la leyenda anclada fuera del gráfico a la derecha |
| Leyenda centrada arriba | `"lower center"` | `[0.5, 1.02]` | Centro inferior de la leyenda anclado encima del gráfico |
| Leyenda en el centro del gráfico | `"center"` | `[0.5, 0.5]` | Centro de la leyenda anclado en el centro del gráfico |

### Casos de Uso

- Para colocar la leyenda **dentro** del gráfico, use valores entre 0 y 1 para ambas coordenadas
- Para colocar la leyenda **fuera** del gráfico, use valores menores que 0 o mayores que 1
- Para ajustar finamente la posición, modifique ligeramente los valores (por ejemplo, 0.98 en lugar de 1.0 para evitar recortes)

## Ejemplos de Configuración

### Leyenda Estándar ConDatos para Gráficos Chilenos

```yaml
legend_config:
  loc: "upper right"
  frameon: true
  fontsize: 10
  facecolor: "#f8f8f8"
  edgecolor: "#dddddd"
  title: "Regiones de Chile"
  title_fontsize: 12
  title_fontweight: "bold"
  title_color: "#333333"
```

### Leyenda para Comparativas Regionales

```yaml
legend_config:
  loc: "upper left"
  title: "Países Latinoamericanos"
  title_fontsize: 14
  title_fontweight: "bold"
  fontsize: 12
  frameon: true
  font:
    color: "#333333"
  ncol: 1  # Una columna para facilitar comparación entre países
```

### Leyenda para Indicadores Económicos

```yaml
legend_config:
  loc: "lower center"
  ncol: 3
  fontsize: 10
  columnspacing: 1.0
  title: "Indicadores Económicos"
  title_fontsize: 12
  title_color: "#444444"
```

### Leyenda con Destaque para Chile

```yaml
legend_config:
  loc: "center right"
  frameon: true
  facecolor: "#f8f8f8"
  edgecolor: "#333333"
  framealpha: 0.9
  fancybox: true
  shadow: false
  font:
    family: "Nunito"
    style: "normal"
    color: "#555555"
  # Configuración de marcadores personalizada para destacar a Chile
  # Nota: Los marcadores específicos deben configurarse en el código Python
  # o utilizando el parámetro 'highlight' para las series
```

### Leyenda Fuera del Gráfico (para Visualizaciones Detalladas)

```yaml
legend_config:
  loc: "upper left"
  bbox_to_anchor: [1.05, 1]
  borderaxespad: 0
  title: "Sectores Económicos de Chile"
  title_fontsize: 13
  title_fontweight: "bold"
```

## Recomendaciones Regionales

### Para Gráficos con Múltiples Países

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

### Para Visualizaciones de Indicadores Regionales

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

## Notas Técnicas

- Las opciones avanzadas tienen prioridad sobre las básicas cuando ambas están presentes.
- El sistema utiliza la función `norm_legend_loc` para normalizar las ubicaciones "humanas" a los códigos válidos de Matplotlib.
- Para leyendas fuera del gráfico, es posible que necesite ajustar los márgenes de la figura.

## Estándares para Visualizaciones de ConDatos

Para mantener la consistencia en todas las visualizaciones de datos chilenos y latinoamericanos, se recomienda seguir estos estándares para las leyendas:

1. **Fuente y tamaño**: Usar la familia de fuentes "Nunito" con tamaño 10-12pt para etiquetas y 12-14pt para títulos.

2. **Colores**: Utilizar colores de texto #333333 (gris oscuro) para mejor legibilidad y colores de fondo #f8f8f8 (gris muy claro) cuando se requiera un marco.

3. **Posicionamiento**: Preferir las posiciones "upper right", "lower right" o "best" para visualizaciones estándar.

4. **Destacado de Chile**: En comparativas regionales, resaltar siempre a Chile con un color distintivo (#D22730 - rojo) o un estilo de línea más prominente.

5. **Idioma**: Todas las leyendas deben estar en español, utilizando la terminología correcta para los conceptos económicos y sociales según los estándares chilenos.
