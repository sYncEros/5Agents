# Diagrama Visual: Arquitectura de Doctors - 5Agents

**Visualización paso a paso del flujo completo**  
16 de enero de 2026

---

## 1️⃣ ÁRBOL DE HERENCIA COMPLETO

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        5AGENTS ARCHITECTURE                                  │
└──────────────────────────────────────────────────────────────────────────────┘

RAMA A: Legacy Agents (profiles/)
═══════════════════════════════════

                        ┌─────────────────────┐
                        │   AgentProfile      │
                        │  (dataclass)        │
                        ├─────────────────────┤
                        │ - nombre: str       │
                        │ - rol: str          │
                        │ - prompt_base: str  │
                        │ - modelo_llm: str   │
                        │ - tags: list        │
                        │ - capabilities:list │
                        │                     │
                        │ build_prompt()      │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │    BaseAgent        │
                        │   (ABC)             │
                        ├─────────────────────┤
                        │ + llm_client        │
                        │ + _history: []      │
                        │                     │
                        │ @abstractmethod     │
                        │   process()         │
                        │ analyze()           │
                        │ collaborate()       │
                        └──────────┬──────────┘
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
        ┌──────────▼───────┐  ┌───▼────────────┐  │
        │  Cassandra       │  │ Otros Agentes  │  │
        │  QuarkAgent      │  │ (simples)      │  │
        │ (profiles/)      │  │                │  │
        │                  │  │ - archivador   │  │
        │ ✅ LLM Client    │  │ - experiment   │  │
        │ ✅ Historial     │  │ - logos        │  │
        │ ❌ Sub-agentes   │  │ - valis        │  │
        └──────────────────┘  └────────────────┘  │
                                                  │
                          (sin sub-agentes)


RAMA B: Advanced Doctors (doctors/)
════════════════════════════════════

                        ┌─────────────────────┐
                        │    BaseAgente       │
                        │  (simple, NO ABC)   │
                        ├─────────────────────┤
                        │ - nombre: str       │
                        │ - subagentes: []    │
                        │ - debug_enabled     │
                        │ - debug_steps: []   │
                        │ - _step_hook        │
                        │ - _slowdown_ms      │
                        │                     │
                        │ analizar()          │
                        │ activar_subagentes()│
                        │ log_step()          │
                        │ set_step_hook()     │
                        └──────────┬──────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
    ┌───▼──────────────┐   ┌──────▼──────────┐   ┌──────────▼───┐
    │  LOGICIANS (3)   │   │ CARTOGRAPHERS(3)│   │ INTERPRETERS │
    │  ──────────────  │   │ ──────────────  │   │   (5)        │
    │                  │   │                  │   │              │
    │ • Dra.Quark      │   │ • Dra.Veld       │   │ • Dr.Eidon   │
    │ • Dra.Monad      │   │ • Dra.Mnemosyne  │   │ • Dr.Valis   │
    │ • Dra.Moebius    │   │ • Dra.Memnon     │   │ • Dra.Lorentz│
    └────┬─────────────┘   └────┬─────────────┘   │ • Dra.Kaon   │
         │                      │                 │ • Dra.Tlalt. │
         │ 3 sub c/u           │ 3 sub c/u       └─────┬────────┘
         │                      │                      │
    ┌────▼──────────────────────────────────────────────┴──────┐
    │                                                           │
    │  CADA DOCTOR INSTANCIA 3 SUB-AGENTES EN __init__        │
    │                                                           │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │  Dra.Quark                                      │    │
    │  │  ├─ QuantumFieldMapper                          │    │
    │  │  ├─ NeuralDynamicalProfiler                     │    │
    │  │  └─ BioInfoTransductionAnalyzer                 │    │
    │  └─────────────────────────────────────────────────┘    │
    │                                                           │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │  Dra.Veld                                       │    │
    │  │  ├─ VisualizationSelector                       │    │
    │  │  ├─ SpatialNarrativeDescriber                   │    │
    │  │  └─ ExportSchemaBuilder                         │    │
    │  └─────────────────────────────────────────────────┘    │
    │                                                           │
    │  ┌─────────────────────────────────────────────────┐    │
    │  │  [Y 16 Doctors MÁS...]                          │    │
    │  │  [18 DOCTORS × 3 SUB-AGENTS = 54 TOTAL]        │    │
    │  └─────────────────────────────────────────────────┘    │
    │                                                           │
    └────────────────────────────────────────────────────────────┘
```

---

## 2️⃣ FLUJO DE INSTANCIACIÓN

### Paso 1: Crear un Doctor

```python
# File: backend/agents/profiles/doctors/logicians/Dra.Quark.py

class CassandraQuarkAgent(BaseAgente):      # ← Hereda de BaseAgente
    
    def __init__(self):
        super().__init__(nombre="Dra. Cassandra Quark")
        # ↑ Llama BaseAgente.__init__()
        
        self.id = "CassandraQuarkAgent"
        self.rol = "NeuroBioQuantum Decoder"
        self.dominios = [...]
        
        # ← INSTANCIA LOS 3 SUB-AGENTES
        self.subagentes = [
            QuantumFieldMapper(),              # ← Sub-agente 1
            NeuralDynamicalProfiler(),         # ← Sub-agente 2
            BioInfoTransductionAnalyzer(),     # ← Sub-agente 3
        ]


    ┌─ Estado en memoria:
    │
    │  CassandraQuarkAgent {
    │    nombre: "Dra. Cassandra Quark",
    │    id: "CassandraQuarkAgent",
    │    subagentes: [
    │      QuantumFieldMapper { ... },
    │      NeuralDynamicalProfiler { ... },
    │      BioInfoTransductionAnalyzer { ... }
    │    ],
    │    debug_enabled: False,
    │    debug_steps: [],
    │    _step_hook: None
    │  }
    │
```

---

## 3️⃣ FLUJO DE ANÁLISIS

```
USER INPUT
    │
    "¿Cómo el entrelazamiento cuántico...?"
    │
    ▼
┌─────────────────────────────────────────────┐
│  app.py (Streamlit)                         │
│  selectBox: "Selecciona Doctor"             │
│  user clicks: "Dra. Cassandra Quark"        │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  agents_manager.process_idea()              │
│  input: "¿Cómo el entrelazamiento...?"     │
│  doctor_id: "CassandraQuarkAgent"           │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  agent_registry.get_doctor()                │
│  Busca: "CassandraQuarkAgent"               │
│  Retorna: CassandraQuarkAgent()             │
└──────────────┬──────────────────────────────┘
               │
               ▼
        ┌──────────────┐
        │  doctor.__init__()
        │  Instancia 3 sub-agentes
        └──────────────┬──────────────┐
                       │              │
                       ▼              ▼
            ┌────────────────────────────────────┐
            │  doctor.analizar(                  │
            │    texto="¿Cómo el entrelazamiento│
            │    contexto={}                     │
            │  )                                 │
            └────────────────┬───────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐
    │ SubAgent 1   │  │ SubAgent 2    │  │ SubAgent 3      │
    │              │  │               │  │                 │
    │ Quantum      │  │ Neural        │  │ BioInfo         │
    │ FieldMapper  │  │ Dynamical     │  │ Transduction    │
    │              │  │ Profiler      │  │ Analyzer        │
    │              │  │               │  │                 │
    │ .analizar()  │  │ .analizar()   │  │ .analizar()     │
    │              │  │               │  │                 │
    │ ↓            │  │ ↓             │  │ ↓               │
    │ BÚSQUEDA     │  │ BÚSQUEDA      │  │ BÚSQUEDA        │
    │ pistas en    │  │ patrones      │  │ códigos         │
    │ texto        │  │ neurales      │  │ biológicos      │
    │              │  │               │  │                 │
    │ RETORNA:     │  │ RETORNA:      │  │ RETORNA:        │
    │ {            │  │ {             │  │ {               │
    │ "hipotesis": │  │ "hipotesis":  │  │ "hipotesis":    │
    │  "...",      │  │  "...",       │  │  "...",         │
    │ "hallazgos": │  │ "hallazgos":  │  │ "hallazgos":    │
    │  [...],      │  │  [...],       │  │  [...],         │
    │ "chiste": "..│  │ "prototipo": "│  │ "oblicuidad":"..│
    │ }            │  │ }             │  │ }               │
    └──────┬───────┘  └───────┬───────┘  └────────┬────────┘
           │                  │                   │
           └──────────────────┼───────────────────┘
                              │
              ┌───────────────▼───────────────┐
              │  Doctor INTEGRA RESULTADOS    │
              │                               │
              │  titulo = "Sincronías en     │
              │           el borde..."        │
              │                               │
              │  hipotesis = {                │
              │    "entrelazada": "...",      │
              │    "robusta": "...",          │
              │    "definitiva": "..."        │
              │  }                            │
              │                               │
              │  return {                     │
              │    "doctor": "Dra. Q.",       │
              │    "titulo": "...",           │
              │    "hipotesis": {...},        │
              │    "hallazgos": [res1,        │
              │                  res2,        │
              │                  res3],       │
              │    "tiempo_ms": 245           │
              │  }                            │
              └───────────────┬───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │ agents_manager    │
                    │ actualiza         │
                    │ estadísticas      │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ statistics_manager│
                    │ .add_event({...}) │
                    │ .increment(...)   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼──────────┐
                    │ JSON guardado en   │
                    │ data/statistics.json
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │ app.py muestra:    │
                    │ - Titulo           │
                    │ - Hipótesis        │
                    │ - Hallazgos c/sub  │
                    │ - Tiempo           │
                    └────────────────────┘
```

---

## 4️⃣ ESTRUCTURA DE RESPUESTA

```json
{
  "doctor": "Dra. Cassandra Quark",
  "id_tecnico": "CassandraQuarkAgent",
  "rol": "NeuroBioQuantum Decoder",
  "titulo": "Sincronías en el borde: del qubit al attractor cortical",
  "hipotesis": {
    "entrelazada": "Estructuras narrativas muestran acoplamientos análogos...",
    "robusta": "La plasticidad semántica sugiere cambios de fase...",
    "definitiva": "Operadores de medición semántica colapsan..."
  },
  "hallazgos_subagentes": [
    {
      "subagente": "QuantumFieldMapper",
      "hipotesis": "La información narrada exhibe fases de coherencia/ruido...",
      "hallazgos": ["Rastros cuánticos: coherencia, entrelazamiento"],
      "oblicuidad": "Cuidado con metáforas duras...",
      "prototipo": "Espectrograma semántico...",
      "chiste": "Medí el texto y colapsó..."
    },
    {
      "subagente": "NeuralDynamicalProfiler",
      "hipotesis": "...",
      "hallazgos": [...],
      ...
    },
    {
      "subagente": "BioInfoTransductionAnalyzer",
      "hipotesis": "...",
      "hallazgos": [...],
      ...
    }
  ],
  "tiempo_ms": 245
}
```

---

## 5️⃣ ESTRUCTURA DE DIRECTORIOS

```
backend/agents/profiles/doctors/
│
├── base_agents.py                    ← LA BASE
│   class BaseAgente:
│       def __init__(nombre)
│       def analizar()
│       def activar_subagentes()
│       def log_step()
│
├── logicians/                        ← CATEGORÍA 1
│   ├── Dra.Quark.py
│   │   class CassandraQuarkAgent(BaseAgente):
│   │       self.subagentes = [3 sub-agents]
│   │       def analizar()
│   │       def generate_prompt()
│   │
│   ├── Dra.Monad.py
│   ├── Dra.Moebius.py
│   │
│   └── _subagents/
│       ├── NeuroBioQuantumDecoder/
│       │   ├── __init__.py
│       │   ├── QuantumFieldMapper.py
│       │   │   class QuantumFieldMapper:
│       │   │       def analizar()
│       │   │
│       │   ├── NeuralDynamicalProfiler.py
│       │   └── BioInfoTransductionAnalyzer.py
│       │
│       ├── MetaFormalParadigmEngineer/
│       │   ├── TopoMethodDesigner.py
│       │   ├── StructureLiftDetector.py
│       │   └── CreativeFormalismGenerator.py
│       │
│       └── QuantumMultiverseLogician/
│           ├── ParaconsistentEvaluator.py
│           ├── ModalInferenceBuilder.py
│           └── AxiomExtractor.py
│
├── cartographers/                    ← CATEGORÍA 2
│   ├── Dra.Veld.py
│   ├── Dra.Mnemosyne.py
│   ├── Dra.Memnon.py
│   └── _subagents/
│       ├── CognitiveVisualMapper/
│       ├── CognitiveMemoryCartographer/
│       └── MemeticGeoPowerAnalyzer/
│
├── interpreters/                     ← CATEGORÍA 3
├── aestheticians/                    ← CATEGORÍA 4
├── analysts/                         ← CATEGORÍA 5
├── transversales/                    ← CATEGORÍA 6
│
└── fallback/                         ← AGENTES DE RESPALDO
    ├── HeuristicSeedAgent.py
    └── HeuristicSeedAgentPlus.py
```

---

## 6️⃣ PATRÓN: DOCTOR CON 3 SUB-AGENTES

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCTOR (Main Agent)                      │
│                                                              │
│  class DoctorName(BaseAgente):                              │
│    def __init__(self):                                      │
│      super().__init__(nombre="...")                         │
│      self.id = "..."                                        │
│      self.rol = "..."                                       │
│      self.dominios = [...]                                  │
│                                                              │
│      ┌──────────────────────────────────────────────────┐  │
│      │ Instancia 3 Sub-agentes:                         │  │
│      │                                                   │  │
│      │ self.subagentes = [                              │  │
│      │   SubAgent1(),  ────────┐                        │  │
│      │   SubAgent2(),  ────────┼─────────┐              │  │
│      │   SubAgent3(),  ────────┼─────────┼────────┐     │  │
│      │ ]                       │         │        │     │  │
│      └──────────────────────────────────────────────────┘  │
│                                                              │
│    def generate_prompt(user_question):                      │
│      # Retorna prompt estructurado para CrewAI              │
│                                                              │
│    def analizar(texto, contexto):                           │
│      # 1. Invoca cada sub-agente                            │
│      resultados = []                                        │
│      for sa in self.subagentes:                             │
│        res = sa.analizar(texto, contexto)                   │
│        resultados.append(res)                               │
│                                                              │
│      # 2. Integra resultados                                │
│      return {                                               │
│        "doctor": self.nombre,                               │
│        "titulo": "...",                                     │
│        "hipotesis": {...},                                  │
│        "hallazgos_subagentes": resultados,                  │
│        "tiempo_ms": ...                                     │
│      }                                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ SubAgent 1   │   │ SubAgent 2   │   │ SubAgent 3   │
    │              │   │              │   │              │
    │ class SA1:   │   │ class SA2:   │   │ class SA3:   │
    │   def        │   │   def        │   │   def        │
    │   analizar() │   │   analizar() │   │   analizar() │
    │      ↓       │   │      ↓       │   │      ↓       │
    │   return {   │   │   return {   │   │   return {   │
    │   "result": │   │   "result": │   │   "result": │
    │   "..."}     │   │   "..."}     │   │   "..."}     │
    └──────────────┘   └──────────────┘   └──────────────┘
```

---

## 7️⃣ CICLO COMPLETO EN TEXTO

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  FASE 1: SETUP (Una sola vez)                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. Agent Registry descubre todos los Doctors                  │
│     └─ Encuentra 18 Doctors en 6 categorías                    │
│     └─ Mapea 54 Sub-agentes (3 × 18)                           │
│                                                                 │
│  2. Statistics Manager inicializa                              │
│     └─ Carga data/statistics.json                              │
│                                                                 │
│  3. AgentsManager carga registry                               │
│     └─ Listo para procesar ideas                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  FASE 2: RUNTIME (Cada idea)                                   │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. Usuario escribe: "¿Cómo surge la conciencia?"              │
│                                                                 │
│  2. Streamlit captura y llama AgentsManager                     │
│     result = agents_manager.process_idea(idea)                 │
│                                                                 │
│  3. AgentsManager selecciona doctor (aleatorio o específico)    │
│     doctor = registry.get_doctor("CassandraQuarkAgent")        │
│     ↓ Instancia: CassandraQuarkAgent()                         │
│     ↓ Que instancia sus 3 Sub-agentes                          │
│                                                                 │
│  4. AgentsManager llama doctor.analizar()                       │
│     ↓ Doctor llama cada Sub-agente.analizar()                  │
│     ↓ Sub-agentes procesan en paralelo lógico                  │
│     ↓ Retornan resultados estructurados                        │
│                                                                 │
│  5. Doctor integra resultados                                  │
│     ↓ Síntesis de hipótesis                                    │
│     ↓ Agregación de hallazgos                                  │
│     ↓ Timing total                                             │
│                                                                 │
│  6. AgentsManager registra evento en Statistics                │
│     stats.add_event({                                          │
│       "doctor": "CassandraQuarkAgent",                          │
│       "category": "logicians",                                 │
│       "subagents_called": 3,                                   │
│       "time_ms": 245                                           │
│     })                                                          │
│                                                                 │
│  7. Streamlit recibe resultado JSON                             │
│     {                                                           │
│       "doctor": "Dra. Quark",                                  │
│       "titulo": "Sincronías...",                               │
│       "hipotesis": {...},                                      │
│       "hallazgos_subagentes": [{...}, {...}, {...}],          │
│       "tiempo_ms": 245                                         │
│     }                                                           │
│                                                                 │
│  8. Streamlit muestra resultado con:                           │
│     ✅ Nombre Doctor                                           │
│     ✅ Título síntesis                                         │
│     ✅ Hipótesis integradas                                    │
│     ✅ Hallazgos por Sub-agente (expandible)                   │
│     ✅ Tiempo de procesamiento                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8️⃣ RESUMEN VISUAL: Las 4 Capas

```
┌──────────────────────────────────────────────────────────┐
│              CAPA 1: USER INTERFACE                      │
│                     Streamlit                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ [TextInput] [SelectBox] [Button]                   │  │
│  │ Muestra: Doctor | Titulo | Hipótesis | Hallazgos  │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│         CAPA 2: ORQUESTACIÓN                             │
│         AgentsManager                                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 1. Selecciona Doctor                              │  │
│  │ 2. Instancia via registry                          │  │
│  │ 3. Llama doctor.analizar()                         │  │
│  │ 4. Actualiza estadísticas                          │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│         CAPA 3: DOCTORS + SUB-AGENTES                    │
│         18 Doctors × 3 Sub-agentes                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Doctor instancia Sub-agentes en __init__           │  │
│  │ Doctor.analizar() invoca Sub-agentes               │  │
│  │ Cada Sub-agente procesa y retorna resultado        │  │
│  │ Doctor integra resultados                          │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│         CAPA 4: PERSISTENCIA                             │
│         Statistics Manager                              │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Registra evento en data/statistics.json            │  │
│  │ Actualiza contadores                              │  │
│  │ Mantiene historial de procesamiento                │  │
│  └────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

**Documento completo:** 16 de enero de 2026  
**Estado:** Referencia visual lista para desarrollo
