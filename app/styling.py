from __future__ import annotations
from typing import Sequence
import warnings
import os
import matplotlib as mpl
import matplotlib.font_manager as fm
from pathlib import Path

def register_fonts():
    """Registra las fuentes del proyecto en matplotlib."""
    fonts_dir = Path(__file__).parent.parent / 'fonts'
    if fonts_dir.exists():
        for font_file in fonts_dir.glob('*.ttf'):
            try:
                fm.fontManager.addfont(str(font_file))
            except Exception as e:
                warnings.warn(f"No se pudo cargar la fuente {font_file.name}: {e}")

def verify_font_availability(font_name: str = "Nunito") -> bool:
    """Verifica si una fuente está disponible en el sistema."""
    fonts = [f.name for f in fm.fontManager.ttflist]
    available = font_name in fonts
    if not available:
        warnings.warn(f"La fuente {font_name} no está disponible. Se usará la fuente de respaldo.")
    return available

def _apply_one_style(style_path: str) -> None:
    """Aplica un estilo .mplstyle o un estilo de librería.
    Primero intenta matplotlib.style.use(); si falla, carga el archivo con rc_params_from_file().
    Nunca interrumpe la ejecución: emite un warning y continúa.
    """
    try:
        import matplotlib.style as mstyle  # disponible en Matplotlib 3.10+
    except Exception:
        mstyle = None

    # Normaliza rutas relativas (por legibilidad en warnings)
    style_disp = style_path
    if os.path.exists(style_path):
        style_disp = os.path.relpath(style_path)

    try:
        if mstyle is not None:
            mstyle.use(style_path)
            return
    except Exception as e:
        # cae al fallback de archivo explícito
        pass

    # Fallback: cargar parámetros desde archivo .mplstyle (si existe)
    try:
        from matplotlib import rc_params_from_file
        params = rc_params_from_file(style_path, use_default_template=False)
        mpl.rcParams.update(params)
    except FileNotFoundError:
        warnings.warn(f"[Condatos] Estilo no encontrado: {style_disp}. Se continúa sin aplicarlo.", RuntimeWarning)
    except Exception as e:
        warnings.warn(f"[Condatos] No se pudo aplicar estilo '{style_disp}': {e}. Se continúa.", RuntimeWarning)

def apply_style(style_path: str | Sequence[str] | None,
                width_in: float | None,
                height_in: float | None) -> None:
    """Aplica uno o varios estilos y, si vienen, fija figure.figsize desde plantilla.

    style_path puede ser:
      - None
      - str  (p.ej. "styles/base.mplstyle")
      - str  con coma  (p.ej. "styles/base.mplstyle, styles/condatos.mplstyle")
      - Sequence[str]  (lista o tupla de rutas o nombres de estilo)

    width_in / height_in (en pulgadas) ajustan el tamaño por defecto de la figura.
    """
    # Registrar y verificar fuentes primero
    register_fonts()
    verify_font_availability("Nunito")

    # 1) Aplica estilos
    if style_path:
        if isinstance(style_path, str):
            # Permite "a,b,c" separado por comas
            styles = [s.strip() for s in style_path.split(",")] if ("," in style_path) else [style_path]
        else:
            styles = list(style_path)

        for s in styles:
            if s:  # evita strings vacíos
                _apply_one_style(s)

    # 2) Fija tamaño por plantilla (si viene)
    if width_in and height_in:
        mpl.rcParams["figure.figsize"] = (width_in, height_in)