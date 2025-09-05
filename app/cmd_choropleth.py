# /app/cmd_choropleth.py
from __future__ import annotations
from pathlib import Path
from rich import print as rprint
from .styling import apply_style
from .io_utils import save_fig_multi

def choropleth(config: Path):
    """Mapa coroplético LATAM/mundo por clave (ej. ISO_A3)."""
    try:
        import geopandas as gpd
        import pandas as pd
        import matplotlib.pyplot as plt
    except Exception:
        rprint("[red]Faltan dependencias de mapas.[/red] Instala: geopandas shapely pyproj fiona mapclassify (conda-forge).")
        raise

    import yaml
    with open(config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    with open(Path(cfg["template"]), "r", encoding="utf-8") as f:
        tpl = yaml.safe_load(f)

    p = tpl | {"outfile": cfg.get("outfile", "out/mapa")} | cfg.get("overrides", {})
    apply_style(p.get("style"), p.get("width_in"), p.get("height_in"))

    geofile = Path(p["geofile"])
    if not geofile.exists():
        raise FileNotFoundError(f"No se encontró el GeoJSON/Shapefile: {geofile}")
    geo_key = p.get("geo_key", "ISO_A3")

    scheme = p.get("scheme")
    if scheme:
        try:
            import mapclassify  # noqa: F401
        except Exception as e:
            raise RuntimeError("Se indicó 'scheme' en la plantilla pero falta 'mapclassify'.") from e

    gdf = gpd.read_file(geofile)

    dcfg = cfg.get("data", tpl.get("data", {}))
    if "csv" in dcfg:
        df = pd.read_csv(dcfg["csv"])
        data_key = dcfg.get("csv_key", "iso3")
        value_col = dcfg.get("value_col", "valor")
    else:
        rows = dcfg["inline"]["rows"]
        key_name = dcfg["inline"]["key"]
        val_name = dcfg["inline"]["value"]
        df = pd.DataFrame(rows).rename(columns={key_name: "iso3", val_name: "valor"})
        data_key, value_col = "iso3", "valor"

    gdf[geo_key] = gdf[geo_key].astype(str).str.upper()
    df[data_key] = df[data_key].astype(str).str.upper()
    gdf = gdf.merge(df[[data_key, value_col]], left_on=geo_key, right_on=data_key, how="left")

    fig, ax = plt.subplots()
    ax.set_axis_off()

    plot_kwargs = dict(
        column=value_col,
        cmap=p.get("cmap", "magma"),
        linewidth=float(p.get("linewidth", 0.4)),
        edgecolor=p.get("edgecolor", "#ffffff"),
        missing_kwds={"color": p.get("missing_color", "#eeeeee"), "edgecolor": p.get("edgecolor", "#ffffff"), "hatch": "///"},
    )
    if scheme:
        plot_kwargs.update(dict(scheme=scheme, k=int(p.get("k", 5)), legend=bool(p.get("legend", True)),
                                legend_kwds={"loc": p.get("legend_loc", "lower left"), "title": p.get("legend_title", ""),
                                             "frameon": False, "fontsize": 8}))
    else:
        plot_kwargs["legend"] = False

    gdf.plot(ax=ax, **plot_kwargs)
    ax.set_title(p["title"], loc="left", pad=8)
    if p.get("subtitle"):
        ax.text(0.0, -0.02, p["subtitle"], transform=ax.transAxes, ha="left", va="top", fontsize=8)

    save_fig_multi(
        fig, Path(p["outfile"]),
        formats=p["formats"],
        jpg_quality=p.get("jpg_quality", 92),
        webp_quality=p.get("webp_quality", 92),
        avif_quality=p.get("avif_quality", 55),
        scour_svg=p.get("scour_svg", True),
    )
    plt.close(fig)
    rprint(f"[bold green]OK[/bold green] → {p['outfile']}.[{','.join(p['formats'])}]")
