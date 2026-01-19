# Ecosistema sΨnc∑ros (workspace)

Este documento describe cómo encajan los 3 repos del workspace y el camino recomendado para integrarlos sin duplicar esfuerzos.

## Repos y responsabilidades

### `ai-team/` (producto principal)

- **Qué es:** app full‑stack (Node/Express + tRPC + DB + React).
- **Problema que resuelve:** "mesa de trabajo" multi‑agente con chat, métricas, persistencia, uploads, etc.
- **Recomendación:** tratarlo como **la UI principal** y el backend de negocio.

### `5Agents/` (servicio/laboratorio de agentes en Python)

- **Qué es:** módulos Python (CrewAI/Ollama + análisis de capas + estadísticas) y un dashboard React en construcción.
- **Uso recomendado:** exponer capacidades como **API HTTP** (Flask) y consumir desde React.
- **API sugerida:** `backend/api/server.py`.

### `AI_Team/` (dominio N‑Axial / roles)

- **Qué es:** modelo de roles organizacionales (40 roles, 3 bloques, 5 ejes) + API de roles.
- **Uso recomendado:** fuente de verdad del dominio "roles" y proveedor de datos para vistas/organigramas.

## Integración recomendada (simple)

### Opción A (rápida): `ai-team` como frontend + backend, consumiendo servicios externos

- `ai-team` consume:
  - `5Agents` como microservicio de análisis/agentes (HTTP)
  - `AI_Team` como microservicio de roles (HTTP)

### Opción B (monorepo conceptual): extraer librerías y reusar

- Extraer el dominio de roles a un paquete compartible.
- Extraer utilidades/contratos de API a `shared/` (TypeScript) y/o OpenAPI.

## Puertos sugeridos (evitar choques)

- `5Agents` API (Flask): `http://localhost:8000`
- `5Agents` dashboard (Vite): `http://localhost:5173`
- `ai-team` app (dev): típicamente `http://localhost:3000`
- DB MySQL (docker): `localhost:3306`

## Contratos mínimos (para React)

### Servicio Python (`5Agents`)

- `POST /api/process` → { process_id, agents, analysis }
- `GET /api/stats` → métricas
- `GET /api/history?limit=5` → histórico

### Servicio roles (`AI_Team`)

- `GET /api/roles/constellation`
- `GET /api/roles/export/agents`

## Notas

- Evita duplicar UI: elige **una UI principal** (recomendado: `ai-team`).
- Evita duplicar lógica de agentes: centraliza decisiones en un servicio o en un coordinador.
