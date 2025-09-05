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
    # Procesamiento de título y subtítulo
    title = params.get("title", {})
    subtitle = params.get("subtitle", {})

    # Extraer el texto correctamente del diccionario
    title_text = title.get("text", "") if isinstance(title, dict) else str(title)
    subtitle_text = subtitle.get("text", "") if isinstance(subtitle, dict) else str(subtitle)

    if not (title_text or subtitle_text):
        return 0.0

    # Configuración
    H = params.get("header", {}) or {}
    title_size = float(H.get("title_size", 40))
    title_weight = H.get("title_weight", "bold")
    subtitle_size = float(H.get("subtitle_size", 28))

    # Usar la altura del header desde la configuración
    header_height = float(H.get("height", 0.30))  # Usar el valor del YAML
    header_top = 1.0
    header_bottom = header_top - header_height
    
     # SIMPLIFICADO: Usar valores absolutos directamente
    title_y = 0.85     # Posición absoluta del título
    subtitle_y = 0.75  # Posición absoluta del subtítulo

    # Obtener márgenes para alinear con el gráfico
    ml, mr, mt, mb = _get_layout(params)
    
    # Calcular el centro del área del gráfico
    x_center = ml + (1.0 - ml - mr) / 2

    # DEBUG: Imprimir valores justo antes de dibujar
    print(f"DEBUG: Header height: {header_height:.2f}")
    print(f"DEBUG: Header zone: {header_bottom:.2f} to {header_top:.2f}")
    print(f"DEBUG: Title y: {title_y:.2f}, Subtitle y: {subtitle_y:.2f}")


    # Función para wrapping de texto
    def wrap_text(text, fontsize):
        from textwrap import wrap
        width = 1.0 - ml - mr  # Ancho del área del gráfico
        chars = int(width * fig.get_figwidth() * 72 / (fontsize * 0.5))
        return '\n'.join(wrap(text, width=chars))

    # Dibujar título con wrapping
    if title_text:
        wrapped_title = wrap_text(title_text, title_size)
        fig.text(x_center, title_y,
                wrapped_title,
                ha='center',
                va='top',
                fontsize=title_size,
                fontweight=title_weight,
                fontfamily='Nunito',
                color='#333333')

    # Dibujar subtítulo con wrapping
    if subtitle_text:
        wrapped_subtitle = wrap_text(subtitle_text, subtitle_size)
        fig.text(x_center, subtitle_y,
                wrapped_subtitle,
                ha='center',
                va='top',
                fontsize=subtitle_size,
                fontfamily='Nunito',
                color='#666666')

    return mt

def apply_frame(fig, params: Mapping[str, Any]):
    """
    Aplica el layout general respetando las tres zonas:
    - Header: 25% superior
    - Body: 60% central
    - Footer: 15% inferior
    """
    # Configurar DPI
    dpi = float(params.get("dpi", 300))
    fig.set_dpi(dpi)
    
     # Obtenemos los márgenes y altura del header desde la configuración
    H = params.get("header", {}) or {}
    header_height = float(H.get("height", 0.30))  # Usar el valor del YAML

    
    # Obtenemos los márgenes
    ml, mr, mt, mb = _get_layout(params)
    
   # ACTUALIZADO: Definimos las zonas usando el header_height del YAML
    footer_height = 0.15  # 15% para footer
    body_height = 1.0 - header_height - footer_height  # Resto para el gráfico
    
    # Calculamos las posiciones verticales
    header_top = 1.0
    header_bottom = header_top - header_height
    body_top = header_bottom
    body_bottom = footer_height
    
    # Primero ajustamos los márgenes generales
    fig.subplots_adjust(
        left=ml,
        right=1.0 - mr,
        top=header_top,     # NUEVO: Usamos toda la altura
        bottom=0            # NUEVO: Desde el fondo
    )
    
    # Ajustamos el área del gráfico a su zona específica
    for ax in fig.axes:
        ax.set_position([
            ml,              # izquierda
            body_bottom,     # NUEVO: comienza sobre el footer
            1.0 - ml - mr,  # ancho
            body_height     # NUEVO: altura calculada
        ])
    
    # Dibujamos el header en su zona
    _draw_header(fig, params)
    
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