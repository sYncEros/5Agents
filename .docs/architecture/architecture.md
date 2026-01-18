# Arquitectura Técnica de Doctors - 5Agents

**Documento:** Especificación de implementación del sistema multi-agent  
**Versión:** 1.0  
**Fecha:** 16 de enero de 2026  

---

## 1️⃣ Visión General

El sistema 5Agents es una **arquitectura multi-agent jerárquica** donde:

- **Nivel 1:** 18 **Doctors** (Agentes Principales) organizados en 6 categorías
- **Nivel 2:** 54 **Sub-agents** (3 por Doctor) especializados en subdominios
- **Nivel 3:** **Statistics Manager** (Persistencia de eventos)
- **Nivel 4:** **UI Layer** (Streamlit actual, React futura)

```
┌─────────────────────────────────────────────────────┐
│              User Interface (Streamlit/React)       │
├─────────────────────────────────────────────────────┤
│                 Agents Manager                      │
│        (Orquestación dinámica de Doctors)          │
├─────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Logicians│  │Cartograph│  │Interpret │...      │
│  │ (3 Docs) │  │ (3 Docs) │  │  (5 Docs)│         │
│  └──────────┘  └──────────┘  └──────────┘          │
│    │ 3 subs    │ 3 subs      │ 3 subs               │
│    └───┬───┬───┘ └───┬───┬───┘ └───┬───┬──...      │
├─────────────────────────────────────────────────────┤
│         Statistics Manager (JSON Persistence)      │
├─────────────────────────────────────────────────────┤
│      LLM Layer (Ollama + CrewAI Framework)         │
└─────────────────────────────────────────────────────┘
```

---

## 2️⃣ Estructura de Directorios

```
5Agents/
│
├── backend/                          # ← ANTERIOR (DEPRECADO)
│   └── agents/profiles/doctors/     # ← NUEVA UBICACIÓN REAL
│       ├── base_agents.py           # Base class para todos
│       ├── logicians/               # Categoría 1
│       │   ├── Dra.Quark.py         # Doctor principal
│       │   ├── Dra.Monad.py
│       │   ├── Dra.Moebius.py
│       │   └── _subagents/
│       │       ├── NeuroBioQuantumDecoder/
│       │       ├── MetaFormalParadigmEngineer/
│       │       └── QuantumMultiverseLogician/
│       │
│       ├── cartographers/           # Categoría 2
│       │   ├── Dra.Veld.py
│       │   ├── Dra.Mnemosyne.py
│       │   ├── Dra.Memnon.py
│       │   └── _subagents/
│       │       ├── CognitiveVisualMapper/
│       │       ├── CognitiveMemoryCartographer/
│       │       └── MemeticGeoPowerAnalyzer/
│       │
│       ├── interpreters/            # Categoría 3
│       ├── aestheticians/           # Categoría 4
│       ├── analysts/                # Categoría 5
│       ├── transversales/           # Categoría 6
│       └── fallback/                # Agentes de respaldo
│
├── components/
│   ├── core/
│   │   ├── agent_activator.py       # Activador original
│   │   ├── agents_manager.py        # ← A REFACTORIZAR (Usa 4 hardcoded)
│   │   ├── agent_registry.py        # ← A CREAR (Auto-discovery)
│   │   ├── statistics_manager.py    # ✅ Funcional
│   │   └── ...
│   └── ...
│
├── app.py                           # Streamlit actual (✅ Funcional)
├── .docs/
│   ├── doctors-inventory.md         # ← TÚ ESTÁS AQUÍ (Inventario)
│   └── architecture.md              # ← Este documento
│
└── tests/
    ├── test_agent_registry.py       # ← A CREAR
    └── ...
```

---

## 3️⃣ Patrón de Diseño de Doctor

### Estructura Base

```python
from doctors.base_agents import BaseAgente
from typing import Any, Dict, List

class [DoctorClassName](BaseAgente):
    """
    [Nombre Completo] – [Descripción corta]
    Identidad técnica: [TechnicalID]
    """
    
    def __init__(self):
        super().__init__(nombre="[Nombre Completo]")
        self.id = "[TechnicalID]"
        self.rol = "[Rol especializado]"
        self.dominios = [
            "[Dominio 1]",
            "[Dominio 2]",
            "[Dominio 3]",
        ]
        self.subagentes = [
            SubAgent1(),
            SubAgent2(),
            SubAgent3(),
        ]
    
    def generate_prompt(self, user_input: str) -> str:
        """
        Retorna prompt específico para CrewAI.
        Formato: Instrucciones + contexto + tarea
        """
        return f"""
[Instrucciones específicas del Doctor]
...
PREGUNTA: {user_input}
"""
    
    def analizar(self, entrada: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método principal de análisis.
        - Normaliza entrada
        - Invoca sub-agentes
        - Integra resultados
        - Retorna resultado estructurado
        """
        resultado = {}
        for i, subagente in enumerate(self.subagentes):
            resultado[f"subagent_{i+1}"] = subagente.analizar(entrada)
        return resultado
```

### Sub-agentes

```python
class SubAgentName:
    """
    Sub-agente especializado de [Doctor].
    Responsable de: [Tarea específica]
    """
    
    def __init__(self):
        pass
    
    def analizar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis específico del sub-agente.
        
        Args:
            contexto: {
                "pregunta": str,
                "historial": List[str],
                "datos_previos": Dict
            }
        
        Returns:
            {
                "resultado": str,
                "confianza": float,
                "evidencia": List[str],
                "siguiente_paso": str
            }
        """
        # Implementación específica
        return {
            "resultado": "...",
            "confianza": 0.85,
            "evidencia": [...],
            "siguiente_paso": "..."
        }
```

---

## 4️⃣ Importación y Rutas

### Problema Actual

En `backend/agents/profiles/doctors/`, los imports son relativos:

```python
# En Dra.Quark.py (backend/agents/profiles/doctors/logicians/Dra.Quark.py)
from _subagents.NeuroBioQuantumDecoder.QuantumFieldMapper import QuantumFieldMapper
```

⚠️ Esto asume que estás en la carpeta `backend/agents/profiles/doctors/` como root.

### Solución Propuesta

**Opción A: Path relativo completo (Actual)**
```python
# En 5Agents/backend/agents/profiles/doctors/logicians/Dra.Quark.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _subagents.NeuroBioQuantumDecoder.QuantumFieldMapper import QuantumFieldMapper
```

**Opción B: Import absoluto con paquete (Recomendado)**

```python
# Requiere __init__.py en cada carpeta
# En 5Agents/backend/agents/profiles/doctors/__init__.py

from backend.agents.profiles.doctors.logicians.Dra_Quark import CassandraQuarkAgent

# Entonces en agents_manager.py:
from backend.agents.profiles.doctors import CassandraQuarkAgent
```

---

## 5️⃣ Estrategia de Integración

### Fase 1: Agent Registry (NO TOQUES DOCTORS AÚN)

**Archivo nuevo:** `components/core/agent_registry.py`

```python
import importlib
import os
import inspect
from pathlib import Path
from typing import Dict, List, Type, Any

class AgentRegistry:
    """Registry dinámico de todos los Doctors y Sub-agentes."""
    
    def __init__(self, doctors_root: str):
        self.doctors_root = Path(doctors_root)
        self.doctors: Dict[str, Type] = {}
        self.categories: Dict[str, List[str]] = {}
        self._discover_doctors()
    
    def _discover_doctors(self):
        """Auto-descubre todos los Doctors en estructura de directorios."""
        for category_dir in self.doctors_root.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("_"):
                continue
            
            category_name = category_dir.name
            self.categories[category_name] = []
            
            for doctor_file in category_dir.glob("Dra.*.py") or category_dir.glob("Dr.*.py"):
                # Importa dinámicamente
                doctor_class = self._import_doctor(doctor_file)
                if doctor_class:
                    self.doctors[doctor_class.__name__] = doctor_class
                    self.categories[category_name].append(doctor_class.__name__)
    
    def _import_doctor(self, file_path: Path) -> Type | None:
        """Importa un Doctor desde archivo .py."""
        try:
            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Encuentra la clase Doctor
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, 'rol'):
                    return obj
        except Exception as e:
            print(f"Error importando {file_path}: {e}")
        return None
    
    def get_doctor(self, doctor_id: str) -> Any | None:
        """Instancia un Doctor por ID."""
        return self.doctors.get(doctor_id)()
    
    def get_all_doctors(self) -> Dict[str, Any]:
        """Retorna instancias de todos los Doctors."""
        return {name: cls() for name, cls in self.doctors.items()}
    
    def get_doctors_by_category(self, category: str) -> Dict[str, Any]:
        """Retorna Doctors de una categoría."""
        doctor_names = self.categories.get(category, [])
        return {name: self.doctors[name]() for name in doctor_names}
```

### Fase 2: Actualizar AgentsManager

**Archivo actual:** `components/core/agents_manager.py`

```python
# ANTES (Hardcodeado)
AGENTS = {
    "científico": "🔬 Científico",
    "creativo": "🎨 Creativo",
    # ... solo 4
}

# DESPUÉS (Dinámico)
class AgentsManager:
    def __init__(self):
        doctors_path = Path(__file__).parent.parent.parent / "backend" / "agents" / "profiles" / "doctors"
        self.registry = AgentRegistry(str(doctors_path))
        self.all_doctors = self.registry.get_all_doctors()
    
    def process_idea(self, idea: str, doctor_id: str = None) -> Dict[str, Any]:
        """
        Procesa idea con un Doctor específico.
        Si no se especifica, rotea por categoría.
        """
        if doctor_id:
            doctor = self.registry.get_doctor(doctor_id)
        else:
            # Selecciona aleatoriamente
            doctor = random.choice(list(self.all_doctors.values()))
        
        resultado = doctor.analizar({"pregunta": idea})
        
        # Actualiza estadísticas
        self.stats_manager.increment_ideas_processed()
        self.stats_manager.increment_agents_active()
        
        return resultado
```

### Fase 3: Actualizar Streamlit

```python
# app.py

# ANTES
st.sidebar.selectbox("Selecciona agente", ["🔬 Científico", "🎨 Creativo", ...])

# DESPUÉS
doctors = agents_manager.registry.get_all_doctors()
categories = agents_manager.registry.categories

for category, doctor_ids in categories.items():
    with st.expander(f"{category.upper()}"):
        for doctor_id in doctor_ids:
            if st.button(doctor_id):
                # Procesa con ese Doctor
                resultado = agents_manager.process_idea(user_input, doctor_id)
                st.write(resultado)
```

---

## 6️⃣ Compatibilidad LLM

### CrewAI + Ollama

Cada Doctor genera prompt que CrewAI ejecuta:

```python
from crewai import Agent, Task, Crew

doctor = agents_manager.get_doctor("CassandraQuarkAgent")
prompt = doctor.generate_prompt("¿Cómo surge la conciencia cuántica?")

agent = Agent(
    role=doctor.rol,
    goal=doctor.generate_prompt("..."),
    tools=[],  # Sin herramientas externas
    llm=llm  # Ollama instance
)

task = Task(
    description=prompt,
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

resultado = crew.kickoff()
```

---

## 7️⃣ Persistencia y Estadísticas

### Statistics Manager (Ya funcional)

```python
# components/core/statistics_manager.py

stats.add_event({
    "timestamp": datetime.now().isoformat(),
    "doctor_id": "CassandraQuarkAgent",
    "doctor_category": "logicians",
    "input_length": len(idea),
    "subagents_called": 3,
    "processing_time_ms": 1250,
    "result_confidence": 0.92
})

stats.increment_counter("doctors_invoked_total")
stats.increment_counter("logicians_active")
```

---

## 8️⃣ Testing Strategy

### Test structure

```
tests/
├── test_agent_registry.py       # Auto-discovery
├── test_agents_manager.py       # Integración
├── test_individual_doctors.py   # Por categoría
├── test_llm_integration.py      # Ollama + CrewAI
└── test_statistics.py           # Persistencia
```

### Test example

```python
# tests/test_agent_registry.py

def test_registry_discovers_all_doctors():
    registry = AgentRegistry("backend/agents/profiles/doctors")
    
    assert len(registry.doctors) == 18
    assert "logicians" in registry.categories
    assert len(registry.categories["logicians"]) == 3

def test_doctor_has_three_subagents():
    doctor = registry.get_doctor("CassandraQuarkAgent")
    assert len(doctor.subagentes) == 3

def test_doctor_analysis():
    doctor = registry.get_doctor("CassandraQuarkAgent")
    resultado = doctor.analizar({"pregunta": "test"})
    assert "subagent_1" in resultado
    assert "subagent_2" in resultado
    assert "subagent_3" in resultado
```

---

## 9️⃣ Pasos de Deploying

### Paso 1: Crea Agent Registry
- [ ] Crear `components/core/agent_registry.py`
- [ ] Implementar auto-discovery
- [ ] Test con `test_agent_registry.py`

### Paso 2: Refactoriza AgentsManager
- [ ] Actualizar `components/core/agents_manager.py`
- [ ] Reemplazar hardcoding con registry
- [ ] Mantener compatibilidad backwards

### Paso 3: Actualiza Streamlit
- [ ] Modificar `app.py` para mostrar todos los Doctors
- [ ] Agrupar por categoría
- [ ] Expandible: Doctor → Sub-agentes

### Paso 4: Crea Node-RED Endpoint
- [ ] Crear `components/api/doctors_endpoint.py` (FastAPI)
- [ ] Routing dinámico
- [ ] JSON responses

### Paso 5: Testing
- [ ] Ejecutar suite completa de tests
- [ ] Validar 18 Doctors funcionales
- [ ] Verificar persistencia de estadísticas

---

## 🔟 Roadmap Técnico

| Semana | Tarea | Componentes | Status |
|--------|-------|------------|--------|
| 1 | Agent Registry | `agent_registry.py` | ⏳ TODO |
| 2 | Refactor AgentsManager | `agents_manager.py` | ⏳ TODO |
| 2 | Update Streamlit | `app.py` | ⏳ TODO |
| 3 | Node-RED Integration | `doctors_endpoint.py` | ⏳ TODO |
| 3 | Full Test Suite | `tests/` | ⏳ TODO |
| 4 | Production Ready | Deployment | ⏳ TODO |

---

## ✅ Checklist de Implementación

- [ ] Inventario completado (TÚ AQUÍ)
- [ ] Architecture document creado (TÚ AQUÍ)
- [ ] Agent Registry implementado
- [ ] AgentsManager refactorizado
- [ ] Streamlit actualizado
- [ ] Tests pasando (80%+ coverage)
- [ ] Node-RED endpoint funcional
- [ ] Documentación de uso completa
- [ ] Demo funcional con todos los 18 Doctors
- [ ] Prodcution deployment

---

**Documento preparado:** 16 de enero de 2026  
**Próximo paso:** Implementar Agent Registry (Fase 1)
