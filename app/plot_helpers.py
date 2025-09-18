# app/plot_helpers.py
from __future__ import annotations
from typing import Mapping, Any
from pathlib import Path
import hashlib, io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.axes import Axes
from PIL import Image
from .branding import add_branding
from .io_utils import save_fig_multi
from matplotlib.legend_handler import HandlerBase
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

# =============================
# IO / utilidades de imágenes
# =============================

def load_image_cached(path_or_url: str, cache_dir: str | None = None):
    """
    Lee imagen local o desde URL (con caché opcional) y devuelve un np.array RGBA.
    """
    if not path_or_url:
        return None

    is_url = path_or_url.startswith("http://") or path_or_url.startswith("https://")
    if not is_url:
        p = Path(path_or_url)
        if p.exists():
            try:
                return mpimg.imread(str(p))
            except Exception:
                return None
        return None

    local = None
    if cache_dir:
        cache = Path(cache_dir); cache.mkdir(parents=True, exist_ok=True)
        h = hashlib.sha1(path_or_url.encode("utf-8")).hexdigest()[:16]
        ext = ".png" if path_or_url.lower().endswith(".png") else ".jpg"
        local = cache / f"{h}{ext}"
        if local.exists():
            try:
                return mpimg.imread(str(local))
            except Exception:
                # si falla, intentamos redescargar abajo
                pass

    try:
        import requests
        r = requests.get(path_or_url, timeout=10); r.raise_for_status()
        if local is not None:
            local.write_bytes(r.content)
            try:
                return mpimg.imread(str(local))
            except Exception:
                return None
        im = Image.open(io.BytesIO(r.content)).convert("RGBA")
        return np.array(im)
    except Exception:
        return None


def _resolve_repo_abs(path_or_url: str) -> str:
    """
    Si el path comienza con '/', lo vuelve absoluto relativo al repo actual (cwd).
    """
    if path_or_url and path_or_url.startswith("/"):
        return str((Path.cwd() / path_or_url.lstrip("/")).resolve())
    return path_or_url


def _flags_iter(df, cat_col: str, flag_col: str, pattern: str | None):
    """
    Genera pares (categoria:str, ruta_flag:str|None) siguiendo el orden de df.
    Si no hay valor en flag_col y hay pattern, usa pattern con el campo 'code'.
    """
    for _, row in df.iterrows():
        p = str(row.get(flag_col, "")).strip()
        if not p and pattern:
            code = str(row.get("code", "")).strip()
            p = pattern.format(code=code, CODE=code.upper())
        yield str(row[cat_col]), (p or None)


# =============================
# Utilidades de layout/figura
# =============================

# --- Autosize de figura -------------------------------------------------------
# app/plot_helpers.py

def autosize_figure(fig, params: dict, *, n_rows: int) -> None:
    """
    Ajusta el tamaño de la figura manteniendo alturas fijas para header/footer.
    """
    a = params.get("autosize", {})
    if not a or not a.get("enabled", False):
        return

    # Configuración de anchura
    width_in = float(a.get("width_in", 12.0))
    
    # Alturas fijas para header y footer (en pulgadas)
    header_height_in = float(a.get("header_height_in", 1.5))
    footer_height_in = float(a.get("footer_height_in", 1.0))
    
    # Altura para el contenido principal (body)
    h_per_row = float(a.get("height_per_row", 0.25))  # Reducido de 0.3 a 0.25
    body_height_in = h_per_row * n_rows
    
    # 4. Establecer límites para el body solamente
    min_body_height = float(a.get("min_body_height", 6.0))
    max_body_height = float(a.get("max_body_height", 12.0))
    body_height_in = max(min_body_height, min(max_body_height, body_height_in))
    
    # 5. Calcular altura total de la figura
    height_in = header_height_in + body_height_in + footer_height_in
    
    # 6. Actualizar parámetros
    params["width_in"] = width_in
    params["height_in"] = height_in
    
    # 7. Calcular proporciones para el layout
    total_height = height_in
    params["layout"] = params.get("layout", {})
    params["layout"]["margin_top"] = header_height_in / total_height
    params["layout"]["margin_bottom"] = footer_height_in / total_height
    
    # 8. Si hay una figura, actualizar sus dimensiones
    if fig is not None:
        fig.set_size_inches(width_in, height_in, forward=True)
        
    # Ajusta los márgenes para dar espacio a los títulos
    try:
        if params.get("title") or params.get("subtitle"):
            title_margin = float(a.get("title_margin", 0.15))  # 15% del espacio para títulos
            fig.subplots_adjust(top=1.0 - title_margin)
    except Exception:
        pass




def autosize_for_rows(params: dict, n_rows: int):
    """
    Calcula (width_in, height_in) automáticamente en función de la cantidad de filas.
    Respeta límites min/max. Devuelve None si autosize no está habilitado.
    """
    a = (params or {}).get("autosize", {})
    if not a or not a.get("enabled"):
        return None
    mode = str(a.get("mode", "rows")).lower()
    if mode != "rows":
        return None
    width_in = float(a.get("width_in", params.get("width_in", 10)))
    hpr = float(a.get("height_per_row", 0.28))
    hmin = float(a.get("min_height", 6))
    hmax = float(a.get("max_height", 18))
    height_in = max(hmin, min(hmax, n_rows * hpr))
    return (width_in, height_in)


def draw_broken_axis_marks(ax: plt.Axes, x: float, y: float, width: float = 0.03, height: float = 0.015, angle: float = 45, color: str = "#333333") -> None:
    """
    Dibuja marcas de eje roto en una posición específica.
    
    Parameters
    ----------
    ax : plt.Axes
        El eje donde dibujar las marcas
    x : float
        Posición x del centro de las marcas
    y : float
        Posición y del centro de las marcas
    width : float, optional
        Ancho de las marcas en unidades de datos (default: 0.03)
    height : float, optional
        Alto de las marcas en unidades de datos (default: 0.015)
    angle : float, optional
        Ángulo de inclinación de las marcas en grados (default: 45)
    color : str, optional
        Color de las marcas (default: "#333333")
    """
    from matplotlib.patches import Rectangle
    from matplotlib.transforms import Affine2D
    import numpy as np
    
    # Crear dos rectángulos para las marcas
    rect1 = Rectangle((x - width/2, y - height/2), width, height, 
                     facecolor=color, edgecolor="none")
    rect2 = Rectangle((x - width/2, y + height/2), width, height, 
                     facecolor=color, edgecolor="none")
    
    # Rotar los rectángulos
    angle_rad = np.radians(angle)
    t = Affine2D().rotate_around(x, y, angle_rad)
    rect1.set_transform(t + ax.transData)
    rect2.set_transform(t + ax.transData)
    
    # Añadir al eje
    ax.add_patch(rect1)
    ax.add_patch(rect2)

# =============================
# Etiquetas (segmentos y totales)
# =============================

def draw_segment_labels_stacked(
    ax, M: np.ndarray, orientation: str, *, show: bool, percent: bool,
    min_label_height: float, fmt: str, params: dict
):
    """
    Dibuja etiquetas centradas dentro de cada segmento apilado si superan umbral.
    - orientation: "v" (vertical) o "h" (horizontal)
    - M: array shape (S,N) con los valores por serie
    - percent True: usa % relativo al total de la barra
    - params: diccionario con configuración de estilo
    """
    if not show:
        return
    if not isinstance(M, np.ndarray) or M.size == 0:
        return

    # Obtener configuración de fuente
    value_labels_cfg = params.get("value_labels", {})
    if isinstance(value_labels_cfg, bool):
        value_labels_cfg = {}
    
    font_cfg = value_labels_cfg.get("font", {})
    font_size = float(font_cfg.get("size", 8))
    font_family = font_cfg.get("family", None)  # None usa el default de matplotlib
    font_weight = font_cfg.get("weight", "normal")
    font_color = font_cfg.get("color", "#333333")
    font_alpha = float(font_cfg.get("alpha", 1.0))

    S, N = M.shape
    cum = np.cumsum(M, axis=0)  # (S,N) topes por serie

    for s in range(S):
        for n in range(N):
            val = float(M[s, n])
            if val <= 0:
                continue

            # Umbral
            if percent:
                total = float(cum[-1, n]) if cum[-1, n] else 1.0
                share = 100.0 * val / total
                if share < min_label_height:
                    continue
                label_val = share
            else:
                if val < min_label_height:
                    continue
                label_val = val

            # Centro del segmento
            if orientation == "v":
                y0 = cum[s, n] - val
                xc, yc = n, (y0 + val / 2.0)
            else:
                x0 = cum[s, n] - val
                xc, yc = (x0 + val / 2.0), n

            ax.text(
                xc, yc, fmt.format(label_val),
                ha="center", va="center",
                fontsize=font_size,
                fontfamily=font_family,
                fontweight=font_weight,
                color=font_color,
                alpha=font_alpha
            )


def draw_total_labels(
    ax, totals: np.ndarray | list[float], positions, orientation: str, *,
    show: bool, fmt: str, dy_pts: float = 3.0, params: dict = None
):
    """
    Etiqueta totales por barra (sobre tope en vertical, al final en horizontal).
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        El eje donde dibujar las etiquetas
    totals : array o lista
        Los valores totales a etiquetar
    positions : array o lista
        Las posiciones de las barras
    orientation : str
        'v' para barras verticales, 'h' para horizontales
    show : bool
        Si mostrar las etiquetas
    fmt : str
        Formato para los valores (ej: "{:.0f}")
    dy_pts : float, default=3.0
        Offset vertical en puntos tipográficos
    params : dict, optional
        Diccionario con la configuración completa
    """
    if not show:
        return

    # Obtener configuración de fuente
    font_cfg = {}
    if params and "total_labels" in params:
        font_cfg = params["total_labels"].get("font", {})
    
    font_props = {
        "fontsize": float(font_cfg.get("size", 12)),
        "fontfamily": font_cfg.get("family", "DejaVu Sans"),
        "fontweight": font_cfg.get("weight", "bold"),
        "color": font_cfg.get("color", "#000000"),
        "alpha": float(font_cfg.get("alpha", 1.0))
    }

    if orientation == "v":
        from matplotlib.transforms import ScaledTranslation
        for i, t in enumerate(totals):
            trans = ax.transData + ScaledTranslation(0, dy_pts / 72.0, ax.figure.dpi_scale_trans)
            ax.text(positions[i], float(t), fmt.format(float(t)),
                    ha="center", va="bottom", transform=trans, **font_props)
    else:
        from matplotlib.transforms import ScaledTranslation
        trans = ax.transData + ScaledTranslation(dy_pts / 72.0, 0, ax.figure.dpi_scale_trans)
        for i, t in enumerate(totals):
            ax.text(float(t), positions[i], fmt.format(float(t)),
                    ha="left", va="center", transform=trans, **font_props)


# =============================
# Banderas en stacked H / V
# =============================

def add_offset_image(
    ax: plt.Axes,
    im_arr: np.ndarray,
    xdata: float,
    ydata: float,
    *,
    xybox: tuple[float, float] = (0, 0),
    zoom: float = 0.1,
    box_alignment: tuple[float, float] = (0.5, 0.5),
    zorder: int = 20
) -> None:
    """
    Inserta una imagen con offset (AnnotationBbox) sobre ax.
    
    Parameters
    ----------
    ax : plt.Axes
        El eje donde añadir la imagen
    im_arr : np.ndarray
        Array de la imagen (RGBA)
    xdata, ydata : float
        Coordenadas de anclaje
    xybox : tuple[float, float]
        Offset en puntos desde el anclaje
    zoom : float
        Factor de zoom para la imagen
    box_alignment : tuple[float, float]
        Alineación de la caja (0-1, 0-1)
    zorder : int
        Orden Z para control de superposición
    """
    oi = OffsetImage(im_arr, zoom=zoom)
    ab = AnnotationBbox(
        oi,
        (xdata, ydata),
        xycoords="data",
        boxcoords="offset points",
        xybox=xybox,
        frameon=False,
        box_alignment=box_alignment,
        pad=0.0,
        annotation_clip=False,
    )
    ab.set_zorder(zorder)
    ab.set_clip_on(False)
    ab.set_in_layout(True)
    ax.add_artist(ab)

def add_flags_stackedbarh(ax, df, cats, totals, y_positions, flags_cfg: dict, total_labels_cfg: dict = None):
    """
    Añade banderas a barras apiladas horizontales.
    - place: "end" (al final de la barra) o "left" (ancladas a la izquierda)
    - La posición considera el offset del total label si está habilitado
    
    Parameters
    ----------
    total_labels_cfg : dict, optional
        Configuración de las etiquetas totales, incluyendo enabled y x_offset
    """
    if not flags_cfg or not flags_cfg.get("enabled"):
        return

    place     = flags_cfg.get("place", "end").lower()  # "end" | "left"
    cat_col   = flags_cfg.get("category_col") or df.columns[0]
    flag_col  = flags_cfg.get("column", "flag_url")
    zoom      = float(flags_cfg.get("zoom", 0.09))
    xpad      = float(flags_cfg.get("x_offset", 6))
    ypad      = float(flags_cfg.get("y_offset", 0))
    cache_dir = flags_cfg.get("cache_dir")
    debug     = bool(flags_cfg.get("debug", False))
    pattern   = flags_cfg.get("pattern")

    # Calculamos el offset del total label si está habilitado
    total_enabled = False
    total_offset = 0
    
    if total_labels_cfg:
        total_enabled = bool(total_labels_cfg.get("enabled", False))
        if total_enabled:
            # Convertimos puntos tipográficos a unidades de datos
            total_x_offset = float(total_labels_cfg.get("x_offset", 4.0))
            # Convertimos a unidades de datos basado en el DPI actual
            total_offset = total_x_offset * (ax.get_window_extent().width / ax.figure.dpi) * (ax.get_xlim()[1] - ax.get_xlim()[0]) / ax.get_window_extent().width

    # Si anclamos a la izquierda, da un pequeño margen para que no se recorten
    if place == "left":
        cur_left, cur_right = ax.margins()
        ax.margins(x=max(0.12, cur_left))

    # Asegura límites actualizados (por si hace falta leer xlim)
    try:
        ax.figure.canvas.draw()
    except Exception:
        pass

    cat2flag = dict(_flags_iter(df, cat_col=cat_col, flag_col=flag_col, pattern=pattern))

    for i, cat in enumerate(cats):
        raw = cat2flag.get(cat)
        if not raw:
            continue

        path_or_url = _resolve_repo_abs(raw)
        im = load_image_cached(path_or_url, cache_dir=cache_dir)
        if im is None:
            if debug:
                from rich import print as rprint
                rprint(f"[yellow][flags] no se pudo cargar: {path_or_url}[/yellow]")
            continue

        y = y_positions[i]
        if place == "end":
            x_anchor = float(totals[i])
            # Si los totales están habilitados, añadimos su offset
            if total_enabled:
                x_anchor += total_offset
            add_offset_image(ax, im, x_anchor, y,
                           xybox=(xpad, ypad), zoom=zoom,
                           box_alignment=(0.0, 0.5), zorder=20)
            if debug:
                ax.plot([x_anchor], [y], marker="o", ms=6, zorder=21)
        else:
            x_min = ax.get_xlim()[0]
            add_offset_image(ax, im, x_min, y,
                           xybox=(xpad, ypad), zoom=zoom,
                           box_alignment=(0.0, 0.5), zorder=20)
            if debug:
                ax.plot([x_min], [y], marker="o", ms=6, zorder=21)

def add_flags_stackedbar(ax, df, cats, tops, x_positions, flags_cfg: dict):
    """
    Añade banderas a barras apiladas verticales (encima del tope de cada barra).
    Controla tamaño con flags_cfg['zoom'] y desplazamiento vertical con y_offset (pt).
    """
    if not flags_cfg or not flags_cfg.get("enabled"):
        return

    from matplotlib.transforms import ScaledTranslation

    cat_col   = flags_cfg.get("category_col") or df.columns[0]
    flag_col  = flags_cfg.get("column", "flag_url")
    zoom      = float(flags_cfg.get("zoom", 0.11))
    ypad      = float(flags_cfg.get("y_offset", 3.0))  # puntos tipográficos
    cache_dir = flags_cfg.get("cache_dir", "assets/flags")
    debug     = bool(flags_cfg.get("debug", False))
    pattern   = flags_cfg.get("pattern")

    cat2flag = dict(_flags_iter(df, cat_col=cat_col, flag_col=flag_col, pattern=pattern))

    for i, cat in enumerate(cats):
        raw = cat2flag.get(cat)
        if not raw:
            continue

        path_or_url = _resolve_repo_abs(raw)
        im = load_image_cached(path_or_url, cache_dir=cache_dir)
        if im is None:
            if debug:
                from rich import print as rprint
                rprint(f"[yellow][flags] no se pudo cargar: {path_or_url}[/yellow]")
            continue

        x_i = float(x_positions[i])
        y_i = float(tops[i])

        ab = AnnotationBbox(
            OffsetImage(im, zoom=zoom),
            (x_i, y_i),
            xycoords=("data", "data"),
            frameon=False,
            box_alignment=(0.5, 0.0),
            pad=0.0,
            annotation_clip=False,
        )
        trans = ax.transData + ScaledTranslation(0, ypad / 72.0, ax.figure.dpi_scale_trans)
        ab.set_transform(trans)
        ab.set_zorder(20)
        ab.set_clip_on(False)
        ax.add_artist(ab)


def adjust_yaxis_labels(ax, padding_pts: float = 20, fontsize: float = 9) -> None:
    """
    Ajusta automáticamente el margen izquierdo para acomodar las etiquetas del eje Y
    y configura el tamaño de fuente apropiado.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        El eje que contiene las etiquetas a ajustar
    padding_pts : float, optional
        Padding adicional en puntos tipográficos (default: 20)
    fontsize : float, optional
        Tamaño de fuente para las etiquetas (default: 9)
    """
    # Ajusta el tamaño de la fuente
    ax.tick_params(axis='y', labelsize=fontsize)

    # Calcula y ajusta los márgenes
    fig = ax.figure
    fig.canvas.draw()
    bbox = ax.get_yaxis().get_tightbbox(fig.canvas.get_renderer())
    transform = fig.dpi_scale_trans.inverted()
    margin_left = bbox.width + padding_pts
    margin_inches = transform.transform((margin_left, 0))[0]
    
    # Ajusta los márgenes manteniendo el derecho
    fig.subplots_adjust(
        left=margin_inches/fig.get_figwidth(),
        right=0.98  # mantiene un pequeño margen a la derecha
    )


def get_bar_style(params: dict) -> dict:
    """
    Obtiene la configuración de estilo para las barras.
    """
    bar_cfg = params.get("bar", {})
    return {
        "height": float(bar_cfg.get("width", 0.85)),  # Aumentado a 0.85 para barras más altas
        "linewidth": float(bar_cfg.get("linewidth", 0.75)),
        "edgecolor": bar_cfg.get("edgecolor", "white")
    }
    
def adjust_bar_spacing(ax) -> None:
    """
    Ajusta el espaciado entre barras al mínimo posible.
    """
    # Solo ajustar el margen horizontal
    ax.margins(x=0.02)


def add_titles(fig, ax, params: dict) -> None:
    """
    Añade título y subtítulo en el header de la figura.
    """
    if not params or "_layout" not in params:
        return

    # Obtener configuración de layout
    layout = params["_layout"]
    margins = layout["margins"]
    header = layout["header"]
    
    # Calcular posición x central
    x_center = margins["left"] + layout["content_width"] / 2

    # Configuración del título
    title_cfg = params.get("title", {})
    if isinstance(title_cfg, str):
        title_cfg = {"text": title_cfg}
    
    subtitle_cfg = params.get("subtitle", {})
    if isinstance(subtitle_cfg, str):
        subtitle_cfg = {"text": subtitle_cfg}

    # Si no hay títulos, salimos
    if not (title_cfg.get("text") or subtitle_cfg.get("text")):
        return

    # Añadir título si existe
    if title_text := title_cfg.get("text"):
        title_font = title_cfg.get("font", {})
        fig.text(x_center, header["title_y"], title_text,
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=float(title_font.get("size", 24)),
                fontfamily=title_font.get("family", "DejaVu Sans"),
                fontweight=title_font.get("weight", "bold"),
                color=title_font.get("color", "#333333"))

    # Añadir subtítulo si existe
    if subtitle_text := subtitle_cfg.get("text"):
        subtitle_font = subtitle_cfg.get("font", {})
        fig.text(x_center, header["subtitle_y"], subtitle_text,
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=float(subtitle_font.get("size", 12)),
                fontfamily=subtitle_font.get("family", "DejaVu Sans"),
                fontweight=subtitle_font.get("weight", "normal"),
                color=subtitle_font.get("color", "#666666"))

    fig.stale = True

def finish_and_save(fig, params: Mapping[str, Any]):
    """Inserta branding estándar y guarda en todos los formatos."""
    # 1. Configurar DPI para mejor calidad de exportación
    dpi = float(params.get("dpi", 300))
    fig.set_dpi(dpi)

    # 2. Aplicar branding según configuración
    branding_cfg = params.get("branding", {})
    add_branding(fig, branding_cfg)

    # 3. Guardar en múltiples formatos configurados
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

    # 4. Limpiar recursos
    fig.canvas.draw_idle()

class ImageHandler(HandlerBase):
    """
    Handler para incluir imágenes en lugar de marcadores de colores en la leyenda.
    
    Parameters
    ----------
    image_path : str
        Ruta absoluta a la imagen a mostrar
    zoom : float
        Factor de zoom para la imagen
    """
    def __init__(self, image_path, zoom=0.15):
        self.image_path = image_path
        self.zoom = zoom
        super().__init__()
    
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        from matplotlib.image import imread
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        from matplotlib.patches import Rectangle
        import numpy as np
        
        # Cargar la imagen
        img = imread(self.image_path)
        print(f"[DEBUG] Imagen cargada: {self.image_path} shape={img.shape} dtype={img.dtype}")
        # Si tiene canal alfa, convertir a RGB ignorando alfa
        if img.ndim == 3 and img.shape[2] == 4:
            alpha = img[..., 3]
            if np.all(alpha == 0):
                print(f"⚠️ Imagen completamente transparente: {self.image_path}")
            img = img[..., :3]  # Quitar canal alfa
            print(f"[DEBUG] Imagen convertida a RGB (sin alfa): shape={img.shape}")
        elif np.all(img == 0):
            print(f"⚠️ Imagen completamente vacía (todo ceros): {self.image_path}")

        # Crear imagen con zoom (prueba con zoom mayor si no se ve)
        imagebox = OffsetImage(img, zoom=max(self.zoom, 0.3))
        imagebox.image.axes = legend.axes

        # Crear annotation box centrada en la posición
        ab = AnnotationBbox(
            imagebox,
            (xdescent + width/2., ydescent + height/2.),
            frameon=False,
            pad=0.0,
            box_alignment=(0.5, 0.5),
        )
        ab.set_transform(trans)

        # Agregar un borde visual para debug
        border = Rectangle(
            (xdescent, ydescent), width, height,
            linewidth=1, edgecolor='red', facecolor='none', zorder=10
        )
        border.set_transform(trans)

        return [ab, border]


class ColorableSVGHandler(HandlerBase):
    """
    Handler para incluir SVGs coloreables en la leyenda.
    
    Esta clase permite usar un único archivo SVG como plantilla y aplicarle
    diferentes colores para representar diferentes elementos en la leyenda.
    
    Parameters
    ----------
    svg_path : str
        Ruta absoluta al archivo SVG a mostrar
    color : str
        Color en formato hex (#RRGGBB) para aplicar al SVG
    zoom : float
        Factor de zoom para la imagen
    """
    def __init__(self, svg_path, color, zoom=0.15):
        self.svg_path = svg_path
        self.color = color
        self.zoom = zoom
        super().__init__()
    
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        import io
        import matplotlib.pyplot as plt
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        from pathlib import Path
        
        # Leer el archivo SVG
        with open(self.svg_path, 'r') as f:
            svg_content = f.read()
        
        # Reemplazar 'currentColor' por el color especificado
        # Esto asume que el SVG usa 'currentColor' como valor para los atributos
        # que deben ser coloreados dinámicamente
        colored_svg = svg_content.replace('currentColor', self.color)
        
        # Crear un archivo en memoria con el SVG modificado
        svg_buffer = io.BytesIO()
        svg_buffer.write(colored_svg.encode('utf-8'))
        svg_buffer.seek(0)
        
        # Usar matplotlib para cargar el SVG modificado
        try:
            # Crear una figura temporal para cargar el SVG
            temp_fig = plt.figure(figsize=(1, 1), dpi=100)
            img = plt.imread(svg_buffer, format='svg')
            plt.close(temp_fig)
            
            # Crear imagen con zoom
            imagebox = OffsetImage(img, zoom=self.zoom)
            imagebox.image.axes = legend.axes
            
            # Crear annotation box centrada en la posición
            ab = AnnotationBbox(
                imagebox,
                (xdescent + width/2., ydescent + height/2.),
                frameon=False,
                pad=0.0,
                box_alignment=(0.5, 0.5),
            )
            ab.set_transform(trans)
            
            return [ab]
            
        except Exception as e:
            print(f"⚠️ Error al cargar SVG coloreado: {e}")
            # Fallback: usar un rectángulo del color especificado
            from matplotlib.patches import Rectangle
            rect = Rectangle((xdescent, ydescent), width, height, 
                             facecolor=self.color, edgecolor='black')
            rect.set_transform(trans)
            return [rect]

def add_logo_to_figure(fig, logo_config):
    """
    Añade un logo a la figura basado en la configuración.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        La figura donde añadir el logo
    logo_config : dict
        Configuración del logo con keys:
        - path: ruta al archivo de imagen
        - position: 'above_legend', 'top_left', 'top_right', 'custom'
        - zoom: factor de zoom (default: 0.15)
        - x, y: coordenadas personalizadas (si position='custom')
        - margin: margen sobre la leyenda (si position='above_legend')
    """
    if not logo_config or not logo_config.get("path"):
        return
        
    from matplotlib.image import imread
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    from pathlib import Path
    
    # Cargar logo
    logo_path = logo_config.get("path")
    zoom = logo_config.get("zoom", 0.15)
    position = logo_config.get("position", "custom")
    margin = logo_config.get("margin", 0.02)
    
    if not Path(logo_path).exists():
        print(f"⚠️ No se encontró el archivo de logo: {logo_path}")
        return
        
    img = imread(logo_path)
    imagebox = OffsetImage(img, zoom=zoom)
    
    # Determinar posición
    x, y = 0.9, 0.9  # Valores por defecto
    
    print(f"📌 Añadiendo logo desde: {logo_path}")
    print(f"📌 Posición configurada: {position}")
    
    if position == "above_legend":
        # Buscar la leyenda en todos los ejes, incluyendo legend_ax que podría existir para leyendas personalizadas
        legend_found = False
        
        # Primero buscar leyendas estándar
        for ax in fig.axes:
            legend = ax.get_legend()
            if legend:
                legend_found = True
                bbox = legend.get_window_extent().transformed(fig.transFigure.inverted())
                x = (bbox.x0 + bbox.x1) / 2
                y = bbox.y1 + margin
                print(f"📌 Leyenda estándar encontrada, colocando logo en x={x:.2f}, y={y:.2f}")
                break
        
        # Si no se encontró una leyenda estándar, buscar un axes específico para leyenda personalizada
        if not legend_found:
            for ax in fig.axes:
                # Verificar si este es un axes específico para leyenda personalizada
                if hasattr(ax, 'get_label') and ('legend' in str(ax.get_label()).lower() or 'custom_legend' in str(ax.get_label()).lower()):
                    legend_found = True
                    bbox = ax.get_window_extent().transformed(fig.transFigure.inverted())
                    x = (bbox.x0 + bbox.x1) / 2
                    y = bbox.y1 + margin
                    print(f"📌 Axes de leyenda personalizada encontrado, colocando logo en x={x:.2f}, y={y:.2f}")
                    break
        
        # Posición fallback si no se encuentra ninguna leyenda
        if not legend_found:
            print("⚠️ No se encontró leyenda para posicionar el logo encima, usando posición predeterminada")
            # Usar una posición razonable en el cuadrante derecho superior
            if logo_config.get("fallback_position") == "top_right":
                x, y = 0.9, 0.9
                print(f"📌 Usando posición fallback para logo en esquina superior derecha: x={x}, y={y}")
            elif logo_config.get("fallback_position") == "top_center":
                x, y = 0.5, 0.9
                print(f"📌 Usando posición fallback para logo en centro superior: x={x}, y={y}")
                
    elif position == "top_left":
        x, y = 0.05, 0.95
        print(f"📌 Logo en esquina superior izquierda: x={x}, y={y}")
    elif position == "top_right":
        x, y = 0.95, 0.95
        print(f"📌 Logo en esquina superior derecha: x={x}, y={y}")
    elif position == "custom":
        x = logo_config.get("x", 0.9)
        y = logo_config.get("y", 0.9)
        print(f"📌 Logo en posición personalizada: x={x}, y={y}")
    
    # Añadir logo
    ab = AnnotationBbox(
        imagebox,
        (x, y),
        frameon=False,
        box_alignment=(0.5, 0.5),  # Centrado
        pad=0,
        xycoords='figure fraction',
        annotation_clip=False
    )
    fig.add_artist(ab)
    return ab

def create_custom_legend_with_images(ax, fig, legend_config):
    """
    Crea una leyenda personalizada con imágenes o SVGs coloreables en lugar de marcadores de colores.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        El eje donde se añadirá la leyenda
    fig : matplotlib.figure.Figure
        La figura para coordenadas de transformación
    legend_config : dict
        Configuración de la leyenda incluyendo 'icons' con las imágenes
        
    Returns
    -------
    matplotlib.legend.Legend
        La leyenda creada, o None si no se pudo crear
    """
    # Verificar si queremos usar la implementación alternativa con imágenes directas
    if legend_config.get("custom_icons") and legend_config.get("use_direct_drawing", True):
        try:
            from .custom_legend import CustomImageLegend
            print("🔍 Leyenda personalizada: Usando implementación directa con CustomImageLegend")
            custom_legend = CustomImageLegend(fig, ax, legend_config)
            if custom_legend.draw():
                print("✅ Leyenda personalizada dibujada correctamente con CustomImageLegend")
                return None  # No hay leyenda estándar para devolver
            else:
                print("⚠️ Error al dibujar leyenda personalizada, intentando método alternativo")
        except Exception as e:
            print(f"❌ Error con CustomImageLegend: {e}. Usando método alternativo.")
    
    # Si no se usa la implementación directa o falló, usar el método original
    if not legend_config.get("custom_icons"):
        return None
        
    print("🔍 Creando leyenda personalizada con imágenes (método original)")
        
    icons = legend_config.get("icons", [])
    if not icons:
        print("⚠️ Se solicitó leyenda con íconos pero no se proporcionaron imágenes.")
        return None
        
    print(f"🔍 Encontradas {len(icons)} imágenes para la leyenda personalizada")
    
    # Crear elementos ficticios para la leyenda
    import matplotlib.patches as mpatches
    handles = [mpatches.Rectangle((0, 0), 1, 1) for _ in range(len(icons))]
    labels = [icon.get("label", f"Item {i+1}") for i, icon in enumerate(icons)]
    
    print(f"🔍 Etiquetas para la leyenda: {labels}")
    
    # Crear diccionario de handlers
    handler_map = {}
    for i, (handle, icon) in enumerate(zip(handles, icons)):
        # Determinar si es un SVG coloreable o una imagen normal
        if icon.get("svg_template") and icon.get("color"):
            # Es un SVG coloreable
            svg_path = icon.get("svg_template")
            color = icon.get("color")
            zoom = icon.get("zoom", 0.15)
            
            if not Path(svg_path).exists():
                print(f"⚠️ No se encontró el SVG plantilla: {svg_path}")
                continue
            
            handler_map[handle] = ColorableSVGHandler(svg_path, color, zoom)
            print(f"✅ SVG coloreable añadido: {svg_path} con color {color} (zoom={zoom})")
            
        else:
            # Es una imagen normal
            image_path = icon.get("image")
            if not image_path:
                print(f"⚠️ No se especificó ruta de imagen para el elemento {i+1}")
                continue
                
            if not Path(image_path).exists():
                print(f"⚠️ No se encontró la imagen para la leyenda: {image_path}")
                continue
            
            zoom = icon.get("zoom", 0.15)
            handler_map[handle] = ImageHandler(image_path, zoom)
            print(f"✅ Imagen añadida correctamente: {image_path} (zoom={zoom})")
    
    # Extraer parámetros de configuración de la leyenda
    # Lista de parámetros que sabemos que son compatibles con la leyenda de matplotlib
    valid_params = [
        'loc', 'bbox_to_anchor', 'ncol', 'fontsize', 'frameon', 'title',
        'borderpad', 'labelspacing', 'handlelength', 'handleheight',
        'handletextpad', 'borderaxespad', 'columnspacing', 'facecolor',
        'edgecolor', 'framealpha', 'shadow', 'fancybox'
    ]
    
    # Filtrar solo los parámetros válidos
    legend_params = {}
    for param in valid_params:
        if param in legend_config:
            legend_params[param] = legend_config[param]
    
    # Guardar el título para después
    title = legend_params.get('title')
    title_fontsize = legend_config.get('title_fontsize')
    title_fontweight = legend_config.get('title_fontweight')
    
    print(f"🔍 Parámetros filtrados para la leyenda: {legend_params}")
    
    # Añadir leyenda con handlers personalizados
    legend = ax.legend(handles, labels, handler_map=handler_map, **legend_params)
    
    # Configurar el título de la leyenda después de crearla
    if legend and title:
        title_obj = legend.get_title()
        if title_obj:
            if title_fontsize:
                title_obj.set_size(title_fontsize)
            if title_fontweight:
                title_obj.set_weight(title_fontweight)
    
    return legend

def add_logo_above_legend(fig, ax, logo_config):
    """
    Añade un logo encima de la leyenda o en una posición personalizada.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        La figura donde se añadirá el logo
    ax : matplotlib.axes.Axes
        El eje para las coordenadas y la leyenda
    logo_config : dict
        Configuración del logo incluyendo 'path', 'position', 'zoom', etc.
        
    Returns
    -------
    matplotlib.offsetbox.AnnotationBbox or None
        El objeto de anotación creado, o None si hubo un error
    """
    if not logo_config or not logo_config.get("path"):
        return None
        
    logo_path = logo_config.get("path")
    if not Path(logo_path).exists():
        print(f"⚠️ No se encontró el archivo de logo: {logo_path}")
        return None
    
    zoom = logo_config.get("zoom", 0.15)
    position = logo_config.get("position", "custom")
    margin = logo_config.get("margin", 0.02)  # Margen entre logo y leyenda
    
    # Cargar logo
    from matplotlib.image import imread
    img = imread(logo_path)
    imagebox = OffsetImage(img, zoom=zoom)
    
    # Determinar posición
    x, y = 0.9, 0.9  # Posición predeterminada
    
    if position == "above_legend":
        legend = ax.get_legend()
        if legend:
            bbox = legend.get_window_extent().transformed(fig.transFigure.inverted())
            x = (bbox.x0 + bbox.x1) / 2
            y = bbox.y1 + margin
        else:
            print("⚠️ Se solicitó logo sobre leyenda pero no hay leyenda visible.")
            position = "custom"  # Fallback a posición personalizada
    
    if position == "custom":
        x = logo_config.get("x", x)
        y = logo_config.get("y", y)
    
    # Añadir logo
    ab = AnnotationBbox(
        imagebox,
        (x, y),
        frameon=False,
        box_alignment=(0.5, 0.0),  # Centrado horizontalmente, abajo verticalmente
        pad=0,
        xycoords='figure fraction',
        annotation_clip=False
    )
    fig.add_artist(ab)
    
    return ab
