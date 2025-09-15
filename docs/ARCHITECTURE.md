# ConDatos · Figuras estáticas

ConDatos-Figs-App es una plataforma para la creación de visualizaciones estandarizadas y profesionales, diseñada siguiendo un enfoque similar a Statista pero adaptada específicamente para representar datos del contexto chileno y latinoamericano. Este documento describe la arquitectura técnica que sustenta esta visión.

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
- Fuentes de datos:
  - `data.csv`: Datos desde archivo CSV.
  - `data.inline`: Datos definidos directamente en el YAML.
  - `data.postgresql`: *(planificado)* Datos desde base de datos PostgreSQL.
- `style` (uno o varios `.mplstyle`).  
- `formats`: p.ej. `["png","svg","pdf","webp"]`.

## Convenciones

- Reusar helpers de `plot_helpers.py` antes de crear funciones nuevas.
- Guardados SIEMPRE vía `save_fig_multi` (no usar `fig.savefig` directo).

## Principios de diseño

La arquitectura de ConDatos-Figs-App está basada en los siguientes principios:

1. **Estandarización**: Garantizar la consistencia visual entre todas las figuras producidas.
2. **Configuración declarativa**: Separar la configuración (YAML) del código para facilitar ajustes sin modificar el código.
3. **Adaptabilidad regional**: Incluir características específicas para el contexto chileno y latinoamericano (banderas, formatos regionales, etc.).
4. **Extensibilidad**: Diseño modular que permite añadir nuevos tipos de gráficos manteniendo la coherencia del sistema.
5. **Calidad de exportación**: Priorizar formatos de exportación de alta calidad adecuados para publicaciones profesionales.
6. **Templates fijos**: Utilizar templates predefinidos que aceptan datos en formatos específicos para facilitar la creación estandarizada de visualizaciones.
7. **Flexibilidad en fuentes de datos**: Soportar múltiples fuentes de datos (CSV, inline, y próximamente PostgreSQL) manteniendo la consistencia visual.
