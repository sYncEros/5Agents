# Análisis de φAgents

## **1. Estructura General del Repositorio**

El repositorio φAgents está organizado para soportar un sistema de agentes inteligentes con una arquitectura modular. A continuación, se presenta un análisis detallado de la estructura del proyecto y su flujo.

### Estructura del Repositorio

El repositorio está dividido en varias carpetas y archivos clave. Aquí está el desglose:

**Archivos principales en la raíz:**

```bash
app.py: Punto de entrada principal para la aplicación (probablemente usando Streamlit).
app_streamlit.py: Otro punto de entrada con Streamlit (versión alternativa o en desarrollo).
App.tsx: Archivo relacionado con el frontend (React/Vite).
config.toml: Archivo de configuración para parámetros globales.
requirements.txt: Lista de dependencias de Python.
vite.config.js: Configuración para el frontend con Vite.
start.sh: Script para iniciar el proyecto (Unix).
.env: Variables de entorno (claves API, configuraciones sensibles, etc.).
```

**Carpetas principales:**

```bash
backend: Contiene la lógica principal del sistema, dividida en submódulos:
adapters/: Adaptadores para entrada/salida o controladores.
agents/: Definición de agentes y perfiles específicos.
core/: Lógica central (activadores de agentes, controladores, motores de innovación.)
llm/: Integraciones con modelos de lenguaje (Ollama, Mistral).
pipelines/: Construcción y ejecución de flujos de trabajo.
resources/: Recursos adicionales, como taxonomías.
tasks/: Definición de tareas específicas.
dashboard: Contiene el frontend basado en React/Vite + Node-Red
src/: Código fuente del frontend.
public/: Archivos estáticos.
data: Archivos de datos, como estadísticas.
tests: Pruebas unitarias para los diferentes módulos.
```

**Documentación:**

```bash
.docs: Contiene guías y referencias técnicas.
README.md: Archivo principal de documentación.
```

## 2. Flujo del Proyecto

El flujo del proyecto parece estar dividido en dos partes principales:

### **A. Backend (Lógica de Agentes)**

**Definición de Agentes:**

- Los agentes están definidos en agents.
- La lógica central para activarlos y gestionarlos está en core.

**Procesamiento y Tareas:**

- Las tareas específicas están en tasks.
- Los pipelines para ejecutar flujos de trabajo están en pipelines.
- Integración con Modelos de Lenguaje:
  · llm maneja la conexión con modelos como Ollama.

**Controladores y Adaptadores:**

- adapters y core gestionan la interacción entre los agentes y el sistema.

### **B. Frontend (Interfaz de Usuario)**

**Streamlit (Actual):**

- app.py y app_streamlit.py son las interfaces actuales para interactuar con el sistema.
- Usa streamlit-elements para visualizaciones avanzadas.

**React/Vite (Futuro):**

- El frontend moderno está en dashboard.
- src/ contiene los componentes React y la lógica de la interfaz.
- public/ almacena los archivos estáticos necesarios para la aplicación web.
- Node-Red se utiliza para flujos visuales y control de la interfaz.

## 3. Pasos para Ponerlo en Funcionamiento

### A. Backend (Streamlit)

**1. Instalar dependencias:**

Asegúrate de tener un entorno virtual activo:

```bash
python -m venv .venv
source .venv/bin/activate         # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configurar variables de entorno:**

- Crea un archivo `.env` basado en `.env.example` y añade tus claves API y configuraciones necesarias.

**3. Ejecutar la aplicación Streamlit:**

```bash
python app.py
o
python app_streamlit.py
```

### B. Frontend (React/Vite)

**1. Instalar dependencias:**

Navega a la carpeta `dashboard` y ejecuta:

```bash
cd dashboard
pnpm install
```

**2. Ejecutar la aplicación React/Vite:**

```bash
pnpm run dev
```

**3. Acceder a la aplicación:**

Abre tu navegador y ve a `http://localhost:5173` (o el puerto que Vite indique).

## 4. Organización y mejoras

Para mejorar la organización del proyecto, se recomienda:

**Documentación:**

- Mantener la documentación actualizada en `.docs` y `README.md`.

**Estandarización:**

- Seguir convenciones de codificación consistentes en todo el proyecto.

**Pruebas:**

- Ejecutar y mantener las pruebas en la carpeta `tests` para asegurar la calidad del código con cada cambio, usando frameworks como `unittest` o `pytest`.

**Modularidad:**

- Asegurarse de que cada módulo tenga una responsabilidad clara y esté bien documentado.

**Limpieza de Código:**

- Eliminar código comentado o no utilizado para mantener la base de código limpia y legible.
- No hardcodear, no inventar endpoints o claves API directamente en el código fuente; usar variables de entorno.
- Seguir las mejores prácticas de seguridad para manejar datos sensibles.
- Mantener las dependencias actualizadas y revisar regularmente los archivos de configuración.
- Implementar un sistema de control de versiones adecuado para gestionar cambios y colaboraciones.
- Utilizar herramientas de análisis estático de código para mejorar la calidad del código.
- Fomentar la colaboración y revisión de código entre los miembros del equipo para asegurar la calidad y coherencia del proyecto.