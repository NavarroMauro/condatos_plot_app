from __future__ import annotations
from pathlib import Path
from datetime import date
from typing import Mapping, Any
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def add_branding(fig, params: Mapping[str, Any] | None = None):
    """
    Pie de marca con iconos CC centrados y texto debajo:
      • Centro: Iconos CC + texto fuente/nota
      • Derecha (opcional): Logo
    Control por YAML en la clave `branding`.
    """
    if not params:
        return
    b = dict(params)  # copia segura

    # Obtener márgenes del layout
    layout = params.get("layout", {})
    margins = layout.get("margins", {})
    margin_left = float(margins.get("left", 0.20))
    margin_right = float(margins.get("right", 0.12))
    margin_bottom = float(margins.get("bottom", 0.20))

    # --------- Parámetros ----------
    # Texto y separadores
    source = b.get("source", "")
    note = b.get("note", "")
    date_auto = bool(b.get("date_auto", True))
    date_fmt = b.get("date_format", "%Y-%m-%d")
    separator = b.get("text_separator", " · ")

    # Línea separadora
    sep = bool(b.get("separator", False))
    sep_color = b.get("separator_color", "0.85")
    sep_alpha = float(b.get("separator_alpha", 1.0))
    sep_width = float(b.get("separator_width", 0.6))
    sep_y = margin_bottom * float(b.get("separator_y", 0.75))
    pad = float(b.get("pad", 0.035))

    # Estética
    fontsize = float(b.get("fontsize", 12))
    color = b.get("color", "0.25")
    alpha = float(b.get("alpha", 0.95))
    font_family = b.get("font_family", "DejaVu Sans")
    font_weight = b.get("font_weight", "normal")

    # Posiciones Y (adjust these to be relative to margin_bottom)
    text_y = margin_bottom * float(b.get("text_y", 0.25))
    icons_y = margin_bottom * float(b.get("icons_y", 0.60))
    logo_y = margin_bottom * float(b.get("logo_y", 0.60))

    # --------- Setup de footer ---------
    import matplotlib.pyplot as plt
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox

    ax_footer = fig.add_axes([0.00, 0.00, 1.00, 0.0001], frameon=False)
    ax_footer.set_axis_off()

    # Línea separadora
    if sep:
        fig.lines.append(
            plt.Line2D(
                [margin_left, 1.0 - margin_right],
                [pad * sep_y, pad * sep_y],
                transform=fig.transFigure,
                linewidth=sep_width,
                color=sep_color,
                alpha=sep_alpha,
                zorder=10
            )
        )

    # --------- Preparar texto ---------
    bits = []
    if source: bits.append(f"Fuente: {source}")
    if note: bits.append(note)
    if date_auto: bits.append(date.today().strftime(date_fmt))
    footer_text = separator.join(bits)

    # --------- Calcular dimensiones totales ---------
    logo_width = float(b.get("logo_width", 0.06))
    logo_path = Path(b.get("logo", "")).expanduser()
    logo_alpha = float(b.get("logo_alpha", 0.95))
    
    icons = [Path(p).expanduser() for p in b.get("icons", [])]
    icons_zoom = float(b.get("icons_zoom", 0.020))
    icons_gap = float(b.get("icons_gap", 0.055))
    icons_alpha = float(b.get("icons_alpha", 0.95))
    
    # Calcular ancho total del conjunto
    icons_width = 0
    if icons:
        # Ancho de cada ícono
        icon_width = icons_zoom * fig.get_figwidth() * fig.get_dpi() / fig.get_dpi()
        # Ancho total = (ancho de cada ícono * número de íconos) + (espacio entre íconos * (número de íconos - 1))
        icons_width = (icon_width * len(icons)) + (icons_gap * (len(icons) - 1))
    
    # Ancho total del grupo incluyendo logo y espacio entre logo e iconos
    total_group_width = icons_width + logo_width + icons_gap  # icons_gap como espacio entre iconos y logo
    
    # Centro de la figura
    center_x = 0.5
    
    # Posición inicial para los iconos (centrado del grupo completo)
    start_x = center_x - (total_group_width / 2)
    
    # --------- Dibujar iconos CC ---------
    if icons:
        for i, icon in enumerate(icons):
            if not icon.exists():
                continue
            try:
                im = plt.imread(str(icon))
                x_pos = start_x + (i * icons_gap)
                
                ab = AnnotationBbox(
                    OffsetImage(im, zoom=icons_zoom, alpha=icons_alpha),
                    (x_pos, icons_y),
                    xycoords="figure fraction",
                    frameon=False,
                    box_alignment=(0.5, 0.5),
                    pad=0.0
                )
                ab.set_zorder(11)
                ab.set_clip_on(False)
                fig.add_artist(ab)
            except Exception:
                continue
    
    # --------- Logo ---------
    if logo_path.exists():
        try:
            im = plt.imread(str(logo_path))
            fig_w_in = fig.get_figwidth()
            dpi = fig.get_dpi()
            target_px = max(1.0, logo_width * fig_w_in * dpi)
            zoom = max(0.01, target_px / im.shape[1])

            # Posicionar logo después de los iconos
            x_logo = start_x + icons_width + icons_gap
            
            ab = AnnotationBbox(
                OffsetImage(im, zoom=zoom, alpha=logo_alpha),
                (x_logo, logo_y),
                xycoords="figure fraction",
                frameon=False,
                box_alignment=(0, 0.5),  # Alinear a la izquierda
                pad=0.0
            )
            ab.set_zorder(11)
            ab.set_clip_on(False)
            fig.add_artist(ab)
        except Exception:
            pass

    # --------- Texto centrado ---------
    if footer_text:
        fig.text(
            center_x,  # Usar el centro exacto de la figura
            text_y,
            footer_text,
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color=color,
            alpha=alpha,
            family=font_family,
            weight=font_weight
        )