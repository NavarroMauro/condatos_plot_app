# app/plot.py
from __future__ import annotations
import typer

app = typer.Typer(help="Condatos · Figuras estáticas")

from .plots import stackedbarh as _stackedbarh_mod
_stackedbarh_mod.add_command(app)

if __name__ == "__main__":
    app()
