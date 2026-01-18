# Tests - 5Agents

Este directorio contiene tests para el sistema multi-agente.

## 📋 Estructura de Tests

```
tests/
├── conftest.py                      # Configuración global y fixtures
├── test_agent_activator.py         # Tests del sistema de activación
├── test_synthesis_engine.py        # Tests del motor de síntesis
├── test_conversation_controller.py # Tests del controlador principal
└── test_ollama_client.py           # Tests de integración con Ollama
```

## 🚀 Ejecutar Tests

### Instalar dependencias de testing

```bash
pip install pytest pytest-cov
```

### Ejecutar todos los tests

```bash
# Desde el directorio raíz del proyecto
pytest tests/ -v
```

### Ejecutar tests específicos

```bash
# Un archivo específico
pytest tests/test_agent_activator.py -v

# Una clase específica
pytest tests/test_agent_activator.py::TestDetectorTemasPlanos -v

# Un test específico
pytest tests/test_agent_activator.py::TestDetectorTemasPlanos::test_analizar_conversacion_basica -v
```

### Ejecutar solo tests que NO requieren Ollama

```bash
pytest tests/ -v -m "not skipif"
```

### Ejecutar tests con cobertura

```bash
pytest tests/ --cov=components --cov-report=html
```

## ⚠️ Tests que Requieren Ollama

Algunos tests están marcados con `@pytest.mark.skipif(True, reason="Requiere Ollama...")` porque necesitan Ollama en ejecución:

- `test_ollama_client.py` - Casi todos los tests
- `test_conversation_controller.py::test_process_con_ollama`
- `test_conversation_controller.py::test_flujo_completo_*`

### Para ejecutar estos tests

1. **Instalar Ollama:**

   ```bash
   # Windows
   winget install Ollama.Ollama
   
   # O descargar desde: https://ollama.com/download
   ```

2. **Descargar un modelo:**

   ```bash
   ollama pull mistral
   # o
   ollama pull llama2
   ```

3. **Verificar que Ollama está corriendo:**

   ```bash
   ollama --version
   ollama list  # Ver modelos instalados
   ```

4. **Cambiar los tests a ejecutables:**
   En los archivos de test, cambiar:

   ```python
   @pytest.mark.skipif(True, reason="...")
   ```

   Por:

   ```python
   @pytest.mark.skipif(False, reason="...")
   ```

5. **Ejecutar:**

   ```bash
   pytest tests/test_ollama_client.py -v
   pytest tests/test_conversation_controller.py::test_process_con_ollama -v
   ```

## 🎯 Filosofía de Testing

### ❌ NO hacemos

- Mockear APIs externas inventadas
- Hardcodear respuestas esperadas
- Usar datos ficticios que no reflejan el uso real

### ✅ SÍ hacemos

- Tests que fallan si el sistema no funciona
- Verificar comportamiento real de los componentes
- Usar fixtures para datos de prueba realistas
- Separar tests que requieren servicios externos (Ollama)

## 📊 Cobertura Esperada

Los tests cubren:

- **DetectorTemasPlanos**: Detección de temas, planos, capas, complejidad
- **SistemaActivacionAgentes**: Scoring y activación de agentes
- **MotorSintesis**: Síntesis, convergencias, tensiones, hipótesis
- **ConversationController**: Flujo completo end-to-end
- **OllamaClient**: Integración real con Ollama

## 🐛 Debugging Tests

Si un test falla:

1. **Leer el error completo:**

   ```bash
   pytest tests/test_agent_activator.py::test_nombre -v -s
   # -s muestra prints
   ```

2. **Usar pytest con debugging:**

   ```bash
   pytest tests/test_agent_activator.py::test_nombre --pdb
   # Entra en debugger cuando falla
   ```

3. **Ver más detalles:**

   ```bash
   pytest tests/ -vv --tb=long
   ```

## 📝 Añadir Nuevos Tests

Template básico:

```python
def test_nueva_funcionalidad():
    """Test que verifica X comportamiento."""
    # Arrange
    componente = MiComponente()
    
    # Act
    resultado = componente.hacer_algo()
    
    # Assert
    assert resultado is not None
    assert isinstance(resultado, TipoEsperado)
```

Para tests que requieren Ollama:

```python
@pytest.mark.skipif(True, reason="Requiere Ollama en ejecución")
def test_con_ollama():
    client = OllamaClient()
    
    if not client.is_available():
        pytest.skip("Ollama no está disponible")
    
    # ... test code ...
```

## 🔧 Configuración Avanzada

Editar `conftest.py` para añadir:

- Fixtures globales
- Hooks de pytest
- Configuración de markers
- Setup/teardown de tests

---

**Última actualización:** 15 de enero de 2026
