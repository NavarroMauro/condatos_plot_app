# app/plot_helpers.py
from __future__ import annotations

from pathlib import Path
import hashlib, io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.axes import Axes
from PIL import Image

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
    Ajusta el tamaño de la figura EN FUNCIÓN DE LAS FILAS y escribe los valores
    calculados en params['width_in'] y params['height_in'].
    No hace nada si autosize.enabled es False o falta config.
    """
    a = (params.get("autosize") or {})
    if not a or not a.get("enabled", False):
        return

    mode = str(a.get("mode", "rows")).lower()
    if mode != "rows":
        return  # ahora solo soportamos modo por filas

    # lee parámetros con defaults sensatos
    width_in       = float(a.get("width_in", 12.0))
    h_per_row      = float(a.get("height_per_row", 0.28))
    min_height_in  = float(a.get("min_height", 6.0))
    max_height_in  = float(a.get("max_height", 18.0))

    # calcula altura base para las filas
    height_in = h_per_row * float(n_rows)
    
    # Añade espacio para títulos si existen
    if params.get("title") or params.get("subtitle"):
        title_height = float(a.get("title_height", 2.0))  # 2 pulgadas por defecto para títulos
        height_in += title_height

    # aplica límites min/max
    height_in = max(min_height_in, min(max_height_in, height_in))

    # escribe en params para que las siguientes funciones respeten esto
    params["width_in"]  = width_in
    params["height_in"] = height_in

    # aplica al objeto figura actual
    try:
        fig.set_size_inches(width_in, height_in, forward=True)
        
        # Ajusta los márgenes para dar espacio a los títulos
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


def norm_legend_loc(loc: str) -> str:
    """
    Acepta ubicaciones “humanas” y las traduce a Matplotlib.
    """
    if not loc:
        return "upper right"
    m = {
        "top left": "upper left",
        "top right": "upper right",
        "bottom left": "lower left",
        "bottom right": "lower right",
        "center left": "center left",
        "center right": "center right",
        "top center": "upper center",
        "bottom center": "lower center",
        "center": "center",
    }
    return m.get(loc.strip().lower(), loc)


def get_label_fmt(params: dict, default: str = "{:.0f}"):
    """
    Devuelve el formato de etiquetas de valores.
    Usa params['yfmt'] si existe, si no devuelve 'default'.
    """
    fmt = params.get("yfmt")
    if isinstance(fmt, str) and fmt:
        return fmt
    return default

# ...existing code...

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
        "height": float(bar_cfg.get("width", 0.65)),  # para barras horizontales, height controla el ancho
        "linewidth": float(bar_cfg.get("linewidth", 0.75)),
        "edgecolor": bar_cfg.get("edgecolor", "white")
    }
    

def apply_layout(fig, ax, params: dict) -> None:
    """
    Aplica la estructura de tres secciones (header, body, footer) a la figura.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        La figura a configurar
    ax : matplotlib.axes.Axes
        El eje principal que contiene el gráfico
    params : dict
        Diccionario de configuración con las opciones de layout
        
    La estructura se divide en:
    - HEADER (30% superior): Título y subtítulo
    - BODY (55% central): Gráfico principal
    - FOOTER (15% inferior): Branding y fuente
    """
    # Configuración de márgenes
    layout = params.get("layout", {})
    
    # Márgenes predeterminados - AJUSTADOS
    margin_top = float(layout.get("margin_top", 0.30))     # 30% para header
    margin_bottom = float(layout.get("margin_bottom", 0.15)) # 15% para footer
    margin_left = float(layout.get("margin_left", 0.22))    # 22% margen izquierdo
    margin_right = float(layout.get("margin_right", 0.12))  # 12% margen derecho

    # 1. Ajustar el área del gráfico (BODY)
    ax.set_position([
        margin_left,                    # left
        margin_bottom,                  # bottom
        1.0 - margin_left - margin_right, # width
        1.0 - margin_top - margin_bottom  # height
    ])

    # Guardar la configuración en params
    params["_layout"] = {
        "margins": {
            "top": margin_top,
            "bottom": margin_bottom,
            "left": margin_left,
            "right": margin_right
        },
        "content_width": 1.0 - margin_left - margin_right
    }

    # Dejar que layout.py maneje el header y footer
    from .layout import apply_frame, finish_and_save
    apply_frame(fig, params)
    finish_and_save(fig, params)

    fig.stale = True


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