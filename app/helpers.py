# app/helpers.py
from __future__ import annotations
from matplotlib.transforms import ScaledTranslation
from rich import print as rprint


def norm_legend_loc(loc: str | None) -> str | None:
    """Normaliza 'bottom right' -> 'lower right', 'top left' -> 'upper left', etc."""
    if not isinstance(loc, str):
        return loc
    loc = loc.strip().lower()
    return loc.replace("bottom", "lower").replace("top", "upper")

def get_label_fmt(params: dict, default: str = "{:.0f}") -> str:
    """Devuelve formato numérico a partir de overrides.label_fmt o yfmt."""
    return params.get("label_fmt", params.get("yfmt", default))

def apply_text_offset(ax, txt_artist, x_pt=0.0, y_pt=0.0, fig=None):
    """Desplaza un texto en puntos, independientemente del sistema de coords."""
    if fig is None:
        fig = ax.figure
    txt_artist.set_transform(
        ax.transData + ScaledTranslation(x_pt/72.0, y_pt/72.0, fig.dpi_scale_trans)
    )
    txt_artist.set_clip_on(False)

def should_show_val(val: float, params: dict, percent_key: str = "percent") -> bool:
    """Decide si mostrar etiqueta según min_label_height y si percent=True."""
    if val <= 0:
        return False
    min_h = float(params.get("min_label_height", 0.0))
    if params.get(percent_key, False):
        return val >= min_h  # en percent, min_h es porcentaje
    return (min_h == 0.0) or (val >= min_h)

def _bar_cfg(params):
    b = params.get("bar", {}) or {}
    return {
        "bar_width": float(b.get("bar_width", 0.65)),
        "linewidth": float(b.get("linewidth", 0.8)),
        "edgecolor": (b.get("edgecolor", "white") or None),
    }

# -- helpers.py --

# Normaliza ubicaciones "humanas" a códigos válidos de Matplotlib.
def norm_legend_loc(loc: str | None, default: str = "upper right") -> str:
    if not loc:
        return default
    loc = loc.strip().lower()
    mapping = {
        "upper left": "upper left",
        "upper right": "upper right",
        "lower left": "lower left",
        "lower right": "lower right",
        "upper center": "upper center",
        "lower center": "lower center",
        "center left": "center left",
        "center right": "center right",
        "center": "center",
        # alias “humanos”
        "top left": "upper left",
        "top right": "upper right",
        "bottom left": "lower left",
        "bottom right": "lower right",
        "left": "center left",
        "right": "center right",
        "top": "upper center",
        "bottom": "lower center",
    }
    return mapping.get(loc, default)

# Obtiene el formato de etiqueta, con fallback.
def get_label_fmt(params: dict, default: str = "{:.0f}") -> str:
    # permite usar yfmt o value_fmt como overrides
    return (
        params.get("yfmt")
        or params.get("value_fmt")
        or default
    )

# << NUEVO >>: asegura que params['bar'] exista y tenga defaults.
def _bar_cfg(params: dict) -> dict:
    bar = params.setdefault("bar", {})
    bar.setdefault("bar_width", 0.65)   # horizontal: height; vertical: width
    bar.setdefault("linewidth", 0.8)
    bar.setdefault("edgecolor", "white")
    return bar

def _print_ok(params):
    exts = ",".join(params.get("formats", ["png","svg","pdf"]))
    rprint(f"[bold green]OK[/bold green] → {params.get('outfile','out/figure')}.{exts}")
    


