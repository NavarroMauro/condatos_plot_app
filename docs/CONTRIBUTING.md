# Estilo y flujo

- Python ≥3.10. Ruff es el formateador por defecto.
- No crear helpers duplicados; utilidades de etiquetas/leyendas en `plot_helpers.py` o `helpers.py`.
- Para nuevas figuras: añadir comando en `app/plot.py`, reusar `apply_style`, `apply_frame`, `finish_and_save`.

## Comandos de ejemplo

- Stacked bar H: `python -m app.plot stackedbarh config.yml`
- Choropleth: `python -m app.cmd_choropleth path.yml`

## Tests rápidos (smoke)

- Render mínimo con `stackedbar-horizontal-condatos.yml` y verificar que genera PNG+SVG.
