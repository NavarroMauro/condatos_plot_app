from pathlib import Path
import typer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.plots.base_chart import BaseChart

class VerticalBarChart(BaseChart):
    """
    Clase para gráficos de barras verticales.
    Hereda de BaseChart e implementa los métodos específicos para este tipo de gráfico.
    """
    def setup_dimensions(self):
        """Configura las dimensiones del gráfico basado en el contenido."""
        autosize = self.params.get("autosize", {})
        if autosize.get("enabled", False) or True:  # Siempre usar el autoajuste como en stackedbarh
            # Calcular ancho basado en el número de categorías
            n_cols = len(self.cats)
            width_per_col = float(autosize.get("width_per_col", 0.6))
            
            # Calcular ancho total necesario
            total_width = n_cols * width_per_col
            
            # Aplicar límites min/max
            width_in = min(
                float(autosize.get("max_width", 12)),
                max(float(autosize.get("min_width", 6)), total_width)
            )
            
            # Añadir ancho adicional para títulos grandes si se especifica
            add_width_ratio = float(autosize.get("add_width_ratio", 0))
            if add_width_ratio > 0:
                width_in += width_in * add_width_ratio
                print(f"📏 Añadiendo {add_width_ratio*100:.1f}% de ancho extra para títulos grandes")
            
            # Altura proporcional al contenido
            text_length = max(len(str(cat)) for cat in self.cats)
            base_height = float(autosize.get("base_height", 6))
            height_adjustment = text_length * 0.1
            height_in = base_height + height_adjustment if autosize.get("adjust_height", False) else float(self.params.get("height_in", 6))
        else:
            width_in = float(self.params.get("width_in", 8))
            height_in = float(self.params.get("height_in", 6))

        self.params.update({
            "width_in": width_in,
            "height_in": height_in
        })
        
    def create_figure(self):
        """Crea la figura con las dimensiones adecuadas y configura los ejes."""
        super().create_figure()  # Llama al método de la clase base
        
        # Configuración adicional específica para barras verticales
        margins_config = self.params.get("margins", {})
        auto_adjust = margins_config.get("auto_adjust", False)  # Por defecto, no ajustar automáticamente
        margin_left = float(margins_config.get("left", 0.10))
        margin_right = float(margins_config.get("right", 0.02))
        margin_bottom = float(margins_config.get("bottom", 0.12))
        margin_top = float(margins_config.get("top", 0.25))  # Espacio para header
        
        # Si hay etiquetas rotadas, ajustar el margen inferior
        if self.params.get("rotate_xticks"):
            xtick_config = self.params.get("xtick_config", {})
            margin_bottom = float(xtick_config.get("bottom_space", margin_bottom))
        
        # Calcular y aplicar los márgenes
        self.ax.set_position([margin_left, margin_bottom, 1.0-margin_left-margin_right, 1.0-margin_bottom-margin_top])
        
        print(f"ℹ️ Márgenes aplicados: izq={margin_left:.2f}, der={margin_right:.2f}, inf={margin_bottom:.2f}, sup={margin_top:.2f}")
        
        return self.fig

    def prepare_data(self):
        """Prepara los datos para el gráfico."""
        # Determinar columna de categorías
        cat_col_from_params = self.params.get("data", {}).get("category_col")
        self.cat_col = cat_col_from_params if cat_col_from_params else self.df.columns[0]
        
        print(f"🔍 En prepare_data: Usando columna de categorías: '{self.cat_col}'")
        
        # Determinar columna para los valores
        value_col = self.params.get("data", {}).get("value_col")
        
        if value_col and value_col in self.df.columns:
            self.value_col = value_col
            print(f"🔍 Usando columna de valores: '{self.value_col}'")
        else:
            # Si no se especifica una columna de valores, intentar detectar automáticamente
            numeric_cols = [c for c in self.df.columns if c != self.cat_col and 
                           pd.api.types.is_numeric_dtype(self.df[c])]
            
            if not numeric_cols:
                raise ValueError("No se encontraron columnas numéricas en el DataFrame")
            
            # Usar la primera columna numérica disponible
            self.value_col = numeric_cols[0]
            print(f"🔍 Usando primera columna numérica como valores: '{self.value_col}'")
        
        # Preparar datos
        self.cats = self.df[self.cat_col].astype(str).tolist()
        values = self.df[self.value_col].astype(float).tolist()
        
        # Aplicar transformación de valores si está configurada
        transform_values = self.params.get("data", {}).get("transform_values", False)
        if transform_values:
            # Por defecto, convertir de millones a miles de millones
            divisor = float(self.params.get("data", {}).get("value_divisor", 1000))
            values = [val / divisor for val in values]
            print(f"🔄 Transformando valores: dividiendo por {divisor}")
            
        self.values = values
        
        # Ordenar si se especifica
        if self.params.get("sort_by_value", False):
            # Crear pares (categoría, valor) para ordenar
            cat_val_pairs = list(zip(self.cats, self.values))
            
            # Ordenar por valores
            invert_order = self.params.get("invert_order", False)
            if invert_order:
                # Orden ascendente
                cat_val_pairs.sort(key=lambda x: x[1])
                print("🔄 Aplicando orden ASCENDENTE (de menor a mayor)")
            else:
                # Orden descendente (por defecto)
                cat_val_pairs.sort(key=lambda x: x[1], reverse=True)
                print("🔄 Aplicando orden DESCENDENTE (de mayor a menor)")
            
            # Desempaquetar las listas ordenadas
            self.cats, self.values = zip(*cat_val_pairs)
            
            # Convertir a listas
            self.cats = list(self.cats)
            self.values = list(self.values)
            
            # Imprimir información de depuración
            print("📊 Primeras 5 categorías después de ordenar:")
            for i, (cat, val) in enumerate(zip(self.cats[:5], self.values[:5])):
                print(f"  - {i+1}: {cat} = {val}")
        
    def draw_chart(self):
        """Dibuja las barras verticales."""
        # Obtener configuración de barras
        bar_config = self.params.get("bar", {})
        bar_width = float(bar_config.get("width", 0.7))
        bar_edgecolor = bar_config.get("edgecolor", "white")
        bar_linewidth = float(bar_config.get("linewidth", 0.5))
        bar_color = bar_config.get("color", "#1F6FEB")  # Color por defecto
        
        # Imprimir la configuración para depuración
        print("📊 Configuración de barras:")
        print(f"  - Ancho: {bar_width:.2f}")
        print(f"  - Color: {bar_color}")
        print(f"  - Color del borde: {bar_edgecolor}")
        print(f"  - Grosor del borde: {bar_linewidth:.2f}")
        
        # Posiciones de las barras
        self.x_positions = np.arange(len(self.cats))
        
        # Dibujar barras
        self.bars = self.ax.bar(
            self.x_positions, self.values, 
            width=bar_width,
            color=bar_color,
            edgecolor=bar_edgecolor,
            linewidth=bar_linewidth
        )
            
        # Añadir etiquetas de valores en las barras
        if bool(self.params.get("value_labels", False)):
            # Obtener configuración de etiquetas de valores
            value_labels_config = (
                self.params.get("value_labels_config", {}) 
                if isinstance(self.params.get("value_labels"), bool) 
                else self.params.get("value_labels", {})
            )
            
            # Obtener tamaño de fuente y formato
            font_size = float(value_labels_config.get("font_size", 9))
            font_weight = value_labels_config.get("font_weight", "normal")
            fmt = self.params.get("value_format", "{:.0f}")
            
            # Si el formato contiene una coma (,), usamos format para números con miles separados
            if fmt.find(",") >= 0:
                print(f"📊 Usando formato con separador de miles: {fmt}")
                formatter = lambda x: f"{x:{fmt}}"
            else:
                # Formato estándar sin separador de miles
                formatter = lambda x: fmt.format(x)
            
            # Imprimir información de configuración para depuración
            print("📊 Configuración de etiquetas de valores:")
            print(f"  - Tamaño de fuente: {font_size}")
            print(f"  - Peso de fuente: {font_weight}")
            print(f"  - Formato: {fmt}")
            
            # Configurar la posición vertical de las etiquetas
            vertical_alignment = value_labels_config.get("va", "bottom")
            label_padding = float(value_labels_config.get("padding", 3))
            
            for i, rect in enumerate(self.bars):
                # Valor de la barra
                value = self.values[i]
                
                # Calcular posición para la etiqueta
                height = rect.get_height()
                if vertical_alignment == "bottom":
                    # Colocar etiqueta dentro de la barra en la parte inferior
                    y_pos = height / 2
                    text_color = value_labels_config.get("color_inside", "white")
                elif vertical_alignment == "inside":
                    # Colocar etiqueta dentro de la barra
                    y_pos = height / 2
                    text_color = value_labels_config.get("color_inside", "white")
                else:
                    # Colocar etiqueta encima de la barra
                    y_pos = height + label_padding
                    text_color = value_labels_config.get("color", "black")
                
                self.ax.text(
                    rect.get_x() + rect.get_width() / 2, 
                    y_pos,
                    formatter(value),
                    ha='center', 
                    va='center' if vertical_alignment in ["bottom", "inside"] else 'bottom',
                    color=text_color,
                    fontsize=font_size,
                    fontweight=font_weight
                )

    def configure_axes(self):
        """Configura los ejes y sus elementos."""
        # Configuración de ejes
        self.ax.set_xticks(self.x_positions)
        # No mostrar los nombres de los países en el eje X (se mostrarán arriba de cada barra)
        self.ax.set_xticklabels([])
        
        # Margen superior con padding (aumentado para dar espacio a las etiquetas de país)
        max_value = max(self.values)
        
        # Calcular el espacio adicional necesario basado en la configuración
        country_labels_config = self.params.get("country_labels_config", {})
        top_margin_factor = float(country_labels_config.get("top_margin", 0.30))
        
        # Aplicar margen superior
        self.ax.set_ylim(0, max_value * (1 + top_margin_factor))  # Por defecto 30% de margen arriba
        
        # Configurar etiquetas de ejes
        if self.params.get("xlabel"):
            self.ax.set_xlabel(self.params.get("xlabel"))
        
        if self.params.get("ylabel"):
            self.ax.set_ylabel(self.params.get("ylabel"))
        
        # Configurar rotación de etiquetas del eje X
        if self.params.get("rotate_xticks"):
            rotation = float(self.params.get("rotate_xticks"))
            
            # Opciones avanzadas para la rotación de etiquetas
            xtick_config = self.params.get("xtick_config", {})
            
            # Alineación horizontal: 'right', 'center' o 'left'
            ha = xtick_config.get("ha", "right")
            
            # Aplicar rotación a las etiquetas
            self.ax.set_xticklabels(self.cats, rotation=rotation, ha=ha)
            
            # Ajustar manualmente la figura para dar espacio a las etiquetas rotadas
            # El espacio inferior se puede configurar o usar un valor predeterminado
            bottom_space = xtick_config.get("bottom_space", 0.24)  # Valor predeterminado
            self.fig.subplots_adjust(bottom=float(bottom_space))
            
            print(f"ℹ️ Ajustando espaciado inferior para etiquetas rotadas: {bottom_space:.2f}")
            
            # Verificar si se necesita ajuste adicional para etiquetas largas
            if xtick_config.get("adjust_for_long_labels", False):
                # Usar un enfoque más robusto y compatible para etiquetas largas
                self.fig.canvas.draw()
                
                # En lugar de tight_layout, ajustamos manualmente los márgenes
                # Obtener altura de las etiquetas del eje X
                renderer = self.fig.canvas.get_renderer()
                
                # Asegurar que las etiquetas no se superponen con el footer
                bottom_space_adjusted = bottom_space
                if xtick_config.get("text_padding", True):
                    # Añadir un poco más de espacio para mayor seguridad
                    bottom_space_adjusted += 0.01
                
                # Aplicar el ajuste final
                self.fig.subplots_adjust(bottom=bottom_space_adjusted)
                print(f"✓ Ajuste adicional aplicado para etiquetas de texto largas (espacio inferior: {bottom_space_adjusted:.2f})")
        
        # Grid opcional
        if self.params.get("grid", False):
            self.ax.grid(axis='y', linestyle='--', alpha=0.3, color='#cccccc')
            self.ax.set_axisbelow(True)  # Grid detrás de las barras
        
        # Personalización de ejes X e Y
        xaxis_config = self.params.get("xaxis", {})
        yaxis_config = self.params.get("yaxis", {})
        
        # Ocultar etiquetas del eje Y si se especifica
        if not yaxis_config.get("show_labels", True):
            self.ax.set_yticklabels([])
        
        # Ocultar etiquetas del eje X si se especifica
        if not xaxis_config.get("show_labels", True):
            self.ax.set_xticklabels([])
        
        # Eliminar spines innecesarios
        spines_to_hide = ["top", "right"]
        
        # Si se especifica, ocultar también spines izquierdo y/o inferior
        if not yaxis_config.get("show_ticks", True):
            spines_to_hide.append("left")
            # Ocultar solamente los ticks, manteniendo las etiquetas si show_labels es True
            self.ax.tick_params(axis='y', which='both', left=False, labelleft=yaxis_config.get("show_labels", True))
            
        if not xaxis_config.get("show_ticks", True):
            # Solo ocultar el spine si se indica explícitamente
            if not xaxis_config.get("show_spine", True):
                spines_to_hide.append("bottom")
            # Ocultar los ticks del eje X, manteniendo las etiquetas si show_labels es True
            self.ax.tick_params(axis='x', which='both', bottom=False, labelbottom=xaxis_config.get("show_labels", False))
            
        # Ocultar spines según configuración
        for spine in spines_to_hide:
            self.ax.spines[spine].set_visible(False)
        
        # Aplicar estilos de fuente a las etiquetas si están visibles
        if xaxis_config.get("show_labels", True) and "font" in xaxis_config:
            font_cfg = xaxis_config["font"]
            for label in self.ax.get_xticklabels():
                label.set_fontsize(font_cfg.get("size", 9))
                label.set_color(font_cfg.get("color", "#333333"))
        
        if yaxis_config.get("show_labels", True) and "font" in yaxis_config:
            font_cfg = yaxis_config["font"]
            for label in self.ax.get_yticklabels():
                label.set_fontsize(font_cfg.get("size", 9))
                label.set_color(font_cfg.get("color", "#333333"))
    
    def add_labels(self):
        """
        Añade etiquetas de país arriba de cada barra y etiquetas de valor si están configuradas.
        """
        # Añadir etiquetas de país arriba de cada barra
        for i, (bar, cat) in enumerate(zip(self.bars, self.cats)):
            # Obtener altura de la barra
            height = bar.get_height()
            
            # Configuración para etiquetas de país
            country_labels_config = self.params.get("country_labels_config", {})
            font_size = float(country_labels_config.get("font_size", 9))
            font_weight = country_labels_config.get("font_weight", "normal")
            font_color = country_labels_config.get("color", "#333333")  
            rotation = float(country_labels_config.get("rotation", 0))
            padding = float(country_labels_config.get("padding", 8))
            
            # Posicionar texto arriba de la barra con padding
            # Calcular posición vertical basada en el valor máximo del eje Y
            y_max = self.ax.get_ylim()[1]
            padding_factor = float(country_labels_config.get("padding_factor", 0.08))
            y_position = height + (y_max * padding_factor)
            
            # Determinar si se deben mostrar valores
            show_values = country_labels_config.get("show_values", False)
            value = self.values[i]
            
            # Posición para la etiqueta del país
            country_x = bar.get_x() + bar.get_width() / 2
            country_y = y_position
            
            # Añadir etiqueta del país
            self.ax.text(
                country_x,
                country_y,
                cat,
                ha='center', 
                va='bottom',
                fontsize=font_size,
                fontweight=font_weight,
                color=font_color,
                rotation=rotation
            )
            
            # Añadir etiqueta del valor debajo del nombre del país si está habilitado
            if show_values:
                # Formato para el valor
                value_format = self.params.get("value_format", "{:.0f}")
                
                # Si el formato contiene una coma (,), usamos format para números con miles separados
                if value_format.find(",") >= 0:
                    formatter = lambda x: f"{x:{value_format}}"
                else:
                    # Formato estándar sin separador de miles
                    formatter = lambda x: value_format.format(x)
                
                # Configuración para la etiqueta de valor
                value_font_size = float(country_labels_config.get("value_font_size", font_size * 0.9))
                value_font_weight = country_labels_config.get("value_font_weight", "normal")
                value_color = country_labels_config.get("value_color", font_color)
                value_padding = float(country_labels_config.get("value_padding", 0.02))
                
                # Calcular la posición Y para el valor (debajo del país)
                value_y = country_y - (y_max * value_padding)
                
                # Añadir texto del valor debajo del país
                self.ax.text(
                    country_x, 
                    value_y,
                    formatter(value),
                    ha='center', 
                    va='top',
                    fontsize=value_font_size,
                    fontweight=value_font_weight,
                    color=value_color
                )
        
        # Usar método de la clase base si hay etiquetas de totales configuradas
        if self.params.get("total_labels", {}).get("enabled", False):
            super().add_labels()

    def add_title(self):
        """
        Añade título y subtítulo en un área dedicada sobre el gráfico con opciones avanzadas.
        Permite controlar el espaciado vertical y horizontal y usar fuentes personalizadas.
        """
        # Obtener configuración de títulos
        title_config = self.params.get("title_config", {})
        subtitle_config = self.params.get("subtitle_config", {})
        title_spacing = self.params.get("title_spacing", {})
        
        # Espaciado vertical para título y subtítulo
        title_top_margin = float(title_spacing.get("top_margin", 0.15))  # Espacio arriba del título
        title_bottom_margin = float(title_spacing.get("bottom_margin", 0.1))  # Espacio debajo del título
        subtitle_top_margin = float(title_spacing.get("subtitle_top_margin", 0.05))  # Espacio entre título y subtítulo
        
        # Espaciado horizontal para título y subtítulo (márgenes globales)
        left_margin = float(title_spacing.get("left_margin", 0.0))  # Margen izquierdo global
        right_margin = float(title_spacing.get("right_margin", 0.0))  # Margen derecho global
        
        print("\nℹ️ Configuración de espaciado de títulos:")
        print(f"  - Espacio superior del título: {title_top_margin:.2f} (desde borde superior)")
        print(f"  - Espacio entre título y subtítulo: {title_bottom_margin:.2f} + {subtitle_top_margin:.2f}")
        print(f"  - Márgenes horizontales globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
        
        # Obtener contenido de título y subtítulo
        title = self.params.get("title", "")
        subtitle = self.params.get("subtitle", "")
        
        # Si no hay configuración avanzada, usar el modo compatible con versiones anteriores
        if not title_config and title:
            # Posición horizontal y vertical
            x_pos = self.params.get("title_x_position", 0.5)
            y_pos = 1.0 - title_top_margin  # Posicionar desde la parte superior con el margen
            
            # Alineación horizontal y vertical
            ha = self.params.get("title_horizontal_alignment", "center")
            va = self.params.get("title_vertical_alignment", "top")  # Alineado hacia arriba
            
            # Propiedades de texto
            fontsize = float(self.params.get("title_font_size", 18))
            fontweight = self.params.get("title_font_weight", "bold")
            color = self.params.get("title_color", "#333333")
            fontfamily = self.params.get("title_font_family", "Nunito")  # Usar Nunito por defecto
            fontstyle = self.params.get("title_font_style", "normal")
            bbox = self.params.get("title_bbox", None)
            
            self.ax_header.text(x_pos, y_pos, title, 
                                ha=ha, va=va,
                                fontsize=fontsize,
                                fontweight=fontweight,
                                color=color,
                                family=fontfamily,
                                style=fontstyle,
                                bbox=bbox,
                                transform=self.ax_header.transAxes)
        elif title_config and title:
            # Usar configuración avanzada
            ha = title_config.get("ha", "center")
            padding_left = float(title_config.get("padding_left", 0.0))  # Padding izquierdo específico del título
            padding_right = float(title_config.get("padding_right", 0.0))  # Padding derecho específico del título
            
            # Calcular ancho disponible después de aplicar márgenes globales
            available_width = 1.0 - left_margin - right_margin
            
            # Calcular posición X final basada en alineación
            if ha == "left":
                x_pos = left_margin + padding_left
            elif ha == "right":
                x_pos = 1.0 - right_margin - padding_right
            else:  # center u otros
                x_pos = left_margin + (available_width / 2)
            
            # SIEMPRE calcular la posición Y basada en el margen superior
            y_pos = 1.0 - title_top_margin
            
            # Debug para ver los valores calculados
            print("DEBUG: Márgenes horizontales aplicados al título:")
            print(f"  - Márgenes globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
            print(f"  - Paddings específicos: izquierdo={padding_left:.2f}, derecho={padding_right:.2f}")
            print(f"  - Posición X calculada: {x_pos:.2f} (alineación='{ha}')")
            print(f"DEBUG: Posición Y calculada para título = {y_pos:.2f} (basada en top_margin = {title_top_margin:.2f})")
            
            # Usar siempre la misma alineación vertical para consistencia
            ha = title_config.get("ha", "center")
            va = "top"  # Fijar siempre a 'top' para evitar inconsistencias
            
            # Propiedades avanzadas del texto
            explicit_fontsize = self.params.get("_explicit_title_fontsize", None)
            config_fontsize = title_config.get("fontsize", None)
            global_fontsize = self.params.get("title_font_size", 18)
            
            # Mostrar los valores para depuración
            print("DEBUG: Valores de tamaño para el título:")
            print(f" - Valor explícito guardado: {explicit_fontsize}")
            print(f" - Valor en title_config.fontsize: {config_fontsize}")
            print(f" - Valor en params.title_font_size: {global_fontsize}")
            
            # Precedencia: Valor explícito > Valor en title_config > Valor global
            if explicit_fontsize is not None:
                fontsize = float(explicit_fontsize)
                print(f"Título (modo explícito): Tamaño = {fontsize}")
            elif config_fontsize is not None:
                fontsize = float(config_fontsize)
                print(f"Título (modo avanzado): Tamaño = {fontsize}, Color = {title_config.get('color', '#333333')}")
            else:
                fontsize = float(global_fontsize)
                print(f"Título (modo básico): Tamaño = {fontsize}")
            
            text_props = {
                "fontsize": fontsize,
                "fontweight": title_config.get("fontweight", self.params.get("title_font_weight", "bold")),
                "color": title_config.get("color", self.params.get("title_color", "#333333")),
                "family": title_config.get("family", "Nunito"),  # Usar Nunito por defecto
                "style": title_config.get("style", "normal"),
                "rotation": title_config.get("rotation", 0),
                "linespacing": title_config.get("linespacing", 1.2),
            }
            
            # Imprimir propiedades para depuración
            print("DEBUG: Aplicando propiedades al título:")
            for key, value in text_props.items():
                print(f"  - {key}: {value}")
            
            # Añadir el título al gráfico
            print(f"\nℹ️ Colocando título en posición: x={x_pos:.2f}, y={y_pos:.2f}, va='{va}', ha='{ha}'")
            title_artist = self.ax_header.text(x_pos, y_pos, title, 
                                ha=ha, va=va,
                                transform=self.ax_header.transAxes,
                                **text_props)
            
            # Aplicar wrapping manual para el texto largo
            if title_config.get("word_wrap", False) or title_config.get("wrap", False):
                try:
                    import textwrap
                    wrap_width = title_config.get("width", 0.85)
                    
                    # Ajustar el ancho de wrapping considerando los márgenes horizontales
                    available_width = 1.0 - left_margin - right_margin
                    padding_left = float(title_config.get("padding_left", 0.0))
                    padding_right = float(title_config.get("padding_right", 0.0))
                    
                    # El ancho efectivo disponible se reduce por los márgenes y paddings
                    effective_wrap_width = available_width * wrap_width - padding_left - padding_right
                    
                    print("📝 Aplicando ajuste automático de texto al título:")
                    print(f"  - Ancho de wrapping base: {wrap_width:.2f}")
                    print(f"  - Ancho disponible tras márgenes: {available_width:.2f}")
                    print(f"  - Ancho efectivo para wrapping: {effective_wrap_width:.2f}")
                    
                    # Obtener ancho de figura en pulgadas
                    fig_width_inches = self.fig.get_figwidth()
                    # Convertir wrap_width de fracción a pulgadas, considerando el ancho efectivo
                    wrap_width_inches = fig_width_inches * effective_wrap_width
                    
                    # Obtener el título actual
                    current_text = title_artist.get_text()
                    # Calcular aproximadamente cuántos caracteres caben en el ancho deseado
                    # Este es un cálculo aproximado basado en el tamaño de fuente
                    fontsize = float(title_artist.get_fontsize())
                    # Estimar caracteres por pulgada (aproximación)
                    chars_per_inch = 72.0 / (fontsize * 0.55)  # Factor 0.55 permite más caracteres por línea
                    # Ajustar para fuentes más grandes
                    if fontsize > 28:
                        # Ajuste más suave para títulos grandes para permitir más texto por línea
                        factor = max(0.7, 28 / fontsize)  # Limitar el factor de reducción a 0.7
                        chars_per_inch = chars_per_inch * factor
                        print(f"  - Ajustando estimación para fuente grande ({fontsize}pt): factor = {factor:.2f}")
                    
                    # Añadir un 10% adicional de caracteres para usar más espacio
                    max_chars = int(wrap_width_inches * chars_per_inch * 1.10)
                    
                    # Envolver texto con un mínimo de caracteres razonable
                    max_chars = max(25, max_chars)  # Asegurar al menos 25 caracteres por línea
                    wrapped_text = textwrap.fill(current_text, width=max_chars)
                    
                    # Actualizar texto con versión envuelta
                    title_artist.set_text(wrapped_text)
                    
                    # Contar cuántas líneas resultaron
                    num_lines = len(wrapped_text.split('\n'))
                    print(f"✅ Texto ajustado: {max_chars} caracteres por línea, {num_lines} línea(s) total")
                    
                except Exception as e:
                    print(f"⚠️ Error al aplicar wrapping manual al título: {e}")
            
            # Guardar la posición final del título para posicionar el subtítulo si es necesario
            self.title_artist = title_artist
        
        # Gestionar el subtítulo
        if subtitle:
            # Calcular posición del subtítulo basada en la posición del título
            if hasattr(self, 'title_artist') and self.title_artist:
                # Calcula la posición Y del subtítulo basada en la posición del título
                title_pos = self.title_artist.get_position()[1]
                y_pos = title_pos - title_bottom_margin - subtitle_top_margin
                print(f"ℹ️ Posición del subtítulo calculada a partir del título: {y_pos:.2f}")
            else:
                y_pos = 1.0 - title_top_margin - title_bottom_margin - subtitle_top_margin
                print(f"ℹ️ Posición del subtítulo calculada sin referencia al título: {y_pos:.2f}")
            
            # Configuración de subtítulo
            if not subtitle_config:
                # Configuración básica para compatibilidad
                x_pos = self.params.get("subtitle_x_position", 0.5)
                ha = self.params.get("subtitle_horizontal_alignment", "center")
                va = "top"  # Alineado hacia arriba
                
                fontsize = float(self.params.get("subtitle_font_size", 13))
                color = self.params.get("subtitle_color", "#666666")
                fontfamily = self.params.get("subtitle_font_family", "Nunito")  # Usar Nunito por defecto
                fontstyle = self.params.get("subtitle_font_style", "normal")
                
                self.ax_header.text(x_pos, y_pos, subtitle, 
                                    ha=ha, va=va,
                                    fontsize=fontsize,
                                    color=color,
                                    family=fontfamily,
                                    style=fontstyle,
                                    transform=self.ax_header.transAxes)
            else:
                # Usar configuración avanzada para el subtítulo
                ha = subtitle_config.get("ha", "center")
                padding_left = float(subtitle_config.get("padding_left", 0.0))
                padding_right = float(subtitle_config.get("padding_right", 0.0))
                
                # Calcular ancho disponible después de aplicar márgenes globales
                available_width = 1.0 - left_margin - right_margin
                
                # Calcular posición X final basada en alineación
                if ha == "left":
                    x_pos = left_margin + padding_left
                elif ha == "right":
                    x_pos = 1.0 - right_margin - padding_right
                else:  # center u otros
                    x_pos = left_margin + (available_width / 2)
                
                # Debug para ver los valores calculados
                print("DEBUG: Márgenes horizontales aplicados al subtítulo:")
                print(f"  - Márgenes globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
                print(f"  - Paddings específicos: izquierdo={padding_left:.2f}, derecho={padding_right:.2f}")
                print(f"  - Posición X calculada: {x_pos:.2f} (alineación='{ha}')")
                
                va = "top"  # Fijar siempre a 'top' para evitar inconsistencias
                
                # Propiedades avanzadas para el subtítulo
                explicit_fontsize = self.params.get("_explicit_subtitle_fontsize", None)
                config_fontsize = subtitle_config.get("fontsize", None)
                global_fontsize = self.params.get("subtitle_font_size", 13)
                
                # Mostrar los valores para depuración
                print("DEBUG: Valores de tamaño para el subtítulo:")
                print(f" - Valor explícito guardado: {explicit_fontsize}")
                print(f" - Valor en subtitle_config.fontsize: {config_fontsize}")
                print(f" - Valor en params.subtitle_font_size: {global_fontsize}")
                
                # Precedencia: Valor explícito > Valor en subtitle_config > Valor global
                if explicit_fontsize is not None:
                    fontsize = float(explicit_fontsize)
                    print(f"Subtítulo (modo explícito): Tamaño = {fontsize}")
                elif config_fontsize is not None:
                    fontsize = float(config_fontsize)
                    print(f"Subtítulo (modo avanzado): Tamaño = {fontsize}, Color = {subtitle_config.get('color', '#666666')}")
                else:
                    fontsize = float(global_fontsize)
                    print(f"Subtítulo (modo básico): Tamaño = {fontsize}")
                    
                color = subtitle_config.get("color", self.params.get("subtitle_color", "#666666"))
                
                text_props = {
                    "fontsize": fontsize,
                    "color": color,
                    "family": subtitle_config.get("family", "Nunito"),  # Usar Nunito por defecto
                    "style": subtitle_config.get("style", "normal"),
                    "rotation": subtitle_config.get("rotation", 0),
                    "linespacing": subtitle_config.get("linespacing", 1.0),
                }
                
                # Opciones para el cuadro de fondo (si se especifica)
                if "bbox" in subtitle_config:
                    text_props["bbox"] = subtitle_config.get("bbox")
                
                # Imprimir propiedades para depuración
                print("DEBUG: Aplicando propiedades al subtítulo:")
                for key, value in text_props.items():
                    print(f"  - {key}: {value}")
                    
                subtitle_artist = self.ax_header.text(x_pos, y_pos, subtitle, 
                                ha=ha, va=va,
                                transform=self.ax_header.transAxes,
                                **text_props)
                
                # Aplicar wrapping manual para el texto largo
                if subtitle_config.get("wrap", False):
                    try:
                        import textwrap
                        wrap_width = subtitle_config.get("width", 0.85)
                        
                        # Ajustar el ancho de wrapping considerando los márgenes horizontales
                        available_width = 1.0 - left_margin - right_margin
                        padding_left = float(subtitle_config.get("padding_left", 0.0))
                        padding_right = float(subtitle_config.get("padding_right", 0.0))
                        
                        # El ancho efectivo disponible se reduce por los márgenes y paddings
                        effective_wrap_width = available_width * wrap_width - padding_left - padding_right
                        
                        print("Aplicando ajuste manual de texto al subtítulo:")
                        print(f"  - Ancho de wrapping base: {wrap_width:.2f}")
                        print(f"  - Ancho disponible tras márgenes: {available_width:.2f}")
                        print(f"  - Ancho efectivo para wrapping: {effective_wrap_width:.2f}")
                        
                        # Obtener ancho de figura en pulgadas
                        fig_width_inches = self.fig.get_figwidth()
                        # Convertir wrap_width de fracción a pulgadas, considerando el ancho efectivo
                        wrap_width_inches = fig_width_inches * effective_wrap_width
                        
                        # Obtener el subtítulo actual
                        current_text = subtitle_artist.get_text()
                        # Calcular aproximadamente cuántos caracteres caben en el ancho deseado
                        fontsize = float(subtitle_artist.get_fontsize())
                        # Estimar caracteres por pulgada (aproximación)
                        chars_per_inch = 72.0 / (fontsize * 0.6)  # Factor 0.6 es una aproximación
                        max_chars = int(wrap_width_inches * chars_per_inch)
                        
                        # Envolver texto
                        wrapped_text = textwrap.fill(current_text, width=max_chars)
                        
                        # Actualizar texto con versión envuelta
                        subtitle_artist.set_text(wrapped_text)
                        
                        print(f"✅ Subtítulo ajustado manualmente: {max_chars} caracteres por línea")
                        
                    except Exception as e:
                        print(f"⚠️ Error al aplicar wrapping manual al subtítulo: {e}")
    
    def add_footer(self):
        """
        Añade un footer con logo y texto en la parte inferior del gráfico.
        Utiliza la implementación centralizada de branding.py para evitar duplicación.
        """
        from app.branding import add_footer
        
        # Usar la función centralizada para añadir el footer
        add_footer(self.fig, self.params.get("footer", {}))
    
    def finalize(self):
        """
        Finaliza y guarda el gráfico.
        Nota: add_branding ya se llama desde el método add_footer,
        por lo que finish_and_save no debe volver a llamar a add_branding.
        """
        # Usar la función centralizada para guardar en múltiples formatos
        from app.io_utils import save_fig_multi
        
        # Guardar en los formatos especificados
        if "outfile" in self.params:
            formatos = self.params.get("formats", ["png"])
            
            # Asegurar que outfile es un Path
            if isinstance(self.params["outfile"], str):
                outfile = Path(self.params["outfile"])
            else:
                outfile = self.params["outfile"]
                
            # Llamar a la función de guardado multi-formato
            save_fig_multi(
                fig=self.fig,
                base=outfile,
                formats=formatos,
                jpg_quality=int(self.params.get("jpg_quality", 92)),
                webp_quality=int(self.params.get("webp_quality", 92)),
                avif_quality=int(self.params.get("avif_quality", 55)),
                scour_svg=self.params.get("scour_svg", True)
            )


def barv(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    """Gráfico de barras verticales con elementos básicos de matplotlib."""
    from app.chart_utils import render_chart
    
    # Usar la función genérica para renderizar el gráfico
    render_chart(VerticalBarChart, config)

def add_command(app: typer.Typer) -> None:
    app.command("barv")(barv)

if __name__ == "__main__":
    # Para pruebas directas
    import sys
    if len(sys.argv) > 1:
        barv(Path(sys.argv[1]))
    else:
        print("Uso: python barv.py ruta/al/config.yml")