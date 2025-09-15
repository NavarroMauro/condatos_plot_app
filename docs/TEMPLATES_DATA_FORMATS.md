# Templates y Formatos de Datos en ConDatos

Este documento explica el sistema de templates fijos diseñados para aceptar datos en formatos predeterminados, facilitando la creación estandarizada de visualizaciones para Chile y su contexto regional latinoamericano.

## Concepto de Templates Fijos

ConDatos utiliza un sistema de templates fijos que funcionan como "moldes" preconfigurados para diferentes tipos de visualizaciones. Estos templates:

1. **Definen la estructura visual**: Establecen los aspectos visuales como colores, tipografía, posicionamiento de elementos y formato general.
2. **Especifican formatos de datos esperados**: Indican exactamente qué estructura deben tener los datos de entrada.
3. **Garantizan consistencia**: Aseguran que todas las visualizaciones mantengan la identidad visual de ConDatos.

## Formatos de Datos Aceptados

### Formato Actual: CSV

Actualmente, ConDatos acepta datos en formato CSV (Comma-Separated Values) con estructuras específicas para cada tipo de visualización:

#### Estructura para Gráficos de Barras Horizontales Apiladas

```csv
categoria,valor1,valor2,valor3,code
"Chile",235,108,105,"CL"
"Argentina",75,66,111,"AR"
"Brasil",169,62,179,"BR"
"Colombia",73,75,63,"CO"
"México",42,42,28,"MX"
```

Requisitos:

- La primera columna debe contener las categorías (países, regiones, etc.)
- Las columnas intermedias contienen los valores para cada serie
- La última columna `code` es opcional y contiene códigos ISO para banderas

#### Estructura para Gráficos de Líneas Temporales

```csv
fecha,serie1,serie2,serie3
"2020-01",25.3,15.7,10.2
"2020-02",26.1,15.9,11.5
"2020-03",24.8,16.2,12.1
```

Requisitos:

- La primera columna debe contener fechas o períodos temporales
- Cada columna adicional representa una serie de datos
- Los nombres de las columnas se utilizan automáticamente en la leyenda

### Formato Futuro: PostgreSQL

En futuras versiones, ConDatos implementará conexión directa con bases de datos PostgreSQL:

#### Conexión Planificada

```yaml
# Configuración de conexión a PostgreSQL
data_source:
  type: "postgresql"
  connection:
    host: "localhost"
    port: 5432
    database: "condatos"
    schema: "public"
    table: "indicadores_economicos"
    user: "usuario"
    password_env: "DB_PASSWORD"  # Tomar contraseña de variable de entorno
  query: "SELECT anio, pib, inflacion, desempleo FROM indicadores_economicos WHERE pais = 'Chile' ORDER BY anio"
```

#### Estructuras de Tablas Esperadas

ConDatos espera encontrar tablas con estructuras estandarizadas en PostgreSQL:

1. **Tabla de Indicadores Económicos**:

   ```sql
   CREATE TABLE indicadores_economicos (
       id SERIAL PRIMARY KEY,
       pais VARCHAR(100),
       codigo_iso CHAR(2),
       anio INTEGER,
       periodo VARCHAR(10),
       pib NUMERIC(15,2),
       inflacion NUMERIC(5,2),
       desempleo NUMERIC(5,2),
       -- otros indicadores
       fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

2. **Tabla de Datos Geográficos**:

   ```sql
   CREATE TABLE datos_geograficos (
       id SERIAL PRIMARY KEY,
       region VARCHAR(100),
       codigo_region VARCHAR(10),
       indicador VARCHAR(100),
       valor NUMERIC(15,2),
       anio INTEGER,
       fuente VARCHAR(200),
       -- otros campos
       fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## Uso de Templates con Diferentes Fuentes de Datos

### Ejemplo 1: Template con Datos CSV

```yaml
# Usar un template existente con datos CSV
template: "templates/stackedbar-horizontal-condatos.yml"
data_source:
  type: "csv"
  path: "data/medallas-juegos-panamericanos-junior-2025.csv"
  
# Personalizaciones específicas
title: "Medallas por país - Juegos Panamericanos Junior 2025"
subtitle: "Total de preseas ganadas (oro, plata y bronce)"
```

### Ejemplo 2: Template con Datos Inline

```yaml
# Usar template con datos definidos directamente en el archivo YAML
template: "templates/linechart-template.yml"
data_source:
  type: "inline"
  data:
    - { "Año": "2020", "Chile": 13.2, "Argentina": 8.7, "Brasil": 7.1 }
    - { "Año": "2021", "Chile": 14.7, "Argentina": 9.1, "Brasil": 7.8 }
    - { "Año": "2022", "Chile": 15.5, "Argentina": 9.5, "Brasil": 8.3 }

# Personalizaciones específicas
title: "Evolución de PIB per cápita"
subtitle: "Valores en miles de USD"
```

### Ejemplo 3: Template Futuro con PostgreSQL

```yaml
# Usar template con conexión directa a PostgreSQL
template: "templates/stackedbar-horizontal-condatos.yml"
data_source:
  type: "postgresql"
  query: "SELECT region, educacion, salud, infraestructura FROM presupuesto_regional WHERE anio = 2025 ORDER BY total DESC LIMIT 10"
  connection:
    host: "db.condatos.cl"
    database: "estadisticas_chile"

# Personalizaciones específicas
title: "Distribución Presupuestaria Regional 2025"
subtitle: "Principales partidas por región (en millones de pesos)"
```

## Ventajas del Sistema de Templates Fijos

1. **Estandarización**: Garantiza que todas las visualizaciones mantengan una identidad visual coherente.
2. **Eficiencia**: Reduce el tiempo de creación de nuevas visualizaciones.
3. **Consistencia**: Asegura que los datos se visualicen de manera uniforme.
4. **Validación**: Permite verificar que los datos cumplan con el formato esperado antes de generar visualizaciones.
5. **Escalabilidad**: Facilita la incorporación de nuevas fuentes de datos sin modificar el código base.
6. **Mantenimiento**: Centraliza los cambios en la apariencia visual en los templates.

## Recomendaciones para la Creación de Templates

1. **Definir claramente el formato de datos esperado**: Documentar la estructura exacta de las columnas o campos requeridos.
2. **Establecer valores predeterminados sensatos**: Configurar valores por defecto que funcionen bien con datos típicos.
3. **Incluir ejemplos de uso**: Proporcionar ejemplos de cómo usar el template con diferentes fuentes de datos.
4. **Documentar las opciones de personalización**: Especificar qué aspectos pueden ser personalizados y cómo.
5. **Diseñar pensando en la audiencia regional**: Considerar las convenciones de formato numérico y fecha utilizadas en Chile y Latinoamérica.

## Uso del Makefile Dinámico

ConDatos incluye un Makefile dinámico que facilita trabajar con múltiples configuraciones y templates. Este sistema:

1. **Detecta automáticamente** los archivos de configuración en el directorio `config/`
2. **Genera targets específicos** para cada archivo de configuración y tipo de gráfico
3. **Permite renderizar configuraciones individuales** o grupos completos de gráficos

### Comandos Básicos

```bash
# Listar todas las configuraciones disponibles
make list-configs

# Renderizar una configuración específica como un gráfico de líneas
make linechart:ejemplo-linechart

# Renderizar una configuración específica como un gráfico de barras horizontales
make stackedbarh:medallas-juegos-panamericanos-junior-2025-stacked-horizontal
```

### Comandos por Tipo de Gráfico

```bash
# Renderizar todos los archivos de configuración como gráficos de líneas
make linechart

# Renderizar todos los archivos de configuración como gráficos de barras horizontales
make stackedbarh
```

### Preparación para PostgreSQL

Cuando se implementen las conexiones a PostgreSQL, se deberán configurar las credenciales de acceso:

```bash
# Configurar variables de entorno para conexiones PostgreSQL
export DB_USER=usuario_condatos
export DB_PASSWORD=contraseña_segura

# Verificar que las variables de entorno están correctamente configuradas
make check-postgres-env
```

## Próximos Pasos en la Implementación

1. **Desarrollo del adaptador PostgreSQL**: Implementación de la conexión directa a bases de datos PostgreSQL.
2. **Creación de esquemas de validación**: Desarrollo de validadores para asegurar que los datos cumplan con los formatos esperados.
3. **Expansión de la biblioteca de templates**: Creación de nuevos templates para visualizaciones especializadas en datos regionales.
4. **Implementación de un sistema de caché**: Para optimizar el rendimiento con consultas frecuentes a la base de datos.
5. **Desarrollo de una interfaz de usuario**: Herramienta visual para seleccionar templates y conectar fuentes de datos.
6. **Mejora del sistema de build**: Refinamiento del Makefile dinámico para soportar más tipos de visualizaciones y fuentes de datos.
