from pathlib import Path
import typer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import yaml

class SimpleBarChart:
    def __init__(self, params, df):
        self.params = params
        self.df = df
        self.register_custom_fonts()
        self.prepare_data()
        self.setup_dimensions()
        
    def register_custom_fonts(self):
        """Registra fuentes personalizadas para usar en el gráfico."""
        fonts_dir = Path("fonts")
        if fonts_dir.exists():
            # Buscar todas las fuentes Nunito disponibles
            nunito_fonts = list(fonts_dir.glob("Nunito-*.ttf"))
            nunito_variable_fonts = list(fonts_dir.glob("Nunito-*VariableFont*.ttf"))
            
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
        
        # Preparar matriz de datos
        self.M = np.vstack([self.df[c].astype(float).to_numpy() for c in self.cols])
        
        # Calcular totales por país para ordenamiento
        self.totals = self.M.sum(axis=0)
        
        # Ordenar datos según total
        if self.params.get("sort_by_total", True):
            # Verificar si se debe invertir el orden
            invert_order = self.params.get("invert_order", False)
            
            # Índices ordenados: si invert_order es True, ordenamos de menor a mayor
            if invert_order:
                sorted_indices = np.argsort(self.totals)  # Orden ascendente (de menor a mayor)
                print("🔄 Aplicando orden ASCENDENTE (de menor a mayor)")
            else:
                sorted_indices = np.argsort(-self.totals)  # Orden descendente (de mayor a menor)
                print("🔄 Aplicando orden DESCENDENTE (de mayor a menor)")
            
            # Aplicar ordenamiento a datos y nombres
            self.M = self.M[:, sorted_indices]
            self.totals = self.totals[sorted_indices]
            self.cats = [self.df[self.cat_col].astype(str).tolist()[i] for i in sorted_indices]
            
            # Imprimir información de depuración sobre las categorías
            print(f"📊 Primeros 5 nombres de países después de ordenar:")
            for i, cat in enumerate(self.cats[:5]):
                print(f"  - {i+1}: {cat}")
            
            # Guardar el dataframe ordenado para uso posterior
            self.df = self.df.iloc[sorted_indices].reset_index(drop=True)
        else:
            # Sin ordenamiento especial
            self.cats = self.df[self.cat_col].astype(str).tolist()
        
        # Aplicar porcentaje si está configurado
        if bool(self.params.get("percent", False)):
            colsum = self.M.sum(axis=0)
            colsum[colsum == 0] = 1.0
            self.M = self.M / colsum * 100.0
            
    def _get_series_columns(self):
        """Determina las columnas de series a usar."""
        series_order = self.params.get("series_order")
        cols_map = {c.lower(): c for c in self.df.columns}
        
        if series_order:
            missing = [s for s in series_order if s.lower() not in cols_map]
            if missing:
                raise KeyError(f"No encontré estas series en el CSV: {missing}. Columnas vistas: {list(self.df.columns)}")
            return [cols_map[s.lower()] for s in series_order]
        
        noise = {"rank","code","pais","country","flag_url","total"}
        cols = [c for c in self.df.columns if c != self.cat_col and c.lower() not in noise and pd.api.types.is_numeric_dtype(self.df[c])]
        if not cols:
            raise ValueError("No hay columnas numéricas para apilar. Usa overrides.series_order.")
        return cols
    
    def create_figure(self):
        width_in = float(self.params.get("width_in", 12))
        height_in = float(self.params.get("height_in", 8))
        self.fig = plt.figure(figsize=(width_in, height_in))
        
        # Header: Aumentamos significativamente la altura para dar más espacio al título y subtítulo
        # El valor por defecto es 0.15, pero lo aumentamos a 0.25 para asegurar suficiente espacio
        header_height = float(self.params.get("margins", {}).get("top", 0.25))
        print(f"Altura del header: {header_height * 100:.1f}% de la altura total")
        
        # Eje para el header (título)
        self.ax_header = self.fig.add_axes([0, 1-header_height, 1, header_height], frameon=False)
        self.ax_header.set_axis_off()
        
        # Obtener configuración de márgenes del YAML
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
        
        # Eje principal para el gráfico con los márgenes configurados
        self.ax = self.fig.add_axes([left_margin, margin_bottom, plot_width, 1.0-margin_bottom-header_height])
        
    def draw_bars(self):
        """Dibuja las barras apiladas horizontales."""
        # Obtener configuración de barras
        bar_config = self.params.get("bar", {})
        bar_height = float(bar_config.get("height", 0.7))
        bar_edgecolor = bar_config.get("edgecolor", "white")
        bar_linewidth = float(bar_config.get("linewidth", 0.5))
        bar_gap = float(bar_config.get("gap", 0.0))  # Espacio entre barras como fracción de altura
        
        # Imprimir la configuración para depuración
        print(f"📊 Configuración de barras:")
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
                for j, val in enumerate(vals):
                    if val > 0:  # Solo mostrar valores positivos
                        # Calcular posición central para la etiqueta
                        x_pos = self.bottoms[j] + val/2
                        y_pos = self.y_positions[j]
                        
                        # Determinar formato
                        fmt = self.params.get("value_format", "{:.0f}")
                        
                        # Determinar color del texto (contraste)
                        text_color = "white" if val > 5 else "black"
                        
                        self.ax.text(
                            x_pos, y_pos, 
                            fmt.format(val),
                            ha='center', va='center',
                            color=text_color,
                            fontsize=9
                        )
            
            # Actualizar las posiciones para la próxima serie
            self.bottoms += vals
        
        # Comprobar si las banderas estarán al final de las barras, y si es así, ajustar el límite del eje X
        flags_config = self.params.get("flags", {})
        if flags_config.get("enabled", False) and flags_config.get("position", "") == "end":
            # Aumentar el margen derecho para dar espacio a las banderas al final de las barras
            max_bottom = self.bottoms.max()
            self.ax.set_xlim(0, max_bottom * 1.15)  # 15% de margen a la derecha para banderas

    def configure_axes(self):
        """Configura los ejes y sus elementos."""
        # Ajustar límites con padding
        self.ax.set_ylim(-0.5, len(self.cats) - 0.5)
        
        # Verificar si necesitamos un margen extra para banderas al final
        flags_config = self.params.get("flags", {})
        if flags_config.get("enabled", False) and flags_config.get("position", "") == "end":
            # Margen extra para banderas al final
            self.ax.set_xlim(0, self.bottoms.max() * 1.15)  # 15% de margen a la derecha
        else:
            # Margen estándar
            self.ax.set_xlim(0, self.bottoms.max() * 1.05)  # 5% de margen a la derecha
        
        # Configurar eje Y según configuración
        yaxis_config = self.params.get("yaxis", {})
        
        # Primero establecemos las posiciones de los ticks
        self.ax.set_yticks(self.y_positions)
        
        # Verificar si se deben ocultar las etiquetas del eje Y
        if yaxis_config.get("show_labels", True) == False:
            self.ax.set_yticklabels([])
            print("🙈 Etiquetas del eje Y ocultas por configuración")
        else:
            self.ax.set_yticklabels(self.cats)
        
        # Verificar si se deben ocultar los ticks del eje Y
        if yaxis_config.get("show_ticks", True) == False:
            self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
            print("🙈 Ticks del eje Y ocultos por configuración")
            
        # Eliminar spines innecesarios y configurar eje X según configuración
        spines_to_hide = ["top", "right"]
        
        # Si estamos ocultando ticks del eje Y, también ocultamos la línea del spine
        if yaxis_config.get("show_ticks", True) == False:
            spines_to_hide.append("left")
        
        # Verificar si se debe ocultar el eje X
        xaxis_config = self.params.get("xaxis", {})
        if xaxis_config.get("show_ticks", True) == False or xaxis_config.get("hide_axis", False):
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
            if yaxis_config["show_labels"] == False:
                self.ax.set_yticklabels([])
                print("🙈 Etiquetas del eje Y ocultas por configuración de yaxis.show_labels=false")
            else:
                self.ax.set_yticklabels(self.cats)
                print(f"✅ Etiquetas del eje Y mostradas por configuración de yaxis.show_labels=true")
                # Información de depuración sobre las etiquetas
                for i, cat in enumerate(self.cats[:5]):
                    print(f"  - {i+1}: {cat}")
        else:
            # Si no hay configuración específica de yaxis.show_labels, usar la de flags
            if flags_config.get("show_axis_labels", True):
                self.ax.set_yticklabels(self.cats)
                print(f"🔤 Etiquetas establecidas en el eje Y (por flags.show_axis_labels):")
                for i, cat in enumerate(self.cats[:5]):
                    print(f"  - {i+1}: {cat}")
            else:
                self.ax.set_yticklabels([])
                print("🔤 Etiquetas ocultas por configuración de flags.show_axis_labels=false")
        
        # Verificar si debemos ocultar los ticks del eje Y
        if yaxis_config.get("show_ticks", True) == False:
            # Ocultamos las marcas de tick pero mantenemos las etiquetas si show_labels es true
            if yaxis_config.get("show_labels", True):
                self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=True)
                print("🙈 Ticks del eje Y ocultos pero etiquetas visibles")
            else:
                self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
                print("🙈 Ticks y etiquetas del eje Y ocultos por configuración")
            
            # También ocultamos el spine izquierdo
            self.ax.spines["left"].set_visible(False)
        
        # Aplicar estilos de fuente a las etiquetas si están visibles
        if yaxis_config.get("show_labels", True) and "font" in yaxis_config:
            font_cfg = yaxis_config["font"]
            for label in self.ax.get_yticklabels():
                label.set_fontsize(font_cfg.get("size", 11))
                label.set_color(font_cfg.get("color", "#333333"))
        
        # Eliminar spines innecesarios
        for spine in ["top", "right", "bottom"]:
            self.ax.spines[spine].set_visible(False)
        
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
                        # Colocar bandera al inicio (junto al eje Y)
                        ab = AnnotationBbox(
                            imagebox,
                            (-0.12, y_pos),  # Posición x a la izquierda del eje Y
                            xycoords=('axes fraction', 'data'),
                            box_alignment=(0.5, 0.5),  # Centrado horizontal y vertical
                            pad=0,
                            frameon=False
                        )
                        print(f"Bandera para {cat} colocada junto al eje Y")
                    
                    self.ax.add_artist(ab)
                    
                except Exception as e:
                    print(f"Error al añadir bandera para {cat}: {e}")
    
    def debug_flag_paths(self):
        """Muestra información de depuración sobre las rutas de las banderas."""
        flags_config = self.params.get("flags", {})
        if not flags_config.get("enabled", True):
            print("⚠️ Las banderas no están habilitadas en la configuración.")
            return
            
        flag_col = flags_config.get("column", "flag_url")
        pattern = flags_config.get("pattern", "assets/flags/{CODE}.png")
        code_col = flags_config.get("code_column", "code")
        
        has_code_col = code_col in self.df.columns
        has_flag_col = flag_col in self.df.columns
        
        print(f"🔍 Depuración de rutas de banderas:")
        print(f"- Columna de banderas '{flag_col}': {'✅ Presente' if has_flag_col else '❌ No encontrada'}")
        print(f"- Columna de códigos '{code_col}': {'✅ Presente' if has_code_col else '❌ No encontrada'}")
        print(f"- Patrón: {pattern}")
        print(f"- Directorio actual: {Path.cwd()}")
        
        for i, cat in enumerate(self.cats):
            flag_path = None
            
            # Intentar obtener del dataframe
            if has_flag_col:
                flag_path = self.df.iloc[i].get(flag_col, None)
                print(f"  - {cat}: Valor en columna '{flag_col}': {flag_path}")
            
            # Intentar construir desde código
            if has_code_col:
                code = str(self.df.iloc[i].get(code_col, "")).strip()
                constructed_path = pattern.format(code=code.lower(), CODE=code.upper())
                print(f"  - {cat}: Código '{code}' → Ruta: {constructed_path}")
                
                if Path(constructed_path).exists():
                    print(f"    ✅ Archivo existe")
                else:
                    print(f"    ❌ Archivo no existe")
                    
                if not flag_path:
                    flag_path = constructed_path
            
            # Verificar existencia
            if flag_path:
                if flag_path.startswith('/'):
                    flag_path = str(Path.cwd() / flag_path.lstrip('/'))
                
                exists = Path(flag_path).exists()
                print(f"  - {cat}: Ruta final: {flag_path} ({'✅ Existe' if exists else '❌ No existe'})")
    
    def add_legend(self):
        """Añade la leyenda si está habilitada."""
        # La versión simplificada solo usa los parámetros básicos para evitar errores
        if bool(self.params.get("legend", True)):
            # Obtener configuración
            legend_config = self.params.get("legend_config", {})
            
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
    def add_labels(self):
        """Añade etiquetas de totales."""
        # Etiquetas de totales
        total_cfg = self.params.get("total_labels", {})
        if bool(total_cfg.get("enabled", False)):
            offset = float(total_cfg.get("x_offset", 4.0))
            font_size = float(total_cfg.get("font_size", 11))
            font_weight = total_cfg.get("font_weight", "bold")
            
            for i, total in enumerate(self.bottoms):
                self.ax.text(
                    total + offset/72 * (self.fig.get_figwidth() * self.fig.dpi) / (self.ax.get_position().width * self.fig.get_figwidth()),
                    self.y_positions[i],
                    f"{int(total)}",
                    ha='left', va='center',
                    fontsize=font_size,
                    fontweight=font_weight,
                    color="#333333"
                )
    
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
        
        print(f"\nℹ️ Configuración de espaciado de títulos:")
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
            
            # Calcular ancho disponible después de aplicar márgenes globales
            available_width = 1.0 - left_margin - right_margin
            
            # Calcular posición X final basada en alineación
            if ha == "left":
                x_pos = left_margin + padding_left
            elif ha == "right":
                x_pos = 1.0 - right_margin - padding_right
            else:  # center u otros
                x_pos = left_margin + (available_width / 2)
            
                        # SIEMPRE calcular la posición Y basada en el margen superior,
            # ignorando cualquier valor directo de 'y' en title_config para mantener consistencia
            y_pos = 1.0 - title_top_margin
            
            # Debug para ver los valores calculados
            print(f"DEBUG: Márgenes horizontales aplicados al título:")
            print(f"  - Márgenes globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
            print(f"  - Paddings específicos: izquierdo={padding_left:.2f}, derecho={padding_right:.2f}")
            print(f"  - Posición X calculada: {x_pos:.2f} (alineación='{ha}')")
            print(f"DEBUG: Posición Y calculada para título = {y_pos:.2f} (basada en top_margin = {title_top_margin:.2f})")
            
            # Usar siempre la misma alineación vertical para consistencia
            ha = title_config.get("ha", "center")
            va = "top"  # Fijar siempre a 'top' para evitar inconsistencias
            
            # Propiedades avanzadas del texto - asegurándonos de obtener el fontsize correcto
            # y convertirlo explícitamente a float para evitar problemas de tipo
            explicit_fontsize = self.params.get("_explicit_title_fontsize", None)
            config_fontsize = title_config.get("fontsize", None)
            global_fontsize = self.params.get("title_font_size", 18)
            
            # Mostrar los valores para depuración
            print(f"DEBUG: Valores de tamaño para el título:")
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
                    
                    print(f"📝 Aplicando ajuste automático de texto al título:")
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
            base_x_pos = subtitle_config.get("x", 0.5)
            
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
            print(f"DEBUG: Márgenes horizontales aplicados al subtítulo:")
            print(f"  - Márgenes globales: izquierdo={left_margin:.2f}, derecho={right_margin:.2f}")
            print(f"  - Paddings específicos: izquierdo={padding_left:.2f}, derecho={padding_right:.2f}")
            print(f"  - Posición X calculada: {x_pos:.2f} (alineación='{ha}')")
            
            va = "top"  # Fijar siempre a 'top' para evitar inconsistencias
            
            # Propiedades avanzadas para el subtítulo - asegurándonos de obtener el fontsize correcto
            # y convertirlo explícitamente a float
            explicit_fontsize = self.params.get("_explicit_subtitle_fontsize", None)
            config_fontsize = subtitle_config.get("fontsize", None)
            global_fontsize = self.params.get("subtitle_font_size", 13)
            
            # Mostrar los valores para depuración
            print(f"DEBUG: Valores de tamaño para el subtítulo:")
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
                    
                    print(f"Aplicando ajuste manual de texto al subtítulo:")
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
        footer = self.params.get("footer", {})
        if not footer:
            return
        
        # Configuración general del footer
        footer_config = footer.get("config", {})
        
        # Posición vertical para el footer (parte inferior de la figura)
        footer_y = float(footer_config.get("y_position", 0.03))
        
        # Espaciado vertical para elementos del footer
        footer_spacing = float(footer_config.get("spacing", 0.02))
        
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
                transform=self.fig.transFigure,
                zorder=-1                       # Dibujar detrás de todo
            )
            self.fig.add_artist(rect)
            
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
            source_x = float(source_config.get("x_position", 0.15))
            
            print(f"ℹ️ Configurando texto de fuente en footer:")
            print(f"  - Texto: '{source_text}'")
            print(f"  - Posición: x={source_x}, y={footer_y}")
            
            self.fig.text(
                source_x,     # Posición horizontal personalizable
                footer_y,     # Parte inferior
                source_text,
                ha='left',
                va='center',
                fontsize=source_fontsize,
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
            note_align = note_config.get("alignment", "center")
            
            print(f"ℹ️ Configurando texto de nota en footer:")
            print(f"  - Texto: '{note_text}'")
            print(f"  - Posición: x={note_x}, y={footer_y}")
            
            self.fig.text(
                note_x,       # Posición horizontal personalizable
                footer_y,     # Parte inferior
                note_text,
                ha=note_align,
                va='center',
                fontsize=note_fontsize,
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
                    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
                    import numpy as np
                    
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
                        fig_width_inches, fig_height_inches = self.fig.get_size_inches()
                        
                        # Si solo se especifica una dimensión, mantener la proporción
                        if logo_width_inches > 0 and logo_height_inches == 0:
                            logo_zoom = (logo_width_inches / fig_width_inches) * (fig_width_inches / (img_width / self.fig.dpi))
                        elif logo_height_inches > 0 and logo_width_inches == 0:
                            logo_zoom = (logo_height_inches / fig_height_inches) * (fig_height_inches / (img_height / self.fig.dpi))
                        else:
                            # Si ambos están especificados, usar el menor factor para evitar distorsión
                            zoom_width = (logo_width_inches / fig_width_inches) * (fig_width_inches / (img_width / self.fig.dpi))
                            zoom_height = (logo_height_inches / fig_height_inches) * (fig_height_inches / (img_height / self.fig.dpi))
                            logo_zoom = min(zoom_width, zoom_height)
                    
                    elif size_method == "fraction" and (logo_width_fraction > 0 or logo_height_fraction > 0):
                        # Convertir fracción de figura a factor de zoom
                        img_height, img_width = logo_img.shape[:2] if len(logo_img.shape) > 2 else logo_img.shape
                        fig_width_inches, fig_height_inches = self.fig.get_size_inches()
                        
                        if logo_width_fraction > 0 and logo_height_fraction == 0:
                            logo_zoom = logo_width_fraction * (fig_width_inches / (img_width / self.fig.dpi))
                        elif logo_height_fraction > 0 and logo_width_fraction == 0:
                            logo_zoom = logo_height_fraction * (fig_height_inches / (img_height / self.fig.dpi))
                        else:
                            zoom_width = logo_width_fraction * (fig_width_inches / (img_width / self.fig.dpi))
                            zoom_height = logo_height_fraction * (fig_height_inches / (img_height / self.fig.dpi))
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
                    
                    # Si se solicita, redimensionar la imagen manteniendo las proporciones
                    if logo_config.get("preserve_aspect_ratio", True) and size_method != "zoom":
                        # Ya se ha calculado el factor de zoom considerando proporciones
                        pass
                    
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
                    
                    print(f"ℹ️ Añadiendo logo en footer:")
                    print(f"  - Archivo: '{logo_path}'")
                    print(f"  - Método de tamaño: '{size_method}'")
                    print(f"  - Factor de zoom calculado: {logo_zoom:.4f}")
                    print(f"  - Posición: x={logo_x}, y={footer_y}")
                    
                    # Crear un OffsetImage con la imagen del logo
                    imagebox = OffsetImage(logo_img, zoom=logo_zoom)
                    
                    # Posicionar el logo según la configuración
                    ab = AnnotationBbox(
                        imagebox, 
                        (logo_x, footer_y),    # Posición personalizable
                        xycoords='figure fraction',
                        box_alignment=logo_align,
                        frameon=False
                    )
                    
                    # Añadir el logo a la figura
                    self.fig.add_artist(ab)
                except Exception as e:
                    print(f"⚠️ Error al cargar el logo {logo_path}: {e}")
    
    def finalize(self):
        """Finaliza y guarda el gráfico."""
        # No usar tight_layout que puede afectar la posición de los títulos
        # plt.tight_layout()
        # Elimina o comenta la siguiente línea:
        # self.ax.set_position([0.15, 0.05, 0.8, 0.8])
        # Guardar si se especifica un archivo de salida
        if "outfile" in self.params:
            dpi = int(self.params.get("dpi", 300))
            formatos = self.params.get("formats", ["png"])
            base_outfile = str(self.params["outfile"]).rsplit(".", 1)[0]
            for fmt in formatos:
                outfile = f"{base_outfile}.{fmt}"
                self.fig.savefig(
                    outfile,
                    dpi=dpi,
                    bbox_inches=None
                )
                print(f"✅ Gráfico guardado en: {outfile}")
        plt.close(self.fig)

def _load_yaml(path: Path) -> dict:
    """Carga configuración desde archivo YAML."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def _merge_params(base: dict, override: dict) -> dict:
    """
    Combina parámetros base con sobreescrituras, asegurando que las configuraciones
    de nivel inferior (anidadas) tengan prioridad sobre las globales.
    """
    result = base.copy()
    for k, v in override.items():
        if isinstance(v, dict) and k in result and isinstance(result[k], dict):
            result[k] = _merge_params(result[k], v)
        else:
            result[k] = v
            
    # Asegurar que las configuraciones específicas de título y subtítulo tengan prioridad
    if 'title_config' in override and 'fontsize' in override['title_config']:
        # Guardar explícitamente el tamaño de fuente del título en un campo especial
        # para asegurar que no se pierda
        result['_explicit_title_fontsize'] = float(override['title_config']['fontsize'])
    
    if 'subtitle_config' in override and 'fontsize' in override['subtitle_config']:
        # Guardar explícitamente el tamaño de fuente del subtítulo en un campo especial
        # para asegurar que no se pierda
        result['_explicit_subtitle_fontsize'] = float(override['subtitle_config']['fontsize'])
            
    return result

def _render_simple_stackedbarh(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    """Gráfico de barras horizontales apiladas con elementos básicos de matplotlib."""
    # Cargar configuración
    cfg = _load_yaml(config)
    
    # Cargar template si existe
    if "template" in cfg:
        tpl = _load_yaml(Path(cfg["template"]))
        params = _merge_params(tpl, cfg)
    else:
        params = cfg
    
    # Depuración para tamaños de fuente
    print("\nDEBUG: Configuración final de tamaños de fuente:")
    print(f" - title_font_size (global): {params.get('title_font_size')}")
    print(f" - subtitle_font_size (global): {params.get('subtitle_font_size')}")
    
    if 'title_config' in params and 'fontsize' in params['title_config']:
        print(f" - title_config.fontsize: {params['title_config']['fontsize']}")
    else:
        print(" - title_config.fontsize: No definido")
        
    if 'subtitle_config' in params and 'fontsize' in params['subtitle_config']:
        print(f" - subtitle_config.fontsize: {params['subtitle_config']['fontsize']}")
    else:
        print(" - subtitle_config.fontsize: No definido")
        
    # Valores explícitos guardados durante el merge
    print(f" - _explicit_title_fontsize: {params.get('_explicit_title_fontsize')}")
    print(f" - _explicit_subtitle_fontsize: {params.get('_explicit_subtitle_fontsize')}")
    
    # Cargar datos
    if "csv" in params.get("data", {}):
        df = pd.read_csv(params["data"]["csv"])
    else:
        rows = params.get("data", {}).get("inline", {}).get("rows", [])
        df = pd.DataFrame(rows)

    # Añadir información de depuración sobre categorías
    cat_col = params.get("data", {}).get("category_col", "")
    print(f"🔍 Columna de categorías configurada: '{cat_col}'")
    if cat_col in df.columns:
        print(f"✅ Columna '{cat_col}' encontrada en el DataFrame")
        print(f"📊 Ejemplos de valores en '{cat_col}':")
        for i, val in enumerate(df[cat_col].head(5)):
            print(f"  - {i+1}: {val}")
    else:
        print(f"❌ Columna '{cat_col}' NO encontrada en el DataFrame")
        print(f"📋 Columnas disponibles: {list(df.columns)}")
        
    # Crear y renderizar el gráfico
    chart = SimpleBarChart(params, df)
    
    # Depurar información de banderas si está habilitado
    if params.get("debug", False):
        chart.debug_flag_paths()
    
    chart.create_figure()
    chart.draw_bars()
    
    # Usar configure_axes normal en lugar de configure_axes_with_flags cuando las banderas están desactivadas
    if not params.get("flags", {}).get("enabled", False):
        chart.configure_axes()
    else:
        chart.configure_axes_with_flags()
        
    chart.add_legend()
    chart.add_labels()
    chart.add_title()
    chart.add_footer()
    chart.finalize()

def add_command(app: typer.Typer) -> None:
    app.command("simple_stackedbarh")(_render_simple_stackedbarh)

if __name__ == "__main__":
    # Para pruebas directas
    import sys
    if len(sys.argv) > 1:
        _render_simple_stackedbarh(Path(sys.argv[1]))
    else:
        print("Uso: python simple_stackedbarh.py ruta/al/config.yml")