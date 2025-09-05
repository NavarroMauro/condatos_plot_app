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

choropleth:
	$(PYTHON) -m app.plot choropleth config/choropleth-ejemplo.yml

heatmap:
	$(PYTHON) -m app.plot heatmap config/heatmap-ejemplo.yml

clean:
	rm -f out/*.{png,svg,pdf,webp,avif,jpg} out/*.tmp.png || true
