# 5Agents — React-first

5Agents es un sistema multi‑agente con UI moderna en **React/Vite** y backend en **Python** (CrewAI + Ollama).
El objetivo es operar así:

**React Dashboard** → **Python API** → **CrewAI/Ollama** → respuesta estructurada

---

## 🧩 Ecosistema (estos 3 repos)

Este repo convive con otros dos repos en el workspace:

- **`ai-team/`**: producto “workspace” full‑stack (Node/Express + tRPC + DB + React). Es la app más completa a nivel producto.
- **`AI_Team/`**: modelo/infra de organización N‑Axial (roles + API de roles). Útil como “domain library” e insumo para organigramas/roles.

Recomendación de forma:

- **`5Agents`** = laboratorio/servicio de agentes en Python (API ligera consumible desde React).
- **`ai-team`** = producto principal (UI/experiencia completa).
- **`AI_Team`** = dominio de roles (referencia y/o módulo extraíble).

---

## ✅ Quickstart (modo recomendado)

### 1) Backend (API Python)

Instala dependencias:

```bash
pip install -r requirements.txt
```

Inicia el servidor API (ver `backend/api/server.py`):

```bash
python backend/api/server.py
```

Por defecto:

- API: `http://localhost:8000`

> Requisito: si vas a usar CrewAI con Ollama, asegúrate de tener Ollama corriendo y el modelo instalado.

---

### 2) Frontend (React/Vite)

```bash
cd dashboard
npm install
npm run dev
```

Por defecto:

- UI: `http://localhost:5173`

---

## 🔧 Configuración (env)

El frontend usa:

- `VITE_AGENT_API_URL` → URL base del backend API (ej. `http://localhost:8000`)

Ejemplo recomendado en `.env` (raíz del repo):

```dotenv
VITE_AGENT_API_URL=http://localhost:8000
```

---

## 🤖 Ollama (recomendado)

Verifica instalación:

```bash
ollama --version
```

Instala un modelo (ejemplo):

```bash
ollama pull llama3
```

---

## 🗂️ Estructura relevante

- `dashboard/` → UI React/Vite (interfaz principal)
- `backend/` → lógica y módulos Python (agentes, capas, estadísticas)
- `backend/api/server.py` → servidor HTTP para el dashboard (API oficial)

---

## 🧪 Tests

```bash
pytest -q
```
