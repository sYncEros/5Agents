# 5Agents — Estado actual y plan de rearme

Este repo mezcla **tres capas** distintas:

1. **UI web (Vite/React)** — No está completamente integrada.
2. **UI alternativa (Streamlit)** — Funcional como demo de agentes (`app.py`).
3. **Agentes CrewAI** — Base de agentes y ejemplos (`crew_components/`, `crewai_demo.py`).

El README anterior no corresponde con la estructura real. Aquí tienes el mapa actualizado y un plan de rearme claro.

---

## 🧭 Estructura real del repo

components/
├── core/              # Lógica central
│   ├── palimpsestos.py
│   ├── motor_innovacion.py
│   └── utils.py
├── agents/            # Agentes CrewAI
│   ├── agents.py
│   └── specific_agents.py
├── llm/              # Integración con LLMs (nuevo)
│   ├── ollama_client.py  (a crear)
│   └── profiles.py       (a crear)
└── tasks/            # Tareas y orquestación
    └── task.py

## ✅ Qué funciona hoy

### Opción A — Streamlit (funciona)

`app.py` es una demo visual y funcional. Es lo más estable actualmente.

### Opción B — CrewAI (funciona)

`crewai_demo.py` corre un flujo básico entre agentes.

### Opción C — Vite/React (incompleto)

Hay dependencia instalada, pero faltan carpetas (`components/`, `pages/`, `contexts/`, etc.) y la app no arranca tal cual.

---

## 🔧 Plan de rearme (propuesto)

### Fase 1 — Unificar la UI

Escoge **una** de estas rutas:

**Ruta 1 (rápida):**

- Usar solo `app.py` (Streamlit) como interfaz oficial.

**Ruta 2 (web moderna):**

- Crear estructura estándar `src/` para Vite.
- Mover `App.jsx` y `App.css` a `src/`.
- Crear `src/main.jsx` y `src/index.css`.
- Añadir carpetas `components/`, `pages/`, `contexts/`.

### Fase 2 — Conectar agentes reales

- Exponer un backend (FastAPI/Flask) para CrewAI.
- Consumir desde la UI escogida (Streamlit o React).

### Fase 3 — Documentación viva

- Crear `docs/` con: arquitectura, endpoints, ejemplos de prompt, agentes activos.

---

## ▶️ Cómo ejecutar (estado actual)

### Streamlit

```bash
pip install -r requirements.txt
python app.py
```

### Vite (solo si se rearma)

```bash
pnpm install
pnpm dev
```
