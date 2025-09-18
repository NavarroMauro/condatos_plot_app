# Estilos de ConDatos-Figs-App

Este directorio contiene los estilos (mplstyle) disponibles para las visualizaciones de ConDatos-Figs-App.

## Estilos Disponibles

- **base.mplstyle**: Estilo base con configuraciones fundamentales
- **condatos.mplstyle**: Estilo oficial de ConDatos
- **condatos-map.mplstyle**: Estilo para mapas de ConDatos
- **dark.mplstyle**: Estilo con tema oscuro
- **minimal.mplstyle**: Estilo minimalista
- **vibrant.mplstyle**: Estilo con colores vibrantes

## Uso

Para usar estos estilos en tu visualización, específicalo en el archivo de configuración YAML:

```yaml
styling:
  style: "condatos"  # O cualquier otro estilo disponible
```

También puedes combinar estilos en tu configuración:

```yaml
styling:
  style: ["base", "condatos"]
```

## Personalización

Los estilos se implementan utilizando el sistema mplstyle de Matplotlib. Puedes crear tu propio estilo basado en los existentes copiando y modificando uno de los archivos .mplstyle disponibles.

Para más información sobre la personalización de componentes específicos, consulta la [documentación de personalización](../docs/index.md#personalización).
