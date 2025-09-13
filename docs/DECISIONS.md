# ADR (resumen)

- 2025-09-13: Control independiente para visibilidad de etiquetas y ticks de ejes, permitiendo mostrar etiquetas sin ticks.
- 2025-09-13: Implementación de sistema de espaciado personalizable para título y subtítulo con `title_spacing` con control individual de márgenes.
- 2025-09-13: Mantener tanto `loc` como `bbox_to_anchor` para posicionamiento preciso de leyendas, documentando claramente su relación.
- 2025-09-09: Exportar multi-formato estandarizado con `save_fig_multi` (soporte SVG minificado con scour; JPG/WEBP/AVIF vía Pillow-Heif).
- 2025-09-09: Header separado del área de gráfico en `layout._draw_header` para títulos largos.
