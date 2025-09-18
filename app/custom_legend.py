"""
Implementación de una leyenda personalizada con imágenes para matplotlib.
"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

class CustomImageLegend:
    """
    Leyenda personalizada que dibuja imágenes directamente sobre la figura.
    
    Esta clase implementa una alternativa al sistema de leyendas de matplotlib
    para mostrar imágenes de mayor tamaño y personalización que lo que permite
    el sistema estándar de leyendas.
    """
    
    def __init__(self, fig: plt.Figure, ax: plt.Axes, config: Dict[str, Any]):
        """
        Inicializa la leyenda personalizada.
        
        Parameters
        ----------
        fig : plt.Figure
            La figura donde se dibujará la leyenda
        ax : plt.Axes
            Los ejes de referencia para coordenadas
        config : Dict[str, Any]
            Configuración de la leyenda
        """
        self.fig = fig
        self.ax = ax
        self.config = config
        self.legend_ax = None
        self.title_artist = None
        self.box = None
        self.icons = []
        self.labels = []
        
    def _load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Carga una imagen desde un archivo.
        
        Parameters
        ----------
        image_path : str
            Ruta al archivo de imagen
            
        Returns
        -------
        Optional[np.ndarray]
            Array de la imagen o None si ocurrió un error
        """
        try:
            img = imread(image_path)
            print(f"[DEBUG] Imagen cargada: {image_path} shape={img.shape} dtype={img.dtype}")
            
            # Verificar si queremos preservar el canal alfa
            preserve_alpha = self.config.get("preserve_alpha", True)
            
            if img.ndim == 3 and img.shape[2] == 4:
                if preserve_alpha:
                    # Usar la imagen completa con transparencia
                    print(f"[DEBUG] Usando imagen con canal alfa preservado: shape={img.shape}")
                    return img
                else:
                    # Preservar solo los canales RGB, pero usar el canal alfa para composición
                    # sobre fondo blanco para visualización más clara
                    rgb = img[..., :3]
                    alpha = img[..., 3:4]
                    # Aplicar el canal alfa para mezclar con fondo blanco
                    white_bg = np.ones_like(rgb)
                    img_rgb = alpha * rgb + (1 - alpha) * white_bg
                    print(f"[DEBUG] Imagen convertida a RGB (sin alfa): shape={img_rgb.shape}")
                    return img_rgb
            return img
        except Exception as e:
            print(f"❌ Error al cargar imagen {image_path}: {e}")
            return None
            
    def draw(self) -> bool:
        """
        Dibuja la leyenda personalizada en la figura.
        
        Returns
        -------
        bool
            True si se dibujó correctamente, False si hubo errores
        """
        if not self.config.get("custom_icons") or not self.config.get("icons"):
            print("⚠️ No se encontró configuración de íconos para la leyenda personalizada")
            return False
            
        # Extraer configuración
        icons_config = self.config.get("icons", [])
        if not icons_config:
            print("⚠️ Lista de íconos vacía")
            return False
            
        print(f"🔍 Leyenda personalizada: Dibujando {len(icons_config)} íconos")
        
        # Extraer etiquetas y cargar imágenes
        self.icons = []
        self.labels = []
        
        # Obtener paleta de colores desde config (usada en barras)
        palette = self.config.get("colors", {})

        import re
        def is_hex_color(s):
            return isinstance(s, str) and re.fullmatch(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", s)

        for icon in icons_config:

            label = icon.get("_label_with_total") or icon.get("label", "")
            image_path = icon.get("image", "")
            zoom = icon.get("zoom", 0.15)
            circle_scale = icon.get("circle_scale")
            label_fontsize = icon.get("label_fontsize")
            if not image_path:
                print(f"⚠️ No se especificó ruta de imagen para el ícono: {label}")
                continue
            if not Path(image_path).exists():
                print(f"❌ No se encontró el archivo de imagen: {image_path}")
                continue
            img = self._load_image(image_path)
            if img is None:
                continue
            # Buscar color para este ícono: primero por 'tint', luego por label
            color = None
            tint_key = icon.get("tint")
            print(f"[DEBUG] Resolviendo color para ícono '{label}': tint_key={tint_key!r}, palette={palette}")
            if is_hex_color(tint_key):
                color = tint_key
            elif tint_key:
                # Buscar ignorando mayúsculas/minúsculas
                palette_lc = {str(k).lower(): v for k, v in palette.items()}
                color = palette_lc.get(str(tint_key).lower())
                print(f"[DEBUG] Resultado búsqueda en palette_lc: {color}")
            if not color:
                label_key = icon.get("label", "").strip().lower()
                palette_lc = {str(k).lower(): v for k, v in palette.items()}
                color = palette_lc.get(label_key)
                print(f"[DEBUG] Resultado búsqueda por label en palette_lc: {color}")
            icon_dict = {
                "image": img,
                "path": image_path,
                "zoom": zoom,
                "tint": color
            }
            if circle_scale is not None:
                icon_dict["circle_scale"] = circle_scale
            if label_fontsize is not None:
                icon_dict["label_fontsize"] = label_fontsize
            self.icons.append(icon_dict)
            self.labels.append(label)
            
        if not self.icons:
            print("❌ No se pudo cargar ninguna imagen para la leyenda")
            return False
            
        # Crear el axes para la leyenda
        return self._create_legend_box()
        
    def _create_legend_box(self) -> bool:
        """
        Crea el área de la leyenda y dibuja su contenido.
        Returns
        -------
        bool
            True si se creó correctamente, False si hubo errores
        """
        # Determinar posición de la leyenda
        loc = self.config.get("loc", "lower right")
        bbox_to_anchor = self.config.get("bbox_to_anchor")
        # Determinar tamaño aproximado
        fontsize = self.config.get("fontsize", 12)
        # Forzar alineación vertical de los íconos (una sola columna)
        ncols = 1
        nrows = len(self.icons)
        # Calcular dimensiones aproximadas (en fracción de figura)
        # Usar el zoom máximo de los íconos para el alto real
        icon_zooms = [icon.get("zoom", 0.15) for icon in self.icons]
        max_zoom = max(icon_zooms) if icon_zooms else 0.15
        icon_width = max_zoom
        icon_height = max_zoom
        item_width = 0.32
        item_height = max_zoom
        # Espacio para el título
        title_height = 0.12 if self.config.get("title") else 0.0
        # Calcular ancho y alto total con item_spacing configurable
        item_spacing = self.config.get("item_spacing", 1.2)
        width = item_width * ncols * 1.25
        height = (item_height * nrows * item_spacing) + title_height

        # Determinar posición (x, y) de la esquina inferior izquierda
        if bbox_to_anchor:
            # Usar bbox_to_anchor directamente
            x = bbox_to_anchor[0] - width
            y = bbox_to_anchor[1]
        else:
            # Posición basada en loc
            if loc == "upper right":
                x = 0.95 - width
                y = 0.95 - height
            elif loc == "upper left":
                x = 0.05
                y = 0.95 - height
            elif loc == "lower left":
                x = 0.05
                y = 0.05
            elif loc == "lower right":
                x = 0.95 - width
                y = 0.05
            elif loc == "upper center":
                x = 0.5 - width/2
                y = 0.95 - height
            elif loc == "lower center":
                x = 0.5 - width/2
                y = 0.05
            else:
                x = 0.95 - width
                y = 0.05

        # Crear un axes para la leyenda
        self.legend_ax = self.fig.add_axes([x, y, width, height])
        self.legend_ax.set_label('custom_legend_axes')
        self.legend_ax.set_axis_off()

        # Configurar el fondo y borde si se especifica
        if self.config.get("frameon", True):
            self.legend_ax.patch.set_facecolor(self.config.get("facecolor", "#f8f8f8"))
            self.legend_ax.patch.set_edgecolor(self.config.get("edgecolor", "#dddddd"))
            self.legend_ax.patch.set_alpha(self.config.get("framealpha", 0.9))
            self.legend_ax.patch.set_linewidth(0.5)
        else:
            self.legend_ax.patch.set_alpha(0)

        # Añadir título si está especificado
        if title := self.config.get("title"):
            title_fontsize = self.config.get("title_fontsize", fontsize * 1.2)
            title_fontweight = self.config.get("title_fontweight", "bold")
            x_label = 0.09  # Debe coincidir con el x de los labels
            self.title_artist = self.legend_ax.text(
                x_label, 0.95, title,
                horizontalalignment="left",
                verticalalignment="top",
                transform=self.legend_ax.transAxes,
                fontsize=title_fontsize,
                fontweight=title_fontweight,
                fontfamily=self.config.get("font", {}).get("family", None),
                color=self.config.get("font", {}).get("color", "#333333")
            )

        # Dibujar los íconos y etiquetas
        return self._draw_legend_items(ncols, nrows, title_height, icon_zooms, item_spacing)
    
    def _draw_legend_items(self, ncols: int, nrows: int, title_height: float, icon_zooms=None, item_spacing=1.2) -> bool:
        """
        Dibuja los íconos y etiquetas dentro del área de la leyenda.
        Parameters
        ----------
        ncols : int
            Número de columnas
        nrows : int
            Número de filas
        title_height : float
            Altura reservada para el título
        Returns
        -------
        bool
            True si se dibujó correctamente, False si hubo errores
        """
        if not self.legend_ax:
            return False
        fontsize = max(10, int(self.config.get("fontsize", 12) * 0.7))  # Reducir tamaño de fuente
        # Ajustar el área disponible considerando el título
        # Si hay título, los íconos empiezan justo debajo
        if title_height > 0:
            y_start = 1.0 - title_height - 0.04  # 0.04 de margen visual
        else:
            y_start = 0.9
        y_end = 0.1
        y_range = y_start - y_end
        icon_zooms = icon_zooms or [0.15] * len(self.icons)
        total_icon_height = sum(icon_zooms)
        if nrows > 1:
            padding = (y_range - total_icon_height) / (nrows - 1) if y_range > total_icon_height else 0
        else:
            padding = 0
        y = y_start
        for i, (icon_info, label, zoom) in enumerate(zip(self.icons, self.labels, icon_zooms)):
            y -= zoom / 2
            # Texto a la izquierda, ícono a la derecha
            x_label = 0.09
            x_icon = 0.32
            print(f"[DEBUG] Posición de elemento {i} ({label}): x_label={x_label:.2f}, x_icon={x_icon:.2f}, y={y:.2f}")
            # Permitir tamaño de fuente individual por ícono
            label_fontsize = icon_info.get('label_fontsize', fontsize)
            self.legend_ax.text(
                x_label, y, label,
                horizontalalignment="left",
                verticalalignment="center",
                transform=self.legend_ax.transAxes,
                fontsize=label_fontsize,
                fontfamily=self.config.get("font", {}).get("family", None)
            )
            # Dibuja el ícono a la derecha
            self._draw_image(icon_info, x_icon, y)
            y -= zoom / 2
            if i < nrows - 1:
                y -= padding * item_spacing
        return True
            
    def _draw_image(self, icon_info: Dict[str, Any], x: float, y: float) -> None:
        """
        Dibuja una imagen en la posición especificada, con borde blanco grueso.
        """
        img = icon_info["image"]
        zoom = icon_info["zoom"]
        path = icon_info["path"]
        tint = icon_info.get("tint")
        img_size = zoom
        try:
            height, width = img.shape[:2]
            aspect_ratio = width / height
            img_width = img_size
            img_height = img_size / aspect_ratio if aspect_ratio > 1 else img_size
            img_width = max(img_width, 0.07)
            img_height = max(img_height, 0.07)
            # Dibuja un círculo de color debajo del PNG
            if tint:
                # Permitir controlar el tamaño del círculo desde el YAML (por icono) con 'circle_scale'
                circle_scale = icon_info.get('circle_scale', 0.7)  # 0.7 por defecto
                # El círculo será un porcentaje del tamaño del PNG (más pequeño)
                circle_size = max(img_width, img_height) * circle_scale
                # El centro es (x, y) en coordenadas de la leyenda
                circ_ax = self.legend_ax.inset_axes([
                    x - circle_size/2, y - circle_size/2, circle_size, circle_size
                ], transform=self.legend_ax.transAxes)
                circ_ax.patch.set_alpha(0)
                from matplotlib.patches import Circle
                circ = Circle((0.5, 0.5), 0.5, facecolor=tint, edgecolor='white', linewidth=2, zorder=0)
                circ_ax.add_patch(circ)
                circ_ax.set_aspect('equal')
                circ_ax.axis('off')
            # Mostrar el PNG original sin tintado
            img_to_show = img
            print(f"[DEBUG] Dibujando imagen en leyenda: {path}, tamaño={img_width:.4f}x{img_height:.4f}, tint={tint}")
            img_ax = self.legend_ax.inset_axes(
                [x - img_width/2, y - img_height/2, img_width, img_height],
                transform=self.legend_ax.transAxes
            )
            img_ax.patch.set_alpha(0)
            img_ax.imshow(img_to_show, interpolation='bilinear', zorder=1)
            # Borde blanco opcional sobre el PNG
            from matplotlib.patches import Circle
            circ = Circle((width/2, height/2), min(width, height)/2-2, linewidth=7, edgecolor='white', facecolor='none', zorder=2)
            img_ax.add_patch(circ)
            img_ax.axis('off')
            print(f"✅ Imagen dibujada correctamente en leyenda: {path}")
        except Exception as e:
            print(f"❌ Error al dibujar imagen en leyenda {path}: {e}")