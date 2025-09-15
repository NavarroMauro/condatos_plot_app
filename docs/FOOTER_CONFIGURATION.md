# Configuración del Footer en Gráficos Condatos

Este documento explica cómo configurar correctamente el footer en los gráficos generados con la biblioteca de visualización de Condatos, adaptado para las visualizaciones estandarizadas de datos chilenos y del contexto latinoamericano.

## Estructura del Footer

El footer típicamente contiene tres elementos principales:

1. **Texto de fuente**: Indica la procedencia de los datos (fuentes oficiales chilenas o latinoamericanas)
2. **Texto de licencia/nota**: Proporciona información sobre los derechos de uso
3. **Logo**: Muestra el logo de Condatos u otra organización colaboradora

Para visualizaciones estandarizadas de datos chilenos, recomendamos incluir información específica sobre la fuente de datos nacional cuando corresponda (INE, Banco Central de Chile, etc.).

## Posicionamiento Correcto

Para evitar la superposición de elementos en el footer, es importante definir coordenadas `y_position` distintas para cada elemento:

```yaml
footer:
  config:
    y_position: 0.05      # Posición base vertical del footer
    show_frame: false     # Opción para mostrar/ocultar marco
    spacing: 0.025        # Espacio vertical entre elementos
    
  # Primera línea (texto de fuente)
  source: "Fuente: Organización XXX, YYYY"
  source_config:
    fontsize: 16          # Tamaño de fuente
    x_position: 0.15      # Posición horizontal (izquierda)
    y_position: 0.065     # Posición vertical - línea superior
    alignment: "left"     # Alineación del texto
    width: 0.30           # Ancho máximo del texto
    
  # Segunda línea (licencia)
  note: "Licencia XXX"
  note_config:
    fontsize: 14          # Tamaño ligeramente menor
    x_position: 0.15      # Misma posición horizontal
    y_position: 0.03      # Posición vertical - línea inferior
    alignment: "left"     # Alineación de texto
    color: "#666666"      # Color diferente opcional
    
  # Logo
  logos:
    - path: "assets/logo.png"
      size_method: "fraction"
      width_fraction: 0.18  # Tamaño como fracción del ancho total
      x_position: 0.95      # Posición horizontal (derecha)
```

## Buenas Prácticas

1. **Separación vertical**: Asegúrate de que exista suficiente espacio entre elementos estableciendo diferentes valores de `y_position` para cada uno

2. **Coordenadas**: Los valores de posición son fracciones relativas al tamaño total de la figura
   - `x_position = 0` representa el borde izquierdo
   - `x_position = 1` representa el borde derecho
   - `y_position = 0` representa el borde inferior
   - `y_position = 1` representa el borde superior

3. **Tamaños de fuente**: Usa tamaños proporcionales a la escala del gráfico
   - Para gráficos grandes: 16-18pt para texto de fuente, 14-16pt para licencias
   - Para gráficos pequeños: 12-14pt para texto de fuente, 10-12pt para licencias

4. **Alineación**: Mantén consistencia en la alineación de textos relacionados

5. **Ancho máximo**: Usa la propiedad `width` para controlar el ancho del texto y evitar que ocupe demasiado espacio

6. **Formatos estandarizados para fuentes de datos chilenas**:
   - Datos oficiales: "Fuente: [Institución], [Año]" (ej. "Fuente: INE Chile, 2023")
   - Datos regionales: "Fuentes: [Institución Chile] y [Institución Regional], [Año]"
   - Elaboración propia: "Elaboración: ConDatos en base a [Fuente], [Año]"

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

## Ejemplos de Uso

### Caso 1: Visualización de Datos Económicos Chilenos

Configuración para un gráfico de indicadores económicos del Banco Central:

```yaml
footer:
  config:
    y_position: 0.05
    show_frame: false
    spacing: 0.025
    
  source: "Fuente: Banco Central de Chile, 2023"
  source_config:
    fontsize: 16
    x_position: 0.15
    y_position: 0.065
    alignment: "left"
    width: 0.30
    
  note: "Elaborado por ConDatos • Licencia CC BY 4.0"
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

### Caso 2: Comparativa Regional Latinoamericana

Configuración para un gráfico comparativo entre países latinoamericanos:

```yaml
footer:
  config:
    y_position: 0.05
    show_frame: false
    spacing: 0.025
    
  source: "Fuentes: CEPAL y Banco Mundial, 2023"
  source_config:
    fontsize: 16
    x_position: 0.15
    y_position: 0.065
    alignment: "left"
    width: 0.35
    
  note: "Elaboración: ConDatos en base a datos oficiales • CC BY-NC-SA 4.0"
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

### Caso 3: Evento Deportivo Regional

En el gráfico de medallas de los Juegos Panamericanos Junior 2025, se utilizó la siguiente configuración:

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
