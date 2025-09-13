# Personalización de Footer

Este documento describe las opciones disponibles para personalizar el footer (pie de página) de las gráficas.

## Estructura básica

El footer se puede configurar dentro de cualquier archivo YAML de configuración con la siguiente estructura:

```yaml
footer:
  # Configuración general
  config: {...}
  
  # Texto de fuente
  source: "Texto de la fuente"
  source_config: {...}
  
  # Texto de nota
  note: "Texto de la nota"
  note_config: {...}
  
  # Logos
  logos: [...]
```

## Opciones de configuración general

```yaml
footer:
  config:
    y_position: 0.03       # Posición vertical (0=abajo, 1=arriba)
    spacing: 0.02          # Espaciado entre elementos
    show_frame: true       # Mostrar un marco para el footer
    frame_padding: 0.01    # Relleno interno del marco
    frame_alpha: 0.08      # Transparencia del marco (0-1)
    frame_color: "#f0f0f0" # Color del marco
```

## Configuración del texto de fuente

```yaml
footer:
  # Texto simple (compatibilidad)
  source: "Fuente: Organización XYZ, 2025"
  source_fontsize: 9       # Tamaño de fuente (legacy)
  source_color: "#666666"  # Color (legacy)
  
  # Configuración avanzada
  source_config:
    fontsize: 9            # Tamaño de fuente
    color: "#666666"       # Color
    style: "italic"        # Estilo: "normal", "italic"
    weight: "normal"       # Peso: "normal", "bold", "light", etc.
    family: "Nunito"       # Familia de fuente
    x_position: 0.15       # Posición horizontal (0=izquierda, 1=derecha)
```

## Configuración del texto de nota

```yaml
footer:
  # Texto simple (compatibilidad)
  note: "Licencia CC BY-NC-SA 4.0"
  note_fontsize: 9         # Tamaño de fuente (legacy)
  note_color: "#666666"    # Color (legacy)
  
  # Configuración avanzada
  note_config:
    fontsize: 9            # Tamaño de fuente
    color: "#666666"       # Color
    style: "normal"        # Estilo: "normal", "italic"
    weight: "normal"       # Peso: "normal", "bold", "light", etc.
    family: "Nunito"       # Familia de fuente
    x_position: 0.5        # Posición horizontal (0=izquierda, 1=derecha)
    alignment: "center"    # Alineación: "left", "center", "right"
```

## Configuración de logos

### Método simple (compatibilidad)

```yaml
footer:
  logo: "ruta/al/logo.png"
  logo_zoom: 0.15
```

### Método avanzado (múltiples logos)

```yaml
footer:
  logos:
    - path: "ruta/al/logo1.png"
      # Método para controlar el tamaño: "zoom", "absolute_inches", "fraction", "pixels"
      size_method: "zoom"  # Método por defecto
      
      # OPCIÓN 1: Factor de zoom simple
      zoom: 0.12  # Factor de escala relativo
      
      # OPCIÓN 2: Tamaño absoluto en pulgadas
      width_inches: 1.2  # Ancho en pulgadas
      height_inches: 0.8 # Alto en pulgadas (opcional)
      
      # OPCIÓN 3: Tamaño como fracción de la figura
      width_fraction: 0.10  # 10% del ancho de la figura
      height_fraction: 0.05 # 5% del alto de la figura (opcional)
      
      # OPCIÓN 4: Tamaño en píxeles
      width_pixels: 120  # Ancho en píxeles
      height_pixels: 80  # Alto en píxeles (opcional)
      
      # Mantener proporción
      preserve_aspect_ratio: true  # Mantener proporción original
      
      # Posición y alineación
      x_position: 0.85  # Posición horizontal
      alignment: "right"  # "right", "left", "center" o tuple (x,y)
    
    - path: "ruta/al/logo2.png"
      size_method: "fraction"
      width_fraction: 0.08  # 8% del ancho de la figura
      x_position: 0.70
      alignment: "right"
```

## Ejemplo completo

```yaml
footer:
  config:
    y_position: 0.03
    spacing: 0.02
    show_frame: true
    frame_padding: 0.01
    frame_alpha: 0.08
    frame_color: "#f0f0f0"

  source: "Fuente: Comité Olímpico Panamericano, 2025"
  source_config:
    fontsize: 9
    color: "#555555"
    style: "italic"
    weight: "normal"
    family: "Nunito"
    x_position: 0.15

  note: "Licencia CC BY-NC-SA 4.0"
  note_config:
    fontsize: 9
    color: "#555555"
    style: "normal"
    weight: "normal"
    family: "Nunito"
    x_position: 0.5
    alignment: "center"

  logos:
    - path: "assets/logo_condatos.png"
      size_method: "fraction"  # Usar tamaño como fracción de la figura
      width_fraction: 0.10     # 10% del ancho de la figura
      preserve_aspect_ratio: true
      x_position: 0.85
      alignment: "right"
    - path: "assets/cc_by_nc_sa.png"
      size_method: "pixels"    # Usar tamaño en píxeles
      width_pixels: 80         # 80 píxeles de ancho
      x_position: 0.70
      alignment: "right"
```
