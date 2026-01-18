"""
Configuración global de pytest para el proyecto 5Agents.
"""
import pytest
import sys
from pathlib import Path

# Añadir el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


def pytest_configure(config):
    """Configuración inicial de pytest."""
    config.addinivalue_line(
        "markers", 
        "skipif: marca tests que requieren condiciones específicas (Ollama, etc.)"
    )
    config.addinivalue_line(
        "markers",
        "integration: marca tests de integración que requieren servicios externos"
    )


@pytest.fixture(scope="session")
def ollama_disponible():
    """Fixture que verifica si Ollama está disponible."""
    from components.llm.ollama_client import OllamaClient
    
    client = OllamaClient()
    return client.is_available()


@pytest.fixture
def sample_input_cientifico():
    """Fixture con input de prueba científico."""
    return "¿Cómo se relaciona la física cuántica con la consciencia?"


@pytest.fixture
def sample_input_tecnico():
    """Fixture con input de prueba técnico."""
    return "Diseña una arquitectura de microservicios con contenedores Docker"


@pytest.fixture
def sample_input_filosofico():
    """Fixture con input de prueba filosófico."""
    return "Los mitos antiguos revelan arquetipos universales sobre la condición humana"


@pytest.fixture
def sample_contexto():
    """Fixture con contexto de prueba."""
    from components.core.agent_activator import ContextoActivacion
    
    return ContextoActivacion(
        temas=["fisica_cuantica", "consciencia"],
        planos=["tecnico", "simbolico"],
        capas=["metacognitiva"],
        complejidad=4
    )


@pytest.fixture
def sample_respuestas():
    """Fixture con respuestas de prueba."""
    return {
        "cassandra_quark": "La física cuántica sugiere superposición de estados.",
        "valis": "Los mitos hablan de dualidades fundamentales.",
        "logos": "Técnicamente, esto requiere algoritmos complejos."
    }
