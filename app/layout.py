# app/layout.py
from __future__ import annotations
from pathlib import Path
from typing import Mapping, Any
import matplotlib.pyplot as plt

from .branding import add_branding
from .io_utils import save_fig_multi

def _get_layout(params: Mapping[str, Any]):
    """
    Obtiene los márgenes normalizados (0-1) desde layout o defaults.
    Retorna: (margin_left, margin_right, margin_top, margin_bottom)
    """
    L = params.get("layout", {}) or {}
    H = params.get("header", {}) or {}
    header_height = float(H.get("height", 0.30))  # Usar el mismo valor que el header
    
    return (
        float(L.get("margin_left", 0.22)),    # más espacio izq para labels Y
        float(L.get("margin_right", 0.12)),   # espacio para banderas/totales
        header_height,                        # Usar el mismo valor del header
        float(L.get("margin_bottom", 0.15)),  # 15% para footer
    )

def _draw_header(fig, params: Mapping[str, Any]) -> float:
    """
    Dibuja el header como una entidad aislada, alineado con el área del gráfico.
    """
    # Obtener configuración del header
    H = params.get("header", {}) or {}
    title_config = params.get("title", {}) or {}
    subtitle_config = params.get("subtitle", {}) or {}
    
    # Extraer texto y configuración
    title_text = title_config.get("text", "")
    subtitle_text = subtitle_config.get("text", "")
    title_size = H.get("title_size", 38)
    subtitle_size = H.get("subtitle_size", 28)
    title_weight = title_config.get("font", {}).get("weight", "bold")
    
    # Usar la altura del header desde la configuración
    header_height = float(H.get("height", 0.25))  # Reducido a 25%
    
    # Obtener márgenes para alinear con el gráfico
    ml = float(params.get("layout", {}).get("margin_left", 0.22))
    mr = float(params.get("layout", {}).get("margin_right", 0.12))
    
    # Crear un Axes específico para el header con posición ajustada
    header_ax = fig.add_axes([
        ml,                 # izquierda
        1.0 - header_height,# abajo
        1.0 - ml - mr,     # ancho
        header_height      # alto
    ])
    
    # Configurar el Axes del header
    header_ax.set_xticks([])
    header_ax.set_yticks([])
    for spine in header_ax.spines.values():
        spine.set_visible(False)
    
    # Función para wrapping de texto
    def wrap_text(text, fontsize):
        from textwrap import wrap
        width = 1.0 - ml - mr  # Ancho del área del gráfico
        chars = int(width * fig.get_figwidth() * 72 / (fontsize * 0.5))
        return '\n'.join(wrap(text, width=chars))

    # Dibujar título usando el Axes del header
    if title_text:
        wrapped_title = wrap_text(title_text, title_size)
        header_ax.text(0.5, 0.85,  # Ajustado a 85% desde abajo
                wrapped_title,
                ha='center',
                va='top',
                fontsize=title_size,
                fontweight=title_weight,
                fontfamily='Nunito',
                color='#333333',
                transform=header_ax.transAxes)

    # Dibujar subtítulo usando el Axes del header
    if subtitle_text:
        wrapped_subtitle = wrap_text(subtitle_text, subtitle_size)
        header_ax.text(0.5, 0.35,  # Ajustado a 35% desde abajo
                wrapped_subtitle,
                ha='center',
                va='top',
                fontsize=subtitle_size,
                fontfamily='Nunito',
                color='#666666',
                transform=header_ax.transAxes)

    return header_height

def apply_frame(fig, params: Mapping[str, Any]):
    """
    Aplica el layout general respetando las tres zonas.
    """
    # Configurar DPI
    dpi = float(params.get("dpi", 300))
    fig.set_dpi(dpi)
    
    # Obtenemos los márgenes y altura del header desde la configuración
    H = params.get("header", {}) or {}
    header_height = float(H.get("height", 0.25))  # Mantener consistente con _draw_header
    
    # Obtenemos los márgenes
    ml, mr, mt, mb = _get_layout(params)
    
    # Configurar los límites de la figura
    fig.set_size_inches(fig.get_figwidth(), fig.get_figheight())
    
    # Ajustar los márgenes
    fig.subplots_adjust(
        left=ml,
        right=1.0 - mr,
        top=0.95,          # Dar más espacio arriba
        bottom=0
    )
    
    # Definir zonas
    footer_height = 0.15
    body_height = 1.0 - header_height - footer_height
    
    # Posicionar el área del gráfico
    for ax in fig.axes:
        ax.set_position([
            ml,
            footer_height,
            1.0 - ml - mr,
            body_height
        ])
    
    # Dibujar el header cuando todo lo demás está configurado
    _draw_header(fig, params)
    
    # Actualización final
    fig.canvas.draw()


def finish_and_save(fig, params: Mapping[str, Any]):
    """Inserta branding estándar y guarda en todos los formatos."""
    # Obtener DPI y configuración de calidad
    dpi = float(params.get("dpi", 300))
    
    # Obtener configuración de branding
    branding_cfg = params.get("branding", {})
    
    # Configurar DPI solo para la figura
    fig.set_dpi(dpi)
    
    # Aplicar branding pasando el diccionario completo de parámetros
    add_branding(fig, branding_cfg)

    # Guardado multi-formato - solo pasar los parámetros que acepta
    out = Path(params.get("outfile", "out/figure"))
    save_fig_multi(
        fig, out,
        formats=params.get("formats", ["png", "svg", "pdf"]),
        jpg_quality=params.get("jpg_quality", 95),
        webp_quality=params.get("webp_quality", 95),
        avif_quality=params.get("avif_quality", 80),
        scour_svg=params.get("scour_svg", True)
    )
    
    # Asegurar que la memoria se libera correctamente
    fig.canvas.draw_idle()