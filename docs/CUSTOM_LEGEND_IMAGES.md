# Leyendas Personalizadas con Imágenes en ConDatos-Figs

Este documento explica cómo personalizar las leyendas para usar imágenes en lugar de colores estándar y cómo añadir logos de organización sobre la leyenda.

## Configuración de Leyendas con Imágenes

Para crear leyendas con imágenes personalizadas en lugar de marcadores de color, utiliza el siguiente formato en tu archivo YAML de configuración:

```yaml
legend_config:
  loc: "upper right"  # Posición de la leyenda
  frameon: true       # Marco alrededor de la leyenda
  fontsize: 12        # Tamaño de fuente
  title: "Tipos"      # Título de la leyenda
  custom_icons: true  # Activa el modo de iconos personalizados
  icons:              # Lista de iconos y etiquetas
    - label: "Oro"    # Texto para este elemento
      image: "assets/icons/gold_medal.png"  # Ruta a la imagen
      zoom: 0.15      # Factor de zoom (ajustar según tamaño de imagen)
    - label: "Plata"
      image: "assets/icons/silver_medal.png"
      zoom: 0.15
    - label: "Bronce"
      image: "assets/icons/bronze_medal.png"
      zoom: 0.15
```

Las imágenes reemplazarán a los marcadores de color estándar en la leyenda, manteniendo todas las demás opciones de configuración de leyenda.

## Añadir Logo de Organización

Para incluir un logo de tu organización en el gráfico, utiliza la siguiente configuración:

```yaml
logo:
  path: "assets/logo_condatos.png"  # Ruta al archivo de imagen
  position: "above_legend"         # Posición (ver opciones abajo)
  zoom: 0.2                        # Factor de zoom
  margin: 0.02                     # Margen sobre la leyenda (si position="above_legend")
```

Opciones para `position`:

- `above_legend`: Coloca el logo justo encima de la leyenda
- `top_left`: Esquina superior izquierda
- `top_right`: Esquina superior derecha
- `custom`: Posición personalizada usando coordenadas x, y

Si seleccionas `custom`, puedes especificar las coordenadas exactas:

```yaml
logo:
  path: "assets/logo_condatos.png"
  position: "custom"
  zoom: 0.2
  x: 0.8  # Coordenada X (0-1)
  y: 0.9  # Coordenada Y (0-1)
```

## Ejemplo Completo

Aquí tienes un ejemplo completo que incluye tanto leyenda personalizada como logo:

```yaml
# Archivo config/ejemplo-leyenda-custom.yml
template: "templates/stackedbar-horizontal-template.yml"
outfile: "out/medallas-ejemplo"
data:
  inline:
    pais: ["Chile", "Argentina", "Perú", "Colombia", "Brasil"]
    oro: [15, 12, 8, 10, 20]
    plata: [10, 14, 9, 11, 18]
    bronce: [12, 15, 10, 12, 15]

title: "Medallero de los Juegos Latinoamericanos 2024"
subtitle: "Distribución de medallas por país"
  
# Leyenda personalizada con imágenes
legend_config:
  loc: "upper right"
  fontsize: 12
  frameon: true
  title: "Tipos de medallas"
  custom_icons: true
  icons:
    - label: "Oro"
      image: "assets/icons/gold_medal.png"
      zoom: 0.15
    - label: "Plata"
      image: "assets/icons/silver_medal.png"
      zoom: 0.15
    - label: "Bronce"
      image: "assets/icons/bronze_medal.png"
      zoom: 0.15
  
# Logo de organización
logo:
  path: "assets/logo_condatos.png"
  position: "above_legend"
  zoom: 0.2
  margin: 0.02
```

**NOTA IMPORTANTE**: La configuración personalizada de leyenda y logo **NO** debe colocarse dentro de la sección `overrides:`, sino directamente en el nivel principal del archivo YAML. Esto es esencial para que funcione correctamente.

## Consideraciones Técnicas

- **Formatos de imagen**: Se recomiendan PNG con transparencia para mejor integración
- **Tamaño de imágenes**: Para iconos de leyenda, idealmente 32x32 o 64x64 píxeles
- **Factor de zoom**: Ajusta el parámetro `zoom` según el tamaño de tus imágenes
- **Resolución**: Asegúrate de que tus imágenes se vean bien tanto en pantalla como en exportaciones de alta resolución
- **Ruta de archivos**: Las rutas son relativas al directorio de trabajo, no al archivo YAML

## Integración con Estilos Corporativos

Esta funcionalidad es ideal para mantener una identidad corporativa coherente en tus visualizaciones:

- Usa logos oficiales de tu organización
- Incluye iconos que representen conceptos específicos de tu industria
- Mantén consistencia visual entre diferentes gráficos y presentaciones
