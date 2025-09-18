# Filtrado por Valor Mínimo

Esta funcionalidad permite filtrar automáticamente los datos del gráfico para mostrar solo aquellos elementos cuyo valor total esté por encima de un umbral mínimo. Es especialmente útil para simplificar visualizaciones con muchas categorías, donde algunas tienen valores muy pequeños y no contribuyen significativamente a la comprensión del gráfico.

## Implementación

La funcionalidad de filtrado está disponible para gráficos de barras horizontales apiladas (`stackedbarh`) y utiliza el método `filter_by_threshold` de la clase base `BaseChart`. Este método filtra las filas del DataFrame basándose en un umbral definido por el usuario.

## Uso

Para aplicar un filtro de valor mínimo, agrega el parámetro `filter_min_value` en la sección `chart` de tu archivo de configuración YAML:

```yaml
chart:
  type: "stackedbarh"
  palette: "condatos"
  # ... otros parámetros ...
  filter_min_value: 5  # Filtra categorías con menos de 5 en la suma total
```

## Parámetros

- `filter_min_value`: Un número que representa el valor mínimo total que debe tener una categoría para ser incluida en el gráfico. El "total" se calcula como la suma de todas las columnas de series para esa categoría.
  - Si se establece a `0` o no se especifica, no se aplicará ningún filtrado.
  - Valores mayores que cero filtrarán las categorías cuya suma total sea menor que el valor especificado.

## Comportamiento

1. El filtrado se aplica en el método `prepare_data()` antes de procesar y ordenar los datos.
2. Se generan mensajes informativos en la consola sobre el número de elementos filtrados y cuáles fueron eliminados.
3. El filtrado no modifica el archivo de datos original, solo afecta a la visualización actual.

## Ejemplo de Uso

El siguiente ejemplo muestra cómo usar esta funcionalidad para mostrar solo los países con 5 o más medallas en total en un gráfico de medalleros olímpicos:

```yaml
title: "Medallero Juegos Panamericanos Junior 2025"
subtitle: "Medallas por país (Países con 5 o más medallas)"
data:
  source_file: "data/medallas-juegos-panamericanos-junior-2025.csv"
  series:
    - "oro"
    - "plata"
    - "bronce"
  category_col: "pais"

chart:
  type: "stackedbarh"
  filter_min_value: 5  # Solo muestra países con 5 o más medallas
  # ... otros parámetros ...
```

## Consideraciones

- El filtrado se realiza sobre el total de todas las series, no sobre series individuales.
- Es importante actualizar el título o subtítulo del gráfico para indicar que se ha aplicado un filtrado, para mantener la transparencia en la visualización de datos.
- Esta funcionalidad es particularmente útil para gráficos con muchas categorías, donde algunas tienen valores muy pequeños que dificultan la lectura del gráfico.
