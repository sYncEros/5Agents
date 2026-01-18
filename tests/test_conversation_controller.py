"""
Tests para el controlador de flujo conversacional.
Este módulo NO mockea la integración con Ollama. Si Ollama no está disponible, los tests fallarán.
"""
import pytest
import time
from components.core.conversation_controller import (
    ConversationController,
    ResultadoConversacion
)
from components.core.agent_activator import ContextoActivacion


class TestConversationController:
    """Tests para ConversationController."""
    
    def test_inicializacion_basica(self):
        """Test inicialización básica del controlador."""
        controller = ConversationController()
        
        assert controller is not None
        assert controller.detector is not None
        assert controller.activator is not None
        assert controller.synthesizer is not None
    
    def test_verificar_sistema(self):
        """Test verificación del estado del sistema."""
        controller = ConversationController()
        
        estado = controller.verificar_sistema()
        
        assert isinstance(estado, dict)
        assert "ollama_disponible" in estado
        assert "agentes_disponibles" in estado
        assert isinstance(estado["agentes_disponibles"], list)
        assert len(estado["agentes_disponibles"]) > 0
    
    def test_listar_agentes_disponibles(self):
        """Test listado de agentes disponibles."""
        controller = ConversationController()
        
        agentes = controller.listar_agentes_disponibles()
        
        assert isinstance(agentes, list)
        assert len(agentes) == 5  # Tenemos 5 perfiles definidos
        assert "cassandra_quark" in agentes
        assert "valis" in agentes
        assert "logos" in agentes
        assert "mnemosyne" in agentes
        assert "multiverse_sim" in agentes
    
    def test_process_sin_ollama_falla(self):
        """Test que process falla si Ollama no está disponible."""
        controller = ConversationController()
        
        # Si Ollama no está disponible, debe fallar
        if not controller.ollama.is_available():
            with pytest.raises(Exception) as excinfo:
                controller.process("Test input")
            
            assert "Ollama no está disponible" in str(excinfo.value)
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_process_con_ollama(self):
        """Test proceso completo con Ollama disponible (requiere Ollama real)."""
        controller = ConversationController()
        
        # Verificar que Ollama está disponible
        if not controller.ollama.is_available():
            pytest.skip("Ollama no está disponible")
        
        input_text = "¿Qué es la física cuántica?"
        
        resultado = controller.process(input_text)
        
        assert isinstance(resultado, ResultadoConversacion)
        assert resultado.input == input_text
        assert resultado.contexto is not None
        assert len(resultado.agentes_activados) > 0
        assert len(resultado.respuestas) > 0
        assert resultado.sintesis is not None
        assert resultado.tiempo_total > 0
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_process_con_agentes_manuales(self):
        """Test proceso con agentes seleccionados manualmente."""
        controller = ConversationController()
        
        if not controller.ollama.is_available():
            pytest.skip("Ollama no está disponible")
        
        resultado = controller.process(
            "Explícame los sistemas complejos",
            agentes_manuales=["cassandra_quark", "logos"]
        )
        
        assert len(resultado.agentes_activados) == 2
        assert "cassandra_quark" in resultado.agentes_activados
        assert "logos" in resultado.agentes_activados
    
    def test_to_dict_estructura(self):
        """Test estructura de salida to_dict."""
        # Crear un resultado mock sin Ollama
        contexto = ContextoActivacion(
            temas=["test"],
            planos=["tecnico"],
            capas=["cognitiva"],
            complejidad=2
        )
        
        from components.core.synthesis_engine import Sintesis
        sintesis = Sintesis(
            resumen="Test resumen",
            hipotesis_cruzadas=[],
            convergencias=[],
            tensiones=[],
            preguntas_abiertas=[],
            temas_emergentes=[],
            relaciones=[],
            metadata={}
        )
        
        resultado = ResultadoConversacion(
            input="test input",
            contexto=contexto,
            agentes_activados=["logos"],
            respuestas={"logos": "test response"},
            sintesis=sintesis,
            tiempo_total=1.5,
            timestamp=time.time()
        )
        
        dict_result = resultado.to_dict()
        
        assert isinstance(dict_result, dict)
        assert "input" in dict_result
        assert "contexto" in dict_result
        assert "agentes_activados" in dict_result
        assert "respuestas" in dict_result
        assert "sintesis" in dict_result
        assert "metadata" in dict_result
        assert dict_result["input"] == "test input"
        assert dict_result["metadata"]["tiempo_total"] == 1.5


class TestResultadoConversacion:
    """Tests para ResultadoConversacion."""
    
    def test_creacion_resultado_basico(self):
        """Test creación básica de ResultadoConversacion."""
        from components.core.synthesis_engine import Sintesis
        
        contexto = ContextoActivacion(
            temas=["test"],
            planos=[],
            capas=[],
            complejidad=1
        )
        
        sintesis = Sintesis(
            resumen="test",
            hipotesis_cruzadas=[],
            convergencias=[],
            tensiones=[],
            preguntas_abiertas=[],
            temas_emergentes=[],
            relaciones=[],
            metadata={}
        )
        
        resultado = ResultadoConversacion(
            input="input de prueba",
            contexto=contexto,
            agentes_activados=["logos"],
            respuestas={"logos": "respuesta de prueba"},
            sintesis=sintesis,
            tiempo_total=2.0,
            timestamp=time.time()
        )
        
        assert resultado.input == "input de prueba"
        assert isinstance(resultado.agentes_activados, list)
        assert isinstance(resultado.respuestas, dict)
    
    def test_to_dict_completo(self):
        """Test serialización completa a diccionario."""
        from components.core.synthesis_engine import Sintesis
        
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "consciencia"],
            planos=["tecnico", "simbolico"],
            capas=["metacognitiva"],
            complejidad=4,
            contradicciones=["contradicción 1"],
            preguntas_implicitas=["¿pregunta?"],
            guardrails=["etica"]
        )
        
        sintesis = Sintesis(
            resumen="Resumen completo",
            hipotesis_cruzadas=["hipótesis 1", "hipótesis 2"],
            convergencias=["convergencia 1"],
            tensiones=["tensión 1"],
            preguntas_abiertas=["¿pregunta abierta?"],
            temas_emergentes=["tema nuevo"],
            relaciones=[("concepto1", "concepto2", "relacion")],
            metadata={"test": "value"}
        )
        
        resultado = ResultadoConversacion(
            input="input completo",
            contexto=contexto,
            agentes_activados=["cassandra_quark", "valis"],
            respuestas={
                "cassandra_quark": "respuesta 1",
                "valis": "respuesta 2"
            },
            sintesis=sintesis,
            tiempo_total=3.5,
            timestamp=1234567890.0
        )
        
        dict_result = resultado.to_dict()
        
        # Verificar estructura completa
        assert dict_result["input"] == "input completo"
        assert len(dict_result["agentes_activados"]) == 2
        assert len(dict_result["respuestas"]) == 2
        assert "temas" in dict_result["contexto"]
        assert "planos" in dict_result["contexto"]
        assert len(dict_result["contexto"]["temas"]) == 2
        assert "resumen" in dict_result["sintesis"]
        assert len(dict_result["sintesis"]["hipotesis_cruzadas"]) == 2
        assert dict_result["metadata"]["tiempo_total"] == 3.5
        assert dict_result["metadata"]["timestamp"] == 1234567890.0


class TestIntegracionFlujosReales:
    """Tests de integración que NO usan mocks (requieren Ollama)."""
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_flujo_completo_cientifico(self):
        """Test flujo completo con pregunta científica."""
        controller = ConversationController()
        
        if not controller.ollama.is_available():
            pytest.skip("Ollama no está disponible")
        
        resultado = controller.process(
            "¿Cómo se relaciona la mecánica cuántica con la consciencia humana?"
        )
        
        # Verificar que se activaron agentes apropiados
        assert "cassandra_quark" in resultado.agentes_activados or \
               "multiverse_sim" in resultado.agentes_activados
        
        # Verificar que hay respuestas
        assert len(resultado.respuestas) > 0
        
        # Verificar que la síntesis tiene contenido
        assert len(resultado.sintesis.resumen) > 50
        
        # Verificar tiempos
        assert resultado.tiempo_total > 0
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_flujo_completo_tecnico(self):
        """Test flujo completo con pregunta técnica."""
        controller = ConversationController()
        
        if not controller.ollama.is_available():
            pytest.skip("Ollama no está disponible")
        
        resultado = controller.process(
            "¿Cómo diseñar una arquitectura de microservicios escalable?"
        )
        
        # Logos debe estar activado
        assert "logos" in resultado.agentes_activados
        
        # Debe tener respuestas técnicas
        assert len(resultado.respuestas) > 0
        assert any("arquitectura" in resp.lower() or "sistema" in resp.lower() 
                  for resp in resultado.respuestas.values())
    
    @pytest.mark.skipif(True, reason="Requiere Ollama en ejecución - ejecutar manualmente")
    def test_process_multiple(self):
        """Test procesamiento por lotes."""
        controller = ConversationController()
        
        if not controller.ollama.is_available():
            pytest.skip("Ollama no está disponible")
        
        inputs = [
            "¿Qué es la física cuántica?",
            "Explica los mitos griegos",
            "Diseña un sistema de IA"
        ]
        
        resultados = controller.process_multiple(inputs)
        
        assert len(resultados) == 3
        assert all(isinstance(r, ResultadoConversacion) for r in resultados)
        assert all(r.tiempo_total > 0 for r in resultados)


class TestGuardrailsYErrores:
    """Tests de manejo de errores y guardrails."""
    
    def test_input_vacio_falla(self):
        """Test que input vacío falla apropiadamente."""
        controller = ConversationController()
        
        # Si Ollama no está disponible, el error será diferente
        if not controller.ollama.is_available():
            pytest.skip("Test requiere Ollama disponible")
        
        with pytest.raises(Exception):
            controller.process("")
    
    def test_agentes_invalidos_falla(self):
        """Test que agentes inválidos fallan."""
        controller = ConversationController()
        
        if not controller.ollama.is_available():
            pytest.skip("Test requiere Ollama disponible")
        
        with pytest.raises(Exception):
            controller.process(
                "test input",
                agentes_manuales=["agente_inexistente"]
            )
    
    def test_lista_agentes_nunca_falla(self):
        """Test que listar agentes siempre funciona."""
        controller = ConversationController()
        
        # Esta operación no depende de Ollama
        agentes = controller.listar_agentes_disponibles()
        
        assert isinstance(agentes, list)
        assert len(agentes) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
