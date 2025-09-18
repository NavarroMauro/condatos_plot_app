# Documentación de ConDatos-Figs-App

Bienvenido a la documentación mejorada de ConDatos-Figs-App, la plataforma para la creación de visualizaciones estandarizadas de datos enfocadas en Chile y su contexto latinoamericano.

## Índice Principal

### 🚀 Primeros Pasos

* [Introducción y Conceptos Básicos](#introducción-y-conceptos-básicos)
* [Instalación y Configuración](#instalación-y-configuración)
* [Tutorial Rápido](#tutorial-rápido)

### 📚 Guía del Usuario

* [Configuración](#configuración)
* [Personalización](#personalización)
* [Tipos de Visualizaciones](#tipos-de-visualizaciones)
* [Casos de Uso](#tipos-de-visualizaciones)

### 🔧 Guía para Desarrolladores

* [Arquitectura](#arquitectura)
* [Contribución](#contribución)
* [Estándares y Prácticas](#estándares-y-prácticas)
* [Tareas Pendientes](TASKS.md)

### 📖 Referencia

* [API](../app/__init__.py)
* [Configuración Avanzada](#configuración)
* [Solución de Problemas](#solución-de-problemas)

---

## Introducción y Conceptos Básicos

* [Arquitectura del Sistema](ARCHITECTURE.md) - Estructura y componentes del proyecto
* [Estándares de Visualización](VISUALIZATIONS_STANDARDS.md) - Principios y estándares visuales para datos chilenos y latinoamericanos
* [Templates y Formatos de Datos](TEMPLATES_DATA_FORMATS.md) - Guía sobre los templates y formatos de datos aceptados

## Instalación y Configuración

* [Configuración del Entorno](../setup_condatos_figs.sh) - Script para configurar el entorno de desarrollo
* [Configuración de Python](../environment.yml) - Configuración del entorno conda
* [Configuración del Makefile](../Makefile.base) - Funcionalidad base para Makefiles

## Tutorial Rápido

* [Generar un Gráfico Simple](../README.md#ejecución-sin-advertencias-de-importación) - Cómo generar un gráfico rápidamente

## Configuración

* [Sintaxis Directa en Makefile](DIRECT_SYNTAX.md) - Uso simplificado de make para generar gráficos
* [Sistema Dinámico](DYNAMIC_SYSTEM.md) - Sistema para detectar tipos de gráficos y generar Makefiles

## Personalización

* [Personalización de Componentes](#personalización-de-componentes) - Guías para personalizar elementos visuales
* [Estilos Predefinidos](../styles/) - Estilos disponibles y su uso

### Personalización de Componentes

* [Títulos y Ejes](AXIS_TITLE_CUSTOMIZATION.md) - Personalización de títulos y ejes
* [Footer/Pie de Página](consolidated/FOOTER.md) - Configuración y personalización del pie de página
* [Leyendas](LEGEND_CUSTOMIZATION.md) - Personalización de leyendas
* [Etiquetas Rotadas](ROTATED_LABELS.md) - Implementación de etiquetas con rotación
* [Etiquetas de Valores y Totales](VALUE_TOTAL_LABELS.md) - Configuración de etiquetas en gráficos
* [Filtrado por Valor](FILTER_BY_VALUE.md) - Filtrar categorías en gráficos por valor mínimo

## Tipos de Visualizaciones

* [Barras Horizontales Apiladas](../app/plots/stackedbarh.py) - Gráficos de barras horizontales apiladas
* [Gráficos de Líneas](../app/plots/linechart.py) - Gráficos de líneas temporales
* [Barras Verticales](../app/plots/barv.py) - Gráficos de barras verticales

## Arquitectura

* [Decisiones de Diseño](DECISIONS.md) - Registro de decisiones arquitectónicas (ADR)
* [Sistema Dinámico](DYNAMIC_SYSTEM.md) - Explicación del sistema de detección de tipos de gráficos

## Contribución

* [Guía para Contribuir](CONTRIBUTING.md) - Cómo contribuir al proyecto
* [Uso con GitHub Copilot](COPILOT.md) - Instrucciones para trabajar con Copilot
* [Mejores Prácticas](BEST_PRACTICES.md) - Prácticas recomendadas para el desarrollo

## Estándares y Prácticas

* [Estandarización](STANDARDIZATION.md) - Guía para estandarizar implementaciones
* [Refactorización](../REFACTORING.md) - Guía de las refactorizaciones implementadas

## Documentación Consolidada

Para una experiencia de documentación mejorada, hemos consolidado algunos documentos relacionados:

* [Sistema de Tracking y Monitoreo](consolidated/TRACKING.md) - Guía de herramientas de tracking
* [Configuración y Personalización del Footer](consolidated/FOOTER.md) - Guía para footers de visualizaciones

Ver [índice de documentación consolidada](consolidated/README.md) para más información.

## Plan de Optimización de la Documentación

Estamos trabajando para mejorar continuamente esta documentación. Consulta nuestro [Plan de Optimización de Documentación](DOC_OPTIMIZATION_PLAN.md) para conocer las próximas mejoras.

---

## Solución de Problemas

* **Problemas Comunes** - (Próximamente) Soluciones a problemas frecuentes
* **Contacto** - Obtén ayuda adicional

## Contacto

Si tienes preguntas o necesitas ayuda adicional, contacta al equipo de desarrollo de ConDatos.

---

© 2025 ConDatos. Todos los derechos reservados.
