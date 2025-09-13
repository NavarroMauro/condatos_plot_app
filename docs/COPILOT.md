# Copilot en ConDatos-Figs

## Estilo de código

- Usa **Typer** para comandos CLI.
- Estructura modular en `app/plots/` (cada gráfico en un archivo).
- `numpy` + `pandas` para cálculos vectorizados (evitar bucles innecesarios).
- `matplotlib` + helpers de `app.plot_helpers` para render.

## Reglas de formato

- Ruff maneja lint + format.
- Imports: primero stdlib, luego terceros, luego internos (`app.*`).
- Strings: comillas dobles `"..."`.
- Siempre cerrar figuras con `plt.close(fig)`.

## Ejemplos

Para un gráfico nuevo:

```python
from app.helpers import _load_yaml, _merge_params, _print_ok
from app.layout import apply_frame, finish_and_save
import matplotlib.pyplot as plt

def add_command(app):
    @app.command("nuevo")
    def nuevo(config: Path):
        cfg = _load_yaml(config)
        tpl = _load_yaml(Path(cfg["template"]))
        params = _merge_params(tpl, cfg)
        fig, ax = plt.subplots()
        apply_frame(fig, params)
        # plot...
        finish_and_save(fig, params)
        plt.close(fig)
        _print_ok(params)
```
