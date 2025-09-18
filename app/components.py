"""
Componentes reutilizables para gráficos en la biblioteca Condatos.
Este módulo contiene funciones generalizadas que pueden ser utilizadas por diferentes tipos de gráficos
para implementar funcionalidades comunes como footers, títulos, elementos decorativos, etc.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import textwrap
from typing import Any, Dict, List, Optional, Union, Tuple

def add_footer(fig, params: Dict[str, Any]):
    """
    Añade un footer con logo y texto en la parte inferior del gráfico.
    Soporta múltiples opciones de personalización para posición, estilo y contenido.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        La figura donde se añadirá el footer
    params : dict
        Diccionario de parámetros con la configuración del footer
    
    Returns:
    --------
    None
    """
    footer = params.get("footer", {})
    if not footer:
        return
    
    # Configuración general del footer
    footer_config = footer.get("config", {})
    
    # Posición vertical para el footer (parte inferior de la figura)
    footer_y = float(footer_config.get("y_position", 0.03))
    
    # Marco opcional para el footer
    show_frame = bool(footer_config.get("show_frame", False))
    frame_padding = float(footer_config.get("frame_padding", 0.01))
    frame_alpha = float(footer_config.get("frame_alpha", 0.1))
    frame_color = footer_config.get("frame_color", "#cccccc")
    
    # Si se activa el marco, dibujarlo
    if show_frame:
        import matplotlib.patches as patches
        
        # Altura del marco del footer
        frame_height = 2 * (footer_y + frame_padding)
        
        # Crear un rectángulo para el marco
        rect = patches.Rectangle(
            (0, 0),                         # Esquina inferior izquierda
            1.0,                            # Ancho (toda la figura)
            frame_height,                   # Altura
            facecolor=frame_color,
            alpha=frame_alpha,
            transform=fig.transFigure,
            zorder=-1                       # Dibujar detrás de todo
        )
        fig.add_artist(rect)
        
        # Ajustar la posición vertical si hay marco
        footer_y = footer_y + frame_padding/2
    
    # Añadir texto de fuente si existe
    source_text = footer.get("source", "")
    if source_text:
        # Configuración de fuente
        source_config = footer.get("source_config", {})
        source_fontsize = float(source_config.get("fontsize", footer.get("source_fontsize", 9)))
        source_color = source_config.get("color", footer.get("source_color", "#666666"))
        source_style = source_config.get("style", "italic")
        source_weight = source_config.get("weight", "normal")
        source_family = source_config.get("family", "Nunito")
    source_x = float(source_config.get("x_position", 0.0))  # Usar x_position si está definido
    source_y = float(source_config.get("y_position", footer_y))
    source_align = source_config.get("alignment", "left")  # Usar alignment si está definido
    max_width = float(source_config.get("width", 1.0))  # Usar width si está definido

    # --- Wrapping automático considerando margen izquierdo y ancho disponible ---
    fig_width = fig.get_figwidth()  # en pulgadas
    chars_per_inch = 13
    # El ancho real disponible es desde x_position hasta x_position+width, pero matplotlib.text usa x como fracción de figura
    # Por lo tanto, el ancho disponible es (1.0 - source_x) si width excede el borde, o simplemente width si cabe
    available_width = min(max_width, 1.0 - source_x)
    max_chars = int(fig_width * available_width * chars_per_inch)
    import textwrap
    wrapped_text = textwrap.fill(source_text, width=max_chars)

    print("ℹ️ Configurando texto de fuente en footer:")
    print(f"  - Texto: '{source_text}'")
    print(f"  - Posición: x={source_x}, y={source_y}")
    print(f"  - Tamaño de fuente: {source_fontsize}")
    print(f"  - Wrapping: {max_chars} caracteres por línea (ancho disponible: {available_width})")
    print(f"  - Alineación: {source_align}")

    fig.text(
        source_x,
        source_y,
        wrapped_text,
        ha=source_align,
        va='center',
        fontsize=float(source_fontsize),
        color=source_color,
        style=source_style,
        weight=source_weight,
        family=source_family
    )
    
    # Añadir texto adicional/nota si existe
    note_text = footer.get("note", "")
    if note_text:
        # Configuración de nota
        note_config = footer.get("note_config", {})
        note_fontsize = float(note_config.get("fontsize", footer.get("note_fontsize", 9)))
        note_color = note_config.get("color", footer.get("note_color", "#666666"))
        note_style = note_config.get("style", "normal")
        note_weight = note_config.get("weight", "normal")
        note_family = note_config.get("family", "Nunito")
        note_x = float(note_config.get("x_position", 0.5))
        note_y = float(note_config.get("y_position", footer_y))
        note_align = note_config.get("alignment", "center")
        
        print("ℹ️ Configurando texto de nota en footer:")
        print(f"  - Texto: '{note_text}'")
        print(f"  - Posición: x={note_x}, y={note_y}")
        print(f"  - Tamaño de fuente: {note_fontsize}")
        
        fig.text(
            note_x,       # Posición horizontal personalizable
            note_y,       # Posición vertical personalizada
            note_text,
            ha=note_align,
            va='center',
            fontsize=float(note_fontsize),  # Asegurarse que es float
            color=note_color,
            style=note_style,
            weight=note_weight,
            family=note_family
        )
    
    # Añadir uno o más logos si se especifican
    logos = footer.get("logos", [])
    # Compatibilidad con versión antigua que usa solo un logo
    if not logos and "logo" in footer:
        logos = [{"path": footer.get("logo", ""), "zoom": footer.get("logo_zoom", 0.15), "x_position": 0.85}]
    
    # Procesar cada logo configurado
    for logo_config in logos:
        logo_path = logo_config.get("path", "")
        if logo_path and Path(logo_path).exists():
            try:
                from matplotlib.image import imread
                
                # Cargar la imagen del logo
                logo_img = imread(logo_path)
                
                # Opciones para controlar el tamaño del logo
                size_method = logo_config.get("size_method", "zoom")
                
                # Método 1: Factor de zoom simple (método original)
                logo_zoom = float(logo_config.get("zoom", 0.15))
                
                # Método 2: Tamaño absoluto en pulgadas
                logo_width_inches = float(logo_config.get("width_inches", 0))
                logo_height_inches = float(logo_config.get("height_inches", 0))
                
                # Método 3: Tamaño relativo a la figura (fracción)
                logo_width_fraction = float(logo_config.get("width_fraction", 0))
                logo_height_fraction = float(logo_config.get("height_fraction", 0))
                
                # Método 4: Tamaño en píxeles
                logo_width_pixels = float(logo_config.get("width_pixels", 0))
                logo_height_pixels = float(logo_config.get("height_pixels", 0))
                
                # Determinar el factor de zoom basado en el método seleccionado
                if size_method == "absolute_inches" and (logo_width_inches > 0 or logo_height_inches > 0):
                    # Convertir tamaño absoluto en pulgadas a un factor de zoom
                    img_height, img_width = logo_img.shape[:2] if len(logo_img.shape) > 2 else logo_img.shape
                    fig_width_inches, fig_height_inches = fig.get_size_inches()
                    
                    # Si solo se especifica una dimensión, mantener la proporción
                    if logo_width_inches > 0 and logo_height_inches == 0:
                        logo_zoom = (logo_width_inches / fig_width_inches) * (fig_width_inches / (img_width / fig.dpi))
                    elif logo_height_inches > 0 and logo_width_inches == 0:
                        logo_zoom = (logo_height_inches / fig_height_inches) * (fig_height_inches / (img_height / fig.dpi))
                    else:
                        # Si ambos están especificados, usar el menor factor para evitar distorsión
                        zoom_width = (logo_width_inches / fig_width_inches) * (fig_width_inches / (img_width / fig.dpi))
                        zoom_height = (logo_height_inches / fig_height_inches) * (fig_height_inches / (img_height / fig.dpi))
                        logo_zoom = min(zoom_width, zoom_height)
                
                elif size_method == "fraction" and (logo_width_fraction > 0 or logo_height_fraction > 0):
                    # Convertir fracción de figura a factor de zoom
                    img_height, img_width = logo_img.shape[:2] if len(logo_img.shape) > 2 else logo_img.shape
                    fig_width_inches, fig_height_inches = fig.get_size_inches()
                    
                    if logo_width_fraction > 0 and logo_height_fraction == 0:
                        logo_zoom = logo_width_fraction * (fig_width_inches / (img_width / fig.dpi))
                    elif logo_height_fraction > 0 and logo_width_fraction == 0:
                        logo_zoom = logo_height_fraction * (fig_height_inches / (img_height / fig.dpi))
                    else:
                        zoom_width = logo_width_fraction * (fig_width_inches / (img_width / fig.dpi))
                        zoom_height = logo_height_fraction * (fig_height_inches / (img_height / fig.dpi))
                        logo_zoom = min(zoom_width, zoom_height)
                        
                elif size_method == "pixels" and (logo_width_pixels > 0 or logo_height_pixels > 0):
                    # Convertir tamaño en píxeles a factor de zoom
                    img_height, img_width = logo_img.shape[:2] if len(logo_img.shape) > 2 else logo_img.shape
                    
                    if logo_width_pixels > 0 and logo_height_pixels == 0:
                        logo_zoom = logo_width_pixels / img_width
                    elif logo_height_pixels > 0 and logo_width_pixels == 0:
                        logo_zoom = logo_height_pixels / img_height
                    else:
                        zoom_width = logo_width_pixels / img_width
                        zoom_height = logo_height_pixels / img_height
                        logo_zoom = min(zoom_width, zoom_height)
                
                # Posición horizontal
                logo_x = float(logo_config.get("x_position", 0.85))
                
                # Alineación del logo
                logo_align = logo_config.get("alignment", (1.0, 0.5))  # Por defecto alineado a la derecha
                
                if isinstance(logo_align, str):
                    # Convertir string a tuple si se proporciona como texto
                    if logo_align == "right":
                        logo_align = (1.0, 0.5)
                    elif logo_align == "left":
                        logo_align = (0.0, 0.5)
                    elif logo_align == "center":
                        logo_align = (0.5, 0.5)
                
                # Posición vertical personalizada del logo
                logo_y = float(logo_config.get("y_position", footer_y))
                
                print("ℹ️ Añadiendo logo en footer:")
                print(f"  - Archivo: '{logo_path}'")
                print(f"  - Método de tamaño: '{size_method}'")
                print(f"  - Factor de zoom calculado: {logo_zoom:.4f}")
                print(f"  - Posición: x={logo_x}, y={logo_y}")
                
                # Crear un OffsetImage con la imagen del logo
                imagebox = OffsetImage(logo_img, zoom=logo_zoom)
                
                # Posicionar el logo según la configuración
                ab = AnnotationBbox(
                    imagebox, 
                    (logo_x, logo_y),    # Posición personalizable
                    xycoords='figure fraction',
                    box_alignment=logo_align,
                    frameon=False
                )
                
                # Añadir el logo a la figura
                fig.add_artist(ab)
            except Exception as e:
                print(f"⚠️ Error al cargar el logo {logo_path}: {e}")


def add_decorative_elements(fig, params: Dict[str, Any]):
    """
    Añade elementos decorativos al gráfico basados en la configuración.
    Soporta rectángulos, líneas y otros elementos visuales para estilo personalizado.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        La figura donde se añadirán los elementos decorativos
    params : dict
        Diccionario de parámetros con la configuración de elementos decorativos
        
    Returns:
    --------
    None
    """
    # Verificar si hay configuración de elementos decorativos
    decorative_elements = params.get("decorative_elements", [])
    
    if not decorative_elements:
        print("ℹ️ No hay elementos decorativos configurados.")
        return
        
    print(f"🎨 Añadiendo {len(decorative_elements)} elementos decorativos...")
    
    for i, element in enumerate(decorative_elements):
        element_type = element.get("type", "").lower()
        
        try:
            # Elemento tipo rectángulo (como la barra vertical roja de Statista)
            if element_type == "rectangle":
                # Coordenadas y dimensiones (en fracción de figura)
                x = float(element.get("x", 0))
                y = float(element.get("y", 0))
                width = float(element.get("width", 0.01))
                height = float(element.get("height", 0.5))
                color = element.get("color", "#ff3b30")  # Color rojo por defecto
                alpha = float(element.get("alpha", 1.0))
                zorder = int(element.get("zorder", 10))  # Orden de capa (sobre/bajo otros elementos)
                
                # Crear un Rectangle patch
                from matplotlib.patches import Rectangle
                rect = Rectangle(
                    (x, y),                     # Posición (x, y) en fracción de figura
                    width, height,              # Ancho y alto en fracción de figura
                    facecolor=color,
                    edgecolor='none',           # Sin borde
                    alpha=alpha,
                    transform=fig.transFigure,  # Usar coordenadas de figura
                    zorder=zorder
                )
                
                # Añadir el rectángulo a la figura
                fig.add_artist(rect)
                print(f"  ✓ Añadido rectángulo decorativo en ({x:.2f}, {y:.2f}) con color {color}")
                
            # Elemento tipo línea (para separadores u otros elementos)
            elif element_type == "line":
                # Coordenadas de inicio y fin (en fracción de figura)
                x1 = float(element.get("x1", 0))
                y1 = float(element.get("y1", 0))
                x2 = float(element.get("x2", 1))
                y2 = float(element.get("y2", 0))
                linewidth = float(element.get("linewidth", 1.0))
                color = element.get("color", "#333333")
                alpha = float(element.get("alpha", 1.0))
                zorder = int(element.get("zorder", 10))
                linestyle = element.get("linestyle", "-")
                
                # Crear una Line2D
                from matplotlib.lines import Line2D
                line = Line2D(
                    [x1, x2], [y1, y2],         # Puntos de inicio y fin
                    linewidth=linewidth,
                    color=color,
                    alpha=alpha,
                    zorder=zorder,
                    linestyle=linestyle,
                    transform=fig.transFigure
                )
                
                # Añadir la línea a la figura
                fig.add_artist(line)
                print(f"  ✓ Añadida línea decorativa de ({x1:.2f}, {y1:.2f}) a ({x2:.2f}, {y2:.2f})")
                
            # Texto decorativo (para etiquetas, notas o watermarks)
            elif element_type == "text":
                # Posición y contenido
                x = float(element.get("x", 0.5))
                y = float(element.get("y", 0.5))
                text = element.get("text", "")
                fontsize = float(element.get("fontsize", 12))
                fontweight = element.get("fontweight", "normal")
                color = element.get("color", "#333333")
                alpha = float(element.get("alpha", 1.0))
                ha = element.get("ha", "center")
                va = element.get("va", "center")
                rotation = float(element.get("rotation", 0))
                zorder = int(element.get("zorder", 10))
                
                # Añadir el texto a la figura
                fig.text(
                    x, y, text,
                    fontsize=fontsize,
                    fontweight=fontweight,
                    color=color,
                    alpha=alpha,
                    ha=ha, va=va,
                    rotation=rotation,
                    zorder=zorder
                )
                print(f"  ✓ Añadido texto decorativo '{text}' en ({x:.2f}, {y:.2f})")
                
            else:
                print(f"  ⚠️ Tipo de elemento decorativo no soportado: '{element_type}'")
        
        except Exception as e:
            print(f"  ⚠️ Error al añadir elemento decorativo #{i+1}: {e}")


def custom_save(fig, params: Dict[str, Any]):
    """
    Guarda la figura en múltiples formatos sin aplicar el sistema estándar de branding.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        La figura a guardar
    params : dict
        Diccionario de parámetros con la configuración de guardado
        
    Returns:
    --------
    None
    """
    # Configurar DPI
    dpi = float(params.get("dpi", 300))
    fig.set_dpi(dpi)
    
    # Guardar directamente sin aplicar branding estándar
    from app.io_utils import save_fig_multi
    out = Path(params.get("outfile", "out/figure"))
    formats = params.get("formats", ["png", "svg", "pdf"])
    print(f"[DEBUG] Custom save without branding: formats: {formats}")
    save_fig_multi(
        fig,
        out,
        formats=formats,
        jpg_quality=params.get("jpg_quality", 95),
        webp_quality=params.get("webp_quality", 95), 
        avif_quality=params.get("avif_quality", 80),
        scour_svg=params.get("scour_svg", True)
    )


def finalize(fig, params: Dict[str, Any]):
    """
    Finaliza y guarda el gráfico, con opción de usar o no el branding estándar.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        La figura a finalizar y guardar
    params : dict
        Diccionario de parámetros con la configuración
        
    Returns:
    --------
    None
    """
    # Añadir elementos decorativos antes de guardar
    add_decorative_elements(fig, params)
    
    # Debug the formats configuration
    print(f"[DEBUG] Finalize: params formats: {params.get('formats', 'Not found')}")
    
    # Verificar si debemos usar el sistema de branding estándar
    footer_config = params.get("footer", {}).get("config", {})
    use_default_branding = footer_config.get("use_default_branding", True)
    
    if use_default_branding:
        # Usar la función centralizada para finalizar y guardar el gráfico
        from app.layout import finish_and_save
        finish_and_save(fig, params)
    else:
        # Implementar nuestra propia versión sin llamar a add_branding
        custom_save(fig, params)
    
    plt.close(fig)