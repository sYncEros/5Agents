# **🛠️ Montaje Técnico: Arquitectura Híbrida**

Este documento define la infraestructura técnica para orquestar los agentes de **Documentación** y **Computación** utilizando una arquitectura en tres capas:

1. **Frontend (React/Vite)**: Interfaz de usuario moderna y reactiva.
2. **Orquestador (Node-RED)**: "Sistema Nervioso" visual para enrutamiento y gestión de flujos.
3. **Backend (Python)**: "Cerebro" lógico donde residen los agentes CrewAI y algoritmos complejos.

---

## 🏛️ Arquitectura del Sistema

El flujo de datos sigue este patrón:
`[Usuario] -> [React Dashboard] -> (HTTP) -> [Node-RED] -> (Exec/API) -> [Python Agents] -> [Resultados]`

### 1. Frontend: React Dashboard

Ubicación: `dashboard/`

- **Tecnología**: Vite + React + TailwindCSS.
- **Componente Principal**: `dashboard/src/components/AgentDashboard.jsx`.
- **Función**: Captura la intención del usuario y muestra resultados estructurados.

### 2. Orquestador: Node-RED

Ubicación: Instancia local o contenedor.

- **Función**: Recibe peticiones del frontend, decide qué agente activar y coordina la respuesta.
- **Enrutamiento**:
  - *Keywords "documenta", "resumen"* -> **Agente Mnemosyne**.
  - *Keywords "código", "lógica"* -> **Agente Logos**.
  - *Keywords "simula", "universo"* -> **Agente Simulador**.

### 3. Backend: Python Agents

Ubicación: `components/` (estructura modular actualizada)

```
components/
├── core/              # Lógica central del sistema
│   ├── layer_detector.py      # Detección de capas y contexto
│   ├── motor_innovacion.py    # Motor de innovación
│   └── utils.py               # Utilidades
├── agents/            # Definiciones de agentes CrewAI
│   ├── agents.py              # Agentes base
│   └── specific_agents.py     # Agentes especializados
├── llm/              # Integración con LLMs locales ⭐ NUEVO
│   ├── ollama_client.py       # Cliente para Ollama
│   └── profiles.py            # Perfiles de agentes conversacionales
└── tasks/            # Orquestación de tareas
    └── task.py
```

- **Tecnología**: Python 3.9+, CrewAI, Ollama.
- **Ejecución**: Scripts invocados por Node-RED o expuestos vía API (Flask/FastAPI).

---

## 🚀 Guía de Instalación y Ejecución

### Paso 1: Backend Python (Cerebro)

Asegura que las dependencias de los agentes estén listas.

```bash
# En la raíz del proyecto
python -m venv venv
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 2: Orquestador Node-RED (Nervios)

Node-RED actúa como middleware.

1. **Instalación** (si no lo tienes):

    ```bash
    npm install -g --unsafe-perm node-red
    ```

2. **Ejecución**:

    ```bash
    node-red
    ```

    *Accede a <http://localhost:1880>*

3. **Configuración del Flujo**:
    - Crea un nodo `HTTP In` (POST) en `/api/agent`.
    - Conecta un nodo `Function` para el enrutamiento (ver lógica abajo).
    - Conecta nodos `Exec` para llamar a los scripts de Python en `components/`.
    - Termina con un nodo `HTTP Response`.

### Paso 3: Frontend React (Cara)

Levanta la interfaz de usuario.

```bash
cd dashboard
pnpm install
# Asegúrate de que AgentDashboard.jsx apunte a http://localhost:1880/api/agent
pnpm dev
```

---

## � Uso del Sistema de LLMs Locales

### Configuración de Ollama

El módulo `components/llm/` proporciona integración con LLMs locales vía Ollama.

**1. Instalar Ollama:**

- Descarga desde [ollama.ai](https://ollama.ai)
- Verifica instalación: `ollama --version`

**2. Descargar modelos:**

```bash
ollama pull mistral      # Modelo general balanceado
ollama pull llama2       # Alternativa robusta
ollama pull phi          # Modelo ligero y rápido
```

**3. Verificar disponibilidad:**

```bash
ollama list  # Lista modelos instalados
```

### Uso del OllamaClient

```python
from components.llm import OllamaClient

# Inicializar cliente
client = OllamaClient(base_url="http://localhost:11434")

# Verificar conexión
if client.is_available():
    print("✅ Ollama conectado")
    print(f"Modelos disponibles: {client.list_models()}")

# Generar respuesta
respuesta = client.generate(
    prompt="Explica la física cuántica en términos simples",
    model="mistral",
    temperature=0.7,
    max_tokens=500
)
print(respuesta)
```

### Uso de Perfiles de Agentes

Los perfiles definen la personalidad y expertise de cada agente:

```python
from components.llm import AGENT_PROFILES, OllamaClient

# Listar perfiles disponibles
print("Agentes disponibles:")
for key, profile in AGENT_PROFILES.items():
    print(f"  - {profile.nombre}: {profile.rol}")

# Usar un perfil específico
client = OllamaClient()
cassandra = AGENT_PROFILES["cassandra_quark"]

# Construir prompt con el perfil
user_input = "¿Puede una IA tener experiencias subjetivas?"
prompt = cassandra.build_prompt(user_input)

# Generar respuesta con el estilo del agente
respuesta = client.generate(
    prompt=prompt,
    model=cassandra.modelo_llm,
    temperature=cassandra.temperatura
)

print(f"\n🤖 {cassandra.nombre} responde:")
print(respuesta)
```

### Perfiles Disponibles

| **Key** | **Agente** | **Especialidad** | **Modelo** | **Temp** |
|---------|-----------|------------------|------------|----------|
| `cassandra_quark` | Dra. Cassandra Quark | Física cuántica y epistemología | mistral | 0.8 |
| `valis` | Dr. Éterio Valis | Antropología mítica y simbólica | mistral | 0.9 |
| `logos` | Agente Logos | Ingeniería de sistemas | mistral | 0.5 |
| `mnemosyne` | Agente Mnemosyne | Documentación y conocimiento | mistral | 0.6 |
| `multiverse_sim` | Simulador de Multiverso | Modelado de escenarios | mistral | 0.85 |

### Ejemplo: Conversación Multi-Agente

```python
from components.llm import OllamaClient, AGENT_PROFILES

client = OllamaClient()
pregunta = "¿Cómo podríamos construir una IA consciente?"

# Activar múltiples agentes
agentes_activos = ["cassandra_quark", "valis", "logos"]

for key in agentes_activos:
    profile = AGENT_PROFILES[key]
    prompt = profile.build_prompt(pregunta)
    
    print(f"\n{'='*60}")
    print(f"🤖 {profile.nombre}")
    print(f"{'='*60}")
    
    respuesta = client.generate(
        prompt=prompt,
        model=profile.modelo_llm,
        temperature=profile.temperatura
    )
    print(respuesta)
```

---

## �🧩 Configuración del Enrutador (Node-RED)

Copia este código en un nodo `Function` en Node-RED para distribuir las tareas:

```javascript
// Detectar intención desde el body del request
var prompt = msg.payload.texto.toLowerCase();
var agent = "default";

if (prompt.includes("document") || prompt.includes("estructura")) {
    agent = "mnemosyne"; // Agente de Documentación
} else if (prompt.includes("código") || prompt.includes("lógica")) {
    agent = "logos"; // Agente de Computación
} else if (prompt.includes("simula") || prompt.includes("universo")) {
    agent = "multiverse_sim"; // Agente Simulador
}

// Preparar comando para Python
// IMPORTANTE: Ajusta la ruta absoluta a tu entorno y script
msg.payload = {
    command: "python",
    args: ["C:/Users/usuario/Downloads/PROJECTS/.repos/5Agents/components/tasks/task.py", "--agent", agent, "--prompt", msg.payload.texto]
};

return msg;
```

---

## 📚 Estructura de Carpetas Actualizada

```
5Agents/
├── .docs/                    # Documentación del proyecto
│   ├── Montaje Técnico.md   # Este archivo
│   └── agents/              # Documentación de agentes específicos
├── components/              # Backend Python
│   ├── core/               # ⭐ Lógica central
│   │   ├── layer_detector.py
│   │   ├── motor_innovacion.py
│   │   └── utils.py
│   ├── agents/             # Definiciones CrewAI
│   │   ├── agents.py
│   │   └── specific_agents.py
│   ├── llm/               # ⭐ NUEVO: Integración LLMs
│   │   ├── ollama_client.py
│   │   └── profiles.py
│   └── tasks/             # ⭐ Orquestación
│       └── task.py
├── dashboard/              # Frontend React
│   └── src/
│       └── components/
│           └── AgentDashboard.jsx
├── app.py                  # Streamlit demo
├── config.toml            # Configuración
├── requirements.txt       # Dependencias Python
└── todo.md               # Tareas pendientes

```

---

## 🔗 Referencias Rápidas

- **Ollama API Docs**: [https://github.com/ollama/ollama/blob/main/docs/api.md](https://github.com/ollama/ollama/blob/main/docs/api.md)
- **Node-RED Docs**: [https://nodered.org/docs/](https://nodered.org/docs/)
- **CrewAI Docs**: [https://docs.crewai.com/](https://docs.crewai.com/)
- **Vite + React**: [https://vitejs.dev/](https://vitejs.dev/)

---

**Última actualización:** 15 de enero de 2026
