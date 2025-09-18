from pathlib import Path
import typer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.plots.base_chart import BaseChart

class StackedHorizontalBarChart(BaseChart):
    """
    Clase para gráficos de barras horizontales apiladas.
    Hereda de BaseChart e implementa los métodos específicos para este tipo de gráfico.
    """
    def setup_dimensions(self):
        """Configura las dimensiones del gráfico basado en el contenido."""
        autosize = self.params.get("autosize", {})
        if autosize.get("enabled", False) or True:  # Siempre usar el autoajuste
            # Calcular altura basada en el número de categorías
            n_rows = len(self.df)
            height_per_row = float(autosize.get("height_per_row", 0.18))
            
            # Calcular altura total necesaria
            total_height = n_rows * height_per_row
            
            # Aplicar límites min/max
            height_in = min(
                float(autosize.get("max_height", 8)),
                max(float(autosize.get("min_height", 5)), total_height)
            )
            
            # Añadir altura adicional para títulos grandes si se especifica
            add_height_ratio = float(autosize.get("add_height_ratio", 0))
            if add_height_ratio > 0:
                height_in += height_in * add_height_ratio
                print(f"📏 Añadiendo {add_height_ratio*100:.1f}% de altura extra para títulos grandes")
            
            # Ancho proporcional al contenido
            text_length = max(len(str(cat)) for cat in self.cats)
            base_width = 12
            width_adjustment = text_length * 0.2
            width_in = base_width + width_adjustment
        else:
            width_in = float(self.params.get("width_in", 12))
            height_in = float(self.params.get("height_in", 6))

        self.params.update({
            "width_in": width_in,
            "height_in": height_in
        })
        
    def prepare_data(self):
        """Prepara los datos para el gráfico y los ordena."""
        # Determinar columna de categorías
        cat_col_from_params = self.params.get("data", {}).get("category_col")
        self.cat_col = cat_col_from_params if cat_col_from_params else self.df.columns[0]
        
        print(f"🔍 En prepare_data: Usando columna de categorías: '{self.cat_col}'")
        
        # Determinar columnas para las series
        self.cols = self._get_series_columns()
        
        # Aplicar filtrado por valor mínimo si está configurado
        filter_min_value = self.params.get("chart", {}).get("filter_min_value", None)
        
        if filter_min_value is not None and filter_min_value > 0:
            print(f"🔍 Aplicando filtro de valor mínimo: {filter_min_value}")
            # Calcular totales antes de filtrar para mensajes informativos
            pre_filter_len = len(self.df)
            
            # Crear una columna de totales temporalmente para el filtrado
            temp_df = self.df.copy()
            temp_df['_temp_total'] = temp_df[self.cols].sum(axis=1)
            
            # Filtrar usando el método de la clase base
            self.df = self.filter_by_threshold(
                temp_df, 
                total_column='_temp_total', 
                threshold=filter_min_value, 
                category_column=self.cat_col
            )
            
            # Eliminar la columna temporal
            self.df.drop('_temp_total', axis=1, inplace=True)
            
            post_filter_len = len(self.df)
            if pre_filter_len > post_filter_len:
                print(f"✅ Filtrado completado: Quedaron {post_filter_len} de {pre_filter_len} elementos.")
        
        # Preparar matriz de datos
        self.M = np.vstack([self.df[c].astype(float).to_numpy() for c in self.cols])
        
        # Calcular totales por categoría para ordenamiento (por defecto suma de todas las series)
        self.totals = self.M.sum(axis=0)
        # Permitir columna de ordenamiento personalizada
        sort_by_column = self.params.get("sort_by_column")
        if sort_by_column is not None:
            # Ordenar por la columna especificada
            if sort_by_column not in self.df.columns:
                raise KeyError(f"La columna para ordenar '{sort_by_column}' no existe en el DataFrame. Columnas disponibles: {list(self.df.columns)}")
            sort_values = self.df[sort_by_column].astype(float).to_numpy()
            invert_order = self.params.get("invert_order", False)
            if invert_order:
                sorted_indices = np.argsort(sort_values)
                print(f"🔄 Aplicando orden ASCENDENTE (de menor a mayor) por columna '{sort_by_column}'")
            else:
                sorted_indices = np.argsort(-sort_values)
                print(f"🔄 Aplicando orden DESCENDENTE (de mayor a menor) por columna '{sort_by_column}'")
            self.M = self.M[:, sorted_indices]
            self.totals = self.totals[sorted_indices]
            self.cats = [self.df[self.cat_col].astype(str).tolist()[i] for i in sorted_indices]
            print("📊 Primeros 5 nombres de países después de ordenar:")
            for i, cat in enumerate(self.cats[:5]):
                print(f"  - {i+1}: {cat}")
            self.df = self.df.iloc[sorted_indices].reset_index(drop=True)
        # Si no se especifica columna, usar el comportamiento anterior (por total)
        elif self.params.get("sort_by_total", True):
            invert_order = self.params.get("invert_order", False)
            if invert_order:
                sorted_indices = np.argsort(self.totals)
                print("🔄 Aplicando orden ASCENDENTE (de menor a mayor)")
            else:
                sorted_indices = np.argsort(-self.totals)
                print("🔄 Aplicando orden DESCENDENTE (de mayor a menor)")
            self.M = self.M[:, sorted_indices]
            self.totals = self.totals[sorted_indices]
            self.cats = [self.df[self.cat_col].astype(str).tolist()[i] for i in sorted_indices]
            print("📊 Primeros 5 nombres de países después de ordenar:")
            for i, cat in enumerate(self.cats[:5]):
                print(f"  - {i+1}: {cat}")
            self.df = self.df.iloc[sorted_indices].reset_index(drop=True)
        else:
            # Sin ordenamiento especial
            self.cats = self.df[self.cat_col].astype(str).tolist()
        
        # Aplicar porcentaje si está configurado
        if bool(self.params.get("percent", False)):
            colsum = self.M.sum(axis=0)
            colsum[colsum == 0] = 1.0
            self.M = self.M / colsum * 100.0

        # === NUEVO: Calcular totales por tipo de medalla para la leyenda ===
        legend_cfg = self.params.get("legend_config", {}).copy()
        # SIEMPRE inyectar la paleta de colores global al legend_config (sobrescribe cualquier valor previo)
        legend_cfg["colors"] = self.params.get("colors", {})
        icons = legend_cfg.get("icons", [])
        # Solo si hay íconos y cada uno tiene un label que coincide con una columna
        if icons and all("label" in icon for icon in icons):
            # Mapear label a columna real (insensible a mayúsculas)
            show_totals = legend_cfg.get("show_totals_in_legend", True)
            col_map = {c.lower(): c for c in self.df.columns}
            for icon in icons:
                label = icon["label"].strip().lower()
                # Buscar columna que coincida con el label
                colname = None
                for c in col_map:
                    if label in c or c in label:
                        colname = col_map[c]
                        break
                if colname and colname in self.df.columns:
                    total = self.df[colname].sum()
                    icon["_total"] = int(total)
                    if show_totals:
                        icon["_label_with_total"] = f"{icon['label']} ({int(total)})"
                    else:
                        icon["_label_with_total"] = icon["label"]
                else:
                    icon["_total"] = None
                    icon["_label_with_total"] = icon["label"]
            
    def _get_series_columns(self):
        """Determina las columnas de series a usar."""
        # Primero buscar en data.series (nueva ubicación preferida para series)
        series_order = self.params.get("data", {}).get("series")
        
        # Si no hay series en data.series, intentar con la ubicación antigua
        if not series_order:
            series_order = self.params.get("series_order")
            
        # Preparar mapeo de columnas para búsqueda insensible a mayúsculas/minúsculas
        cols_map = {c.lower(): c for c in self.df.columns}
        
        if series_order:
            print(f"✅ Usando series definidas en configuración: {series_order}")
            missing = [s for s in series_order if s.lower() not in cols_map]
            if missing:
                raise KeyError(f"No encontré estas series en el CSV: {missing}. Columnas vistas: {list(self.df.columns)}")
            return [cols_map[s.lower()] for s in series_order]
        
        # Si no hay series definidas, detectar automáticamente
        noise = {"rank","code","pais","country","flag_url","total"}
        cols = [c for c in self.df.columns if c != self.cat_col and c.lower() not in noise and pd.api.types.is_numeric_dtype(self.df[c])]
        if not cols:
            raise ValueError("No hay columnas numéricas para apilar. Usa overrides.series_order.")
        
        print(f"✅ Series detectadas automáticamente: {cols}")
        return cols
    
    def create_figure(self):
        """Crea la figura con las dimensiones adecuadas y configura los ejes."""
        super().create_figure()  # Llama al método de la clase base
        
        # Configuración adicional específica para barras horizontales
        margins_config = self.params.get("margins", {})
        auto_adjust = margins_config.get("auto_adjust", True)  # Por defecto, ajuste automático
        margin_bottom = float(margins_config.get("bottom", 0.12))
        margin_right = float(margins_config.get("right", 0.02))
        margin_text_padding = float(margins_config.get("text_padding", 0.1))  # Padding adicional en pulgadas
        
        # Límites para el margen izquierdo
        min_left_margin = float(margins_config.get("min_left", 0.1))
        max_left_margin = float(margins_config.get("max_left", 0.25))
        
        # Margen izquierdo manual si se especifica
        manual_left_margin = margins_config.get("left", None)
        
        # Manejo especial para el margen izquierdo en barras horizontales
        if auto_adjust and manual_left_margin is None:
            # Crear un eje temporal para calcular el ancho exacto de los textos
            temp_fig = plt.figure(figsize=(1, 1))
            temp_ax = temp_fig.add_subplot(111)
            
            # Obtener la configuración de fuente para los nombres
            font_props = {}
            if "yaxis" in self.params and "font" in self.params["yaxis"]:
                font_props = self.params["yaxis"]["font"]
            
            font_size = font_props.get("size", 9)  # Usamos el tamaño de fuente configurado
            
            # Calcular el ancho máximo necesario para los nombres
            max_width = 0
            for cat in self.cats:
                t = temp_ax.text(0, 0, str(cat), fontsize=font_size)
                bbox = t.get_window_extent(temp_fig.canvas.get_renderer())
                width_inches = bbox.width / temp_fig.dpi
                max_width = max(max_width, width_inches)
                t.remove()  # Limpiamos el texto
            
            plt.close(temp_fig)  # Cerramos la figura temporal
            
            # Convertir pulgadas a fracción de figura
            width_in = float(self.params.get("width_in", 12))
            left_margin_inches = max_width + margin_text_padding  # Añadimos el padding configurado
            left_margin = left_margin_inches / width_in
            
            # Limitamos el margen para casos extremos
            left_margin = min(max_left_margin, max(min_left_margin, left_margin))
            
            print(f"Cálculo preciso: Ancho máximo de texto = {max_width:.2f} pulgadas")
            print(f"Ajuste automático: Margen izquierdo = {left_margin:.2f}")
        else:
            # Usar el valor manual si se especificó
            left_margin = float(manual_left_margin) if manual_left_margin is not None else min_left_margin
            print(f"Usando margen izquierdo manual: {left_margin:.2f}")
        
        # Calculamos el ancho disponible para el gráfico
        plot_width = 1.0 - left_margin - margin_right
        print(f"Configuración final: Margen izquierdo = {left_margin:.2f}, Ancho gráfico = {plot_width:.2f}")
        
        # Actualizar el eje principal con los márgenes calculados
        header_height = float(self.params.get("margins", {}).get("top", 0.25))
        self.ax.remove()  # Eliminamos el eje creado por la clase base
        self.ax = self.fig.add_axes([left_margin, margin_bottom, plot_width, 1.0-margin_bottom-header_height])
        
    def draw_chart(self):
        """Dibuja las barras apiladas horizontales."""
        # Obtener configuración de barras
        bar_config = self.params.get("bar", {})
        bar_height = float(bar_config.get("height", 0.7))
        bar_edgecolor = bar_config.get("edgecolor", "white")
        bar_linewidth = float(bar_config.get("linewidth", 0.5))
        bar_gap = float(bar_config.get("gap", 0.0))  # Espacio entre barras como fracción de altura
        
        # Imprimir la configuración para depuración
        print("📊 Configuración de barras:")
        print(f"  - Altura: {bar_height:.2f}")
        print(f"  - Espacio entre barras: {bar_gap:.2f}")
        print(f"  - Color del borde: {bar_edgecolor}")
        print(f"  - Grosor del borde: {bar_linewidth:.2f}")
        
        n_categories = len(self.cats)
        
        # Calcular altura efectiva considerando el espacio entre barras
        effective_height = bar_height
        if bar_gap > 0:
            # Reducir la altura para dejar espacio
            effective_height = bar_height * (1 - bar_gap)
            print(f"🔄 Aplicando espacio entre barras: gap={bar_gap:.2f}, altura efectiva={effective_height:.2f}")
        
        # Posiciones de las barras
        self.y_positions = np.arange(n_categories)
        
        # Configurar colores
        colors = self.params.get("colors", {})
        if not isinstance(colors, dict):
            # Si no es diccionario, usar colores predeterminados
            colors = {}
            default_colors = ['#E5B13A', '#A8A9AD', '#CD7F32', '#4878CF', '#6ACC65', '#D65F5F']
            for i, col in enumerate(self.cols):
                colors[col] = default_colors[i % len(default_colors)]
        
        # Dibujar barras
        self.bottoms = np.zeros(len(self.cats))
        for i, (serie, vals) in enumerate(zip(self.cols, self.M)):
            color = colors.get(serie, plt.cm.tab10.colors[i % 10])
            self.ax.barh(
                self.y_positions, vals, 
                height=effective_height,
                left=self.bottoms, 
                label=str(serie),
                color=color,
                edgecolor=bar_edgecolor,
                linewidth=bar_linewidth
            )
            
            # Añadir etiquetas de valores en las barras
            if bool(self.params.get("value_labels", False)):
                # Obtener configuración de etiquetas de valores
                value_labels_config = self.params.get("value_labels_config", {}) if isinstance(self.params.get("value_labels"), bool) else self.params.get("value_labels", {})
                
                # Obtener tamaño de fuente y formato
                font_size = float(value_labels_config.get("font_size", 9))
                font_weight = value_labels_config.get("font_weight", "normal")
                fmt = self.params.get("value_format", "{:.0f}")
                
                # Imprimir información de configuración para depuración
                print("📊 Configuración de etiquetas de valores:")
                print(f"  - Tamaño de fuente: {font_size}")
                print(f"  - Peso de fuente: {font_weight}")
                print(f"  - Formato: {fmt}")
                
                for j, val in enumerate(vals):
                    if val > 0:  # Solo mostrar valores positivos
                        # Calcular posición central para la etiqueta
                        x_pos = self.bottoms[j] + val/2
                        y_pos = self.y_positions[j]
                        
                        # Determinar color del texto (contraste)
                        text_color = "white" if val > 5 else "black"
                        
                        self.ax.text(
                            x_pos, y_pos, 
                            fmt.format(val),
                            ha='center', va='center',
                            color=text_color,
                            fontsize=font_size,
                            fontweight=font_weight
                        )
            
            # Actualizar las posiciones para la próxima serie
            self.bottoms += vals
            
        # Añadir etiquetas de totales al final de las barras
        total_labels_config = self.params.get("total_labels", {})
        if total_labels_config.get("enabled", False) and total_labels_config.get("position", "end") == "end":
            # Obtener configuración para etiquetas de totales
            x_offset = float(total_labels_config.get("x_offset", 4))
            font_size = float(total_labels_config.get("font_size", 12))
            font_weight = total_labels_config.get("font_weight", "bold")
            font_color = total_labels_config.get("color", "#333333")
            fmt = total_labels_config.get("value_format", "{:.0f}")
            
            print("📊 Añadiendo etiquetas de totales al final de las barras:")
            print(f"  - Offset X: {x_offset}")
            print(f"  - Tamaño de fuente: {font_size}")
            print(f"  - Peso de fuente: {font_weight}")
            print(f"  - Color: {font_color}")
            print(f"  - Formato: {fmt}")
            
            # Añadir etiquetas con los totales
            for i, (cat, total) in enumerate(zip(self.cats, self.bottoms)):
                # Posición para el total (al final de la barra)
                x_pos = self.bottoms[i] + x_offset
                y_pos = self.y_positions[i]
                
                # Añadir etiqueta de total
                self.ax.text(
                    x_pos, y_pos,
                    fmt.format(total),
                    ha='left', va='center',
                    color=font_color,
                    fontsize=font_size,
                    fontweight=font_weight
                )
                print(f"  ✓ Total para {cat}: {total:.0f}")

    def configure_axes(self):
        """Configura los ejes y sus elementos."""
        # Verificar si hay banderas habilitadas para usar el método apropiado
        flags_config = self.params.get("flags", {})
        if flags_config.get("enabled", False):
            # Si hay banderas habilitadas, usar el método específico
            self.configure_axes_with_flags()
            return
        
        # Si no hay banderas, usar la configuración básica
        # Ajustar límites con padding
        self.ax.set_ylim(-0.5, len(self.cats) - 0.5)
        
        # Margen estándar
        self.ax.set_xlim(0, self.bottoms.max() * 1.05)  # 5% de margen a la derecha
        
        # Configurar eje Y según configuración
        yaxis_config = self.params.get("yaxis", {})
        
        # Primero establecemos las posiciones de los ticks
        self.ax.set_yticks(self.y_positions)
        
        # Verificar si se deben ocultar las etiquetas del eje Y
        if not yaxis_config.get("show_labels", True):
            self.ax.set_yticklabels([])
            print("🙈 Etiquetas del eje Y ocultas por configuración")
        else:
            self.ax.set_yticklabels(self.cats)
        
        # Verificar si se deben ocultar los ticks del eje Y
        if not yaxis_config.get("show_ticks", True):
            self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
            print("🙈 Ticks del eje Y ocultos por configuración")
            
        # Eliminar spines innecesarios y configurar eje X según configuración
        spines_to_hide = ["top", "right"]
        
        # Si estamos ocultando ticks del eje Y, también ocultamos la línea del spine
        if not yaxis_config.get("show_ticks", True):
            spines_to_hide.append("left")
        
        # Verificar si se debe ocultar el eje X
        xaxis_config = self.params.get("xaxis", {})
        if not xaxis_config.get("show_ticks", True) or xaxis_config.get("hide_axis", False):
            # Ocultar las etiquetas del eje X
            self.ax.xaxis.set_ticklabels([])
            spines_to_hide.append("bottom")
            print("🙈 Eje X oculto completamente por configuración")
            # Métodos adicionales para asegurarse que todos los elementos del eje X estén ocultos
            self.ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            # Ocultar la línea del eje X completamente
            self.ax.get_xaxis().set_visible(False)
        
        # Ocultar spines según configuración
        for spine in spines_to_hide:
            self.ax.spines[spine].set_visible(False)
            
        # Aplicar estilos de fuente
        if "yaxis" in self.params and "font" in self.params["yaxis"]:
            font_cfg = self.params["yaxis"]["font"]
            for label in self.ax.get_yticklabels():
                label.set_fontsize(font_cfg.get("size", 11))
                label.set_color(font_cfg.get("color", "#333333"))
        
        # Grid sutil (solo si no se oculta el eje X)
        if self.params.get("xaxis", {}).get("show_ticks", True):
            self.ax.grid(axis='x', linestyle='--', alpha=0.3, color='#cccccc')
            self.ax.set_axisbelow(True)  # Grid detrás de las barras
        else:
            print("📊 Grid horizontal desactivado porque el eje X está oculto")
                
    def configure_axes_with_flags(self):
        """Configura los ejes y añade banderas junto a los nombres de países o al final de las barras."""
        # Obtener la configuración de flags
        flags_config = self.params.get("flags", {})
        
        # Configuración básica de ejes
        self.ax.set_ylim(-0.5, len(self.cats) - 0.5)
        
        # Determinar la posición de las banderas
        flag_position = flags_config.get("position", "start")
        
        # Ajustar los límites del eje X según la posición de las banderas
        if flag_position == "end" and flags_config.get("enabled", False):
            # Dar más espacio al final para las banderas
            self.ax.set_xlim(0, self.bottoms.max() * 1.15)
            print("🚩 Banderas configuradas al final de las barras - margen extra añadido.")
        else:
            self.ax.set_xlim(0, self.bottoms.max() * 1.05)
        
        # Configurar etiquetas de eje Y
        self.ax.set_yticks(self.y_positions)
        
        # Verificar configuración del eje Y
        yaxis_config = self.params.get("yaxis", {})
        
        # IMPORTANTE: La configuración de show_labels en yaxis tiene prioridad sobre todo
        if "show_labels" in yaxis_config:
            if not yaxis_config["show_labels"]:
                self.ax.set_yticklabels([])
                print("🙈 Etiquetas del eje Y ocultas por configuración de yaxis.show_labels=false")
            else:
                self.ax.set_yticklabels(self.cats)
                print("✅ Etiquetas del eje Y mostradas por configuración de yaxis.show_labels=true")
                # Información de depuración sobre las etiquetas
                for i, cat in enumerate(self.cats[:5]):
                    print(f"  - {i+1}: {cat}")
        else:
            # Si no hay configuración específica de yaxis.show_labels, usar la de flags
            if flags_config.get("show_axis_labels", True):
                self.ax.set_yticklabels(self.cats)
                print("🔤 Etiquetas establecidas en el eje Y (por flags.show_axis_labels):")
                for i, cat in enumerate(self.cats[:5]):
                    print(f"  - {i+1}: {cat}")
            else:
                self.ax.set_yticklabels([])
                print("🔤 Etiquetas ocultas por configuración de flags.show_axis_labels=false")
        
        # Verificar si debemos ocultar los ticks del eje Y
        if not yaxis_config.get("show_ticks", True):
            # Ocultamos las marcas de tick pero mantenemos las etiquetas si show_labels es true
            if yaxis_config.get("show_labels", True):
                self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=True)
                print("🙈 Ticks del eje Y ocultos pero etiquetas visibles")
            else:
                self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
                print("🙈 Ticks y etiquetas del eje Y ocultos por configuración")
            
            # También ocultamos el spine izquierdo
            self.ax.spines["left"].set_visible(False)
        
        # Verificar posición de las etiquetas del eje Y (izquierda o derecha)
        y_position = yaxis_config.get("position", "left").lower()
        if y_position == "right":
            # Mover etiquetas al lado derecho
            self.ax.tick_params(axis='y', which='both', labelleft=False, labelright=True)
            print("📊 Etiquetas del eje Y posicionadas a la DERECHA por configuración")
        else:
            # Mantener etiquetas en el lado izquierdo (predeterminado)
            self.ax.tick_params(axis='y', which='both', labelleft=True, labelright=False)
            print("📊 Etiquetas del eje Y posicionadas a la IZQUIERDA por configuración")
        
        # Aplicar estilos de fuente a las etiquetas si están visibles y ajustar posición para dejar espacio a las banderas
        if yaxis_config.get("show_labels", True) and "font" in yaxis_config:
            font_cfg = yaxis_config["font"]
            # Obtener el padding para etiquetas (distancia adicional entre etiquetas y eje)
            label_padding = yaxis_config.get("label_padding", -35)  # Valor negativo mueve las etiquetas hacia la izquierda
            
            # Ajustar las etiquetas del eje Y
            self.ax.tick_params(axis='y', which='both', pad=label_padding)
            print(f"📏 Ajustando posición de etiquetas del eje Y: padding = {label_padding}")
            
            # Aplicar configuración de fuente
            for label in self.ax.get_yticklabels():
                label.set_fontsize(font_cfg.get("size", 11))
                label.set_color(font_cfg.get("color", "#333333"))
        
        # Eliminar spines innecesarios
        for spine in ["top", "right", "bottom"]:
            self.ax.spines[spine].set_visible(False)
            
        # Forzar ocultación del eje X cuando está configurado
        if self.params.get("xaxis", {}).get("hide_axis", False) or \
           not self.params.get("xaxis", {}).get("visible", True):
            self.ax.xaxis.set_ticklabels([])
            self.ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            self.ax.get_xaxis().set_visible(False)
            print("🙈 Eje X ocultado forzosamente por la configuración xaxis.hide_axis o xaxis.visible=false")
        
        # Grid sutil (solo si no se oculta el eje X)
        if self.params.get("grid", True) and self.params.get("xaxis", {}).get("show_ticks", True):
            self.ax.grid(axis='x', linestyle='--', alpha=0.3, color='#cccccc')
            self.ax.set_axisbelow(True)
        else:
            print("📊 Grid horizontal desactivado porque el eje X está oculto")
        
        # Si no hay banderas habilitadas, terminamos aquí
        if not flags_config.get("enabled", False):
            print("⚠️ Las banderas están desactivadas en la configuración.")
            return
            
        # Configuración para banderas
        flag_col = flags_config.get("column", "flag_url")
        pattern = flags_config.get("pattern", "")
        zoom = float(flags_config.get("zoom", 0.08))
        
        # Añadir banderas para cada país
        for i, cat in enumerate(self.cats):
            # Posición y del país
            y_pos = self.y_positions[i]
            
            # Determinar ruta de bandera
            flag_path = None
            
            # Intentar obtener directamente de la columna flag_url
            if flag_col in self.df.columns:
                flag_path = self.df.iloc[i].get(flag_col, None)
                if flag_path and flag_path.startswith('/'):
                    # Convertir path absoluto desde raíz del repo
                    flag_path = str(Path.cwd() / flag_path.lstrip('/'))
            
            # Intentar construir con código si no hay path directo y hay patrón
            if not flag_path and pattern:
                code_col = flags_config.get("code_column", "code")
                if code_col in self.df.columns:
                    code = str(self.df.iloc[i].get(code_col, "")).strip()
                    if code:
                        flag_path = pattern.format(code=code.lower(), CODE=code.upper())
            
            # Si tenemos una ruta de bandera válida, mostrarla
            if flag_path and Path(flag_path).exists():
                try:
                    from matplotlib.image import imread
                    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
                    
                    # Cargar la imagen
                    img = imread(flag_path)
                    
                    # Crear la caja con la imagen
                    imagebox = OffsetImage(img, zoom=zoom)
                    
                    # Posicionar la bandera según la configuración
                    if flag_position == "end":
                        # Colocar bandera al final de la barra
                        total_value = self.bottoms[i]
                        
                        # Añadir la bandera al final de la barra con un pequeño desplazamiento
                        offset = 1.0  # Offset horizontal para separar la bandera de la barra
                        
                        ab = AnnotationBbox(
                            imagebox,
                            (total_value + offset, y_pos),  # Posición x al final de la barra con offset
                            xycoords='data',  # Usar coordenadas de datos
                            box_alignment=(0, 0.5),  # Alinear a la izquierda y centrado verticalmente
                            pad=0.02,
                            frameon=False
                        )
                        print(f"Bandera para {cat} colocada al final de la barra en posición x={total_value:.1f}")
                    else:
                        # Colocar bandera en un punto fijo entre las etiquetas y las barras
                        from matplotlib import transforms
                        # Combinar transformación de figura para X y datos para Y
                        trans = transforms.blended_transform_factory(
                            self.fig.transFigure,  # Para coordenadas X en sistema de figura
                            self.ax.transData      # Para coordenadas Y en sistema de datos
                        )
                        
                        # Obtener los límites del eje en coordenadas de figura
                        ax_pos = self.ax.get_position()
                        
                        # Calcular posición ideal para las banderas
                        # Posicionar las banderas justo antes del inicio de las barras (ax_pos.x0)
                        # usando el offset configurado (o un valor predeterminado)
                        offset_factor = float(flags_config.get("offset", 0.05))
                        flag_x = ax_pos.x0 - offset_factor  # Posición ajustada con el offset
                        
                        ab = AnnotationBbox(
                            imagebox,
                            (flag_x, y_pos),    # Posición x fija en coordenadas de figura
                            xycoords=trans,      # Transformación combinada
                            box_alignment=(0.5, 0.5),  # Centrado horizontal y vertical
                            pad=0,              # Sin padding adicional
                            frameon=False
                        )
                        print(f"Bandera para {cat} colocada entre el nombre y las barras")
                    
                    self.ax.add_artist(ab)
                    
                except Exception as e:
                    print(f"Error al añadir bandera para {cat}: {e}")
    
    def debug_flag_paths(self):
        """Muestra información de depuración sobre las rutas de las banderas."""
        from app.debug_utils import debug_flag_paths
        
        flags_config = self.params.get("flags", {})
        cat_col = self.params.get("data", {}).get("category_col", "")
        
        # Usar la función auxiliar de depuración
        debug_flag_paths(
            df=self.df,
            flags_config=flags_config,
            cat_col=cat_col,
            current_dir=Path.cwd()
        )
    
    def add_legend(self):
        """Añade la leyenda si está habilitada."""
        # Asegurar que la paleta de colores esté presente en legend_config antes de pasarla a la base
        legend_cfg = self.params.get("legend_config", {}).copy()
        legend_cfg["colors"] = self.params.get("colors", {})
        self.params["legend_config"] = legend_cfg
        super().add_legend()
    def add_labels(self):
        """Añade etiquetas de totales."""
        # No llamamos a super().add_labels() porque los totales ya se añaden en el método draw_chart
        # Esto evita la duplicación de etiquetas de totales
        pass
    
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
        subtitle_bottom_margin = float(title_spacing.get("subtitle_bottom_margin", 0.15))  # Espacio debajo del subtítulo
        
        # Espaciado horizontal para título y subtítulo (márgenes globales)
        left_margin = float(title_spacing.get("left_margin", 0.0))  # Margen izquierdo global
        right_margin = float(title_spacing.get("right_margin", 0.0))  # Margen derecho global
        
        print("\nℹ️ Configuración de espaciado de títulos:")
        print(f"  - Espacio superior del título: {title_top_margin:.2f} (desde borde superior)")
        print(f"  - Espacio entre título y subtítulo: {title_bottom_margin:.2f} + {subtitle_top_margin:.2f} = {title_bottom_margin + subtitle_top_margin:.2f}")
        print(f"  - Espacio debajo del subtítulo: {subtitle_bottom_margin:.2f}")
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
            # base_x_pos = title_config.get("x", 0.5)
            
            # Ajustar la posición X según los márgenes izquierdo y derecho
            # y según la alineación horizontal (ha) del texto
            ha = title_config.get("ha", "center")
            padding_left = float(title_config.get("padding_left", 0.0))  # Padding izquierdo específico del título
            padding_right = float(title_config.get("padding_right", 0.0))  # Padding derecho específico del título
            
            # Comprobar si queremos usar coordenadas de la figura completa 
            use_figure_transform = title_config.get("transform", "") == "figure"
            
            # Si usamos coordenadas de figura completa, permitir y explícito
            if use_figure_transform:
                # Usar coordenadas de figura directamente para posicionamiento extremo izquierdo
                x_pos = float(title_config.get("x", 0.01))  # Usar valor especificado o un valor mínimo
                if "y" in title_config:
                    y_pos = float(title_config["y"])
                    print(f"🖼️ Usando transformación de figura completa para el título con y explícito: y={y_pos}")
                else:
                    y_pos = 0.98  # Cerca del tope de la figura
                    print("🖼️ Usando transformación de figura completa para el título (y por defecto)")
            else:
                # Comportamiento normal usando márgenes del eje de título
                # Calcular ancho disponible después de aplicar márgenes globales
                available_width = 1.0 - left_margin - right_margin
                # Calcular posición X final basada en alineación
                if ha == "left":
                    x_pos = left_margin + padding_left
                elif ha == "right":
                    x_pos = 1.0 - right_margin - padding_right
                else:  # center u otros
                    x_pos = left_margin + (available_width / 2)
                # Permitir y explícito si está en title_config, si no usar margen superior
                if "y" in title_config:
                    y_pos = float(title_config["y"])
                    print(f"📌 Usando posición Y explícita para título: y={y_pos}")
                else:
                    y_pos = 1.0 - title_top_margin
                    print(f"📌 Usando posición Y por margen superior para título: y={y_pos}")
            
            # Debug para ver los valores calculados
            print("DEBUG: Márgenes horizontales aplicados al título:")
            print(f"  - Márgenes globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
            print(f"  - Paddings específicos: izquierdo={padding_left:.2f}, derecho={padding_right:.2f}")
            print(f"  - Posición X calculada: {x_pos:.2f} (alineación='{ha}')")
            print(f"DEBUG: Posición Y calculada para título = {y_pos:.2f} (basada en top_margin = {title_top_margin:.2f})")
            
            # Usar siempre la misma alineación vertical para consistencia
            ha = title_config.get("ha", "center")
            va = "top"  # Fijar siempre a 'top' para evitar inconsistencias
            
            # Determinar la transformación a usar
            transform = None
            if title_config.get("transform", "") == "figure":
                transform = self.fig.transFigure  # Usar coordenadas de la figura completa
                print("🎯 Usando transformación de figura completa para el título")
            
            # Propiedades avanzadas del texto - asegurándonos de obtener el fontsize correcto
            # y convertirlo explícitamente a float para evitar problemas de tipo
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
                "linespacing": title_config.get("linespacing", 1.1),
            }
            
            # Opciones para el cuadro de fondo con valores predeterminados si no se especifica
            # bbox_props = title_config.get("bbox", {
            #     "boxstyle": "round,pad=0.5",
            #     "facecolor": "#f8f8f8",
            #     "edgecolor": "#dddddd",
            #     "alpha": 0.8
            # })
            # text_props["bbox"] = bbox_props
            
            # Imprimir propiedades para depuración
            print("DEBUG: Aplicando propiedades al título:")
            for key, value in text_props.items():
                print(f"  - {key}: {value}")
            
            # Añadir el título al gráfico
            print(f"\nℹ️ Colocando título en posición: x={x_pos:.2f}, y={y_pos:.2f}, va='{va}', ha='{ha}'")
            if transform:
                # Usar la transformación personalizada (coordenadas de figura)
                title_artist = self.fig.text(x_pos, y_pos, title,
                                ha=ha, va=va,
                                transform=transform,
                                **text_props)
                print(f"✨ Título añadido directamente a la figura en posición absoluta: x={x_pos:.2f}, y={y_pos:.2f}")
            else:
                # Usar la transformación del eje de título (comportamiento normal)
                title_artist = self.ax_header.text(x_pos, y_pos, title, 
                                ha=ha, va=va,
                                transform=self.ax_header.transAxes,
                                **text_props)
            
            # Aplicar wrapping manual para el texto largo
            if title_config.get("word_wrap", False) or title_config.get("wrap", False):
                try:
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
                    
                    # Implementar wrapping manual dividiendo el texto en líneas
                    import textwrap
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
        if not subtitle_config and subtitle:
            # Configuración básica para compatibilidad
            x_pos = self.params.get("subtitle_x_position", 0.5)
            # Posicionar el subtítulo debajo del título con margen adicional
            if hasattr(self, 'title_artist') and self.title_artist:
                # Calcula la posición Y del subtítulo basada en la posición del título
                # La posición dependerá de la alineación vertical del título
                title_pos = self.title_artist.get_position()[1]
                y_pos = title_pos - title_bottom_margin - subtitle_top_margin
                print(f"ℹ️ Posición del subtítulo calculada a partir del título: {y_pos:.2f} (título en {title_pos:.2f})")
            else:
                y_pos = 1.0 - title_top_margin - title_bottom_margin - subtitle_top_margin
                print(f"ℹ️ Posición del subtítulo calculada sin referencia al título: {y_pos:.2f}")
                
            ha = self.params.get("subtitle_horizontal_alignment", "center")
            va = self.params.get("subtitle_vertical_alignment", "top")  # Alineado hacia arriba
            
            fontsize = float(self.params.get("subtitle_font_size", 13))
            color = self.params.get("subtitle_color", "#666666")
            fontfamily = self.params.get("subtitle_font_family", "Nunito")  # Usar Nunito por defecto
            
            self.ax_header.text(x_pos, y_pos, subtitle, 
                                ha=ha, va=va,
                                fontsize=fontsize,
                                color=color,
                                family=fontfamily,
                                style=self.params.get("subtitle_font_style", "normal"),
                                transform=self.ax_header.transAxes)
        elif subtitle_config and subtitle:
            # Usar configuración avanzada para el subtítulo
            
            # Comprobar si queremos usar coordenadas de la figura completa para el subtítulo
            use_figure_transform_subtitle = subtitle_config.get("transform", "") == "figure"
            
            if use_figure_transform_subtitle:
                # Usar coordenadas de figura directamente para posicionamiento extremo izquierdo
                x_pos = float(subtitle_config.get("x", 0.01))  # Usar valor especificado o un valor mínimo
                
                # Verificar si hay una posición Y explícita en la configuración
                if "y" in subtitle_config:
                    y_pos = float(subtitle_config.get("y"))
                    print(f"📌 Usando posición Y explícita para subtítulo: {y_pos}")
                # Calcular posición Y basada en el título y considerando espacio completo de la figura
                elif hasattr(self, 'title_artist') and self.title_artist:
                    # Si el título usa transformación de figura, colocar muy cerca del título
                    y_pos = 0.92  # Por defecto cerca del título
                    
                    # Intentar obtener información del título para ajustar el subtítulo
                    title_text = self.title_artist.get_text()
                    title_lines = title_text.count('\n') + 1
                    
                    # Ajustar según el número de líneas del título
                    # Cuanto más líneas tiene el título, más abajo debe ir el subtítulo
                    # Pero nunca demasiado abajo
                    if title_lines == 1:
                        y_pos = 0.93  # Muy cerca del título si es una sola línea
                    elif title_lines == 2:
                        y_pos = 0.89  # Ligeramente más abajo para títulos de 2 líneas
                    else:
                        y_pos = 0.85  # Más espacio para títulos de 3+ líneas
                else:
                    y_pos = 0.92  # Posición estándar si no hay título
                print("🖼️ Usando transformación de figura completa para el subtítulo")
            else:
                # Comportamiento normal usando márgenes del eje de título
                # Ajustar la posición X según los márgenes izquierdo y derecho
                # y según la alineación horizontal (ha) del texto
                ha = subtitle_config.get("ha", "center")
                padding_left = float(subtitle_config.get("padding_left", 0.0))  # Padding izquierdo específico del subtítulo
                padding_right = float(subtitle_config.get("padding_right", 0.0))  # Padding derecho específico del subtítulo
                
                # Calcular ancho disponible después de aplicar márgenes globales
                available_width = 1.0 - left_margin - right_margin
                
                # Calcular posición X final basada en alineación
                if ha == "left":
                    x_pos = left_margin + padding_left
                elif ha == "right":
                    x_pos = 1.0 - right_margin - padding_right
                else:  # center u otros
                    x_pos = left_margin + (available_width / 2)
            
            # SIEMPRE calcular la posición basada en los márgenes, ignorando cualquier valor directo
            # de 'y' en subtitle_config para mantener consistencia
            
            # Posicionar el subtítulo debajo del título con margen adicional
            if hasattr(self, 'title_artist') and self.title_artist:
                # Calcular posición basada en el título y los márgenes
                # Para alineación 'top', la posición del subtítulo debe ser menor que la del título
                title_pos = y_pos  # Usar la posición del título que ya conocemos
                
                # Aumentar el espacio entre título y subtítulo para evitar sobreposición
                # especialmente cuando el título es largo y se ajusta en varias líneas
                subtitle_y_pos = title_pos - title_bottom_margin - subtitle_top_margin
                
                # Verificar si necesitamos ajuste adicional basado en el número de líneas del título
                if hasattr(self, 'title_artist') and '\n' in self.title_artist.get_text():
                    # Contar el número de líneas y ajustar posición
                    num_lines = len(self.title_artist.get_text().split('\n'))
                    # Ajustar 0.03 adicional por cada línea después de la primera
                    line_adjustment = max(0, (num_lines - 1) * 0.03)
                    subtitle_y_pos -= line_adjustment
                    print(f"DEBUG: Ajuste adicional por {num_lines} líneas en el título: -{line_adjustment:.2f}")
                
                print(f"DEBUG: Cálculo de posición del subtítulo: {title_pos} - {title_bottom_margin} - {subtitle_top_margin} = {subtitle_y_pos}")
                y_pos = subtitle_y_pos
                print(f"ℹ️ Posición del subtítulo calculada a partir del título: {y_pos:.2f}")
            else:
                # Si no hay título, usar posición estándar con márgenes
                y_pos = 1.0 - title_top_margin - title_bottom_margin - subtitle_top_margin
                print(f"ℹ️ Posición del subtítulo calculada sin referencia al título: {y_pos:.2f}")
            
            # Debug para ver los valores calculados
            print("DEBUG: Márgenes horizontales aplicados al subtítulo:")
            print(f"  - Márgenes globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
            print(f"  - Paddings específicos: izquierdo={padding_left:.2f}, derecho={padding_right:.2f}")
            print(f"  - Posición X calculada: {x_pos:.2f} (alineación='{ha}')")
            
            # Si hay posición Y explícita, mostrarla
            if use_figure_transform_subtitle and "y" in subtitle_config:
                # Usar la posición Y definida en el YAML
                y_pos = float(subtitle_config.get("y"))  # Usar el valor del YAML
                print(f"� FORZANDO posición Y explícita para el subtítulo: {y_pos:.2f}")
            
            va = "top"  # Fijar siempre a 'top' para evitar inconsistencias
            
            # Propiedades avanzadas para el subtítulo - asegurándonos de obtener el fontsize correcto
            # y convertirlo explícitamente a float
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
                "linespacing": subtitle_config.get("linespacing", 1.1),
            }
            
            # Opciones para el cuadro de fondo (si se especifica)
            if "bbox" in subtitle_config:
                text_props["bbox"] = subtitle_config.get("bbox")
            
            # Imprimir propiedades para depuración
            print("DEBUG: Aplicando propiedades al subtítulo:")
            for key, value in text_props.items():
                print(f"  - {key}: {value}")
                
            transform_subtitle = None
            if subtitle_config.get("transform", "") == "figure":
                transform_subtitle = self.fig.transFigure  # Usar coordenadas de la figura completa
                
                # Forzar la posición Y desde la configuración independientemente de todo lo anterior
                # Esto es necesario porque hay problemas con la detección del valor Y en la configuración
                explicit_y = subtitle_config.get("y")
                # Usar la posición Y definida en el YAML
                if explicit_y is not None:
                    y_pos = float(explicit_y)  # Usar el valor del YAML
                else:
                    # Si no hay valor en el YAML, mantener el valor calculado previamente
                    print(f"ℹ️ Manteniendo posición Y calculada para el subtítulo: {y_pos:.2f}")
                print(f"� FORZANDO posición Y explícita para el subtítulo: {y_pos:.2f}")
                
                # Usar la transformación personalizada (coordenadas de figura)
                subtitle_artist = self.fig.text(x_pos, y_pos, subtitle,
                            ha=ha, va=va,
                            transform=transform_subtitle,
                            **text_props)
                print(f"✨ Subtítulo añadido directamente a la figura en posición absoluta: x={x_pos:.2f}, y={y_pos:.2f}")
            else:
                # Usar la transformación del eje de título (comportamiento normal)
                subtitle_artist = self.ax_header.text(x_pos, y_pos, subtitle, 
                            ha=ha, va=va,
                            transform=self.ax_header.transAxes,
                            **text_props)
            
            # Aplicar wrapping manual para el texto largo
            if subtitle_config.get("wrap", False):
                try:
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
                    
                    # Implementar wrapping manual dividiendo el texto en líneas
                    import textwrap
                    # Obtener el subtítulo actual
                    current_text = subtitle_artist.get_text()
                    # Calcular aproximadamente cuántos caracteres caben en el ancho deseado
                    # Este es un cálculo aproximado basado en el tamaño de fuente
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
        Soporta múltiples opciones de personalización para posición, estilo y contenido.
        """
        from app.components import add_footer
        add_footer(self.fig, self.params)
    
    def add_decorative_elements(self):
        """
        Añade elementos decorativos al gráfico basados en la configuración.
        Soporta rectángulos, líneas y otros elementos visuales para estilo personalizado.
        """
        from app.components import add_decorative_elements
        add_decorative_elements(self.fig, self.params)
                
    def finalize(self):
        """Finaliza y guarda el gráfico."""
        # No usar tight_layout que puede afectar la posición de los títulos
        # plt.tight_layout()
        # Elimina o comenta la siguiente línea:
        # self.ax.set_position([0.15, 0.05, 0.8, 0.8])
        
        # Usar la función centralizada para finalizar y guardar el gráfico
        from app.components import finalize
        finalize(self.fig, self.params)
        
        # Debug the formats configuration
        print(f"[DEBUG] StackedHorizontalBarChart.finalize: usando componentes centralizados")

# Las funciones _load_yaml y _merge_params se han trasladado a app/io_utils.py

def stackedbarh(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    """Gráfico de barras horizontales apiladas con elementos básicos de matplotlib."""
    from app.chart_utils import render_chart
    
    # Usar la función render_chart que maneja correctamente la carga de templates
    render_chart(StackedHorizontalBarChart, config)

def add_command(app: typer.Typer) -> None:
    app.command("stackedbarh")(stackedbarh)

if __name__ == "__main__":
    # Para pruebas directas
    import sys
    # Evitar conflicto cuando se ejecuta como módulo
    if not sys.argv[0].endswith('__main__.py'):
        if len(sys.argv) > 1:
            stackedbarh(Path(sys.argv[1]))
        else:
            print("Uso: python stackedbarh.py ruta/al/config.yml")