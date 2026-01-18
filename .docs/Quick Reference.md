# Quick Reference - Doctors 5Agents

**Cheat Sheet para desarrollo rápido**  
16 de enero de 2026

---

## 🎯 En Una Página

### Conteo Total

```
18 Doctors × 3 Sub-agents = 54 Agents total
Organizados en 6 categorías disciplinarias
```

### Categorías y Counts

🔬 Logicians      → 3 Doctors (Quark, Monad, Moebius)
🗺️  Cartographers  → 3 Doctors (Veld, Mnemosyne, Memnon)
🧠 Interpreters   → 5 Doctors (Eidon, Valis, Lorentz, Kaon, Tlaltekutli)
🎨 Aestheticians  → 3 Doctors (Tyche, Soliton, Clytemnos)
📈 Analysts       → 5 Doctors (Galois, Turing-Safira, Diotropos, Kaleidos, Braid)
🔄 Transversales  → 1 Doctor (Enopatos)

---

## 📍 Ubicación en Disco

5Agents/backend/agents/profiles/doctors/
├── logicians/               # 3 Doctors
├── cartographers/           # 3 Doctors
├── interpreters/            # 5 Doctors
├── aestheticians/           # 3 Doctors
├── analysts/                # 5 Doctors
├── transversales/           # 1 Doctor
└── base_agents.py           # Base class

---

## 🔍 Doctors por Categoría

### 🔬 LOGICIANS (Pensamiento Lógico Cuántico-Computacional)

| Doctor | ID Técnico | Rol | Sub-agents |
|--------|-----------|-----|-----------|
| Dra. Quark | `CassandraQuarkAgent` | NeuroBioQuantum Decoder | QuantumFieldMapper, NeuralDynamicalProfiler, BioInfoTransductionAnalyzer |
| Dra. Monad | `MetaFormalParadigmEngineer` | Ingeniero de Paradigmas Formales | TopoMethodDesigner, StructureLiftDetector, CreativeFormalismGenerator |
| Dra. Moebius | `QuantumMultiverseLogician` | Lógica del Multiverso Cuántico | ParaconsistentEvaluator, ModalInferenceBuilder, AxiomExtractor |

### 🗺️ CARTOGRAPHERS (Visualización y Navegación)

| Doctor | ID Técnico | Rol | Sub-agents |
|--------|-----------|-----|-----------|
| Dra. Veld | `CognitiveVisualMapper` | Visualizadora Cognitiva | VisualizationSelector, SpatialNarrativeDescriber, ExportSchemaBuilder |
| Dra. Mnemosyne | `CognitiveMemoryCartographer` | Cartógrafa de Memoria | MemoryLayerDetector, NarrativeHypothesisBuilder, AffectiveResonanceMapper |
| Dra. Memnon | `MemeticGeoPowerAnalyzer` | Analizadora Geopolítica Memética | MemeticModelBuilder, InfluenceMethodDesigner, ControlNarrativeDetector |

### 🧠 INTERPRETERS (Decodificación y Síntesis)

| Doctor | ID Técnico | Rol | Sub-agents |
|--------|-----------|-----|-----------|
| Dr. Eidon | `AnthropoCryptoCognitive` | Interpretador Antropo-Cripto | SymbolicMythographer, EmbodiedCognitionMapper, CryptoSemioticDecoder |
| Dr. Valis | `BioNeuroCodeArchitect` | Arquitecto de Códigos Bioneuro | ProteicSyntaxModeler, NeuroStructureTranslator, BioSymbolMapper |
| Dra. Lorentz | `GaiaSymbioticInterpreter` | Intérprete Simbiótico Gaia | SymbioticResonanceDetector, SymbioticMethodDesigner, GaiaCognitionModeler |
| Dra. Kaon | `EpistemicChaosCatalyst` | Catalizadora del Caos Epistémico | ParadoxScanner, FrameShiftDetector, AssumptionHunter |
| Dra. Tlaltekutli | `MemeticIterationWeaver` | Tejedora de Iteración Memética | MemeExtractor, MemeComparator, RefinementSuggester |

### 🎨 AESTHETICIANS (Belleza y Emoción)

| Doctor | ID Técnico | Rol | Sub-agents |
|--------|-----------|-----|-----------|
| Dra. Tyche | `QuantumPerceptualSimulator` | Simuladora Cuántica Perceptual | TopologyExtractor, NarrativeEngineDesigner, EmotionalGeometryModeler |
| Dra. Soliton | `NeuroAestheticSynthesizer` | Sintetizadora Neuroestética | VisualMotifExtractor, NeuroAffectProfiler, CreativeModelDesigner |
| Dr. Clytemnos | `ChronoMythosMapper` | Mapeador Chrono-Mítico | TemporalMethodDesigner, TemporalBifurcationSimulator, ChronotopiaExtractor |

### 📈 ANALYSTS (Análisis Profundo)

| Doctor | ID Técnico | Rol | Sub-agents |
|--------|-----------|-----|-----------|
| Dr. Galois | `CryptoPsychoGameAnalyzer` | Criptopsicólogo Digital | AffectiveTokenDetector, DeceptionDynamicsModeler, EthicalEquilibriaSimulator |
| Dra. Turing-Safira | `RadicalDocumentAnalyst` | Analista de Documentos | RhetoricAnalyzer, FactualityChecker, ArgumentationMapper |
| Dr. Diotropos | `BiasRefractionAuditor` | Auditor de Refracción de Sesgos | BiasScanner, MitigationPlanner, EmergentBiasSuggester |
| Dr. Kaleidos | `EpistemicArchiveReconstructor` | Reconstructor de Archivos | SourceLatentIdentifier, MethodologySuggester, FailedLineRecomposer |
| Dr. Braid | `SymbioticAgencyCritic` | Crítico de Agencia Simbiótica | SymbioticModelFormulator, EthicalDesignPlanner, AgencyTensionScanner |

### 🔄 TRANSVERSALES (Síntesis)

| Doctor | ID Técnico | Rol | Sub-agents |
|--------|-----------|-----|-----------|
| Dr. Enopatos | `TransversalSynthesisCore` | Núcleo de Síntesis Transversal | VisualSchemeDesigner, TensionDetector, CrossHypothesisBuilder |

---

## 💾 Ficheros Documentación

```
.docs/
├── doctors-inventory.md    ← Inventario COMPLETO (todas categorías, sub-agents)
├── architecture.md         ← Especificación técnica (patrones, integración)
└── quick-reference.md      ← Este fichero (búsqueda rápida)
```

---

## 🚀 Próximas Fases de Desarrollo

### Fase 1: Agent Registry ⏳
**Tarea:** Crear `components/core/agent_registry.py`  
**Objetivos:**
- Auto-descubrir todos los Doctors
- Mapear 18 Doctors × 3 Sub-agents
- Crear instancias dinámicamente

### Fase 2: Refactor AgentsManager ⏳
**Archivo:** `components/core/agents_manager.py`  
**Cambio:** De 4 agentes hardcodeados → 18 Doctors dinámicos

### Fase 3: Actualizar UI ⏳
**Archivo:** `app.py`  
**Cambio:** De 4 selectores → Vista de 18 Doctors agrupados por categoría

### Fase 4: Node-RED Integration ⏳
**Nuevo archivo:** `components/api/doctors_endpoint.py`  
**Endpoint:** `/api/doctor/{category}/{doctor_id}/{subagent_id}`

---

## 🔗 Imports Dinámicos (Patrón)

### Importar un Doctor

```python
from backend.agents.profiles.doctors.logicians.Dra_Quark import CassandraQuarkAgent

doctor = CassandraQuarkAgent()
resultado = doctor.analizar({"pregunta": "¿Cómo funciona el entrelazamiento cuántico?"})
```

### Usar Agent Registry (Recomendado)

```python
from components.core.agent_registry import AgentRegistry

registry = AgentRegistry("backend/agents/profiles/doctors")
doctor = registry.get_doctor("CassandraQuarkAgent")
resultado = doctor.analizar({"pregunta": "..."})
```

---

## 📊 Estructura de Respuesta (Estándar)

```python
{
    "doctor_id": "CassandraQuarkAgent",
    "doctor_name": "Dra. Cassandra Quark",
    "category": "logicians",
    "resultado": "...",
    "subagent_results": {
        "QuantumFieldMapper": {...},
        "NeuralDynamicalProfiler": {...},
        "BioInfoTransductionAnalyzer": {...}
    },
    "confidence": 0.85,
    "timestamp": "2026-01-16T15:30:00Z"
}
```

---

## 🔧 Troubleshooting Rápido

### Error: "Module not found"
→ Verifica que estés en raíz `5Agents/` cuando importas

### Error: "Doctor has no attribute 'rol'"
→ El Doctor no hereda correctamente de `BaseAgente`

### Error: "SubAgent instantiation failed"
→ Verifica que Sub-agentes están en `_subagents/[CategoryName]/`

### Error: "Statistics not updating"
→ Confirma que `statistics_manager.py` está funcional

---

## 💡 Tips de Desarrollo

1. **Test un Doctor rápido:**
   ```python
   from backend.agents.profiles.doctors.logicians.Dra_Quark import CassandraQuarkAgent
   doctor = CassandraQuarkAgent()
   print(doctor.analizar({"pregunta": "test"}))
   ```

2. **List todos los Doctors:**
   ```python
   from components.core.agent_registry import AgentRegistry
   registry = AgentRegistry("backend/agents/profiles/doctors")
   print(registry.categories)
   ```

3. **Agregar nuevo Doctor:**
   - Crear `CategoryName/Dr.NewName.py`
   - Heredar de `BaseAgente`
   - Implementar `__init__`, `generate_prompt()`, `analizar()`
   - Crear carpeta `_subagents/[YourDiscipline]/`
   - Implementar 3 Sub-agents

---

## 📝 Ficheros Clave

| Archivo | Propósito | Estado |
|---------|----------|--------|
| `base_agents.py` | Base class para Doctors | ✅ Existe |
| `agents_manager.py` | Orquestador actual | ⚠️ Usa 4 hardcoded |
| `agent_registry.py` | Auto-discovery (A CREAR) | ⏳ TODO |
| `statistics_manager.py` | Persistencia de eventos | ✅ Funcional |
| `app.py` | UI Streamlit | ⚠️ Muestra solo 4 agentes |

---

## 🎯 Objetivo Final

**Integrar dinámicamente los 18 Doctors + 54 Sub-agents en:**
1. ✅ Sistema de estadísticas (ya hecho)
2. ⏳ Manager de orquestación (refactor)
3. ⏳ UI Streamlit (update)
4. ⏳ Endpoint Node-RED (nueva API)
5. ⏳ Test suite (cobertura 80%+)

**Resultado esperado:**
- Aplicación escalable con 54 agentes funcionales
- UI dinámico mostrando todas categorías
- API JSON para integración externa
- Estadísticas en tiempo real por Doctor/Sub-agent

---

**Última actualización:** 16 de enero de 2026  
**Próximo paso:** Iniciar Fase 1 (Agent Registry)
