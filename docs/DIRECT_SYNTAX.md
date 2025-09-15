# Uso del Makefile con sintaxis directa

Este archivo explica cómo usar la nueva sintaxis simplificada de comandos para el Makefile.

## Nueva sintaxis disponible

Ahora puedes renderizar configuraciones específicas con esta sintaxis más directa:

```bash
make <tipo-grafico> <nombre-configuracion>
```

Por ejemplo:

```bash
make stackedbarh mi-configuracion
```

Donde:

- `<tipo-grafico>` puede ser: `stackedbarh`, `linechart`, `barv`, etc.
- `<nombre-configuracion>` es el nombre del archivo YAML en la carpeta `config/` (sin la extensión `.yml`)

## Implementación

Hemos creado tres opciones para usar esta funcionalidad:

1. **Makefile.mini** (recomendado): Implementación minimalista y robusta

   ```bash
   make -f Makefile.mini stackedbarh mi-configuracion
   ```

2. **Makefile.dynamic** (modificado): El sistema dinámico existente con soporte para la nueva sintaxis

   ```bash
   make -f Makefile.dynamic stackedbarh mi-configuracion
   ```

3. **Makefile principal**: Si decides regenerar el Makefile principal con el script actualizado

   ```bash
   python scripts/generate_makefile.py --install
   make stackedbarh mi-configuracion
   ```

## Ventajas de la nueva sintaxis

- Más intuitiva y sencilla de recordar
- Más parecida a comandos de terminal tradicionales
- Compatible con autocompletado de shell
- Soporta todos los tipos de gráficos disponibles

## Elegir una implementación

- **Para uso rápido y directo**: Usa `Makefile.mini`
- **Para sistema completo**: Regenera el Makefile principal con el script actualizado
- **Para pruebas**: Usa `Makefile.dynamic`

Todas las implementaciones son equivalentes en términos de la sintaxis `make <tipo-grafico> <config>` pero difieren en su complejidad y características adicionales.
