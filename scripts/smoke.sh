#!/usr/bin/env bash
set -euo pipefail

# --- Opciones ---
CONFIG_DIR="config"
OUT_DIR="out"
PYTHON_BIN="${PYTHON:-python}"
MATCH=""
DRY_RUN=0
FAIL_FAST=0

usage() {
  cat <<EOF
Usage: $0 [--config DIR] [--out DIR] [--match SUBSTR] [--dry-run] [--fail-fast]

  --config DIR     Carpeta con .yml/.yaml (default: config)
  --out DIR        Carpeta de salida (default: out)
  --match SUBSTR   Solo correr configs cuyo nombre contenga SUBSTR
  --dry-run        Mostrar lo que se correría, sin ejecutar
  --fail-fast      Detenerse ante el primer fallo

Env:
  PYTHON           Ruta a python (default: python)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config)    CONFIG_DIR="$2"; shift 2;;
    --out)       OUT_DIR="$2"; shift 2;;
    --match)     MATCH="$2"; shift 2;;
    --dry-run)   DRY_RUN=1; shift;;
    --fail-fast) FAIL_FAST=1; shift;;
    -h|--help)   usage; exit 0;;
    *) echo "Arg desconocido: $1" >&2; usage; exit 1;;
  esac
done

# --- Detección de subcomandos disponibles en app.plot ---
AVAILABLE="$( $PYTHON_BIN -m app.plot --help 2>/dev/null || true )"
has_cmd() {
  # retorna 0 si el subcomando existe en la ayuda
  grep -qiE "^[[:space:]]*$1([[:space:]]|$)" <<<"$(echo "$AVAILABLE" | sed -n '/Commands:/,$p')"
}

# --- Map simple de patrón->subcomando ---
# Puedes extender esta tabla a medida que migres más plots
resolve_subcmd() {
  local fname="$1"
  case "$fname" in
    *stackedbarh* ) echo "stackedbarh" ;;
    *stackedbar* )  echo "stackedbar"  ;;
    *barh* )        echo "barh"        ;;
    *bar* )         echo "bar"         ;;
    *line* )        echo "line"        ;;
    *heatmap* )     echo "heatmap"     ;;
    *choropleth* )  echo "choropleth"  ;;
    * )             echo ""            ;;
  esac
}

mkdir -p "$OUT_DIR"

shopt -s nullglob
found_any=0
ok=0
fail=0

run_or_echo() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[DRY] $*"
  else
    eval "$@"
  fi
}

for cfg in "$CONFIG_DIR"/*.yml "$CONFIG_DIR"/*.yaml; do
  [[ -e "$cfg" ]] || continue
  base="$(basename "$cfg")"
  [[ -n "$MATCH" && "$base" != *"$MATCH"* ]] && continue

  found_any=1
  subcmd="$(resolve_subcmd "$base")"

  if [[ -z "$subcmd" ]]; then
    echo "?? No se reconoce tipo desde el nombre: $base — saltando"
    continue
  fi

  if [[ "$subcmd" == "choropleth" ]]; then
    # Soporte legado: si no existe subcomando choropleth, usa app.cmd_choropleth
    if has_cmd "choropleth"; then
      echo ">> choropleth (subcmd) :: $cfg"
      if run_or_echo "$PYTHON_BIN -m app.plot choropleth \"$cfg\""; then
        ((ok++))
      else
        ((fail++)); [[ $FAIL_FAST -eq 1 ]] && exit 1
      fi
    else
      echo ">> choropleth (legacy) :: $cfg"
      if run_or_echo "$PYTHON_BIN -m app.cmd_choropleth \"$cfg\""; then
        ((ok++))
      else
        ((fail++)); [[ $FAIL_FAST -eq 1 ]] && exit 1
      fi
    fi
    continue
  fi

  if ! has_cmd "$subcmd"; then
    echo "-- subcomando '$subcmd' no disponible (aún no migrado?) — saltando $base"
    continue
  fi

  echo ">> $subcmd :: $cfg"
  if run_or_echo "$PYTHON_BIN -m app.plot \"$subcmd\" \"$cfg\""; then
    ((ok++))
  else
    ((fail++)); [[ $FAIL_FAST -eq 1 ]] && exit 1
  fi
done

if [[ $found_any -eq 0 ]]; then
  echo "WARN: No se encontraron configs en $CONFIG_DIR"
fi

echo ">> Verificando salidas en $OUT_DIR"
if compgen -G "$OUT_DIR/*.{png,svg,pdf,webp,jpg,avif}" > /dev/null; then
  echo "OK: hay salidas en $OUT_DIR"
else
  echo "WARN: no se generaron salidas en $OUT_DIR"
fi

echo "Resumen: OK=$ok  FAIL=$fail"
[[ $fail -gt 0 ]] && exit 1 || exit 0
