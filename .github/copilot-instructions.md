# Copilot Instructions for φAgents

Este proyecto es un sistema de IA multi-agente actualmente en transición entre un prototipo basado en Streamlit y una arquitectura React/Vite.

---

## **📚 Documentación**
- Mantener la documentación actualizada en la carpeta `.docs/` y en el archivo `README.md`.
- Asegurarse de que cada módulo tenga una descripción clara de su propósito y uso.
- Documentar dependencias externas, configuraciones necesarias y pasos para la instalación.

---

## **🧭 Arquitectura del Proyecto**

El código está dividido en tres capas lógicas:

1.  **Backend / Lógica de Agentes** (`components/`):

    - Contiene los agentes principales de CrewAI, tareas y utilidades.
    - Archivos clave: `components/palimpsestos.py` (Análisis de texto), `components/motor_innovacion.py`.
    - Los agentes están ubicados en `components/agents/`.

2.  **Interfaz Actual (Streamlit)** (`app.py`):
    - Demo funcional del sistema.
    - Usa `streamlit-elements` y `plotly` para visualización.
    - **Nota Crítica**: Algunos imports heredados pueden referenciar `crew_components`. Tratar `crew_components` como `components`.

3.  **Interfaz Futura (Vite/React)** (`dashboard/`):
    - Frontend independiente para reemplazar la interfaz de Streamlit.
    - Actualmente en desarrollo (WIP).
    - Estructura estándar de Vite: `src/main.jsx`, `src/App.jsx`.

---

## **🛠 Flujo de Trabajo para Desarrolladores**

### 1. Ejecutar el Sistema (Actual - Streamlit)

Nuevas características deben probarse aquí primero si involucran lógica de agentes.

```bash
# Activar entorno virtual
# Asegurarse de instalar dependencias: pip install -r requirements.txt
python app.py
# O: streamlit run app.py
```

### 2. Desarrollar el Nuevo Dashboard (Futuro - React)

Trabajar aquí para tareas de modernización de UI/UX.

```bash
cd dashboard
pnpm install
pnpm dev
```

### 3. Patrón de Resolución de Imports

El código ha sido reestructurado.

- **Problema**: Puedes ver imports como `from crew_components.palimpsestos import...`
- **Resolución**: La carpeta actual es `components/`. Usa imports directos desde `components` (e.g., `from components.palimpsestos import...`).

---

## **🧠 Estandarización**
- Seguir convenciones de codificación consistentes en todo el proyecto.
  - Nombres de archivos y carpetas en `snake_case` o `kebab-case`.
  - Nombres de clases en `CamelCase`.
  - Nombres de funciones y variables en `snake_case`.
- Usar comentarios claros y concisos para explicar partes complejas del código.
- Evitar duplicación de código; reutilizar funciones y módulos existentes.

---

## **✅ Pruebas**
- Ejecutar y mantener las pruebas en la carpeta `tests/` para asegurar la calidad del código con cada cambio.
- Usar frameworks como `unittest` o `pytest` para las pruebas.
- Asegurar una cobertura mínima del 70% en las pruebas.
- Seguir el patrón de nombres `test_<nombre_modulo>.py` para los archivos de prueba.
- Evitar mocks innecesarios; usar datos reales o simulaciones controladas.

---

## **🔗 Modularidad**
- Asegurarse de que cada módulo tenga una responsabilidad clara y esté bien documentado.
- Dividir la lógica en componentes reutilizables y fáciles de mantener.
- Mantener las dependencias entre módulos al mínimo.

---

## **🧹 Limpieza de Código**
- Eliminar código comentado o no utilizado para mantener la base de código limpia y legible.
- No hardcodear valores sensibles como claves API o endpoints; usar variables de entorno y configuraciones externas.
- Seguir las mejores prácticas de seguridad para manejar datos sensibles.
- Mantener las dependencias actualizadas y revisar regularmente los archivos de configuración (`requirements.txt`, `package.json`, etc.).
- Usar herramientas de análisis estático de código (como `flake8`, `pylint`, o `eslint`) para mejorar la calidad del código.

---

## **🔄 Control de Versiones**
- Usar un sistema de control de versiones adecuado (Git) para gestionar cambios y colaboraciones.
- Crear ramas específicas para cada funcionalidad o corrección de errores.
- Asegurarse de que cada commit tenga un mensaje claro y descriptivo.
- Realizar revisiones de código entre los miembros del equipo antes de fusionar cambios en la rama principal.

---

## **🤝 Colaboración**
- Fomentar la colaboración y revisión de código entre los miembros del equipo para asegurar la calidad y coherencia del proyecto.
- Usar herramientas como `GitHub Issues` o `Trello` para gestionar tareas y prioridades.
- Mantener una comunicación abierta y documentar decisiones importantes en el desarrollo.

---

¿Quieres que lo guarde directamente en el archivo o necesitas algún ajuste adicional?# Copilot Instructions for 5Agents

Este proyecto es un sistema de IA multi-agente actualmente en transición entre un prototipo basado en Streamlit y una arquitectura React/Vite.

---

## **📚 Documentación**
- Mantener la documentación actualizada en la carpeta `.docs/` y en el archivo `README.md`.
- Asegurarse de que cada módulo tenga una descripción clara de su propósito y uso.
- Documentar dependencias externas, configuraciones necesarias y pasos para la instalación.

---

## **🧭 Arquitectura del Proyecto**

El código está dividido en tres capas lógicas:

1.  **Backend / Lógica de Agentes** (`components/`):

    - Contiene los agentes principales de CrewAI, tareas y utilidades.
    - Archivos clave: `components/palimpsestos.py` (Análisis de texto), `components/motor_innovacion.py`.
    - Los agentes están ubicados en `components/agents/`.

2.  **Interfaz Actual (Streamlit)** (`app.py`):
    - Demo funcional del sistema.
    - Usa `streamlit-elements` y `plotly` para visualización.
    - **Nota Crítica**: Algunos imports heredados pueden referenciar `crew_components`. Tratar `crew_components` como `components`.

3.  **Interfaz Futura (Vite/React)** (`dashboard/`):
    - Frontend independiente para reemplazar la interfaz de Streamlit.
    - Actualmente en desarrollo (WIP).
    - Estructura estándar de Vite: `src/main.jsx`, `src/App.jsx`.

---

## **🛠 Flujo de Trabajo para Desarrolladores**

### 1. Ejecutar el Sistema (Actual - Streamlit)

Nuevas características deben probarse aquí primero si involucran lógica de agentes.

```bash
# Activar entorno virtual
# Asegurarse de instalar dependencias: pip install -r requirements.txt
python app.py
# O: streamlit run app.py
```

### 2. Desarrollar el Nuevo Dashboard (Futuro - React)

Trabajar aquí para tareas de modernización de UI/UX.

```bash
cd dashboard
pnpm install
pnpm dev
```

### 3. Patrón de Resolución de Imports

El código ha sido reestructurado.

- **Problema**: Puedes ver imports como `from crew_components.palimpsestos import...`
- **Resolución**: La carpeta actual es `components/`. Usa imports directos desde `components` (e.g., `from components.palimpsestos import...`).

---

## **🧠 Estandarización**
- Seguir convenciones de codificación consistentes en todo el proyecto.
  - Nombres de archivos y carpetas en `snake_case` o `kebab-case`.
  - Nombres de clases en `CamelCase`.
  - Nombres de funciones y variables en `snake_case`.
- Usar comentarios claros y concisos para explicar partes complejas del código.
- Evitar duplicación de código; reutilizar funciones y módulos existentes.

---

## **✅ Pruebas**
- Ejecutar y mantener las pruebas en la carpeta `tests/` para asegurar la calidad del código con cada cambio.
- Usar frameworks como `unittest` o `pytest` para las pruebas.
- Asegurar una cobertura mínima del 70% en las pruebas.
- Seguir el patrón de nombres `test_<nombre_modulo>.py` para los archivos de prueba.
- Evitar mocks innecesarios; usar datos reales o simulaciones controladas.

---

## **🔗 Modularidad**
- Asegurarse de que cada módulo tenga una responsabilidad clara y esté bien documentado.
- Dividir la lógica en componentes reutilizables y fáciles de mantener.
- Mantener las dependencias entre módulos al mínimo.

---

## **🧹 Limpieza de Código**
- Eliminar código comentado o no utilizado para mantener la base de código limpia y legible.
- No hardcodear valores sensibles como claves API o endpoints; usar variables de entorno y configuraciones externas.
- Seguir las mejores prácticas de seguridad para manejar datos sensibles.
- Mantener las dependencias actualizadas y revisar regularmente los archivos de configuración (`requirements.txt`, `package.json`, etc.).
- Usar herramientas de análisis estático de código (como `flake8`, `pylint`, o `eslint`) para mejorar la calidad del código.

---

## **🔄 Control de Versiones**
- Usar un sistema de control de versiones adecuado (Git) para gestionar cambios y colaboraciones.
- Crear ramas específicas para cada funcionalidad o corrección de errores.
- Asegurarse de que cada commit tenga un mensaje claro y descriptivo.
- Realizar revisiones de código entre los miembros del equipo antes de fusionar cambios en la rama principal.

---

## **🤝 Colaboración**
- Fomentar la colaboración y revisión de código entre los miembros del equipo para asegurar la calidad y coherencia del proyecto.
- Usar herramientas como `GitHub Issues` o `Trello` para gestionar tareas y prioridades.
- Mantener una comunicación abierta y documentar decisiones importantes en el desarrollo.

---
