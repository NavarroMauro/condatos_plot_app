# Guía para Desarrolladores de ConDatos-Figs-App

Este documento consolidado proporciona una guía completa para contribuir al desarrollo de ConDatos-Figs-App, una plataforma para la creación de visualizaciones estandarizadas enfocadas en Chile y su contexto latinoamericano.

## Índice

1. [Proceso de Contribución](#proceso-de-contribución)
   - [Flujo de Trabajo](#flujo-de-trabajo-para-contribuciones)
   - [Estilo y Convenciones](#estilo-y-convenciones)
   - [Verificaciones Automatizadas](#verificaciones-automatizadas)

2. [Estándares de Desarrollo](#estándares-de-desarrollo)
   - [Estilo de Código](#estilo-de-código)
   - [Reglas de Formato](#reglas-de-formato)
   - [Estructura del Proyecto](#estructura-del-proyecto)

3. [Trabajando con GitHub Copilot](#trabajando-con-github-copilot)
   - [Buenas Prácticas con Copilot](#buenas-prácticas-con-copilot)
   - [Ejemplos de Código para Copilot](#ejemplos-de-código-para-copilot)

4. [Tareas Pendientes](#tareas-pendientes)
   - [Backlog Actual](#backlog-actual)
   - [Cómo Contribuir a las Tareas](#cómo-contribuir-a-las-tareas)

---

## Proceso de Contribución

### Flujo de Trabajo para Contribuciones

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

### Estilo y Convenciones

- **Python ≥3.10**: Utiliza las características disponibles en Python 3.10 o superior
- **Ruff**: Ruff es el formateador y linter por defecto
- **No duplicar código**: No crear helpers duplicados; utilidades de etiquetas/leyendas en `plot_helpers.py` o `helpers.py`
- **Consistencia**: Para nuevas figuras, añadir comando en `app/plot.py` y reutilizar `apply_style`, `apply_frame`, `finish_and_save`
- **Identidad visual**: Mantener la consistencia con los estándares visuales de ConDatos, similar a Statista pero adaptada al contexto latinoamericano

### Verificaciones Automatizadas

Antes de enviar un Pull Request, asegúrate de que tu código pasa todas las verificaciones:

```bash
# Ejecutar formateo con ruff
make fmt

# Ejecutar linting
make lint

# Ejecutar tests
make test

# Realizar pruebas de humo (smoke tests)
make smoke
```

## Estándares de Desarrollo

### Estilo de Código

- Usa **Typer** para comandos CLI
- Estructura modular en `app/plots/` (cada tipo de gráfico en un archivo)
- `numpy` + `pandas` para cálculos vectorizados (evitar bucles innecesarios)
- `matplotlib` + helpers de `app.plot_helpers` para renderización
- Docstrings descriptivos para todas las funciones y clases públicas
- Comentarios claros para lógica compleja

### Reglas de Formato

- **Linting y formateo**: Ruff maneja lint + format
- **Importaciones**:
  - Primero stdlib
  - Luego terceros
  - Finalmente internos (`app.*`)
- **Strings**: Utiliza comillas dobles `"..."` consistentemente
- **Figuras**: Siempre cerrar figuras con `plt.close(fig)` para evitar fugas de memoria
- **Nombres de variables**: Descriptivos y en snake_case
- **Longitud de línea**: Máximo 88 caracteres (configurado en ruff)

### Estructura del Proyecto

- **`app/plot.py`**: CLI Typer con comandos principales
- **`app/plots/`**: Implementaciones de diferentes tipos de gráficos
- **`app/layout.py`**: Manejo del frame y estructura de la figura
- **`app/styling.py`**: Aplicación de estilos
- **`app/helpers.py` y `app/plot_helpers.py`**: Funciones de utilidad
- **`tests/`**: Tests unitarios y de integración
- **`config/`**: Archivos de configuración YAML
- **`templates/`**: Plantillas YAML base

## Trabajando con GitHub Copilot

GitHub Copilot puede ser una herramienta poderosa para acelerar el desarrollo en ConDatos-Figs-App, pero es importante usarlo correctamente.

### Buenas Prácticas con Copilot

1. **Revisar siempre las sugerencias**: Copilot puede generar código que parece correcto pero no se ajusta a las convenciones del proyecto
2. **Proporcionar contexto**: Incluir comentarios descriptivos y docstrings para guiar a Copilot
3. **Verificar imports**: Asegurarse de que Copilot incluya todos los imports necesarios
4. **Validar lógica**: No asumir que la lógica generada es correcta, especialmente en cálculos complejos
5. **Mantener consistencia**: Asegurar que el código generado siga las convenciones del proyecto

### Ejemplos de Código para Copilot

Para ayudar a Copilot a generar código más relevante, aquí hay un ejemplo de cómo implementar un nuevo tipo de gráfico:

```python
from pathlib import Path
from app.helpers import _load_yaml, _merge_params, _print_ok
from app.layout import apply_frame, finish_and_save
from app.styling import apply_style
import matplotlib.pyplot as plt
import pandas as pd

def add_command(app):
    @app.command("nuevo")
    def nuevo(config: Path):
        """
        Genera un nuevo tipo de gráfico.
        
        Args:
            config: Ruta al archivo YAML de configuración
        """
        # Cargar y fusionar configuración
        cfg = _load_yaml(config)
        tpl = _load_yaml(Path(cfg["template"]))
        params = _merge_params(tpl, cfg)
        
        # Aplicar estilo y crear figura
        apply_style(params.get("styling", {}))
        fig, ax = plt.subplots(figsize=params.get("figsize", (10, 6)))
        
        # Aplicar frame (título, subtítulo, márgenes)
        apply_frame(fig, params)
        
        # Cargar datos
        if "data" in params:
            if "csv" in params["data"]:
                df = pd.read_csv(params["data"]["csv"])
            elif "inline" in params["data"]:
                df = pd.DataFrame(params["data"]["inline"])
        
        # Implementar lógica de gráfico aquí
        # ...
        
        # Finalizar y guardar
        finish_and_save(fig, params)
        plt.close(fig)
        _print_ok(params)
```

## Tareas Pendientes

### Backlog Actual

El proyecto tiene las siguientes tareas pendientes:

1. **Completar `layout.finish_and_save`**: Asegurar que llama a `add_branding` y luego a `save_fig_multi`
2. **Plantillas YAML de ejemplo**: Crear una por cada comando (line/bar/barh/stackedbar/stackedbarh/heatmap/choropleth) con datos inline
3. **Smoke script**: Implementar `scripts/smoke.sh` que renderice todas las figuras a `out/` y devuelva `0` si existen PNG y SVG
4. **Docs de datos**: Especificar columnas obligatorias por tipo de figura (category_col, series_order, flags, etc.)
5. **Paletas de colores regionales**: Desarrollar paletas de colores específicas para representar datos de Chile y países latinoamericanos
6. **Soporte para mapas geográficos detallados**: Mejorar el soporte para mapas coropléticos con nivel de detalle para regiones chilenas y sudamericanas
7. **Plantillas temáticas latinoamericanas**: Crear plantillas YAML específicas para visualizaciones económicas y sociales relevantes para la región
8. **Sistema bilingüe**: Implementar soporte para etiquetas bilingües (español/inglés) en los gráficos

### Cómo Contribuir a las Tareas

1. **Selecciona una tarea**: Revisa el backlog y elige una tarea que te interese
2. **Crea un issue**: Si no existe ya, crea un issue en GitHub describiendo la tarea
3. **Asigna el issue**: Asígnate el issue para que otros sepan que estás trabajando en él
4. **Crea una rama**: Crea una rama específica para la tarea
5. **Implementa la solución**: Trabaja en la implementación siguiendo las convenciones del proyecto
6. **Ejecuta tests**: Asegúrate de que tu implementación pasa todas las pruebas
7. **Envía un PR**: Crea un Pull Request con una descripción clara de los cambios y vinculándolo al issue

---

Para una lista completa y actualizada de tareas pendientes, consulta el archivo [TASKS.md](../TASKS.md) y los issues abiertos en GitHub.

Este documento es una guía viva que puede ser actualizada en función de las necesidades del proyecto y el feedback de los colaboradores. Si encuentras información desactualizada o tienes sugerencias de mejora, no dudes en contribuir con esos cambios.
