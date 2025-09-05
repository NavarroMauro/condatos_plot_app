from __future__ import annotations

from pathlib import Path
import yaml
import typer
from rich import print as rprint

from .styling import apply_style
from .io_utils import save_fig_multi  # aún usado por layout.finish_and_save
from .branding import add_branding     # llamado por layout.finish_and_save
from .layout import apply_frame, finish_and_save

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# === NUEVOS IMPORTS DE HELPERS ===
from .helpers import norm_legend_loc, get_label_fmt, _bar_cfg, _print_ok
from .plot_helpers import (
    add_flags_stackedbarh,
    add_flags_stackedbar,
    draw_segment_labels_stacked,
    draw_total_labels,
    adjust_yaxis_labels,
    autosize_figure,
    draw_broken_axis_marks,
    get_bar_style,
    add_titles
)

app = typer.Typer(help="Condatos · Figuras estáticas multi-formato")

def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge two dictionaries, with values from override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def _load_yaml(p: Path) -> dict:
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _merge_params(tpl: dict, cfg: dict) -> dict:
    """Helper function to merge template and config parameters."""
    base = deep_merge(tpl, {"outfile": cfg.get("outfile", "out/figure")})
    return deep_merge(base, cfg.get("overrides", {}))

# ---------------- LINE ----------------
@app.command()
def line(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)
    data = cfg["data"]

    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))
    
    if params.get("palette"):
        sns.set_palette(params["palette"])
    fig, ax = plt.subplots()
    apply_frame(fig, params)

    if "csv" in data:
        df = pd.read_csv(data["csv"])
        x = df.iloc[:, 0]
        for col in df.columns[1:]:
            ax.plot(
                x, df[col], label=str(col),
                linewidth=params["line"]["linewidth"],
                marker=(params["line"]["marker"] or None)
            )
        ax.legend()
    else:
        x = data["inline"]["x"]
        y_series = data["inline"].get("y_series")
        if y_series:
            for name, ys in y_series.items():
                ax.plot(
                    x, ys, label=str(name),
                    linewidth=params["line"]["linewidth"],
                    marker=(params["line"]["marker"] or None)
                )
            ax.legend()
        else:
            y = data["inline"]["y"]
            ax.plot(
                x, y,
                linewidth=params["line"]["linewidth"],
                marker=(params["line"]["marker"] or None)
            )

    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    if params.get("grid"):
        ax.grid(True, linewidth=0.4, alpha=0.4)

    finish_and_save(fig, params)
    plt.close(fig)
    _print_ok(params)

# ---------------- BAR ----------------
@app.command()
def bar(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)
    data = cfg["data"]

    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    if params.get("palette"):
        sns.set_palette(params["palette"])
    fig, ax = plt.subplots()
    apply_frame(fig, params)
    barcfg = _bar_cfg(params)

    if "csv" in data:
        df = pd.read_csv(data["csv"])
        cats = df.iloc[:, 0].astype(str).tolist()
        vals = df.iloc[:, 1].astype(float).tolist()
    else:
        cats = list(map(str, data["inline"]["categories"]))
        vals = list(map(float, data["inline"]["values"]))

    x = np.arange(len(cats))
    bars = ax.bar(
        x, vals, width=barcfg["bar_width"],
        linewidth=barcfg["linewidth"],
        edgecolor=(barcfg["edgecolor"] or None)
    )

    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    ax.set_xticks(x, cats, rotation=params.get("rotate_xticks", 0))
    if params.get("grid"):
        ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)

    if params.get("value_labels", False):
        fmt = "{:" + params.get("value_fmt", ".2f") + "}"
        ylim = ax.get_ylim()
        dy = params.get("value_offset", 0.02) * (ylim[1] - ylim[0])
        for rect, v in zip(bars, vals):
            ax.text(
                rect.get_x() + rect.get_width() / 2.0,
                rect.get_height() + dy,
                fmt.format(v),
                ha="center", va="bottom", fontsize=8
            )

    finish_and_save(fig, params)
    plt.close(fig)
    _print_ok(params)

# ---------------- BARH ----------------
@app.command()
def barh(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)
    data = cfg["data"]

    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    if params.get("palette"):
        sns.set_palette(params["palette"])
    fig, ax = plt.subplots()
    apply_frame(fig, params)
    barcfg = _bar_cfg(params)

    if "csv" in data:
        df = pd.read_csv(data["csv"])
        cats = df.iloc[:, 0].astype(str).tolist()
        vals = df.iloc[:, 1].astype(float).tolist()
    else:
        cats = list(map(str, data["inline"]["categories"]))
        vals = list(map(float, data["inline"]["values"]))
        
    bar_style = get_bar_style(params)

    y = np.arange(len(cats))
    bars = ax.barh(
        y, vals, height=barcfg["bar_width"],
        linewidth=barcfg["linewidth"],
        edgecolor=(barcfg["edgecolor"] or None)
    )

    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    ax.set_yticks(y, cats)
    if params.get("grid"):
        ax.grid(True, axis="x", linewidth=0.4, alpha=0.4)

    if params.get("value_labels", False):
        fmt = "{:" + params.get("value_fmt", ".2f") + "}"
        xlim = ax.get_xlim()
        dx = params.get("value_offset", 0.02) * (xlim[1] - xlim[0])
        for rect, v in zip(bars, vals):
            ax.text(
                rect.get_width() + dx, rect.get_y() + rect.get_height() / 2.0,
                fmt.format(v), ha="left", va="center", fontsize=8
            )

    finish_and_save(fig, params)
    plt.close(fig)
    _print_ok(params)

# ---------------- STACKEDBAR VERTICAL ----------------
@app.command()
def stackedbar(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)
    data = cfg["data"]

    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    fig, ax = plt.subplots()
    apply_frame(fig, params)
    barcfg = _bar_cfg(params)
    


    if "csv" in data:
        df = pd.read_csv(data["csv"])
    else:
        raise ValueError("Para stackedbar, usa data.csv con columnas: categoría + series.")

    cat_col = params.get("category_col") or df.columns[0]
    series_order = params.get("series_order")
    cols_map = {c.lower(): c for c in df.columns}

    if series_order:
        missing = [s for s in series_order if s.lower() not in cols_map]
        if missing:
            raise KeyError(f"No encontré estas series en el CSV: {missing}. Columnas vistas: {list(df.columns)}")
        cols = [cols_map[s.lower()] for s in series_order]
    else:
        noise = {"rank","code","pais","country","flag_url","total"}
        numeric_cols = [c for c in df.columns if c != cat_col and c.lower() not in noise and pd.api.types.is_numeric_dtype(df[c])]
        if not numeric_cols:
            raise ValueError("No hay columnas numéricas para apilar. Usa overrides.series_order.")
        cols = numeric_cols

    cats = df[cat_col].astype(str).tolist()
    M = np.vstack([df[c].astype(float).to_numpy() for c in cols])  # (S,N)

    percent = bool(params.get("percent", False))
    if percent:
        colsum = M.sum(axis=0)
        colsum[colsum == 0] = 1.0
        M = M / colsum * 100.0

    colors = None
    if "colors" in params and isinstance(params["colors"], dict):
        colors = [params["colors"].get(s, None) for s in cols]

    x = np.arange(len(cats))
    bottoms = np.zeros(len(cats), dtype=float)
    for i, (serie, vals) in enumerate(zip(cols, M)):
        kw = dict(label=str(serie))
        if colors and colors[i]:
            kw["color"] = colors[i]
        ax.bar(x, vals, bottom=bottoms,
               width=barcfg["bar_width"],
               linewidth=barcfg["linewidth"],
               edgecolor=(barcfg["edgecolor"] or None),
               **kw)
        bottoms += vals

    ax.set_xticks(x, cats, rotation=params.get("rotate_xticks", 0))

    if bool(params.get("legend", True)):
        leg_loc = norm_legend_loc(params.get("legend_loc", "upper right"))
        ax.legend(loc=leg_loc, frameon=False, fontsize=8)

    if params.get("grid"):
        ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)

    min_h = float(params.get("min_label_height", 0.0))
    seg_fmt_default = "{:.0f}%" if percent else "{:.0f}"
    seg_fmt = get_label_fmt(params, default=seg_fmt_default)
    draw_segment_labels_stacked(
        ax, M, "v",
        show=bool(params.get("value_labels", False)),
        percent=percent,
        min_label_height=min_h,
        fmt=seg_fmt
    )

    totals = M.sum(axis=0)
    tot_fmt = get_label_fmt(params, default="{:.0f}")
    draw_total_labels(
        ax, totals, positions=x, orientation="v",
        show=bool(params.get("total_labels", False)),
        fmt=tot_fmt,
        dy_pts=float(params.get("total_dy", 3.0))
    )

    add_flags_stackedbar(
        ax, df, cats,
        tops=totals,
        x_positions=x,
        flags_cfg=params.get("flags", {})
    )

    finish_and_save(fig, params)
    plt.close(fig)
    _print_ok(params)

# ---------------- STACKEDBAR HORIZONTAL ----------------
@app.command()
def stackedbarh(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    """
    Crea un gráfico de barras horizontales apiladas.
    """
    # 1. Cargar configuración
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)
    data = cfg["data"]

    # 2. Cargar datos
    if "csv" in data:
        df = pd.read_csv(data["csv"])
    else:
        raise ValueError("Para stackedbarh usa data.csv con columnas: categoría + series.")

    # 3. Configurar figura y estilo
    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))
    
    # Crear figura con tamaño automático según número de filas
    fig = plt.figure()
    N = len(df)
    autosize_figure(fig, params, n_rows=N)
    
    # Aplicar DPI si está especificado
    if params.get("dpi"):
        try:
            fig.set_dpi(float(params["dpi"]))
        except Exception:
            pass

    # 4. Crear y configurar ejes
    ax = fig.add_subplot(111)
    
    # Ocultar eje X y spines innecesarios
    ax.xaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 5. Aplicar layout y títulos
    apply_frame(fig, params)

    # 6. Preparar datos para el gráfico
    # Determinar columnas a usar
    cat_col = params.get("category_col") or df.columns[0]
    series_order = params.get("series_order")
    cols_map = {c.lower(): c for c in df.columns}

    # Obtener columnas según series_order o automáticamente
    if series_order:
        missing = [s for s in series_order if s.lower() not in cols_map]
        if missing:
            raise KeyError(f"No encontré series en el CSV: {missing}. Columnas: {list(df.columns)}")
        cols = [cols_map[s.lower()] for s in series_order]
    else:
        noise = {"rank","code","pais","country","flag_url","total"}
        cols = [c for c in df.columns
                if c != cat_col and c.lower() not in noise and pd.api.types.is_numeric_dtype(df[c])]
        if not cols:
            raise ValueError("No hay columnas numéricas para apilar. Define overrides.series_order.")

    # Preparar datos para plotting
    cats = df[cat_col].astype(str).tolist()
    M = np.vstack([df[c].astype(float).to_numpy() for c in cols])  # (S,N)

    # Calcular porcentajes si es necesario
    percent = bool(params.get("percent", False))
    if percent:
        rowsum = M.sum(axis=0)
        rowsum[rowsum == 0] = 1.0
        M = M / rowsum * 100.0

    # 7. Configurar colores y estilo de barras
    colors = None
    if isinstance(params.get("colors"), dict):
        colors = [params["colors"].get(s, None) for s in cols]
    bar_style = get_bar_style(params)

    # 8. Dibujar barras apiladas
    y = np.arange(len(cats))
    lefts = np.zeros(len(cats), dtype=float)
    for i, (serie, vals) in enumerate(zip(cols, M)):
        kw = dict(label=str(serie))
        if colors and colors[i]:
            kw["color"] = colors[i]
        kw.update(bar_style)
        ax.barh(y, vals, left=lefts, **kw)
        lefts += vals

    # 9. Configurar eje Y
    ax.set_yticks(y, cats)
    ax.invert_yaxis()

    # Aplicar configuración del eje Y si existe
    if "yaxis" in params:
        yaxis_cfg = params["yaxis"]
        
        # Configurar fuente
        if "font" in yaxis_cfg:
            font_cfg = yaxis_cfg["font"]
            for label in ax.get_yticklabels():
                label.set_fontsize(font_cfg.get("size", 12))
                label.set_fontfamily(font_cfg.get("family", "DejaVu Sans"))
                label.set_fontweight(font_cfg.get("weight", "normal"))
                label.set_color(font_cfg.get("color", "#333333"))

        # Configurar ticks
        if "ticks" in yaxis_cfg:
            tick_cfg = yaxis_cfg["ticks"]
            ax.tick_params(
                axis='y',
                length=tick_cfg.get("size", 1),
                pad=tick_cfg.get("pad", 8),
                direction=tick_cfg.get("direction", "out")
            )

        # Configurar spine
        if "spines" in yaxis_cfg:
            spine_cfg = yaxis_cfg["spines"]
            if spine_cfg.get("visible", True):
                ax.spines["left"].set_color(spine_cfg.get("color", "#cccccc"))
                ax.spines["left"].set_linewidth(spine_cfg.get("linewidth", 0.5))
            else:
                ax.spines["left"].set_visible(False)

        # Configurar grid
        if "grid" in yaxis_cfg:
            grid_cfg = yaxis_cfg["grid"]
            if grid_cfg.get("enabled", False):
                ax.grid(
                    True,
                    axis="x",
                    color=grid_cfg.get("color", "#eeeeee"),
                    alpha=grid_cfg.get("alpha", 0.5),
                    linewidth=grid_cfg.get("linewidth", 0.5)
                )
            else:
                ax.grid(False)

    # 10. Configurar leyenda
    if bool(params.get("legend", True)):
        legend_font = params.get("legend_font", {})
        leg_loc = norm_legend_loc(params.get("legend_loc", "center right"))
        
        legend = ax.legend(
            loc=leg_loc,
            frameon=False,
            prop={
                'family': legend_font.get("family", "DejaVu Sans"),
                'size': legend_font.get("size", 10),
                'weight': legend_font.get("weight", "normal")
            }
        )
        
        for text in legend.get_texts():
            text.set_color(legend_font.get("color", "#333333"))
            text.set_alpha(float(legend_font.get("alpha", 1.0)))

    # 11. Añadir etiquetas de segmentos
    min_h = float(params.get("min_label_height", 0.0))
    seg_fmt_default = "{:.0f}%" if percent else "{:.0f}"
    seg_fmt = get_label_fmt(params, default=seg_fmt_default)
    draw_segment_labels_stacked(ax, M, "h",
        show=bool(params.get("value_labels", False)),
        percent=percent, min_label_height=min_h, fmt=seg_fmt, params=params)

    # 12. Añadir etiquetas de totales
    totals = lefts    
    tot_fmt = get_label_fmt(params, default="{:.0f}")
    total_cfg = params.get("total_labels", {})
    
    draw_total_labels(
        ax, totals, 
        positions=y, 
        orientation="h",
        show=bool(total_cfg.get("enabled", False)), 
        fmt=tot_fmt,
        dy_pts=float(total_cfg.get("x_offset", 4.0))
    )

    # 13. Añadir banderas
    add_flags_stackedbarh(
        ax, df,
        cats=cats,
        totals=lefts,
        y_positions=y,
        flags_cfg=params.get("flags", {}),
        total_labels_cfg=total_cfg
    )
    
    # 14. Añadir marcas de eje roto si es necesario
    if params.get("broken_axis", False):
        break_threshold = float(params.get("break_threshold", 0.0))
        break_style = params.get("break_style", {})
        
        for i, total in enumerate(totals):
            if total > break_threshold:
                draw_broken_axis_marks(
                    ax=ax,
                    x=break_threshold + (total - break_threshold) * 0.1,
                    y=y[i],
                    width=float(break_style.get("width", 0.03)),
                    height=float(break_style.get("height", 0.015)),
                    angle=float(break_style.get("angle", 45)),
                    color=break_style.get("color", "#333333")
                )

    # 15. Ajustar límites del eje X
    max_value = lefts.max()
    axis_cfg = params.get("axis", {}).get("x", {})
    extra_space = float(axis_cfg.get("extra_space", 0.15))
    ax.set_xlim(right=max_value * (1 + extra_space))

    # 16. Finalizar y guardar
    finish_and_save(fig, params)
    plt.close(fig)
    _print_ok(params)

# ---------------- HEATMAP ----------------
@app.command()
def heatmap(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)
    data = cfg["data"]

    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    fig, ax = plt.subplots()
    apply_frame(fig, params)

    if "csv" in data:
        df = pd.read_csv(data["csv"])
        row_labels = df.iloc[:, 0].astype(str).tolist()
        df_vals = df.iloc[:, 1:]
        col_labels = df_vals.columns.astype(str).tolist()
        M = df_vals.to_numpy(dtype=float)
    else:
        row_labels = list(map(str, data["inline"]["rows"]))
        col_labels = list(map(str, data["inline"]["cols"]))
        M = np.array(data["inline"]["values"], dtype=float)

    sns.heatmap(
        M, ax=ax,
        cmap=params.get("cmap", "viridis"),
        center=params.get("center", None),
        vmin=params.get("vmin", None),
        vmax=params.get("vmax", None),
        linewidths=params.get("linewidths", 0.0),
        cbar=params.get("cbar", True),
        annot=params.get("annot", False),
        fmt=params.get("fmt", ".1f"),
        annot_kws={"fontsize": 7},
    )
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    ax.set_xticks(np.arange(len(col_labels)) + 0.5, col_labels, rotation=0)
    ax.set_yticks(np.arange(len(row_labels)) + 0.5, row_labels, rotation=0)
    
    if "yaxis" in params:
        yaxis_cfg = params["yaxis"]
        
        if "font" in yaxis_cfg:
            font_cfg = yaxis_cfg["font"]
            for label in ax.get_yticklabels():
                label.set_fontsize(font_cfg.get("size", 12))
                label.set_fontfamily(font_cfg.get("family", "DejaVu Sans"))
                label.set_fontweight(font_cfg.get("weight", "normal"))
                label.set_color(font_cfg.get("color", "#333333"))

        if "ticks" in yaxis_cfg:
            tick_cfg = yaxis_cfg["ticks"]
            ax.tick_params(
                axis='y',
                length=tick_cfg.get("size", 1),
                pad=tick_cfg.get("pad", 8),
                direction=tick_cfg.get("direction", "out")
            )

        if "spines" in yaxis_cfg:
            spine_cfg = yaxis_cfg["spines"]
            if spine_cfg.get("visible", True):
                ax.spines["left"].set_color(spine_cfg.get("color", "#cccccc"))
                ax.spines["left"].set_linewidth(spine_cfg.get("linewidth", 0.5))
            else:
                ax.spines["left"].set_visible(False)

        if "grid" in yaxis_cfg:
            grid_cfg = yaxis_cfg["grid"]
            ax.grid(
                grid_cfg.get("enabled", False),
                axis="x",
                color=grid_cfg.get("color", "#eeeeee"),
                alpha=grid_cfg.get("alpha", 0.5),
                linewidth=grid_cfg.get("linewidth", 0.5)
            )

    adjust_yaxis_labels(ax)

    finish_and_save(fig, params)
    plt.close(fig)
    _print_ok(params)

# ---------------- CHOROPLETH ----------------
@app.command()
def choropleth(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    """Mapa coroplético LATAM/mundo por clave (ej. ISO_A3) con opciones de estilo."""
    try:
        import geopandas as gpd
    except Exception:
        rprint("[red]Faltan dependencias de mapas.[/red] Instala: geopandas shapely pyproj fiona mapclassify (conda-forge).")
        raise

    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = _merge_params(tpl, cfg)

    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))
    fig, ax = plt.subplots()
    apply_frame(fig, params)

    geofile = Path(params["geofile"])
    if not geofile.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {geofile}")
    geo_key = params.get("geo_key", "ISO_A3")

    scheme = params.get("scheme", None)
    if scheme:
        try:
            import mapclassify  # noqa: F401
        except Exception as e:
            raise RuntimeError("Se indicó 'scheme' pero falta 'mapclassify' (conda-forge).") from e

    gdf = gpd.read_file(geofile)
    to_crs = params.get("to_crs")
    if to_crs:
        try:
            gdf = gdf.to_crs(to_crs)
        except Exception as e:
            raise RuntimeError(f"No se pudo reproyectar a {to_crs}: {e}") from e

    dcfg = cfg.get("data", tpl.get("data", {}))
    if "csv" in dcfg:
        df = pd.read_csv(dcfg["csv"])
        data_key = dcfg.get("csv_key", "iso3")
        value_col = dcfg.get("value_col", "valor")
    else:
        rows = dcfg["inline"]["rows"]
        data_key = dcfg["inline"]["key"]
        value_col = dcfg["inline"]["value"]
        df = pd.DataFrame(rows)

    gdf[geo_key] = gdf[geo_key].astype(str).str.upper()
    df[data_key] = df[data_key].astype(str).str.upper()
    gdf = gdf.merge(df[[data_key, value_col]], left_on=geo_key, right_on=data_key, how="left")

    ax.set_axis_off()
    ax.set_facecolor(params.get("ocean_color", "white"))
    fig.patch.set_facecolor("white")

    cmap = params.get("cmap", "magma")
    missing_color = params.get("missing_color", "#eeeeee")
    edgecolor = params.get("edgecolor", "#ffffff")
    linewidth = float(params.get("linewidth", 0.4))
    boundary_color = params.get("boundary_color", "#A3A3A3")
    boundary_lw = float(params.get("boundary_lw", 0.35))
    draw_boundaries = bool(params.get("draw_boundaries", True))
    tight_margin = float(params.get("tight_margin", 0.02))

    legend = bool(params.get("legend", True))
    legend_kwds = {
        "title": params.get("legend_title", ""),
        "frameon": False,
        "fontsize": 8,
        "fmt": "{:.0f}",
        "loc": params.get("legend_loc", "lower left"),
    }
    if params.get("legend_outside", False):
        bx, by = params.get("legend_bbox", [1.02, 0.5])
        legend_kwds.update({"bbox_to_anchor": (bx, by)})

    plot_kwargs = dict(
        column=value_col,
        cmap=cmap,
        linewidth=linewidth,
        edgecolor=edgecolor,
        missing_kwds={"color": missing_color, "edgecolor": edgecolor, "hatch": "///"},
    )
    if scheme:
        plot_kwargs.update(dict(scheme=scheme, k=int(params.get("k", 5)), legend=legend, legend_kwds=legend_kwds))
    else:
        plot_kwargs["legend"] = False

    gdf.plot(ax=ax, **plot_kwargs)

    if draw_boundaries:
        gdf.boundary.plot(ax=ax, color=boundary_color, linewidth=boundary_lw, zorder=5)

    if params.get("labels", False):
        rep = gdf.dropna(subset=[value_col]).copy()
        rep["rep_pt"] = rep.geometry.representative_point()
        for _, row in rep.iterrows():
            x, y = row["rep_pt"].x, row["rep_pt"].y
            ax.text(
                x, y, str(row[geo_key]),
                ha="center", va="center",
                fontsize=float(params.get("label_size", 6)), zorder=6
            )

    ax.margins(x=tight_margin, y=tight_margin)

    finish_and_save(fig, params)
    plt.close(fig)
    rprint(f"[bold green]OK[/bold green] → {params['outfile']}.[{','.join(params['formats'])}]")

if __name__ == "__main__":
    app()