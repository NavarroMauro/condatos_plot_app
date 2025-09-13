# ConDatos · Figuras estáticas

## Módulos

- app/plot.py — CLI Typer. Comandos: `line`, `bar`, `barh`, `stackedbar`, `stackedbarh`, `heatmap`. Carga plantilla+config (YAML), aplica estilo y layout, guarda multi-formato.  
- app/layout.py — Frame de figura: header (título/subtítulo), márgenes, finish_and_save (inserta branding y guarda).  
- app/branding.py — Footer/branding: íconos CC, logo, fuente/nota/fecha.  
- app/io_utils.py — `save_fig_multi(fig, base, formats, …)` (PNG/SVG/PDF/JPG/WEBP/AVIF).  
- app/styling.py — `apply_style(...)`: estilos `.mplstyle`, registra fuentes (Nunito).  
- app/plot_helpers.py — utilidades: autosize por filas, banderas en barras apiladas, labels de segmentos y totales.  
- app/cmd_choropleth.py — comando de mapa coroplético (GeoPandas, scheme opcional vía mapclassify).  
- app/helpers.py — normalización de leyendas, formatos de etiqueta y helpers de barras.

## Flujo (render genérico)

YAML (template + overrides) → `apply_style()` → `plt.subplots()` → `apply_frame()` (header/márgenes) → plot → `finish_and_save()` (branding + export).

## Entradas comunes

- `template` (ruta YAML base) + `overrides` (dict).  
- `data.csv` o `data.inline`.  
- `style` (uno o varios `.mplstyle`).  
- `formats`: p.ej. `["png","svg","pdf","webp"]`.

## Convenciones

- Reusar helpers de `plot_helpers.py` antes de crear funciones nuevas.
- Guardados SIEMPRE vía `save_fig_multi` (no usar `fig.savefig` directo).
