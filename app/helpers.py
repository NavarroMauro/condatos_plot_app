# app/helpers.py
from __future__ import annotations

from pathlib import Path
import yaml
from matplotlib.transforms import ScaledTranslation
from rich import print as rprint


# ----------------------------
# Leyendas / formato etiquetas
# ----------------------------
def norm_legend_loc(loc: str | None, default: str = "upper right") -> str:
    """Normaliza ubicaciones 'humanas' a códigos válidos de Matplotlib."""
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


def get_label_fmt(params: dict, default: str = "{:.0f}") -> str:
    """Obtiene el formato de etiqueta, con fallback a yfmt/value_fmt."""
    return params.get("yfmt") or params.get("value_fmt") or default


# ----------------------------
# Texto / offsets
# ----------------------------
def apply_text_offset(ax, txt_artist, x_pt: float = 0.0, y_pt: float = 0.0, fig=None) -> None:
    """Desplaza un texto en puntos, independientemente del sistema de coords."""
    if fig is None:
        fig = ax.figure
    txt_artist.set_transform(
        ax.transData + ScaledTranslation(x_pt / 72.0, y_pt / 72.0, fig.dpi_scale_trans)
    )
    txt_artist.set_clip_on(False)


# ----------------------------
# Barras / visibilidad / cfg
# ----------------------------
def should_show_val(val: float, params: dict, percent_key: str = "percent") -> bool:
    """Decide si mostrar etiqueta según min_label_height y si percent=True."""
    if val <= 0:
        return False
    min_h = float(params.get("min_label_height", 0.0))
    if params.get(percent_key, False):
        # en percent, min_h se interpreta en % del segmento
        return val >= min_h
    return (min_h == 0.0) or (val >= min_h)


def _bar_cfg(params: dict) -> dict:
    """Asegura que params['bar'] exista y tenga defaults coherentes."""
    bar = params.setdefault("bar", {})
    bar.setdefault("bar_width", 0.65)  # horizontal: height; vertical: width
    bar.setdefault("linewidth", 0.8)
    bar.setdefault("edgecolor", "white")
    return bar


# ----------------------------
# YAML / merge de parámetros
# ----------------------------
def deep_merge(base: dict, override: dict) -> dict:
    """Merge recursivo: los valores de override tienen precedencia."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _load_yaml(p: Path) -> dict:
    """Carga un YAML en dict (utf-8)."""
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _merge_params(tpl: dict, cfg: dict) -> dict:
    """
    Mezcla template y config:
    - Copia todo el root del template.
    - Sobrescribe con root del cfg (excepto 'template' y 'overrides').
    - Aplica 'overrides' recursivamente al final.
    """
    base = tpl.copy()
    for key, value in cfg.items():
        if key not in ("overrides", "template"):
            base[key] = value
    if "overrides" in cfg:
        base = deep_merge(base, cfg["overrides"])
    return base


# ----------------------------
# Logging OK estándar
# ----------------------------
def _print_ok(params: dict) -> None:
    exts = ",".join(params.get("formats", ["png", "svg", "pdf"]))
    rprint(f"[bold green]OK[/bold green] → {params.get('outfile', 'out/figure')}.{exts}")
