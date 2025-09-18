# Módulos de Gráficos

Esta carpeta contiene los módulos para generar diferentes tipos de gráficos.

## Ejecutando los módulos directamente

Para evitar advertencias de importación circular, se recomienda usar el módulo `run.py` cuando se ejecutan directamente desde la línea de comandos:

```bash
# Uso recomendado (sin warnings)
python -m app.plots.run stackedbarh ruta/a/config.yml
python -m app.plots.run barv ruta/a/config.yml
python -m app.plots.run linechart ruta/a/config.yml
```

Si prefieres ejecutar módulos específicos, puedes usar los runners individuales:

```bash
# Alternativa sin warnings
python -m app.plots.stackedbarh_runner ruta/a/config.yml
python -m app.plots.barv_runner ruta/a/config.yml
python -m app.plots.linechart_runner ruta/a/config.yml
```

El método tradicional puede mostrar warnings de importación pero sigue funcionando:

```bash
# Método tradicional (puede mostrar warnings)
python -m app.plots.stackedbarh ruta/a/config.yml
python -m app.plots.barv ruta/a/config.yml
python -m app.plots.linechart ruta/a/config.yml
```

Los módulos runner y el módulo `run.py` están diseñados para evitar los warnings de importación circular que ocurren cuando un módulo es importado tanto por el paquete principal como ejecutado directamente.
