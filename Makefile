SHELL := /bin/bash

# ---------- Ajustes del proyecto ----------
ENV_NAME        ?= condatos-figs-app
PYTHON          ?= $(shell which python || which python3)
CONFIG_DIR      ?= config
OUT_DIR         ?= out

# ---------- Utilidad ----------
.PHONY: help
help:
	@echo "Targets disponibles:"
	@echo "  setup         - Sugerencia para activar conda"
	@echo "  check-env     - Muestra el intérprete Python actual"
	@echo "  lint          - Ruff check (lint)"
	@echo "  fmt           - Ruff format (formatea)"
	@echo "  test          - Pytest si existe carpeta tests/"
	@echo "  smoke         - Render mínimo (stackedbarh/choropleth si existen configs)"
	@echo "  stackedbarh   - Render barras horizontales apiladas"
	@echo "  linechart     - Render gráficos de líneas"
	@echo "  choropleth    - Render mapa (subcomando en app.plot)"
	@echo "  clean         - Borra artefactos en $(OUT_DIR)"
	@echo "  all           - lint + fmt + smoke"

# ---------- Setup / Info ----------
.PHONY: setup check-env
setup:
	@echo "Activa el entorno conda:  conda activate $(ENV_NAME)"
	@echo "Luego selecciona el intérprete en VS Code si es necesario."

check-env:
	@echo "Python ejecutable: $(PYTHON)"
	@$(PYTHON) -c 'import sys; print("sys.executable ->", sys.executable)'

# ---------- Calidad de código ----------
.PHONY: lint fmt test
lint:
	@ruff check .

fmt:
	@ruff format .
	@ruff check . --fix

test:
	@if [ -d tests ]; then \
		echo ">> Ejecutando pytest"; \
		pytest -q; \
	else \
		echo ">> No hay carpeta tests/ — saltando"; \
	fi

# ---------- Renders rápidos ----------
.PHONY: stackedbarh choropleth linechart
stackedbarh:
	conda run -n $(ENV_NAME) python -m app.plots.stackedbarh $(CONFIG_DIR)/medallas-juegos-panamericanos-junior-2025-stacked-horizontal.yml

linechart:
	conda run -n $(ENV_NAME) python -m app.plots.linechart $(CONFIG_DIR)/pib-inflacion-linechart.yml

# choropleth:
# 	conda run -n $(ENV_NAME) python -m app.plots.choropleth $(CONFIG_DIR)/stackedbar-horizontal-condatos.yml

# ---------- Smoke (coherente con lo activo) ----------
.PHONY: smoke
smoke:
	@set -e; \
	echo ">> Smoke: stackedbarh"; \
	if [ -f "$(CONFIG_DIR)/medallas-juegos-panamericanos-junior-2025-stacked-horizontal.yml" ]; then \
		conda run -n $(ENV_NAME) python -m app.plots.stackedbarh $(CONFIG_DIR)/medallas-juegos-panamericanos-junior-2025-stacked-horizontal.yml; \
	else echo "  (skip) falta $(CONFIG_DIR)/stackedbarh-ejemplo.yml"; fi; \
	echo ">> Smoke: linechart"; \
	if [ -f "$(CONFIG_DIR)/line-example.yml" ]; then \
		conda run -n $(ENV_NAME) python -m app.plots.linechart $(CONFIG_DIR)/line-example.yml; \
	else echo "  (skip) falta $(CONFIG_DIR)/line-example.yml"; fi; \
	if ls $(OUT_DIR)/*.{png,svg,pdf,webp,jpg,avif} >/dev/null 2>&1; then \
		echo "OK: hay salidas en $(OUT_DIR)"; \
	else \
		echo "WARN: no se generaron salidas en $(OUT_DIR)"; \
	fi

# ---------- Limpieza ----------
.PHONY: clean
clean:
	@rm -f $(OUT_DIR)/*.{png,svg,pdf,webp,avif,jpg} $(OUT_DIR)/*.tmp.png 2>/dev/null || true

# ---------- Meta ----------
.PHONY: all
all: lint fmt smoke
