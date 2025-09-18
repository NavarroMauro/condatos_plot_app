from pathlib import Path
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import textwrap
import matplotlib.font_manager as fm

class BaseChart:
    """
    Clase base para crear gráficos con matplotlib.
    
    Proporciona métodos comunes que pueden ser heredados por tipos específicos de gráficos.
    Implementa las funcionalidades comunes a todos los gráficos.
    """
    
    def __init__(self, params, df):
        """
        Inicializa el gráfico con la configuración proporcionada.
        
        Params:
            params (dict): Parámetros de configuración para el gráfico
            df (DataFrame): DataFrame con los datos a graficar
        """
        self.params = params
        self.df = df
        self.fig = None
        self.ax = None
        self.ax_header = None
        self.register_custom_fonts()
        
    def register_custom_fonts(self):
        """Registra fuentes personalizadas para usar en el gráfico."""
        fonts_dir = Path("fonts")
        if fonts_dir.exists():
            # Buscar todas las fuentes Nunito disponibles
            nunito_fonts = list(fonts_dir.glob("Nunito-*.ttf"))
            
            # Registrar todas las fuentes encontradas
            for font_path in nunito_fonts:
                try:
                    fm.fontManager.addfont(str(font_path))
                    print(f"✅ Fuente registrada: {font_path.name}")
                except Exception as e:
                    print(f"❌ Error al registrar fuente {font_path.name}: {e}")
                    
            # Verificar si Nunito está disponible después de registrar
            font_names = [f.name for f in fm.fontManager.ttflist]
            if any('Nunito' in name for name in font_names):
                print("✅ Fuente Nunito disponible para usar en los gráficos")
            else:
                print("⚠️ Fuente Nunito no se pudo registrar correctamente")
                
    def create_figure(self):
        """
        Crea la figura básica con las dimensiones especificadas.
        Este método debe ser implementado por las clases hijas.
        """
        from app.layout import apply_frame
        
        width_in = float(self.params.get("width_in", 12))
        height_in = float(self.params.get("height_in", 8))
        self.fig = plt.figure(figsize=(width_in, height_in))
        
        # Usar la función de layout para aplicar el frame
        self.fig, self.ax_header, self.ax = apply_frame(self.fig, self.params)
        
        return self.fig
        
    def prepare_data(self):
        """
        Prepara los datos para el gráfico. Debe ser implementado por subclases específicas.
        """
        raise NotImplementedError("Las subclases deben implementar prepare_data()")
        
    def filter_by_threshold(self, df, total_column=None, threshold=None, category_column=None):
        """
        Filtra el DataFrame eliminando filas donde la suma de columnas o una columna específica 
        está por debajo de un umbral.
        
        Args:
            df (DataFrame): DataFrame a filtrar
            total_column (str, optional): Nombre de la columna que contiene los totales
            threshold (float, optional): Valor umbral mínimo para incluir filas
            category_column (str, optional): Nombre de la columna de categorías (para mensajes de log)
            
        Returns:
            DataFrame: DataFrame filtrado
        """
        # Si no hay umbral definido, devolver el DataFrame sin cambios
        if threshold is None:
            return df
            
        # Obtener configuración del umbral del parámetro si no se especificó
        if isinstance(threshold, bool) and threshold:
            # Si threshold es True, intentar obtener valor de filter_threshold
            threshold = self.params.get("filter_threshold", 0)
            
        # Si el umbral es 0 o negativo, devolver el DataFrame sin filtrar
        if threshold <= 0:
            return df
            
        original_len = len(df)
        
        # Caso 1: Si se proporciona una columna de totales específica
        if total_column and total_column in df.columns:
            filtered_df = df[df[total_column] >= threshold].copy()
            
        # Caso 2: Calcular la suma de todas las columnas numéricas (excluyendo la columna de categorías)
        else:
            # Identificar columnas numéricas
            numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
            
            # Excluir la columna de categorías si está especificada
            if category_column and category_column in numeric_cols:
                numeric_cols.remove(category_column)
                
            # Calcular la suma de todas las columnas numéricas si hay alguna
            if numeric_cols:
                filtered_df = df[df[numeric_cols].sum(axis=1) >= threshold].copy()
            else:
                # Si no hay columnas numéricas, devolver el DataFrame original
                return df
        
        # Registrar cuántos elementos se filtraron
        filtered_count = original_len - len(filtered_df)
        
        if filtered_count > 0:
            # Identificar qué categorías se filtraron para el log
            if category_column and category_column in df.columns:
                filtered_categories = df[~df.index.isin(filtered_df.index)][category_column].tolist()
                
                # Limitar el número de categorías mostradas si son muchas
                if len(filtered_categories) > 10:
                    filtered_categories_str = ", ".join(filtered_categories[:5]) + f" y {len(filtered_categories) - 5} más"
                else:
                    filtered_categories_str = ", ".join(filtered_categories)
                    
                print(f"🔍 Filtrado: Se eliminaron {filtered_count} elementos con valores menores que {threshold}.")
                print(f"   Elementos filtrados: {filtered_categories_str}")
            else:
                print(f"🔍 Filtrado: Se eliminaron {filtered_count} elementos con valores menores que {threshold}.")
        
        return filtered_df
        
    def setup_dimensions(self):
        """
        Configura las dimensiones del gráfico basado en el contenido.
        Por defecto, usa los valores de width_in y height_in del parámetro.
        """
        width_in = float(self.params.get("width_in", 12))
        height_in = float(self.params.get("height_in", 8))
        
        self.params.update({
            "width_in": width_in,
            "height_in": height_in
        })
        
    def draw_chart(self):
        """
        Dibuja el gráfico principal.
        Este método debe ser implementado por las clases hijas.
        """
        raise NotImplementedError("Las subclases deben implementar draw_chart()")
        
    def configure_axes(self):
        """
        Configura los ejes y sus elementos.
        Este método debe ser implementado por las clases hijas.
        """
        raise NotImplementedError("Las subclases deben implementar configure_axes()")
        
    def add_legend(self):
        """
        Añade la leyenda si está habilitada y hay elementos con etiquetas.
        También maneja leyendas personalizadas con imágenes y logos.
        """
        # Verificar si hay elementos con etiquetas
        has_labeled_artists = False
        if hasattr(self.ax, 'get_legend_handles_labels'):
            handles, labels = self.ax.get_legend_handles_labels()
            has_labeled_artists = len(handles) > 0 and len(labels) > 0
            print(f"🔍 Leyenda: Se encontraron {len(handles)} elementos etiquetados")
        
        # Obtener configuración
        legend_config = self.params.get("legend_config", {})
        print(f"🔍 Leyenda: Configuración: {legend_config}")
        
        # Comprobar si tenemos una leyenda personalizada con imágenes
        if legend_config.get("custom_icons") and legend_config.get("icons"):
            print(f"🔍 Leyenda personalizada: Detectada configuración con íconos personalizados")
            print(f"🔍 Leyenda personalizada: Íconos configurados: {legend_config.get('icons')}")
            
            from ..plot_helpers import create_custom_legend_with_images
            legend = create_custom_legend_with_images(self.ax, self.fig, legend_config)
            
            # Añadir logo si está configurado
            logo_config = self.params.get("logo")
            if logo_config and logo_config.get("path"):
                print(f"🔍 Logo: Detectada configuración de logo: {logo_config}")
                from ..plot_helpers import add_logo_to_figure
                add_logo_to_figure(self.fig, logo_config)
            else:
                print(f"⚠️ Logo: No se encontró configuración de logo o ruta")
                
            return
        
        # Solo añadir leyenda estándar si está habilitada y hay elementos etiquetados
        if bool(self.params.get("legend", True)) and has_labeled_artists:
            # Parámetros básicos (compatibilidad)
            legend_loc = self.params.get("legend_loc", "lower right")
            legend_fontsize = self.params.get("legend_fontsize", 10)
            
            # Uso de parámetros avanzados si están disponibles
            loc = legend_config.get("loc", legend_loc)
            fontsize = legend_config.get("fontsize", legend_fontsize)
            frameon = legend_config.get("frameon", False)
            title = legend_config.get("title", None)
            title_fontsize = legend_config.get("title_fontsize", None)
            title_fontweight = legend_config.get("title_fontweight", "normal")
            
            # Parámetros adicionales avanzados
            ncol = legend_config.get("ncol", 1)  # Número de columnas
            bbox_to_anchor = legend_config.get("bbox_to_anchor", None)
            
            # Espaciado y formato avanzados
            borderpad = legend_config.get("borderpad", 0.4)
            labelspacing = legend_config.get("labelspacing", 0.5)
            handlelength = legend_config.get("handlelength", 2.0)
            handleheight = legend_config.get("handleheight", 0.7)
            handletextpad = legend_config.get("handletextpad", 0.8)
            borderaxespad = legend_config.get("borderaxespad", 0.5)
            columnspacing = legend_config.get("columnspacing", 2.0)
            
            # Apariencia de la caja
            facecolor = legend_config.get("facecolor", "inherit")
            edgecolor = legend_config.get("edgecolor", "inherit")
            framealpha = legend_config.get("framealpha", None)
            shadow = legend_config.get("shadow", False)
            fancybox = legend_config.get("fancybox", False)
            
            # Crear la leyenda con parámetros avanzados
            legend = self.ax.legend(
                loc=loc, 
                fontsize=fontsize,
                frameon=frameon,
                title=title,
                title_fontsize=title_fontsize,
                ncol=ncol,
                bbox_to_anchor=bbox_to_anchor,
                borderpad=borderpad,
                labelspacing=labelspacing,
                handlelength=handlelength,
                handleheight=handleheight,
                handletextpad=handletextpad,
                borderaxespad=borderaxespad,
                columnspacing=columnspacing,
                facecolor=facecolor,
                edgecolor=edgecolor,
                framealpha=framealpha,
                shadow=shadow,
                fancybox=fancybox
            )
            
            # Configuración adicional del título de la leyenda
            if title and legend.get_title():
                legend.get_title().set_fontweight(title_fontweight)
                
            # Añadir logo si está configurado
            logo_config = self.params.get("logo")
            if logo_config and logo_config.get("path"):
                from ..plot_helpers import add_logo_to_figure
                add_logo_to_figure(self.fig, logo_config)
                
        elif bool(self.params.get("legend", True)) and not has_labeled_artists:
            # Si se solicita leyenda pero no hay elementos etiquetados, mostrar un mensaje informativo
            print("ℹ️ No hay elementos con etiquetas para mostrar en la leyenda.")
            
    def add_title(self):
        """
        Añade título y subtítulo en un área dedicada sobre el gráfico con opciones avanzadas.
        Permite controlar el espaciado vertical y horizontal y usar fuentes personalizadas.
        """
        # Obtener configuración
        title = self.params.get("title", "")
        subtitle = self.params.get("subtitle", "")
        title_config = self.params.get("title_config", {}) or {}
        subtitle_config = self.params.get("subtitle_config", {}) or {}
        
        # Extraer texto y configuración
        title_text = title if isinstance(title, str) else title.get("text", "")
        subtitle_text = subtitle if isinstance(subtitle, str) else subtitle.get("text", "")
        
        # Configuración de título
        title_fontsize = title_config.get("fontsize", self.params.get("title_font_size", 28))
        title_fontweight = title_config.get("fontweight", self.params.get("title_font_weight", "bold"))
        title_color = title_config.get("color", self.params.get("title_color", "#333333"))
        title_fontfamily = title_config.get("family", self.params.get("title_font_family", "Nunito"))
        title_style = title_config.get("style", self.params.get("title_font_style", "normal"))
        title_ha = title_config.get("ha", self.params.get("title_horizontal_alignment", "center"))
        title_x = title_config.get("x", self.params.get("title_x_position", 0.5))
        
        # Configuración de subtítulo
        subtitle_fontsize = subtitle_config.get("fontsize", self.params.get("subtitle_font_size", 20))
        subtitle_fontweight = subtitle_config.get("fontweight", "normal")
        subtitle_color = subtitle_config.get("color", self.params.get("subtitle_color", "#666666"))
        subtitle_fontfamily = subtitle_config.get("family", self.params.get("subtitle_font_family", "Nunito"))
        subtitle_style = subtitle_config.get("style", self.params.get("subtitle_font_style", "italic"))
        subtitle_ha = subtitle_config.get("ha", self.params.get("subtitle_horizontal_alignment", "center"))
        subtitle_x = subtitle_config.get("x", self.params.get("subtitle_x_position", 0.5))
        
        # Configuración de espaciado
        title_spacing = self.params.get("title_spacing", {})
        top_margin = float(title_spacing.get("top_margin", 0.08))
        title_bottom_margin = float(title_spacing.get("bottom_margin", 0.10))
        subtitle_top_margin = float(title_spacing.get("subtitle_top_margin", 0.05))
        
        # Verificar que existe el eje para el título
        if self.ax_header is None:
            print("⚠️ No hay un eje definido para el título, no se puede añadir el título")
            return
            
        # Limpiar cualquier contenido previo en el eje del título
        self.ax_header.clear()
        self.ax_header.set_axis_off()
        
        # Calcular posiciones verticales
        title_y = 1 - top_margin
        subtitle_y = title_y - title_bottom_margin
        
        # Dibujar título si existe
        if title_text:
            self.ax_header.text(
                title_x, title_y, title_text,
                ha=title_ha, va="top",
                fontsize=title_fontsize,
                fontweight=title_fontweight,
                fontfamily=title_fontfamily,
                fontstyle=title_style,
                color=title_color,
                transform=self.ax_header.transAxes
            )
            
            print(f"✏️ Título añadido: {title_text}")
            
        # Dibujar subtítulo si existe
        if subtitle_text:
            self.ax_header.text(
                subtitle_x, subtitle_y, subtitle_text,
                ha=subtitle_ha, va="top",
                fontsize=subtitle_fontsize,
                fontweight=subtitle_fontweight,
                fontfamily=subtitle_fontfamily,
                fontstyle=subtitle_style,
                color=subtitle_color,
                transform=self.ax_header.transAxes
            )
            
            print(f"✏️ Subtítulo añadido: {subtitle_text}")
            
        # Actualizar la figura
        self.fig.canvas.draw()
    
    def add_footer(self):
        """
        Añade un footer con logo y texto en la parte inferior del gráfico.
        Soporta múltiples opciones de personalización para posición, estilo y contenido.
        """
        from app.branding import add_branding
        
        # Preparar configuración para el footer
        footer_config = self.params.get("footer", {})
        
        # Si no hay configuración, no hacer nada
        if not footer_config:
            return
            
        # Extraer información de configuración del footer
        source = footer_config.get("source", "")
        note = footer_config.get("note", "")
        
        # Preparar parámetros para add_branding
        branding_params = {
            "source": source,
            "note": note,
            "logo": footer_config.get("logo", ""),
            "color": footer_config.get("source_color", "#666666"),
            "fontsize": float(footer_config.get("source_fontsize", 9)),
            "text_y": 0.3,  # Posición relativa del texto en el footer
        }
        
        # Añadir el footer
        add_branding(self.fig, branding_params)
        
        print(f"👟 Footer añadido. Fuente: {source}")
    
    def add_labels(self):
        """
        Añade etiquetas de totales u otros valores a las barras.
        Método genérico que puede ser personalizado o sobreescrito por clases hijas.
        """
        # Etiquetas de totales
        total_cfg = self.params.get("total_labels", {})
        if bool(total_cfg.get("enabled", False)) and hasattr(self, 'bottoms') and hasattr(self, 'y_positions'):
            offset = float(total_cfg.get("x_offset", 4.0))
            font_size = float(total_cfg.get("font_size", 11))
            font_weight = total_cfg.get("font_weight", "bold")
            font_color = total_cfg.get("color", "#333333")
            
            # Imprimir información de configuración para depuración
            print("\n📊 Configuración de etiquetas de totales:")
            print(f"  - Offset X: {offset}")
            print(f"  - Tamaño de fuente: {font_size}")
            print(f"  - Peso de fuente: {font_weight}")
            print(f"  - Color: {font_color}")
            
            # Formato de números para totales
            total_format = total_cfg.get("format", "{:.0f}")
            
            for i, total in enumerate(self.bottoms):
                # Calcular posición precisa con offset
                x_offset_points = offset/72 * (self.fig.get_figwidth() * self.fig.dpi) / (self.ax.get_position().width * self.fig.get_figwidth())
                
                self.ax.text(
                    total + x_offset_points,
                    self.y_positions[i],
                    total_format.format(total),
                    ha='left', va='center',
                    fontsize=font_size,
                    fontweight=font_weight,
                    color=font_color
                )
    
    def add_decorative_elements(self):
        """
        Añade elementos decorativos al gráfico basados en la configuración.
        Soporta rectángulos, líneas y otros elementos visuales para estilo Statista.
        """
        # Verificar si hay configuración de elementos decorativos
        decorative_elements = self.params.get("decorative_elements", [])
        
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
                        transform=self.fig.transFigure,  # Usar coordenadas de figura
                        zorder=zorder
                    )
                    
                    # Añadir el rectángulo a la figura
                    self.fig.add_artist(rect)
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
                        transform=self.fig.transFigure
                    )
                    
                    # Añadir la línea a la figura
                    self.fig.add_artist(line)
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
                    self.fig.text(
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
    
    def finalize(self):
        """Finaliza y guarda el gráfico."""
        from app.layout import finish_and_save
        
        # Añadir elementos decorativos antes de guardar
        self.add_decorative_elements()
        
        # Usar la función centralizada para finalizar y guardar el gráfico
        finish_and_save(self.fig, self.params)
        
    def render(self):
        """
        Método principal para renderizar el gráfico completo.
        Llama a todos los métodos necesarios en el orden correcto.
        """
        self.prepare_data()
        self.setup_dimensions()
        self.create_figure()
        self.draw_chart()
        self.configure_axes()
        self.add_legend()
        self.add_labels()
        self.add_title()
        self.add_footer()
        self.finalize()