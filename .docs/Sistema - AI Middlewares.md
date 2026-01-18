# Sistema AI Middlewares

## **¿Qué es un Middleware?**

Un middleware es un componente intermedio que conecta diferentes partes del sistema, asegurando que los datos fluyan correctamente y sean procesados de manera eficiente. En este sistema, los middlewares cumplen funciones como:

- **Preprocesamiento:** Limpieza y normalización de datos antes de enviarlos a los agentes o Doctores.
- **Enrutamiento:** Decisión de qué agentes o Doctores deben activarse según el contexto.
- **Postprocesamiento:** Síntesis y preparación de las salidas para su visualización o exportación.
- **Persistencia:** Almacenamiento de resultados procesados en bases de datos o sistemas de archivos.

---

## **Middlewares Existentes**

1. **Middleware de Detección de Contexto:**
   - **Función:** Detecta planos activos (simbólico, técnico, histórico, etc.) y temas dominantes.
   - **Estado:** Implementado (si el sistema ya activa agentes o Doctores según el contexto detectado).

2. **Middleware de Enrutamiento:**
   - **Función:** Decide qué agentes o Doctores deben activarse según el contexto.
   - **Estado:** Implementado (si el sistema ya tiene reglas claras para activar Doctores).

---

## **Middlewares Faltantes**

1. **Middleware de Preprocesamiento:**
   - **Función:** Limpia y estructura los datos antes de enviarlos a los agentes o Doctores.
   - **Estado:** Podría faltar si no hay un módulo dedicado a esta tarea.

2. **Middleware de Postprocesamiento:**
   - **Función:** Recoge las salidas de los agentes o Doctores, las sintetiza y las prepara para su visualización o exportación.
   - **Estado:** Podría faltar si las respuestas no se integran automáticamente en informes o visualizaciones.

3. **Middleware de Persistencia:**
   - **Función:** Guarda los resultados procesados (pizarras, hipótesis, modelos) en una base de datos o sistema de almacenamiento.
   - **Estado:** Podría faltar si no hay un sistema que gestione la persistencia de datos.

---

## **Análisis del Flujo Actual**

(En esta sección se incluirá el análisis detallado del flujo y recomendaciones específicas.)
