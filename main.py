#!/usr/bin/env python3
"""
Condatos Figures - CLI para generar gráficos con estilos preestablecidos

Este script proporciona un punto de entrada para generar diferentes tipos 
de gráficos utilizando configuraciones basadas en archivos YAML.

Uso:
  python main.py stackedbarh config/archivo.yml  # Gráfico de barras horizontales apiladas
  python main.py linechart config/archivo.yml    # Gráfico de líneas
"""

import typer

# Importamos las funciones de los diferentes tipos de gráficos
from app.plots.stackedbarh import stackedbarh
from app.plots.barv import barv
from app.plots.linechart import linechart

# Crear la aplicación Typer
app = typer.Typer(help="Condatos Figures - Generador de gráficos con estilos preestablecidos")

# Registrar los comandos
app.command()(barv)
app.command()(stackedbarh)
app.command()(linechart)

if __name__ == "__main__":
    app()