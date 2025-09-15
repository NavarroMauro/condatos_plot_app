# Contribuyendo a ConDatos-Figs-App

ConDatos-Figs-App es una plataforma para la creación de visualizaciones estandarizadas enfocadas en Chile y su contexto latinoamericano. Al contribuir a este proyecto, ayudas a mejorar la calidad de las representaciones visuales de datos económicos, sociales y geográficos de la región.

## Flujo de trabajo para contribuciones

1. **Crear una rama**: Siempre trabaja en una rama separada, no directamente en `main` o `develop`.

   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Ejecutar los hooks de pre-commit**: Instala los hooks para verificaciones automáticas.

   ```bash
   cp .hooks/pre-commit .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

3. **Ejecutar tests antes de commit**: Asegúrate que tus cambios no rompen la funcionalidad existente.

   ```bash
   pytest -xvs tests/
   ```

4. **Regenerar el Makefile** si añadiste nuevas configuraciones o tipos de gráfico.

   ```bash
   python scripts/generate_makefile.py --install
   ```

5. **Hacer un pull request**: Describe claramente los cambios realizados.

## Estilo y convenciones

- Python ≥3.10. Ruff es el formateador por defecto.
- No crear helpers duplicados; utilidades de etiquetas/leyendas en `plot_helpers.py` o `helpers.py`.
- Para nuevas figuras: añadir comando en `app/plot.py`, reusar `apply_style`, `apply_frame`, `finish_and_save`.
- Mantener la consistencia visual con los estándares definidos para ConDatos, siguiendo la línea estética similar a Statista pero adaptada al contexto latinoamericano.

## Comandos de ejemplo

- Stacked bar H: `python -m app.plot stackedbarh config.yml`
- Choropleth: `python -m app.cmd_choropleth path.yml`

## Tests rápidos (smoke)

- Render mínimo con `stackedbar-horizontal-condatos.yml` y verificar que genera PNG+SVG.

## Estándares visuales

Al desarrollar nuevas visualizaciones o modificar las existentes, es importante mantener los siguientes estándares:

- **Identidad visual**: Mantener la consistencia con la identidad visual de ConDatos, utilizando las paletas de colores definidas y los estilos tipográficos establecidos.
- **Contextualización regional**: Adaptar las visualizaciones para que sean relevantes al contexto chileno y latinoamericano, considerando particularidades regionales cuando sea necesario.
- **Accesibilidad**: Asegurar que las visualizaciones sean accesibles y comprensibles para un amplio rango de usuarios.
- **Precisión**: Priorizar la precisión y claridad en la representación de datos sobre elementos decorativos.
- **Bilingüismo**: Cuando sea posible, facilitar la inclusión de elementos bilingües (español/inglés) para mayor alcance de las visualizaciones.
