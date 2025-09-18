# Configuración y Personalización de Footer

Este documento consolida toda la información sobre la configuración y personalización del footer (pie de página) de las gráficas de ConDatos, con ejemplos específicos para visualizaciones de datos chilenos y latinoamericanos.

## Estructura del Footer

El footer típicamente contiene tres elementos principales:

1. **Texto de fuente**: Indica la procedencia de los datos
2. **Texto de licencia/nota**: Proporciona información sobre los derechos de uso
3. **Logo**: Muestra el logo de Condatos u otra organización colaboradora

La configuración se realiza en el archivo YAML con la siguiente estructura básica:

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

## Opciones de Configuración General

```yaml
footer:
  config:
    y_position: 0.03       # Posición vertical base (0=abajo, 1=arriba)
    spacing: 0.02          # Espaciado entre elementos
    show_frame: true       # Mostrar un marco para el footer
    frame_padding: 0.01    # Relleno interno del marco
    frame_alpha: 0.08      # Transparencia del marco (0-1)
    frame_color: "#f0f0f0" # Color del marco
```

## Posicionamiento Correcto

Para evitar la superposición de elementos en el footer, es importante definir coordenadas `y_position` distintas para cada elemento:

- Los valores de posición son fracciones relativas al tamaño total de la figura
  - `x_position = 0` representa el borde izquierdo
  - `x_position = 1` representa el borde derecho
  - `y_position = 0` representa el borde inferior
  - `y_position = 1` representa el borde superior

## Configuración del Texto de Fuente

```yaml
footer:
  # Texto simple (compatibilidad)
  source: "Fuente: INE Chile, 2023"
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
    y_position: 0.065      # Posición vertical específica
    alignment: "left"      # Alineación: "left", "center", "right"
    width: 0.30           # Ancho máximo del texto
```

### Patrones Estandarizados para Citar Fuentes

Para mantener la consistencia en todas las visualizaciones de ConDatos, recomendamos seguir estos formatos estandarizados:

#### Datos de organismos oficiales chilenos

```yaml
source: "Fuente: [Institución], [Año]"
```

Ejemplo: `"Fuente: INE Chile, 2023"` o `"Fuente: Banco Central de Chile, 2023"`

#### Datos regionales latinoamericanos

```yaml
source: "Fuente: [Institución Regional], [Año]"
```

Ejemplo: `"Fuente: CEPAL, 2023"` o `"Fuente: BID, 2023"`

#### Múltiples fuentes

```yaml
source: "Fuentes: [Institución 1] y [Institución 2], [Año]"
```

Ejemplo: `"Fuentes: INE Chile y CEPAL, 2023"`

#### Elaboración propia basada en datos oficiales

```yaml
source: "Elaboración: ConDatos en base a datos de [Fuente], [Año]"
```

Ejemplo: `"Elaboración: ConDatos en base a datos de INE Chile, 2023"`

## Configuración del Texto de Nota

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
    x_position: 0.15       # Posición horizontal (0=izquierda, 1=derecha)
    y_position: 0.03       # Posición vertical específica
    alignment: "left"      # Alineación: "left", "center", "right"
    width: 0.30            # Ancho máximo del texto
```

## Configuración de Logos

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

## Buenas Prácticas

1. **Separación vertical**: Asegúrate de que exista suficiente espacio entre elementos estableciendo diferentes valores de `y_position` para cada uno

2. **Tamaños de fuente**: Usa tamaños proporcionales a la escala del gráfico
   - Para gráficos grandes: 16-18pt para texto de fuente, 14-16pt para licencias
   - Para gráficos pequeños: 12-14pt para texto de fuente, 10-12pt para licencias

3. **Alineación**: Mantén consistencia en la alineación de textos relacionados

4. **Ancho máximo**: Usa la propiedad `width` para controlar el ancho del texto y evitar que ocupe demasiado espacio

## Solución de Problemas Comunes

### Superposición de Textos

Si los textos se superponen, ajusta los valores de `y_position` para crear una separación adecuada:

- Aumenta el valor de `y_position` para el texto de la fuente
- Disminuye el valor de `y_position` para el texto de la nota/licencia

### Texto Cortado

Si el texto aparece cortado o truncado:

- Aumenta el valor de `width` para permitir más espacio horizontal
- Considera reducir el tamaño de fuente
- Implementa el ajuste automático de texto (word wrapping)

### Desbordamiento del Footer

Si los elementos del footer se salen del área visible:

- Aumenta el margen inferior (`margins.bottom`) en la configuración global del gráfico
- Ajusta las posiciones verticales (`y_position`) de todos los elementos del footer

## Ejemplos Completos

### Ejemplo 1: Visualización de Datos Económicos Chilenos

```yaml
footer:
  config:
    y_position: 0.03
    spacing: 0.02
    show_frame: true
    frame_padding: 0.01
    frame_alpha: 0.08
    frame_color: "#f0f0f0"

  source: "Fuente: Banco Central de Chile, 2023"
  source_config:
    fontsize: 16
    color: "#555555"
    style: "italic"
    weight: "normal"
    family: "Nunito"
    x_position: 0.15
    y_position: 0.065
    alignment: "left"
    width: 0.30

  note: "Licencia CC BY-NC-SA 4.0"
  note_config:
    fontsize: 14
    color: "#555555"
    style: "normal"
    weight: "normal"
    family: "Nunito"
    x_position: 0.15
    y_position: 0.03
    alignment: "left"
    width: 0.30

  logos:
    - path: "assets/logos/logo_condatos.png"
      size_method: "fraction"
      width_fraction: 0.10
      preserve_aspect_ratio: true
      x_position: 0.85
      alignment: "right"
    - path: "assets/logos/logo_chile.png"
      size_method: "pixels"
      width_pixels: 60
      x_position: 0.70
      alignment: "right"
```

### Ejemplo 2: Comparativa Regional Latinoamericana

```yaml
footer:
  config:
    y_position: 0.03
    spacing: 0.02
    show_frame: true
    frame_padding: 0.01
    frame_alpha: 0.08
    frame_color: "#f0f0f0"

  source: "Fuentes: CEPAL y Banco Mundial, 2023"
  source_config:
    fontsize: 16
    color: "#555555"
    style: "italic"
    weight: "normal"
    family: "Nunito"
    x_position: 0.15
    y_position: 0.065
    alignment: "left"
    width: 0.35

  note: "Elaboración: ConDatos en base a datos oficiales • CC BY 4.0"
  note_config:
    fontsize: 14
    color: "#555555"
    style: "normal"
    weight: "normal"
    family: "Nunito"
    x_position: 0.15
    y_position: 0.03
    alignment: "left"
    width: 0.35

  logos:
    - path: "assets/logos/logo_condatos.png"
      size_method: "fraction"
      width_fraction: 0.10
      preserve_aspect_ratio: true
      x_position: 0.85
      alignment: "right"
    - path: "assets/cc_by.png"
      size_method: "pixels"
      width_pixels: 80
      x_position: 0.70
      alignment: "right"
```

### Caso 3: Evento Deportivo Regional (Juegos Panamericanos Junior 2025)

```yaml
footer:
  config:
    y_position: 0.05
    show_frame: false
    spacing: 0.025
    
  source: "Fuente: Comité Olímpico Panamericano, 2025"
  source_config:
    fontsize: 16
    x_position: 0.15
    y_position: 0.065
    alignment: "left"
    width: 0.30
    
  note: "Licencia CC BY-NC-SA 4.0"
  note_config:
    fontsize: 14
    x_position: 0.15
    y_position: 0.03
    alignment: "left"
    color: "#666666"
    
  logos:
    - path: "assets/logo_condatos.png"
      size_method: "fraction"
      width_fraction: 0.18
      x_position: 0.95
```

Estas configuraciones garantizan que todos los elementos del footer sean claramente visibles y estén correctamente espaciados, manteniendo el estándar de citación adecuado para las fuentes chilenas y latinoamericanas.
