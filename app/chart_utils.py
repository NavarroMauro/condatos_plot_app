import seaborn as sns
import pandas as pd
import numpy as np
import yaml
from pathlib import Path

import matplotlib.pyplot as plt

def set_style():
    """Set default style for plots"""
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

def create_bar_chart(data, x, y, title="", xlabel="", ylabel="", color="steelblue", figsize=(10, 6)):
    """
    Create a bar chart
    
    Args:
        data: DataFrame containing the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color: Bar color
        figsize: Figure size as tuple (width, height)
    
    Returns:
        matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=data, x=x, y=y, color=color, ax=ax)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    plt.tight_layout()
    return fig, ax

def create_line_chart(data, x, y, title="", xlabel="", ylabel="", color="blue", figsize=(10, 6)):
    """
    Create a line chart
    
    Args:
        data: DataFrame containing the data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color: Line color
        figsize: Figure size as tuple (width, height)
    
    Returns:
        matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    sns.lineplot(data=data, x=x, y=y, color=color, ax=ax)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    plt.tight_layout()
    return fig, ax

def save_figure(fig, filename, dpi=300, bbox_inches='tight'):
    """
    Save figure to file
    
    Args:
        fig: matplotlib figure
        filename: output filename
        dpi: resolution
        bbox_inches: bounding box
    """
    fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
    
def load_yaml(path):
    """
    Carga un archivo YAML y devuelve su contenido como diccionario.
    
    Args:
        path: Ruta al archivo YAML
        
    Returns:
        dict: Contenido del archivo YAML como diccionario
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def merge_params(tpl, cfg):
    """
    Combina parámetros de template y config, dando prioridad a config.
    
    Args:
        tpl: Diccionario con parámetros del template
        cfg: Diccionario con parámetros de la configuración
        
    Returns:
        dict: Diccionario combinado con los parámetros
    """
    # Crear una copia del template para no modificar el original
    result = tpl.copy()
    
    # Sobrescribir con los valores de config
    for key, value in cfg.items():
        if key == "template":  # Ignorar la referencia al template
            continue
        # Si es un diccionario, hacer merge recursivo
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_params(result[key], value)
        else:
            result[key] = value
    
    return result

def render_chart(chart_class, config_path, **kwargs):
    """
    Función genérica para renderizar un gráfico a partir de un archivo de configuración.
    
    Args:
        chart_class: Clase del gráfico a renderizar
        config_path: Path al archivo YAML de configuración
        **kwargs: Argumentos adicionales para pasar al constructor del gráfico
        
    Returns:
        La instancia del gráfico renderizado
    """
    # Cargar configuración
    cfg = load_yaml(config_path)
    
    # Cargar template si existe
    if "template" in cfg:
        tpl = load_yaml(Path(cfg["template"]))
        params = merge_params(tpl, cfg)
    else:
        params = cfg
    
    # Cargar datos
    data_config = params.get("data", {})
    
    # Buscar archivo de datos por diferentes nombres posibles
    csv_path = None
    for key in ["csv", "source_file", "file", "path"]:
        if key in data_config:
            csv_path = data_config[key]
            break
    
    if csv_path:
        # Intentar cargar el archivo CSV
        try:
            print(f"📂 Cargando datos desde: {csv_path}")
            df = pd.read_csv(csv_path)
            print(f"✅ Datos cargados correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
            print(f"   Columnas disponibles: {list(df.columns)}")
        except Exception as e:
            print(f"❌ Error al cargar el archivo {csv_path}: {e}")
            df = pd.DataFrame()  # DataFrame vacío en caso de error
    else:
        # Si no hay archivo CSV, intentar con datos inline
        inline_data = data_config.get("inline", {})
        if isinstance(inline_data, dict) and inline_data:
            # Formato columnar: {col1: [val1, val2, ...], col2: [...]}
            df = pd.DataFrame(inline_data)
        else:
            # Formato de filas: [{col1: val1, col2: val2, ...}, {...}]
            rows = data_config.get("inline", {}).get("rows", [])
            df = pd.DataFrame(rows)
    
    # Crear y renderizar el gráfico
    chart = chart_class(params, df, **kwargs)
    chart.render()
    
    return chart