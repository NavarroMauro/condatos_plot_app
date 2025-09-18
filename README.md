# ConDatos-Figs-App

Aplicación para generar gráficos estadísticos con plantillas predefinidas para visualizaciones de datos chilenos y latinoamericanos.

## Inicio Rápido

1. **Configurar el entorno**:

   ```bash
   ./setup_condatos_figs.sh
   ```

2. **Activar el entorno conda**:

   ```bash
   conda activate condatos-figs
   ```

3. **Ejecutar un gráfico**:

   ```bash
   python -m app.plots.run stackedbarh config/medallas-juegos-panamericanos-junior-2025-stacked-horizontal.yml
   ```

## Cambios Recientes

- **Refactorización y Reorganización**: Se ha mejorado la estructura del proyecto para una mayor mantenibilidad. Ver [REFACTORING.md](REFACTORING.md) para más detalles.
- **Documentación Consolidada**: Se ha reorganizado la documentación para reducir redundancia y mejorar la organización. Ver [docs/consolidated](docs/consolidated/README.md).
- **Nuevos Scripts**: Se han creado scripts específicos para tareas como pruebas de humo y configuración del entorno.
- **Organización de Artefactos**: Se han movido los scripts específicos de desarrollo a `scripts/dev/` y actualizado `.gitignore`.
- **Sistema de Documentación MkDocs**: Se ha implementado MkDocs para una navegación más fácil de la documentación.

## Tipos de Gráficos Disponibles

- **stackedbarh**: Gráficos de barras apiladas horizontales
- **barv**: Gráficos de barras verticales
- **linechart**: Gráficos de líneas

Para ejecutar cualquier gráfico, use el comando unificado:

```bash
python -m app.plots.run [tipo_grafico] [ruta_config]
```

Ejemplo:

```bash
python -m app.plots.run linechart config/pib-inflacion-linechart.yml
```

Para más información sobre cómo ejecutar los módulos de gráficos, consulte [la documentación de los módulos de gráficos](app/plots/README.md).

## Documentación

### Guías Consolidadas

- [Personalización de Componentes](docs/consolidated/COMPONENTS.md) - Personalización de ejes, leyendas, etiquetas y valores
- [Arquitectura y Diseño](docs/consolidated/ARCHITECTURE_DESIGN.md) - Estructura del sistema y decisiones de diseño
- [Estándares y Mejores Prácticas](docs/consolidated/STANDARDS_PRACTICES.md) - Estándares de visualización y prácticas recomendadas
- [Guía de Desarrollo](docs/consolidated/DEVELOPMENT_GUIDE.md) - Cómo contribuir al proyecto

### Características Avanzadas

- [Filtrado por valor mínimo](docs/FILTER_BY_VALUE.md) - Filtrar categorías en gráficos basado en un valor mínimo
- [Personalización del footer](docs/consolidated/FOOTER.md) - Guía completa para configurar el pie de página
- [Sistema de tracking](docs/consolidated/TRACKING.md) - Herramientas de monitoreo de calidad del código

### Visualizar la Documentación con MkDocs

Para ver la documentación en formato web:

1. **Instalar dependencias**:

   ```bash
   make -f Makefile.docs docs-install
   ```

2. **Iniciar servidor local**:

   ```bash
   make -f Makefile.docs docs-serve
   ```

3. **Abrir en el navegador**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
