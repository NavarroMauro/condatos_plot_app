# app/layout.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .branding import add_branding
from .io_utils import save_fig_multi


def _draw_header(fig, params: Mapping[str, Any]) -> None:
    """Dibuja el header como una entidad aislada."""
    # Obtener configuración
    title_config = params.get("title", {}) or {}
    subtitle_config = params.get("subtitle", {}) or {}
    layout = params.get("layout", {})

    # Extraer texto y configuración
    title_text = title_config.get("text", "")
    subtitle_text = subtitle_config.get("text", "")
    title_size = params.get("header", {}).get("title_size", 28)
    subtitle_size = params.get("header", {}).get("subtitle_size", 22)

    # Obtener márgenes
    margin_left = float(layout.get("margin_left", 0.30))
    margin_right = float(layout.get("margin_right", 0.15))
    header_height = float(layout.get("header_height", 0.15))

    # Crear axes para el header
    header_ax = fig.add_axes([
        margin_left,
        1.0 - header_height,
        1.0 - margin_left - margin_right,
        header_height
    ])

    # Configurar el axes
    header_ax.set_xticks([])
    header_ax.set_yticks([])
    for spine in header_ax.spines.values():
        spine.set_visible(False)

    # Función para wrapping de texto
    def wrap_text(text, fontsize):
        from textwrap import wrap
        width = 1.0 - margin_left - margin_right
        chars = int(width * fig.get_figwidth() * 72 / (fontsize * 0.5))
        return "\n".join(wrap(text, width=chars))

    # Posiciones relativas dentro del header
    title_y = 0.9    # 90% desde abajo
    subtitle_y = 0.4  # 40% desde abajo

    # Dibujar título
    if title_text:
        wrapped_title = wrap_text(title_text, title_size)
        header_ax.text(
            0.5, title_y, wrapped_title,
            ha="center", va="top",
            fontsize=title_size,
            fontweight="bold",
            fontfamily="Nunito",
            color="#333333",
            transform=header_ax.transAxes,
        )

    # Dibujar subtítulo
    if subtitle_text:
        wrapped_subtitle = wrap_text(subtitle_text, subtitle_size)
        header_ax.text(
            0.5, subtitle_y, wrapped_subtitle,
            ha="center", va="top",
            fontsize=subtitle_size,
            fontfamily="Nunito",
            color="#666666",
            transform=header_ax.transAxes,
        )


def apply_frame(fig, params: Mapping[str, Any]):
    """Aplica el layout general con posicionamiento absoluto."""
    main_ax = fig.gca()
    
    # Obtener configuración de layout
    layout = params.get("layout", {})
    
    # Definir proporciones
    header_height = float(layout.get("header_height", 0.15))
    footer_height = float(layout.get("footer_height", 0.10))
    content_height = 1.0 - header_height - footer_height
    
    # Obtener márgenes horizontales
    margin_left = float(layout.get("margin_left", 0.30))
    margin_right = float(layout.get("margin_right", 0.15))
    content_width = 1.0 - margin_left - margin_right
    
    # Dibujar header
    _draw_header(fig, params)
    
    # Posicionar contenido principal
    main_ax.set_position([
        margin_left,
        footer_height,
        content_width,
        content_height
    ])
    
    # Actualizar configuración de branding
    branding_cfg = params.get("branding", {})
    branding_cfg.update({
        "height": footer_height,
        "margin_left": margin_left,
        "margin_right": margin_right
    })
    params["branding"] = branding_cfg
    
    # Mantener límites y estado
    xlim, ylim = main_ax.get_xlim(), main_ax.get_ylim()
    visible = main_ax.get_visible()
    main_ax.set_xlim(xlim)
    main_ax.set_ylim(ylim)
    main_ax.set_visible(visible)
    main_ax.set_autoscalex_on(False)
    main_ax.set_autoscaley_on(False)
    
    fig.canvas.draw()


def finish_and_save(fig, params: Mapping[str, Any]):
    """Inserta branding estándar y guarda en todos los formatos."""
    dpi = float(params.get("dpi", 300))
    fig.set_dpi(dpi)

    branding_cfg = params.get("branding", {})
    add_branding(fig, branding_cfg)

    out = Path(params.get("outfile", "out/figure"))
    save_fig_multi(
        fig,
        out,
        formats=params.get("formats", ["png", "svg", "pdf"]),
        jpg_quality=params.get("jpg_quality", 95),
        webp_quality=params.get("webp_quality", 95), 
        avif_quality=params.get("avif_quality", 80),
        scour_svg=params.get("scour_svg", True)
    )

    fig.canvas.draw_idle()