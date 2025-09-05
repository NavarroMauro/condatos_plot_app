#!/usr/bin/env bash
# setup_condatos_figs.sh — Bootstrap ConDatos (gráficos estáticos multi-formato)
# Crea estructura, estilos, plantillas, configs, Makefile, environment.yml
# y (opcional) crea/actualiza entorno conda y corre un smoke test.
# Uso:
#   ./setup_condatos_figs.sh                # crea ./condatos-figs y el entorno
#   ./setup_condatos_figs.sh -n mydir       # crea en ./mydir
#   ./setup_condatos_figs.sh --no-env       # no crea/actualiza entorno
#   ./setup_condatos_figs.sh --run-smoke    # corre ejemplo tras crear entorno

set -euo pipefail

# ---------- Defaults ----------
PROJECT_DIR="condatos-figs"
CREATE_ENV=1
RUN_SMOKE=0
PY_VER="3.11"

# ---------- Colors ----------
c_reset='\033[0m'; c_ok='\033[1;32m'; c_info='\033[1;34m'; c_warn='\033[1;33m'; c_err='\033[1;31m'

# ---------- Parse args ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name) PROJECT_DIR="${2:-condatos-figs}"; shift 2;;
    --no-env)  CREATE_ENV=0; shift;;
    --run-smoke) RUN_SMOKE=1; shift;;
    -h|--help)
      echo "ConDatos setup"
      echo "  -n, --name DIR     Nombre/carpeta del proyecto (default: condatos-figs)"
      echo "      --no-env       No crear/actualizar entorno conda"
      echo "      --run-smoke    Ejecutar ejemplo tras crear el entorno"
      exit 0;;
    *) echo -e "${c_warn}[WARN] Opción no reconocida: $1${c_reset}"; shift;;
  esac
done

echo -e "${c_info}→ Creando proyecto en: ${PROJECT_DIR}${c_reset}"
mkdir -p "${PROJECT_DIR}"/{styles,templates,config,out,app}

# ---------- environment.yml (mínimo, probado) ----------
cat > "${PROJECT_DIR}/environment.yml" <<YML
name: condatos-figs
channels:
  - conda-forge
dependencies:
  - python=${PY_VER}
  - numpy
  - pandas
  - matplotlib>=3.9
  - seaborn
  - pillow>=10
  - pillow-heif
  - pyyaml
  - typer
  - rich
  - scour
YML

# ---------- styles (ConDatos) ----------
cat > "${PROJECT_DIR}/styles/condatos.mplstyle" <<'INI'
figure.figsize: 3.35, 2.4
figure.dpi: 300
savefig.dpi: 300
savefig.bbox: tight
savefig.pad_inches: 0.02
font.family: DejaVu Sans
font.size: 9
axes.titlesize: 11
axes.titleweight: bold
axes.labelsize: 9
axes.linewidth: 0.85
axes.spines.top: False
axes.spines.right: False
axes.grid: False
xtick.direction: out
ytick.direction: out
xtick.major.width: 0.6
ytick.major.width: 0.6
xtick.major.pad: 2.5
ytick.major.pad: 2.5
lines.linewidth: 1.4
legend.frameon: False
legend.fontsize: 8.8
axes.prop_cycle: cycler('color', ['#1F6FEB','#00B5D8','#F25F5C','#F2C14E','#6B7280','#111827'])
patch.edgecolor: none
INI

# ---------- templates ----------
# Líneas multi-serie
cat > "${PROJECT_DIR}/templates/line-condatos.yml" <<'YAML'
title: "Título"
xlabel: ""
ylabel: ""
style: "styles/condatos.mplstyle"
width_in: 3.35
height_in: 2.4
palette: null
grid: false
line:
  linewidth: 1.6
  marker: null
formats: ["png","svg","pdf","webp","avif","jpg"]
jpg_quality: 92
webp_quality: 92
avif_quality: 55
scour_svg: true
YAML

# Barras verticales
cat > "${PROJECT_DIR}/templates/bar-condatos.yml" <<'YAML'
title: "Título"
xlabel: ""
ylabel: ""
style: "styles/condatos.mplstyle"
width_in: 3.35
height_in: 2.4
palette: null
bar:
  edgecolor: null
  linewidth: 0.0
  bar_width: 0.8
grid: false
rotate_xticks: 0
tight_layout: true
formats: ["png","svg","pdf","webp","avif","jpg"]
jpg_quality: 92
webp_quality: 92
avif_quality: 55
scour_svg: true
value_labels: true
value_fmt: ".1f"
value_offset: 0.02
YAML

# Barras horizontales (rankings)
cat > "${PROJECT_DIR}/templates/barh-condatos.yml" <<'YAML'
title: "Título"
xlabel: ""
ylabel: ""
style: "styles/condatos.mplstyle"
width_in: 3.35
height_in: 2.4
palette: null
bar:
  edgecolor: null
  linewidth: 0.0
  bar_width: 0.8
grid: true
tight_layout: true
formats: ["png","svg","pdf","webp","avif","jpg"]
jpg_quality: 92
webp_quality: 92
avif_quality: 55
scour_svg: true
value_labels: true
value_fmt: ".1f"
value_offset: 0.02
YAML

# Heatmap
cat > "${PROJECT_DIR}/templates/heatmap-condatos.yml" <<'YAML'
title: "Título"
xlabel: ""
ylabel: ""
style: "styles/condatos.mplstyle"
width_in: 3.35
height_in: 2.4
cmap: "viridis"
center: null
vmin: null
vmax: null
annot: false
fmt: ".1f"
linewidths: 0.0
cbar: true
formats: ["png","svg","pdf","webp","avif","jpg"]
jpg_quality: 92
webp_quality: 92
avif_quality: 55
scour_svg: true
YAML

# ---------- configs de ejemplo ----------
cat > "${PROJECT_DIR}/config/line-ejemplo.yml" <<'YAML'
template: "templates/line-condatos.yml"
outfile: "out/condatos-linea"
data:
  inline:
    x: [2019,2020,2021,2022,2023,2024]
    y_series:
      Chile:     [100, 98, 105, 110, 113, 118]
      Perú:      [100, 95,  99, 104, 108, 111]
      Colombia:  [100, 97, 103, 109, 114, 120]
overrides:
  title: "Índice base 2019=100 (ejemplo)"
  ylabel: "Índice"
YAML

cat > "${PROJECT_DIR}/config/bar-ejemplo.yml" <<'YAML'
template: "templates/bar-condatos.yml"
outfile: "out/condatos-barras"
data:
  inline:
    categories: ["Chile","Perú","Colombia","México","Argentina"]
    values: [42.5, 37.2, 31.8, 55.1, 28.4]
overrides:
  title: "Ingresos por país (ejemplo)"
  ylabel: "Millones USD"
  rotate_xticks: 15
  bar:
    bar_width: 0.75
  value_fmt: ".1f"
YAML

cat > "${PROJECT_DIR}/config/barh-ejemplo.yml" <<'YAML'
template: "templates/barh-condatos.yml"
outfile: "out/condatos-barh"
data:
  inline:
    categories: ["Uruguay","Chile","Costa Rica","Brasil","México"]
    values: [85, 78, 74, 69, 65]
overrides:
  title: "Índice de transparencia (ejemplo)"
  xlabel: "Puntaje"
YAML

cat > "${PROJECT_DIR}/config/heatmap-ejemplo.yml" <<'YAML'
template: "templates/heatmap-condatos.yml"
outfile: "out/condatos-heatmap"
data:
  inline:
    rows: ["Chile","Perú","Colombia","México","Argentina"]
    cols: [2020,2021,2022,2023,2024]
    values:
      - [65, 68, 71, 73, 76]
      - [60, 62, 64, 66, 69]
      - [55, 58, 61, 63, 66]
      - [70, 72, 74, 77, 80]
      - [50, 52, 55, 57, 60]
overrides:
  title: "Índice (ejemplo) · países × años"
  xlabel: "Año"
  ylabel: "País"
  annot: true
  fmt: ".0f"
  linewidths: 0.5
  cmap: "magma"
YAML

# ---------- app Python ----------
cat > "${PROJECT_DIR}/app/__init__.py" <<'PY'
# paquete condatos-figs
PY

cat > "${PROJECT_DIR}/app/styling.py" <<'PY'
from __future__ import annotations
import matplotlib as mpl

def apply_style(style_path: str | None, width_in: float | None, height_in: float | None):
    if style_path:
        mpl.style.use(style_path)
    if width_in and height_in:
        mpl.rcParams["figure.figsize"] = (width_in, height_in)
PY

cat > "${PROJECT_DIR}/app/io_utils.py" <<'PY'
from __future__ import annotations
import subprocess, sys
from pathlib import Path
from typing import Iterable
from PIL import Image
import pillow_heif  # registra AVIF

def ensure_parent(outpath: Path):
    outpath.parent.mkdir(parents=True, exist_ok=True)

def save_fig_multi(fig, base: Path, formats: Iterable[str],
                   jpg_quality=92, webp_quality=92, avif_quality=55,
                   scour_svg=True):
    base = base.with_suffix("")
    for fmt in formats:
        fmt_lower = fmt.lower()
        if fmt_lower in {"png","pdf","svg"}:
            out = base.with_suffix(f".{fmt_lower}")
            ensure_parent(out)
            fig.savefig(out)
            if fmt_lower == "svg" and scour_svg:
                try:
                    minified = base.with_suffix(".min.svg")
                    subprocess.run(["scour", "-i", str(out), "-o", str(minified),
                                    "--enable-id-stripping", "--enable-comment-stripping",
                                    "--shorten-ids", "--remove-metadata"],
                                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    minified.replace(out)
                except Exception:
                    pass
        elif fmt_lower in {"jpg","jpeg","webp","avif"}:
            tmp_png = base.with_suffix(".tmp.png")
            fig.savefig(tmp_png)
            im = Image.open(tmp_png)
            out = base.with_suffix(f".{fmt_lower}")
            ensure_parent(out)
            if fmt_lower in {"jpg","jpeg"}:
                im = im.convert("RGB")
                im.save(out, format="JPEG", quality=jpg_quality, optimize=True, progressive=True)
            elif fmt_lower == "webp":
                im.save(out, format="WEBP", quality=webp_quality, method=6)
            elif fmt_lower == "avif":
                im.save(out, format="AVIF", quality=avif_quality)
            tmp_png.unlink(missing_ok=True)
        else:
            print(f"[WARN] Formato no soportado: {fmt}", file=sys.stderr)
PY

cat > "${PROJECT_DIR}/app/plot.py" <<'PY'
from __future__ import annotations
from pathlib import Path
import yaml
import typer
from rich import print as rprint

from .styling import apply_style
from .io_utils import save_fig_multi

app = typer.Typer(help="ConDatos · Figuras estáticas multi-formato (PNG/JPG/SVG/PDF/WebP/AVIF).")

def _load_yaml(p: Path) -> dict:
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# -------- LINE --------
@app.command()
def line(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = tpl | {"outfile": cfg.get("outfile", "out/figure")} | cfg.get("overrides", {})
    data = cfg["data"]
    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    import matplotlib.pyplot as plt
    import seaborn as sns
    if params.get("palette"): sns.set_palette(params["palette"])
    fig, ax = plt.subplots()

    if "csv" in data:
        import pandas as pd
        df = pd.read_csv(data["csv"])
        x = df.iloc[:,0]
        for col in df.columns[1:]:
            ax.plot(x, df[col], label=str(col),
                    linewidth=params["line"]["linewidth"],
                    marker=params["line"]["marker"] or None)
        ax.legend()
    else:
        x = data["inline"]["x"]
        y_series = data["inline"].get("y_series")
        if y_series:
            for name, ys in y_series.items():
                ax.plot(x, ys, label=str(name),
                        linewidth=params["line"]["linewidth"],
                        marker=params["line"]["marker"] or None)
            ax.legend()
        else:
            y = data["inline"]["y"]
            ax.plot(x, y,
                    linewidth=params["line"]["linewidth"],
                    marker=params["line"]["marker"] or None)

    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    if params.get("grid"): ax.grid(True, linewidth=0.4, alpha=0.4)

    save_fig_multi(fig, Path(params["outfile"]),
                   formats=params["formats"],
                   jpg_quality=params.get("jpg_quality", 92),
                   webp_quality=params.get("webp_quality", 92),
                   avif_quality=params.get("avif_quality", 55),
                   scour_svg=params.get("scour_svg", True))
    plt.close(fig)
    rprint(f"[bold green]OK[/bold green] → {params['outfile']}.[{','.join(params['formats'])}]")

# -------- BAR --------
@app.command()
def bar(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = tpl | {"outfile": cfg.get("outfile", "out/figure")} | cfg.get("overrides", {})
    data = cfg["data"]
    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    import matplotlib.pyplot as plt, numpy as np, seaborn as sns
    if params.get("palette"): sns.set_palette(params["palette"])
    fig, ax = plt.subplots()

    if "csv" in data:
        import pandas as pd
        df = pd.read_csv(data["csv"])
        cats = df.iloc[:,0].astype(str).tolist()
        vals = df.iloc[:,1].astype(float).tolist()
    else:
        cats = list(map(str, data["inline"]["categories"]))
        vals = list(map(float, data["inline"]["values"]))

    x = np.arange(len(cats))
    bars = ax.bar(x, vals, width=params["bar"]["bar_width"],
                  linewidth=params["bar"]["linewidth"],
                  edgecolor=(params["bar"]["edgecolor"] or None))

    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    ax.set_xticks(x, cats, rotation=params.get("rotate_xticks", 0))
    if params.get("grid"): ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)

    if params.get("value_labels", False):
        fmt = "{:" + params.get("value_fmt", ".2f") + "}"
        ylim = ax.get_ylim(); dy = params.get("value_offset", 0.02) * (ylim[1]-ylim[0])
        for rect, v in zip(bars, vals):
            ax.text(rect.get_x()+rect.get_width()/2.0, rect.get_height()+dy,
                    fmt.format(v), ha="center", va="bottom", fontsize=8)

    save_fig_multi(fig, Path(params["outfile"]),
                   formats=params["formats"],
                   jpg_quality=params.get("jpg_quality", 92),
                   webp_quality=params.get("webp_quality", 92),
                   avif_quality=params.get("avif_quality", 55),
                   scour_svg=params.get("scour_svg", True))
    plt.close(fig)
    rprint(f"[bold green]OK[/bold green] → {params['outfile']}.[{','.join(params['formats'])}]")

# -------- BARH --------
@app.command()
def barh(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = tpl | {"outfile": cfg.get("outfile", "out/figure")} | cfg.get("overrides", {})
    data = cfg["data"]
    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    import matplotlib.pyplot as plt, numpy as np, seaborn as sns
    if params.get("palette"): sns.set_palette(params["palette"])
    fig, ax = plt.subplots()

    if "csv" in data:
        import pandas as pd
        df = pd.read_csv(data["csv"])
        cats = df.iloc[:,0].astype(str).tolist()
        vals = df.iloc[:,1].astype(float).tolist()
    else:
        cats = list(map(str, data["inline"]["categories"]))
        vals = list(map(float, data["inline"]["values"]))

    y = np.arange(len(cats))
    bars = ax.barh(y, vals, height=params["bar"]["bar_width"],
                   linewidth=params["bar"]["linewidth"],
                   edgecolor=(params["bar"]["edgecolor"] or None))

    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    ax.set_yticks(y, cats)
    if params.get("grid"): ax.grid(True, axis="x", linewidth=0.4, alpha=0.4)

    if params.get("value_labels", False):
        fmt = "{:" + params.get("value_fmt", ".2f") + "}"
        xlim = ax.get_xlim(); dx = params.get("value_offset", 0.02) * (xlim[1]-xlim[0])
        for rect, v in zip(bars, vals):
            ax.text(rect.get_width()+dx, rect.get_y()+rect.get_height()/2.0,
                    fmt.format(v), ha="left", va="center", fontsize=8)

    save_fig_multi(fig, Path(params["outfile"]),
                   formats=params["formats"],
                   jpg_quality=params.get("jpg_quality", 92),
                   webp_quality=params.get("webp_quality", 92),
                   avif_quality=params.get("avif_quality", 55),
                   scour_svg=params.get("scour_svg", True))
    plt.close(fig)
    rprint(f"[bold green]OK[/bold green] → {params['outfile']}.[{','.join(params['formats'])}]")

# -------- HEATMAP --------
@app.command()
def heatmap(config: Path = typer.Argument(..., help="Ruta a config YAML")):
    cfg = _load_yaml(config)
    tpl = _load_yaml(Path(cfg["template"]))
    params = tpl | {"outfile": cfg.get("outfile", "out/figure")} | cfg.get("overrides", {})
    data = cfg["data"]
    apply_style(params.get("style"), params.get("width_in"), params.get("height_in"))

    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    fig, ax = plt.subplots()

    if "csv" in data:
        df = pd.read_csv(data["csv"])
        row_labels = df.iloc[:,0].astype(str).tolist()
        df_vals = df.iloc[:,1:]
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
    ax.set_title(params["title"])
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])
    ax.set_xticks(np.arange(len(col_labels)) + 0.5, col_labels, rotation=0)
    ax.set_yticks(np.arange(len(row_labels)) + 0.5, row_labels, rotation=0)

    save_fig_multi(
        fig, Path(params["outfile"]),
        formats=params["formats"],
        jpg_quality=params.get("jpg_quality", 92),
        webp_quality=params.get("webp_quality", 92),
        avif_quality=params.get("avif_quality", 55),
        scour_svg=params.get("scour_svg", True)
    )
    plt.close(fig)
    rprint(f"[bold green]OK[/bold green] → {params['outfile']}.[{','.join(params['formats'])}]")
PY

# ---------- Makefile (robusto respecto a python/python3) ----------
cat > "${PROJECT_DIR}/Makefile" <<'MK'
SHELL := /bin/bash
PYTHON := $(shell which python || which python3)

.PHONY: setup line bar barh heatmap clean

setup:
	@echo "Activa el entorno: conda activate condatos-figs"

line:
	$(PYTHON) -m app.plot line config/line-ejemplo.yml

bar:
	$(PYTHON) -m app.plot bar  config/bar-ejemplo.yml

barh:
	$(PYTHON) -m app.plot barh config/barh-ejemplo.yml

heatmap:
	$(PYTHON) -m app.plot heatmap config/heatmap-ejemplo.yml

clean:
	rm -f out/*.{png,svg,pdf,webp,avif,jpg} out/*.tmp.png || true
MK

# ---------- Crear/actualizar entorno conda ----------
if [[ ${CREATE_ENV} -eq 1 ]]; then
  echo -e "${c_info}→ Preparando entorno conda 'condatos-figs'...${c_reset}"
  if command -v conda >/dev/null 2>&1; then
    if conda env list | awk '{print $1}' | grep -qx "condatos-figs"; then
      echo -e "${c_info}   Ya existe. Actualizando (conda env update --prune)...${c_reset}"
      conda env update -f "${PROJECT_DIR}/environment.yml" --prune
    else
      echo -e "${c_info}   Creando entorno...${c_reset}"
      conda env create -f "${PROJECT_DIR}/environment.yml"
    fi
    echo -e "${c_ok}✔ Entorno listo. Activa con: conda activate condatos-figs${c_reset}"
  else
    echo -e "${c_warn}[WARN] conda no encontrado. Instala Miniconda/Mamba o ejecuta con --no-env.${c_reset}"
  fi
else
  echo -e "${c_warn}→ Omitiendo creación de entorno (--no-env).${c_reset}"
fi

# ---------- Smoke test opcional ----------
if [[ ${RUN_SMOKE} -eq 1 ]]; then
  echo -e "${c_info}→ Ejecutando smoke test (heatmap)...${c_reset}"
  set +e
  # intentamos con python y python3, por si el shell no tiene el env activo
  ( cd "${PROJECT_DIR}" && (python -m app.plot heatmap config/heatmap-ejemplo.yml || python3 -m app.plot heatmap config/heatmap-ejemplo.yml) )
  rc=$?
  set -e
  if [[ $rc -ne 0 ]]; then
    echo -e "${c_err}Smoke test falló. Activa el entorno y ejecuta: conda activate condatos-figs && make -C ${PROJECT_DIR} heatmap${c_reset}"
    exit 1
  else
    echo -e "${c_ok}✔ Smoke test OK. Salidas en ${PROJECT_DIR}/out/${c_reset}"
  fi
fi

echo -e "${c_ok}✔ Proyecto ConDatos listo en '${PROJECT_DIR}'.${c_reset}"
echo "Siguientes pasos:"
echo "  1) conda activate condatos-figs"
echo "  2) make -C ${PROJECT_DIR} heatmap   # prueba"
echo "  3) Ajusta styles/ y templates/ según tu post."
