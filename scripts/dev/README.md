# Scripts de Desarrollo

Esta carpeta contiene scripts destinados exclusivamente al desarrollo y pruebas del proyecto ConDatos-Figs-App. Estos scripts no son necesarios para la funcionalidad principal de la aplicación, pero son útiles durante el desarrollo.

## Scripts Disponibles

### `test_styles.py`

Este script está diseñado para probar diferentes estilos visuales en el gráfico de medallas de los Juegos Panamericanos Junior 2025.

#### Funcionalidad

- Genera el mismo gráfico con diferentes estilos predefinidos (`condatos`, `minimal`, `dark`, `vibrant`)
- Aplica paletas de colores específicas para cada estilo
- Crea una copia de seguridad de la configuración original y la restaura al finalizar
- Genera múltiples archivos de salida con el sufijo del estilo correspondiente

#### Uso

```bash
cd /path/to/condatos-figs-app
python scripts/dev/test_styles.py
```

#### Resultado

El script generará múltiples versiones del gráfico de medallas con diferentes estilos en el directorio `out/`.

## Cuándo Usar Estos Scripts

Estos scripts deben usarse durante:

1. **Desarrollo visual**: Cuando se están explorando diferentes estilos y paletas de colores
2. **Pruebas comparativas**: Para comparar diferentes opciones visuales antes de confirmar un estilo final
3. **Demostración**: Para generar ejemplos con diferentes estilos para presentaciones

## Notas Importantes

- Estos scripts pueden modificar temporalmente los archivos de configuración
- Siempre crean copias de seguridad y restauran la configuración original al finalizar
- No están destinados a ser utilizados en entornos de producción
- Pueden depender de archivos o configuraciones específicas del proyecto
