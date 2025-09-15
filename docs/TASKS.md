# Backlog (atómico)

```markdown
# Backlog (atómico)

- [x] **Eliminar duplicados en helpers**: `norm_legend_loc`, `get_label_fmt`, `_bar_cfg` aparecen dos veces; consolidar una sola versión y ajustar imports.  
- [x] **Documentar configuración de ejes y títulos**: Creado `AXIS_TITLE_CUSTOMIZATION.md` con opciones para personalizar ejes y espaciado de títulos.
- [x] **Documentar etiquetas de valores y totales**: Creado `VALUE_TOTAL_LABELS.md` con opciones para configurar etiquetas en segmentos y totales de barras.
- [ ] **Completar `layout.finish_and_save`** si quedó parcial; asegurar que llama a `add_branding` y luego a `save_fig_multi`.  
- [ ] **Plantillas YAML de ejemplo**: una por cada comando (line/bar/barh/stackedbar/stackedbarh/heatmap/choropleth) con datos inline.
- [ ] **Smoke script**: `scripts/smoke.sh` que renderice todas las figuras a `out/` y devuelva `0` si existen PNG y SVG.
- [ ] **Docs de datos**: especificar columnas obligatorias por tipo de figura (category_col, series_order, flags, etc.).
- [ ] **Paletas de colores regionales**: Desarrollar paletas de colores específicas para representar datos de Chile y países latinoamericanos.
- [ ] **Soporte para mapas geográficos detallados**: Mejorar el soporte para mapas coropléticos con nivel de detalle para regiones chilenas y sudamericanas.
- [ ] **Plantillas temáticas latinoamericanas**: Crear plantillas YAML específicas para visualizaciones económicas y sociales relevantes para la región.
- [ ] **Sistema bilingüe**: Implementar soporte para etiquetas bilingües (español/inglés) en los gráficos.
- [ ] **Documentación de estándares visuales**: Crear un documento completo con los estándares visuales de ConDatos.

```
