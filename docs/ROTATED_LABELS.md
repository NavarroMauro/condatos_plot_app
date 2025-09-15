# Manejo de Etiquetas Rotadas en Gráficos de Barras Verticales

Este documento describe cómo configurar y ajustar las etiquetas del eje X cuando están rotadas en los gráficos de barras verticales, con especial atención a visualizaciones que muestran datos chilenos y comparativas regionales latinoamericanas.

## Configuración Básica

Para rotar las etiquetas del eje X, utiliza el parámetro `rotate_xticks` en tu archivo de configuración YAML:

```yaml
rotate_xticks: 45  # Ángulo de rotación en grados
```

## Configuración Avanzada

Para un control más preciso sobre las etiquetas rotadas, utiliza la sección `xtick_config`:

```yaml
# Rotación básica
rotate_xticks: 45

# Configuración avanzada
xtick_config:
  ha: "right"         # Alineación horizontal: "right", "center", o "left"
  bottom_space: 0.24  # Espacio inferior para etiquetas rotadas (0-1)
```

### Parámetros

- **ha**: Alineación horizontal de las etiquetas. Opciones:
  - `"right"`: Alinea el extremo derecho de la etiqueta (predeterminado para etiquetas rotadas)
  - `"center"`: Alinea el centro de la etiqueta
  - `"left"`: Alinea el extremo izquierdo de la etiqueta

- **bottom_space**: Espacio entre el borde inferior de la figura y el área del gráfico (valor de 0 a 1). Un valor mayor proporciona más espacio para las etiquetas largas o con rotación pronunciada. El valor predeterminado es 0.24.

## Recomendaciones Generales

- Para etiquetas largas, usa valores más altos de `bottom_space` (0.25-0.30).
- Si las etiquetas aún aparecen cortadas, considera:
  1. Aumentar el valor de `bottom_space`
  2. Modificar los márgenes con la sección `margins`
  3. Cambiar la posición del footer con `footer.source_config.y_position` y `footer.logos[].y_position`

## Recomendaciones Específicas para Visualizaciones Regionales

### Para Nombres de Países Latinoamericanos

Los nombres de países latinoamericanos suelen requerir configuraciones específicas para garantizar su correcta visualización:

```yaml
rotate_xticks: 45
xtick_config:
  ha: "right"
  bottom_space: 0.26  # Valor recomendado para nombres de países
```

### Para Regiones de Chile

Cuando se visualizan las 16 regiones de Chile:

```yaml
rotate_xticks: 60  # Mayor rotación para nombres más largos
xtick_config:
  ha: "right"
  bottom_space: 0.30  # Mayor espacio para nombres largos como "Región de Valparaíso"
```

### Para Datos Temporales (Series Trimestrales o Mensuales)

Para visualizaciones con períodos de tiempo (común en indicadores económicos chilenos):

```yaml
rotate_xticks: 45
xtick_config:
  ha: "right"
  bottom_space: 0.24
  fontsize: 9  # Tamaño de fuente más pequeño para muchas etiquetas
```

## Ejemplos Completos

### Comparativa de Países Latinoamericanos

```yaml
title: "PIB per cápita en América Latina (2023)"
subtitle: "En miles de USD"
rotate_xticks: 45
xtick_config:
  ha: "right"
  bottom_space: 0.28
margins:
  bottom: 0.25
  left: 0.10
  right: 0.05
footer:
  source: "Fuente: Banco Mundial, 2023"
  source_config:
    y_position: 0.09
  logos:
    - path: "assets/logos/logo_condatos.png"
      y_position: 0.09
```

### Indicadores por Región en Chile

```yaml
title: "Tasa de Desempleo por Región"
subtitle: "Porcentaje, Primer trimestre 2023"
rotate_xticks: 60
xtick_config:
  ha: "right"
  bottom_space: 0.30
  fontsize: 9  # Tamaño reducido para nombres largos de regiones
margins:
  bottom: 0.28
  left: 0.12
  right: 0.05
footer:
  source: "Fuente: INE Chile, 2023"
  source_config:
    y_position: 0.11
  logos:
    - path: "assets/logos/logo_condatos.png"
      y_position: 0.11
```
