from pathlib import Path
import typer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

from app.plots.base_chart import BaseChart

class LineChart(BaseChart):
    """
    Clase para gráficos de líneas.
    Hereda de BaseChart e implementa los métodos específicos para este tipo de gráfico.
    """
    def prepare_data(self):
        """Prepara los datos para el gráfico."""
        # Obtener la configuración de columnas
        data_config = self.params.get("data_source", {})
        column_mapping = data_config.get("column_mapping", {})
        
        # Validar que existe la columna para el eje x
        x_col = column_mapping.get("x")
        if not x_col:
            raise ValueError("No se especificó una columna para el eje x en column_mapping.x")
        
        # Validar que existe al menos una serie para graficar
        series_config = column_mapping.get("series", [])
        if not series_config:
            raise ValueError("No se especificaron series para graficar en column_mapping.series")
        
        # Obtener información de las columnas
        self.x_col = x_col
        self.series_cols = series_config
        
        # Validar que las columnas existen en el dataframe
        if self.x_col not in self.df.columns:
            raise ValueError(f"La columna '{self.x_col}' no existe en el DataFrame")
        
        for serie in self.series_cols:
            if serie.get("column") not in self.df.columns:
                raise ValueError(f"La columna '{serie.get('column')}' no existe en el DataFrame")
        
        # Ordenar datos por eje x si es necesario
        if self.params.get("sort_by_x", True):
            self.df = self.df.sort_values(by=self.x_col)
        
        # Guardar valores de x como atributo
        self.x_values = self.df[self.x_col].tolist()
        
        # Información de depuración
        print(f"📊 Preparando datos para gráfico de líneas:")
        print(f"  - Columna X: {self.x_col}")
        print(f"  - Series: {[s.get('name') for s in self.series_cols]}")
        print(f"  - Total de puntos: {len(self.x_values)}")

    def setup_dimensions(self):
        """Configura las dimensiones del gráfico basado en el contenido."""
        # Obtener configuración de dimensionamiento automático
        autosize = self.params.get("autosize", {})
        
        # Si el dimensionamiento automático está habilitado
        if autosize.get("enabled", False):
            # Calcular ancho basado en el número de puntos
            n_points = len(self.x_values)
            width_per_point = float(autosize.get("width_per_point", 0.2))
            
            # Calcular ancho total necesario
            total_width = n_points * width_per_point
            
            # Aplicar límites min/max
            width_in = min(
                float(autosize.get("max_width", 14)),
                max(float(autosize.get("min_width", 8)), total_width)
            )
            
            # Altura proporcional al ancho, respetando una relación de aspecto
            aspect_ratio = float(autosize.get("aspect_ratio", 0.6))  # Altura/Ancho
            height_in = width_in * aspect_ratio
            
            # Aplicar límites min/max a la altura
            height_in = min(
                float(autosize.get("max_height", 10)),
                max(float(autosize.get("min_height", 5)), height_in)
            )
        else:
            # Usar dimensiones fijas desde los parámetros
            width_in = float(self.params.get("width_in", 10))
            height_in = float(self.params.get("height_in", 6))
        
        # Actualizar los parámetros con las dimensiones calculadas
        self.params.update({
            "width_in": width_in,
            "height_in": height_in
        })
        
        print(f"📏 Dimensiones del gráfico: {width_in:.2f}\" × {height_in:.2f}\"")

    def draw_chart(self):
        """Dibuja el gráfico de líneas."""
        # Obtener configuración específica para el gráfico de líneas
        line_config = self.params.get("linechart", {})
        
        # Estilos básicos de línea
        linewidth = line_config.get("linewidth", 2.5)
        linestyle = line_config.get("linestyle", "-")
        alpha = line_config.get("alpha", 1.0)
        
        # Configuración de marcadores
        marker_config = line_config.get("marker", {})
        use_markers = marker_config.get("enabled", True)
        marker_size = marker_config.get("size", 6)
        marker_symbol = marker_config.get("symbol", "o")
        marker_edgewidth = marker_config.get("edgewidth", 1.5)
        marker_edgecolor = marker_config.get("edgecolor", "white")
        
        # Lista para almacenar las líneas para la leyenda
        lines = []
        labels = []
        
        # Dibujar cada serie de datos
        for i, serie in enumerate(self.series_cols):
            col_name = serie.get("column")
            serie_name = serie.get("name", col_name)
            
            # Obtener color específico para esta serie o usar un color automático
            color = serie.get("color")
            
            # Dibujar la línea
            line, = self.ax.plot(
                self.df[self.x_col],
                self.df[col_name],
                label=serie_name,
                color=color,
                linewidth=linewidth,
                linestyle=serie.get("linestyle", linestyle),
                alpha=serie.get("alpha", alpha),
                marker=marker_symbol if use_markers else None,
                markersize=marker_size,
                markeredgewidth=marker_edgewidth,
                markeredgecolor=marker_edgecolor,
                markerfacecolor=color
            )
            
            lines.append(line)
            labels.append(serie_name)
            
            print(f"📈 Dibujada línea: {serie_name} (color: {color})")
            
        # Si están configurados, añadir áreas sombreadas bajo las líneas
        if line_config.get("fill_area", False):
            # Para cada serie, rellenar el área bajo la línea
            for i, serie in enumerate(self.series_cols):
                col_name = serie.get("column")
                color = serie.get("color")
                fill_alpha = line_config.get("fill_alpha", 0.2)
                
                self.ax.fill_between(
                    self.df[self.x_col], 
                    0, 
                    self.df[col_name],
                    color=color,
                    alpha=fill_alpha
                )
                
                print(f"  - Área sombreada añadida para: {serie.get('name')}")
        
        # Añadir anotaciones de región si están configuradas
        annotations = self.params.get("annotations", {})
        regions = annotations.get("regions", [])
        
        if regions:
            print(f"🔍 Añadiendo {len(regions)} regiones de anotación...")
            
            for region in regions:
                label = region.get("label", "")
                from_x = region.get("from")
                to_x = region.get("to")
                color = region.get("color", "#f8f8f8")
                alpha = float(region.get("alpha", 0.3))
                
                # Validar que existen los valores from y to
                if from_x is None or to_x is None:
                    print(f"  ⚠️ Región '{label}' no tiene valores from/to definidos")
                    continue
                
                # Intentar convertir from/to al mismo tipo que los valores X
                # Esto es importante para fechas, números, etc.
                try:
                    # Si x_values son fechas, convertir from/to a fechas
                    if pd.api.types.is_datetime64_any_dtype(self.df[self.x_col]):
                        from_x = pd.to_datetime(from_x)
                        to_x = pd.to_datetime(to_x)
                    elif isinstance(from_x, str) and isinstance(to_x, str):
                        # Para valores de string, convertir a los índices correspondientes
                        from_idx = self.df[self.df[self.x_col] == from_x].index
                        to_idx = self.df[self.df[self.x_col] == to_x].index
                        
                        if len(from_idx) > 0 and len(to_idx) > 0:
                            # Usar los valores actuales en el eje X
                            from_x_idx = from_idx[0]
                            to_x_idx = to_idx[0]
                            
                            # Obtener los valores X correspondientes a esos índices
                            from_x = self.df.iloc[from_x_idx][self.x_col]
                            to_x = self.df.iloc[to_x_idx][self.x_col]
                        else:
                            print(f"  ⚠️ No se encontraron valores {from_x} o {to_x} en la columna {self.x_col}")
                            continue
                    
                    # Añadir la región sombreada
                    self.ax.axvspan(from_x, to_x, alpha=alpha, color=color, label=label if label else None)
                    
                    # Añadir una etiqueta en el centro de la región
                    if label:
                        # Calcular la posición central en X
                        if pd.api.types.is_datetime64_any_dtype(self.df[self.x_col]):
                            mid_x = pd.Timestamp(from_x) + (pd.Timestamp(to_x) - pd.Timestamp(from_x)) / 2
                        elif isinstance(from_x, str) and isinstance(to_x, str):
                            # Para strings, usar el índice de los valores en el eje X
                            try:
                                idx_from = self.df[self.df[self.x_col] == from_x].index[0]
                                idx_to = self.df[self.df[self.x_col] == to_x].index[0]
                                mid_idx = (idx_from + idx_to) / 2
                                mid_idx = int(mid_idx) if mid_idx.is_integer() else mid_idx
                                mid_x = self.df.iloc[int(mid_idx)][self.x_col]
                            except (IndexError, ValueError):
                                # Si no se encuentra exactamente, usar un valor intermedio aproximado
                                mid_x = from_x  # Usar el valor 'from' como fallback
                        else:
                            # Para números, calcular el punto medio directamente
                            mid_x = from_x + (to_x - from_x) / 2
                        
                        # Calcular la posición Y (en la parte superior del gráfico)
                        y_max = self.ax.get_ylim()[1]
                        label_y = y_max * 0.95
                        
                        self.ax.text(
                            mid_x, label_y, label,
                            ha='center', va='top',
                            fontsize=10, color='#555555',
                            bbox=dict(
                                facecolor='white',
                                edgecolor='none',
                                alpha=0.7,
                                pad=3
                            )
                        )
                    
                    print(f"  ✓ Región añadida: {label} ({from_x} a {to_x})")
                except Exception as e:
                    print(f"  ⚠️ Error al añadir región '{label}': {e}")

        # Configurar grid
        grid_config = self.params.get("grid", True)
        if isinstance(grid_config, dict):
            # Configuración avanzada del grid
            show_grid = grid_config.get("show", True)
            grid_axis = grid_config.get("axis", "both")  # "x", "y", "both"
            grid_linestyle = grid_config.get("linestyle", "--")
            grid_color = grid_config.get("color", "#cccccc")
            grid_alpha = grid_config.get("alpha", 0.7)
            grid_linewidth = grid_config.get("linewidth", 0.5)
            
            if show_grid:
                self.ax.grid(
                    visible=True,
                    which='major',
                    axis=grid_axis,
                    linestyle=grid_linestyle,
                    linewidth=grid_linewidth,
                    color=grid_color,
                    alpha=grid_alpha
                )
        else:
            # Configuración simple del grid (booleano)
            self.ax.grid(visible=grid_config, which='major', linestyle='--', linewidth=0.5, alpha=0.7)

    def configure_axes(self):
        """Configura los ejes y sus elementos."""
        # Configuración del eje X
        xaxis_config = self.params.get("xaxis", {})
        
        # Configuración de fuente para las etiquetas del eje X
        xfont_config = xaxis_config.get("font", {})
        xfont_size = xfont_config.get("size", 10)
        xfont_color = xfont_config.get("color", "#333333")
        
        # Configuración del eje Y
        yaxis_config = self.params.get("yaxis", {})
        
        # Configuración de fuente para las etiquetas del eje Y
        yfont_config = yaxis_config.get("font", {})
        yfont_size = yfont_config.get("size", 10)
        yfont_color = yfont_config.get("color", "#333333")
        
        # Formatear las etiquetas del eje X
        plt.xticks(fontsize=xfont_size, color=xfont_color)
        
        # Configurar rotación para fechas
        if pd.api.types.is_datetime64_any_dtype(self.df[self.x_col]):
            # Determinar el formato de fecha según los datos
            self.ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y-%m-%d"))
            plt.xticks(rotation=45, ha="right")
            
            # Ajustar el número de ticks para que no se superpongan
            self.fig.autofmt_xdate()
        
        # Formatear las etiquetas del eje Y
        plt.yticks(fontsize=yfont_size, color=yfont_color)
        
        # Configurar límites de los ejes
        if xaxis_config.get("limit"):
            xlim = xaxis_config.get("limit")
            if isinstance(xlim, list) and len(xlim) == 2:
                self.ax.set_xlim(xlim)
        
        if yaxis_config.get("limit"):
            ylim = yaxis_config.get("limit")
            if isinstance(ylim, list) and len(ylim) == 2:
                self.ax.set_ylim(ylim)
        else:
            # Por defecto, comenzar el eje Y desde cero
            y_min, y_max = self.ax.get_ylim()
            if y_min > 0:
                self.ax.set_ylim(bottom=0)
        
        # Títulos de los ejes
        if xaxis_config.get("title"):
            self.ax.set_xlabel(
                xaxis_config.get("title"),
                fontsize=xaxis_config.get("title_fontsize", 12),
                color=xaxis_config.get("title_color", "#333333"),
                fontweight=xaxis_config.get("title_fontweight", "normal")
            )
        
        if yaxis_config.get("title"):
            self.ax.set_ylabel(
                yaxis_config.get("title"),
                fontsize=yaxis_config.get("title_fontsize", 12),
                color=yaxis_config.get("title_color", "#333333"),
                fontweight=yaxis_config.get("title_fontweight", "normal")
            )
        
        # Ocultar spines si se especifica
        if xaxis_config.get("hide_spines", False):
            self.ax.spines['bottom'].set_visible(False)
        if yaxis_config.get("hide_spines", False):
            self.ax.spines['left'].set_visible(False)
        
        # Ocultar ticks si se especifica
        if not xaxis_config.get("show_ticks", True):
            self.ax.xaxis.set_ticks_position('none')
        if not yaxis_config.get("show_labels", True):
            self.ax.xaxis.set_ticklabels([])
            
        if not yaxis_config.get("show_ticks", True):
            self.ax.yaxis.set_ticks_position('none')
        if not yaxis_config.get("show_labels", True):
            self.ax.yaxis.set_ticklabels([])

    def add_labels(self):
        """Añade etiquetas de valores a los puntos en el gráfico."""
        # Verificar si las etiquetas de valores están habilitadas
        value_labels = self.params.get("value_labels", False)
        
        if not value_labels:
            return
        
        # Configuración de etiquetas de valores
        if isinstance(value_labels, dict):
            # Configuración avanzada
            show_labels = value_labels.get("show", True)
            value_format = value_labels.get("format", "{:.1f}")
            fontsize = value_labels.get("fontsize", 9)
            fontweight = value_labels.get("fontweight", "normal")
            color = value_labels.get("color", "#333333")
            background = value_labels.get("background", False)
            bg_color = value_labels.get("bg_color", "white")
            bg_alpha = value_labels.get("bg_alpha", 0.7)
            x_offset = value_labels.get("x_offset", 0)
            y_offset = value_labels.get("y_offset", 5)
            ha = value_labels.get("ha", "center")
            va = value_labels.get("va", "bottom")
            
            # Específico para últimos valores
            only_last = value_labels.get("only_last", False)
            only_first = value_labels.get("only_first", False)
            skip = value_labels.get("skip", 1)  # Mostrar cada N puntos
        else:
            # Configuración simple (booleano)
            show_labels = value_labels
            value_format = "{:.1f}"
            fontsize = 9
            fontweight = "normal"
            color = "#333333"
            background = False
            bg_color = "white"
            bg_alpha = 0.7
            x_offset = 0
            y_offset = 5
            ha = "center"
            va = "bottom"
            only_last = False
            only_first = False
            skip = 1
        
        if not show_labels:
            return
            
        # Añadir etiquetas a cada serie
        for serie in self.series_cols:
            col_name = serie.get("column")
            color = serie.get("color", color)
            
            # Obtener valores X e Y
            x_values = self.df[self.x_col].tolist()
            y_values = self.df[col_name].tolist()
            
            # Determinar qué puntos mostrar
            if only_last:
                # Mostrar solo el último valor
                points_to_label = [(x_values[-1], y_values[-1])]
            elif only_first:
                # Mostrar solo el primer valor
                points_to_label = [(x_values[0], y_values[0])]
            else:
                # Mostrar cada N puntos según skip
                points_to_label = [(x, y) for i, (x, y) in enumerate(zip(x_values, y_values)) if i % skip == 0]
            
            # Añadir etiquetas a los puntos seleccionados
            for x, y in points_to_label:
                label_text = value_format.format(y)
                
                # Crear un bbox si se requiere fondo
                bbox_props = None
                if background:
                    bbox_props = dict(
                        boxstyle="round,pad=0.3",
                        fc=bg_color,
                        ec="none",
                        alpha=bg_alpha
                    )
                
                # Añadir la etiqueta
                self.ax.annotate(
                    label_text,
                    (x, y),
                    xytext=(x_offset, y_offset),
                    textcoords='offset points',
                    fontsize=fontsize,
                    fontweight=fontweight,
                    color=color,
                    ha=ha,
                    va=va,
                    bbox=bbox_props
                )


def linechart(config_path: Path):
    """Función principal para generar un gráfico de líneas."""
    from app.chart_utils import render_chart
    
    try:
        render_chart(LineChart, config_path)
    except Exception as e:
        print(f"❌ Error al generar el gráfico de líneas: {e}")
        raise

def main():
    """Punto de entrada para el CLI."""
    app = typer.Typer()
    
    @app.command()
    def generate(config_path: str):
        """Genera un gráfico de líneas a partir de un archivo de configuración."""
        linechart(Path(config_path))
    
    app()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        linechart(Path(sys.argv[1]))
    else:
        print("❌ Error: Debe proporcionar la ruta al archivo de configuración YAML.")
        sys.exit(1)