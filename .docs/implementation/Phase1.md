# Plan de Integración: Agent Registry - Fase 1

**Documento:** Implementación detallada paso a paso  
**Fecha:** 16 de enero de 2026  
**Estado:** ✅ LISTO PARA CODIFICAR

---

## 🎯 Objetivo Fase 1

Crear `components/core/agent_registry.py` que:

1. Auto-descubre los 18 Doctors en `backend/agents/profiles/doctors/`
2. Mapea sus 3 Sub-agentes cada uno
3. Permite acceso dinámico sin hardcoding

---

## 📋 Tareas Específicas

### TAREA 1: Crear archivo agent_registry.py

**Ubicación:** `components/core/agent_registry.py`

```python
import importlib.util
import inspect
import os
from pathlib import Path
from typing import Dict, Type, Any, Optional, List


class AgentRegistry:
    """
    Registry dinámico de Doctors y Sub-agentes.
    Auto-descubre todos los Doctors en la estructura de directorios.
    """
    
    def __init__(self, doctors_root: str):
        """
        Inicializa el registry.
        
        Args:
            doctors_root: Ruta a backend/agents/profiles/doctors/
        
        Ejemplo:
            registry = AgentRegistry("backend/agents/profiles/doctors")
        """
        self.doctors_root = Path(doctors_root)
        self.doctors: Dict[str, Type] = {}  # {"CassandraQuarkAgent": <class>}
        self.categories: Dict[str, List[str]] = {}  # {"logicians": ["CassandraQuarkAgent", ...]}
        self.subagents_by_doctor: Dict[str, List[str]] = {}  # {"CassandraQuarkAgent": ["QuantumFieldMapper", ...]}
        
        # Auto-descubre
        self._discover_doctors()
    
    def _discover_doctors(self) -> None:
        """
        Auto-descubre todos los Doctors en estructura de directorios.
        
        Estructura esperada:
        backend/agents/profiles/doctors/
        ├── logicians/
        │   ├── Dra.Quark.py
        │   ├── Dra.Monad.py
        │   └── Dra.Moebius.py
        ├── cartographers/
        │   ├── Dra.Veld.py
        │   ...
        """
        if not self.doctors_root.exists():
            raise FileNotFoundError(f"Doctors root not found: {self.doctors_root}")
        
        # Itera sobre categorías (logicians, cartographers, etc.)
        for category_dir in self.doctors_root.iterdir():
            if not category_dir.is_dir():
                continue
            
            # Skip especiales
            if category_dir.name.startswith("_") or category_dir.name in ["fallback"]:
                continue
            
            category_name = category_dir.name
            self.categories[category_name] = []
            
            # Busca archivos Doctor: Dra.*.py, Dr.*.py
            doctor_files = list(category_dir.glob("Dra.*.py")) + list(category_dir.glob("Dr.*.py"))
            
            for doctor_file in doctor_files:
                try:
                    doctor_class = self._import_doctor(doctor_file)
                    if doctor_class:
                        class_name = doctor_class.__name__
                        self.doctors[class_name] = doctor_class
                        self.categories[category_name].append(class_name)
                        
                        # Obtén lista de sub-agentes
                        self._map_subagents(class_name, doctor_class)
                        
                except Exception as e:
                    print(f"⚠️ Error importando {doctor_file}: {e}")
    
    def _import_doctor(self, file_path: Path) -> Optional[Type]:
        """
        Importa dinámicamente un Doctor desde archivo .py.
        
        Args:
            file_path: Path al archivo .py del Doctor
        
        Returns:
            Clase del Doctor o None si falla
        """
        try:
            module_name = f"doctor_{file_path.stem}_{id(file_path)}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            
            if spec is None or spec.loader is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Busca clase que tenga atributos "rol" y "id" (signo de Doctor)
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    hasattr(obj, 'rol') and 
                    hasattr(obj, '__module__') and 
                    obj.__module__ == module.__name__):
                    return obj
            
            return None
        
        except Exception as e:
            print(f"❌ Error importing {file_path}: {e}")
            return None
    
    def _map_subagents(self, doctor_class_name: str, doctor_class: Type) -> None:
        """
        Mapea los 3 Sub-agentes del Doctor.
        
        Args:
            doctor_class_name: Nombre de la clase Doctor
            doctor_class: La clase misma
        """
        try:
            # Instancia temporal para obtener sub-agentes
            temp_doctor = doctor_class()
            subagent_names = [
                sa.__class__.__name__ for sa in temp_doctor.subagentes
            ]
            self.subagents_by_doctor[doctor_class_name] = subagent_names
        except Exception as e:
            print(f"⚠️ Could not map subagents for {doctor_class_name}: {e}")
            self.subagents_by_doctor[doctor_class_name] = []
    
    # ═══════════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════════
    
    def get_doctor(self, doctor_id: str) -> Any:
        """
        Instancia un Doctor por su ID técnico.
        
        Args:
            doctor_id: ID técnico del Doctor (ej: "CassandraQuarkAgent")
        
        Returns:
            Instancia del Doctor o None
        
        Ejemplo:
            doctor = registry.get_doctor("CassandraQuarkAgent")
            result = doctor.analizar("pregunta", {})
        """
        if doctor_id not in self.doctors:
            return None
        return self.doctors[doctor_id]()
    
    def get_all_doctors(self) -> Dict[str, Any]:
        """
        Retorna instancias de TODOS los Doctors.
        
        Returns:
            Dict: {doctor_class_name: doctor_instance}
        
        Ejemplo:
            all_doctors = registry.get_all_doctors()
            for name, doctor in all_doctors.items():
                print(f"{name}: {doctor.nombre}")
        """
        return {name: cls() for name, cls in self.doctors.items()}
    
    def get_doctors_by_category(self, category: str) -> Dict[str, Any]:
        """
        Retorna Doctors de una categoría específica.
        
        Args:
            category: Nombre categoría (ej: "logicians")
        
        Returns:
            Dict: {doctor_class_name: doctor_instance}
        
        Ejemplo:
            logicians = registry.get_doctors_by_category("logicians")
            # Returns: {"CassandraQuarkAgent": <doctor>, ...}
        """
        doctor_names = self.categories.get(category, [])
        return {name: self.doctors[name]() for name in doctor_names}
    
    def get_doctor_by_name(self, full_name: str) -> Optional[Any]:
        """
        Busca un Doctor por su nombre completo.
        
        Args:
            full_name: Nombre completo (ej: "Dra. Cassandra Quark")
        
        Returns:
            Instancia del Doctor o None
        """
        for doctor_class in self.doctors.values():
            temp = doctor_class()
            if temp.nombre == full_name:
                return temp
        return None
    
    def get_categories(self) -> Dict[str, List[str]]:
        """
        Retorna estructura de categorías.
        
        Returns:
            Dict: {"logicians": ["CassandraQuarkAgent", ...], ...}
        """
        return self.categories.copy()
    
    def get_subagents_for_doctor(self, doctor_id: str) -> List[str]:
        """
        Retorna lista de Sub-agentes para un Doctor.
        
        Args:
            doctor_id: ID técnico del Doctor
        
        Returns:
            List: ["SubAgent1", "SubAgent2", "SubAgent3"]
        """
        return self.subagents_by_doctor.get(doctor_id, [])
    
    def list_all_doctors(self) -> Dict[str, Dict]:
        """
        Retorna información completa de todos los Doctors.
        
        Returns:
            Dict con estructura:
            {
                "doctor_id": {
                    "nombre": "...",
                    "categoria": "...",
                    "rol": "...",
                    "subagentes": [...]
                },
                ...
            }
        """
        result = {}
        for doctor_id, doctor_class in self.doctors.items():
            temp = doctor_class()
            # Encuentra categoría
            category = None
            for cat, doctors in self.categories.items():
                if doctor_id in doctors:
                    category = cat
                    break
            
            result[doctor_id] = {
                "nombre": temp.nombre,
                "categoria": category,
                "rol": getattr(temp, "rol", "N/A"),
                "subagentes": self.get_subagents_for_doctor(doctor_id),
                "dominios": getattr(temp, "dominios", [])
            }
        
        return result
    
    def stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas del registry.
        
        Returns:
            Dict con conteos
        """
        total_doctors = len(self.doctors)
        total_subagents = sum(len(v) for v in self.subagents_by_doctor.values())
        
        return {
            "total_doctors": total_doctors,
            "total_subagents": total_subagents,
            "categories": len(self.categories),
            "categories_breakdown": {
                cat: len(doctors) for cat, doctors in self.categories.items()
            }
        }


# ═══════════════════════════════════════════════════════════
# UTILITY FUNCTION
# ═══════════════════════════════════════════════════════════

def create_registry(doctors_path: Optional[str] = None) -> AgentRegistry:
    """
    Factory function para crear un registry.
    
    Args:
        doctors_path: Path a doctors/ (default: auto-detect)
    
    Returns:
        AgentRegistry instance
    
    Ejemplo:
        registry = create_registry()  # Auto-detects path
        or
        registry = create_registry("backend/agents/profiles/doctors")
    """
    if doctors_path is None:
        # Auto-detect: asume que estamos corriendo desde raíz del proyecto
        import os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        doctors_path = os.path.join(base, "backend", "agents", "profiles", "doctors")
    
    return AgentRegistry(doctors_path)
```

---

### TAREA 2: Tests para Agent Registry

**Ubicación:** `tests/test_agent_registry.py`

```python
import pytest
from components.core.agent_registry import AgentRegistry, create_registry
import os


@pytest.fixture
def registry():
    """Fixture que proporciona un registry para tests."""
    doctors_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "backend",
        "agents",
        "profiles",
        "doctors"
    )
    return AgentRegistry(doctors_path)


class TestAgentRegistryDiscovery:
    """Tests para auto-discovery de Doctors."""
    
    def test_registry_discovers_all_doctors(self, registry):
        """Verifica que descubre los 18 Doctors."""
        assert len(registry.doctors) == 18, "Debe descubrir 18 Doctors"
    
    def test_registry_discovers_all_categories(self, registry):
        """Verifica categorías (6 total)."""
        assert len(registry.categories) == 6
        expected_categories = {
            "logicians", "cartographers", "interpreters",
            "aestheticians", "analysts", "transversales"
        }
        assert set(registry.categories.keys()) == expected_categories
    
    def test_category_counts(self, registry):
        """Verifica conteos por categoría."""
        assert len(registry.categories["logicians"]) == 3
        assert len(registry.categories["cartographers"]) == 3
        assert len(registry.categories["interpreters"]) == 5
        assert len(registry.categories["aestheticians"]) == 3
        assert len(registry.categories["analysts"]) == 5
        assert len(registry.categories["transversales"]) == 1
    
    def test_doctor_in_registry(self, registry):
        """Verifica que Dra.Quark está registrada."""
        assert "CassandraQuarkAgent" in registry.doctors


class TestAgentRegistryInstantiation:
    """Tests para instanciación de Doctors."""
    
    def test_get_doctor(self, registry):
        """Verifica que se puede obtener instancia de Doctor."""
        doctor = registry.get_doctor("CassandraQuarkAgent")
        assert doctor is not None
        assert doctor.nombre == "Dra. Cassandra Quark"
    
    def test_get_all_doctors(self, registry):
        """Verifica que obtiene todas las instancias."""
        all_doctors = registry.get_all_doctors()
        assert len(all_doctors) == 18
    
    def test_get_doctors_by_category(self, registry):
        """Verifica obtener Doctors por categoría."""
        logicians = registry.get_doctors_by_category("logicians")
        assert len(logicians) == 3


class TestSubagentMapping:
    """Tests para mapeo de Sub-agentes."""
    
    def test_quark_has_three_subagents(self, registry):
        """Verifica que Dra.Quark tiene 3 Sub-agentes."""
        subagents = registry.get_subagents_for_doctor("CassandraQuarkAgent")
        assert len(subagents) == 3
        assert "QuantumFieldMapper" in subagents
        assert "NeuralDynamicalProfiler" in subagents
        assert "BioInfoTransductionAnalyzer" in subagents
    
    def test_all_doctors_have_three_subagents(self, registry):
        """Verifica que TODOS los Doctors tienen 3 Sub-agentes."""
        for doctor_id, subagents in registry.subagents_by_doctor.items():
            assert len(subagents) == 3, f"{doctor_id} debe tener 3 Sub-agentes, tiene {len(subagents)}"


class TestRegistryAPI:
    """Tests para la API pública."""
    
    def test_list_all_doctors(self, registry):
        """Verifica que list_all_doctors retorna estructura correcta."""
        all_info = registry.list_all_doctors()
        assert len(all_info) == 18
        
        # Verifica estructura
        for doctor_id, info in all_info.items():
            assert "nombre" in info
            assert "categoria" in info
            assert "rol" in info
            assert "subagentes" in info
            assert len(info["subagentes"]) == 3
    
    def test_stats(self, registry):
        """Verifica estadísticas del registry."""
        stats = registry.stats()
        assert stats["total_doctors"] == 18
        assert stats["total_subagents"] == 54  # 18 × 3
        assert stats["categories"] == 6


class TestErrorHandling:
    """Tests para manejo de errores."""
    
    def test_get_nonexistent_doctor(self, registry):
        """Verifica que retorna None para Doctor inexistente."""
        result = registry.get_doctor("NonexistentAgent")
        assert result is None
    
    def test_get_nonexistent_category(self, registry):
        """Verifica que retorna lista vacía para categoría inexistente."""
        result = registry.get_doctors_by_category("nonexistent")
        assert result == {}


# ═══════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════

class TestDoctorFunctionality:
    """Tests que verifica que Doctors funcionan correctamente."""
    
    def test_doctor_analizar_method(self, registry):
        """Verifica que Doctor puede ejecutar analizar()."""
        doctor = registry.get_doctor("CassandraQuarkAgent")
        result = doctor.analizar("test question", {})
        
        assert result is not None
        assert "doctor" in result
        assert "titulo" in result
        assert "hallazgos_subagentes" in result
    
    def test_doctor_has_prompt_generation(self, registry):
        """Verifica que Doctor tiene generate_prompt()."""
        doctor = registry.get_doctor("CassandraQuarkAgent")
        prompt = doctor.generate_prompt("test question")
        
        assert prompt is not None
        assert "test question" in prompt
```

---

### TAREA 3: Integrar con AgentsManager

**Archivo actual:** `components/core/agents_manager.py`

**Cambios necesarios:**

```python
# ANTES (línea ~1-10):
AGENTS = {
    "científico": "🔬 Científico",
    "creativo": "🎨 Creativo",
    "filósofo": "🧠 Filósofo",
    "técnico": "💻 Técnico",
}

# DESPUÉS:
from components.core.agent_registry import AgentRegistry
import os

class AgentsManager:
    def __init__(self):
        # Inicializa registry dinámico
        doctors_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "backend",
            "agents",
            "profiles",
            "doctors"
        )
        self.registry = AgentRegistry(doctors_path)
        self.stats_manager = StatisticsManager()
    
    def process_idea(self, idea: str, doctor_id: str = None) -> Dict[str, Any]:
        """
        Procesa idea con un Doctor.
        
        Si no se especifica doctor_id, selecciona uno aleatorio.
        """
        if doctor_id is None:
            # Selecciona aleatorio
            import random
            all_doctors = self.registry.doctors
            doctor_id = random.choice(list(all_doctors.keys()))
        
        # Obtiene instancia del Doctor
        doctor = self.registry.get_doctor(doctor_id)
        if doctor is None:
            return {"error": f"Doctor {doctor_id} no encontrado"}
        
        # Ejecuta análisis
        try:
            resultado = doctor.analizar(
                texto=idea,
                contexto={"timestamp": datetime.now().isoformat()}
            )
        except Exception as e:
            resultado = {"error": str(e)}
        
        # Actualiza estadísticas
        self.stats_manager.increment_ideas_processed()
        self.stats_manager.add_event({
            "type": "doctor_analysis",
            "doctor_id": doctor_id,
            "doctor_name": doctor.nombre,
            "category": self._get_doctor_category(doctor_id),
            "input_length": len(idea),
            "subagents_called": len(doctor.subagentes),
            "success": "error" not in resultado
        })
        
        return resultado
    
    def _get_doctor_category(self, doctor_id: str) -> str:
        """Obtiene categoría de un Doctor."""
        for category, doctors in self.registry.categories.items():
            if doctor_id in doctors:
                return category
        return "unknown"
    
    def get_all_doctors_info(self) -> Dict:
        """Retorna información de todos los Doctors."""
        return self.registry.list_all_doctors()
```

---

### TAREA 4: Actualizar Streamlit (app.py)

**Cambios clave:**

```python
# ANTES:
agent_choice = st.sidebar.selectbox(
    "Selecciona agente",
    ["🔬 Científico", "🎨 Creativo", "🧠 Filósofo", "💻 Técnico"]
)

# DESPUÉS:
# Obtiene estructura de categorías desde registry
doctors_by_category = agents_manager.registry.get_categories()

selected_category = st.sidebar.selectbox(
    "Selecciona categoría",
    list(doctors_by_category.keys())
)

# Obtiene doctors de esa categoría
category_doctors = agents_manager.registry.get_doctors_by_category(selected_category)

selected_doctor_name = st.sidebar.selectbox(
    "Selecciona Doctor",
    [doctor.nombre for doctor in category_doctors.values()]
)

# Obtiene ID técnico del Doctor
doctor_id = None
for doc_id, doctor in category_doctors.items():
    if doctor.nombre == selected_doctor_name:
        doctor_id = doc_id
        break

# Procesa idea
if user_input and st.button("Analizar"):
    result = agents_manager.process_idea(user_input, doctor_id)
    st.json(result)
```

---

## 🧪 Testing Manual

### Paso 1: Crear archivo y ejecutar tests

```bash
# Terminal
cd 5Agents
python -m pytest tests/test_agent_registry.py -v
```

**Output esperado:**

```
tests/test_agent_registry.py::TestAgentRegistryDiscovery::test_registry_discovers_all_doctors PASSED
tests/test_agent_registry.py::TestAgentRegistryDiscovery::test_registry_discovers_all_categories PASSED
tests/test_agent_registry.py::TestAgentRegistryDiscovery::test_category_counts PASSED
...
18 passed in 2.45s
```

### Paso 2: Prueba interactiva

```python
# python shell
from components.core.agent_registry import AgentRegistry

registry = AgentRegistry("backend/agents/profiles/doctors")

# Test 1: Lista de categorías
print(registry.get_categories())
# Output: {'logicians': [...], 'cartographers': [...], ...}

# Test 2: Instancia un Doctor
doctor = registry.get_doctor("CassandraQuarkAgent")
print(f"Doctor: {doctor.nombre}")
# Output: Doctor: Dra. Cassandra Quark

# Test 3: Ejecuta análisis
result = doctor.analizar("¿Cómo surge la conciencia?", {})
print(result["titulo"])
# Output: Sincronías en el borde: del qubit al attractor cortical

# Test 4: Estadísticas
stats = registry.stats()
print(f"Total Doctors: {stats['total_doctors']}")
print(f"Total Sub-agents: {stats['total_subagents']}")
# Output: Total Doctors: 18, Total Sub-agents: 54
```

---

## ✅ Checklist de Implementación

- [ ] **PASO 1:** Crear `components/core/agent_registry.py` (código arriba)
- [ ] **PASO 2:** Crear `tests/test_agent_registry.py` (código arriba)
- [ ] **PASO 3:** Ejecutar tests: `pytest tests/test_agent_registry.py -v`
- [ ] **PASO 4:** Verificar que todos los tests pasan (18/18)
- [ ] **PASO 5:** Actualizar `components/core/agents_manager.py` (integrar registry)
- [ ] **PASO 6:** Actualizar `app.py` para usar categorías dinámicamente
- [ ] **PASO 7:** Test manual en Streamlit: `streamlit run app.py`
- [ ] **PASO 8:** Verificar que se muestren todos los 18 Doctors agrupados

---

## 📊 Resultado Final (Fase 1)

```
✅ 18 Doctors mapeados dinámicamente
✅ 54 Sub-agentes registrados
✅ 6 Categorías organizadas
✅ API pública lista
✅ Tests 100% passing
✅ AgentsManager refactorizado
✅ Streamlit con UI dinámica
```

---

**Documento completo:** 16 de enero de 2026  
**Status:** ✅ LISTO PARA IMPLEMENTAR
