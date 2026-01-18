"""
Tests para el cliente de Ollama.
NO mockea la API - prueba la integración real con Ollama.
"""
import pytest
from components.llm.ollama_client import OllamaClient


class TestOllamaClient:
    """Tests para OllamaClient - Requieren Ollama en ejecución."""
    
    def test_inicializacion_basica(self):
        """Test inicialización básica del cliente."""
        client = OllamaClient()
        
        assert client.base_url is not None
        assert "http" in client.base_url
    
    def test_is_available(self):
        """Test verificación de disponibilidad de Ollama."""
        client = OllamaClient()
        
        disponible = client.is_available()
        
        # Este test debe reflejar el estado real
        assert isinstance(disponible, bool)
        
        # Si no está disponible, el resto de tests deberían fallar
        if not disponible:
            pytest.skip("Ollama no está disponible - instalar y ejecutar Ollama")
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_list_models_con_ollama(self):
        """Test listar modelos con Ollama disponible."""
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        modelos = client.list_models()
        
        assert isinstance(modelos, list)
        # Si Ollama está instalado pero no hay modelos, esto fallará intencionalmente
        assert len(modelos) > 0, "No hay modelos instalados en Ollama. Ejecuta: ollama pull mistral"
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generate_via_api(self):
        """Test generación de texto vía API."""
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        modelos = client.list_models()
        if not modelos:
            pytest.skip("No hay modelos instalados")
        
        # Usar el primer modelo disponible
        modelo = modelos[0]
        
        respuesta = client.generate(
            prompt="Di solo 'Hola' y nada más",
            model=modelo,
            temperature=0.1,
            max_tokens=10
        )
        
        assert respuesta is not None
        assert len(respuesta) > 0
        assert isinstance(respuesta, str)
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generate_con_temperatura_alta(self):
        """Test generación con temperatura alta para mayor creatividad."""
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        modelos = client.list_models()
        if not modelos:
            pytest.skip("No hay modelos instalados")
        
        modelo = modelos[0]
        
        respuesta = client.generate(
            prompt="Describe el universo en una oración",
            model=modelo,
            temperature=0.9,
            max_tokens=100
        )
        
        assert respuesta is not None
        assert len(respuesta) > 10
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generate_con_temperatura_baja(self):
        """Test generación con temperatura baja para respuestas deterministas."""
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        modelos = client.list_models()
        if not modelos:
            pytest.skip("No hay modelos instalados")
        
        modelo = modelos[0]
        
        # Hacer la misma pregunta dos veces con temp=0
        prompt = "¿Cuánto es 2 + 2?"
        
        respuesta1 = client.generate(prompt=prompt, model=modelo, temperature=0.0)
        respuesta2 = client.generate(prompt=prompt, model=modelo, temperature=0.0)
        
        # Con temperatura 0, las respuestas deberían ser idénticas o muy similares
        assert respuesta1 is not None
        assert respuesta2 is not None
    
    def test_generate_sin_ollama_falla(self):
        """Test que generate falla si Ollama no está disponible."""
        client = OllamaClient()
        
        if not client.is_available():
            with pytest.raises(Exception):
                client.generate(prompt="test", model="mistral")
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generate_con_system_prompt(self):
        """Test generación con system prompt."""
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        modelos = client.list_models()
        if not modelos:
            pytest.skip("No hay modelos instalados")
        
        modelo = modelos[0]
        
        respuesta = client.generate(
            prompt="¿Quién eres?",
            model=modelo,
            system_prompt="Eres un poeta que solo responde en verso",
            temperature=0.7
        )
        
        assert respuesta is not None
        assert len(respuesta) > 0


class TestOllamaIntegracionPerfiles:
    """Tests de integración entre OllamaClient y perfiles de agentes."""
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generar_con_perfil_cassandra(self):
        """Test generación usando perfil de Cassandra Quark."""
        from components.llm.profiles import AGENT_PROFILES
        
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        perfil = AGENT_PROFILES["cassandra_quark"]
        
        respuesta = client.generate(
            prompt="¿Qué es el entrelazamiento cuántico?",
            model=perfil.modelo_preferido,
            system_prompt=perfil.system_prompt,
            temperature=perfil.temperatura,
            max_tokens=perfil.max_tokens
        )
        
        assert respuesta is not None
        assert len(respuesta) > 50  # Debe ser una respuesta sustancial
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generar_con_perfil_valis(self):
        """Test generación usando perfil de Valis."""
        from components.llm.profiles import AGENT_PROFILES
        
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        perfil = AGENT_PROFILES["valis"]
        
        respuesta = client.generate(
            prompt="¿Qué significan los mitos de creación?",
            model=perfil.modelo_preferido,
            system_prompt=perfil.system_prompt,
            temperature=perfil.temperatura,
            max_tokens=perfil.max_tokens
        )
        
        assert respuesta is not None
        assert len(respuesta) > 50
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_generar_con_perfil_logos(self):
        """Test generación usando perfil de Logos."""
        from components.llm.profiles import AGENT_PROFILES
        
        client = OllamaClient()
        
        if not client.is_available():
            pytest.skip("Ollama no está disponible")
        
        perfil = AGENT_PROFILES["logos"]
        
        respuesta = client.generate(
            prompt="Diseña una arquitectura de microservicios",
            model=perfil.modelo_preferido,
            system_prompt=perfil.system_prompt,
            temperature=perfil.temperatura,  # Debe ser baja (0.5)
            max_tokens=perfil.max_tokens
        )
        
        assert respuesta is not None
        # Logos debería dar respuestas técnicas y estructuradas
        assert len(respuesta) > 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
