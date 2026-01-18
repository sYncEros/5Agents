"""
Tests para el sistema de activación automática de agentes.
"""
import pytest
from components.core.agent_activator import (
    DetectorTemasPlanos,
    SistemaActivacionAgentes,
    ContextoActivacion
)


class TestDetectorTemasPlanos:
    """Tests para DetectorTemasPlanos."""
    
    def test_analizar_conversacion_basica(self):
        """Test análisis básico de una conversación simple."""
        detector = DetectorTemasPlanos()
        texto = "¿Puede la física cuántica explicar la consciencia humana?"
        
        contexto = detector.analizar_conversacion(texto)
        
        assert isinstance(contexto, ContextoActivacion)
        assert "fisica_cuantica" in contexto.temas or "consciencia" in contexto.temas
        assert contexto.complejidad >= 1
        assert contexto.complejidad <= 5
    
    def test_detectar_temas_tecnologicos(self):
        """Test detección de temas técnicos."""
        detector = DetectorTemasPlanos()
        texto = "Necesito implementar un algoritmo de machine learning usando redes neuronales"
        
        contexto = detector.analizar_conversacion(texto)
        
        assert "tecnologia" in contexto.temas or "ia" in contexto.temas
        assert len(contexto.temas) > 0
    
    def test_detectar_multiples_temas(self):
        """Test detección de múltiples temas simultáneos."""
        detector = DetectorTemasPlanos()
        texto = """
        El universo es un sistema complejo donde la computación cuántica
        podría revelar patrones en la consciencia humana.
        """
        
        contexto = detector.analizar_conversacion(texto)
        
        # Debe detectar varios temas
        assert len(contexto.temas) >= 2
        assert contexto.complejidad >= 3  # Alta complejidad por múltiples temas
    
    def test_detectar_planos_conceptuales(self):
        """Test detección de planos conceptuales."""
        detector = DetectorTemasPlanos()
        
        # Plano técnico
        texto_tecnico = "Necesito diseñar e implementar una arquitectura de microservicios"
        contexto = detector.analizar_conversacion(texto_tecnico)
        assert "tecnico" in contexto.planos
        
        # Plano simbólico
        texto_simbolico = "Este símbolo representa la metáfora de la transformación"
        contexto = detector.analizar_conversacion(texto_simbolico)
        assert "simbolico" in contexto.planos or "metaforico" in contexto.planos
    
    def test_detectar_contradicciones(self):
        """Test detección de contradicciones en el texto."""
        detector = DetectorTemasPlanos()
        texto = "Por un lado la IA es útil, pero por otro lado genera preocupaciones éticas"
        
        contexto = detector.analizar_conversacion(texto)
        
        assert len(contexto.contradicciones) > 0
    
    def test_detectar_preguntas_explicitas(self):
        """Test detección de preguntas explícitas."""
        detector = DetectorTemasPlanos()
        texto = "¿Cómo funciona esto? ¿Por qué es importante?"
        
        contexto = detector.analizar_conversacion(texto)
        
        assert len(contexto.preguntas_implicitas) > 0
    
    def test_integracion_con_layer_detector(self):
        """Test que verifica integración con layer_detector."""
        detector = DetectorTemasPlanos()
        texto = "Me siento ansioso por estos límites éticos en IA"
        
        contexto = detector.analizar_conversacion(texto)
        
        # Debe detectar capas (puede ser proyectiva, emocional, o critica según layer_detector)
        assert len(contexto.capas) > 0
        # Verificar que layer_detector está funcionando
        assert isinstance(contexto.capas, list)
    
    def test_calculo_complejidad(self):
        """Test cálculo de complejidad."""
        detector = DetectorTemasPlanos()
        
        # Texto simple
        texto_simple = "Hola, ¿cómo estás?"
        contexto_simple = detector.analizar_conversacion(texto_simple)
        
        # Texto complejo
        texto_complejo = """
        La epistemología cuántica en sistemas complejos plantea interrogantes
        sobre la naturaleza del conocimiento, mientras que el mito de la caverna
        nos recuerda los límites de la percepción humana en un universo fractal.
        """
        contexto_complejo = detector.analizar_conversacion(texto_complejo)
        
        # El texto complejo debe tener mayor complejidad
        assert contexto_complejo.complejidad >= contexto_simple.complejidad


class TestSistemaActivacionAgentes:
    """Tests para SistemaActivacionAgentes."""
    
    def test_activacion_basica(self):
        """Test activación básica de agentes."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.3)
        
        # Crear contexto de prueba
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "consciencia"],
            planos=["tecnico"],
            capas=["metacognitiva"],
            complejidad=4
        )
        
        agentes = activator.determinar_agentes_activos(contexto, max_agentes=3)
        
        assert isinstance(agentes, list)
        assert len(agentes) > 0
        assert len(agentes) <= 3
    
    def test_activar_cassandra_quark(self):
        """Test que Cassandra Quark se activa con temas científicos."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.2)
        
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "sistemas_complejos"],
            planos=["tecnico", "sistemico"],
            capas=["metacognitiva"],
            complejidad=5
        )
        
        agentes = activator.determinar_agentes_activos(contexto, max_agentes=5)
        
        # Cassandra debe estar en los agentes activados
        assert "cassandra_quark" in agentes
    
    def test_activar_valis(self):
        """Test que Valis se activa con temas míticos."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.2)
        
        contexto = ContextoActivacion(
            temas=["mitologia", "humanidad"],
            planos=["simbolico", "historico"],
            capas=["mistica"],
            complejidad=4
        )
        
        agentes = activator.determinar_agentes_activos(contexto, max_agentes=5)
        
        assert "valis" in agentes
    
    def test_activar_logos(self):
        """Test que Logos se activa con temas técnicos."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.2)
        
        contexto = ContextoActivacion(
            temas=["tecnologia", "computacion"],
            planos=["tecnico"],
            capas=["cognitiva"],
            complejidad=3
        )
        
        agentes = activator.determinar_agentes_activos(contexto, max_agentes=5)
        
        assert "logos" in agentes
    
    def test_activar_experimentalist(self):
        """Test que Experimentalist se activa con hipótesis experimentales."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.2)
        
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "consciencia"],
            planos=["tecnico", "sistemico"],
            capas=["cognitiva", "critica"],
            complejidad=4
        )
        
        agentes = activator.determinar_agentes_activos(contexto, max_agentes=6)
        
        assert "experimentalist" in agentes
    
    def test_agente_por_defecto(self):
        """Test que se activa agente por defecto si ninguno califica."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.9)  # Umbral muy alto
        
        contexto = ContextoActivacion(
            temas=[],
            planos=[],
            capas=[],
            complejidad=1
        )
        
        agentes = activator.determinar_agentes_activos(contexto)
        
        # Debe retornar al menos el agente por defecto
        assert len(agentes) > 0
        assert "logos" in agentes
    
    def test_limite_max_agentes(self):
        """Test que respeta el límite de agentes máximos."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.1)  # Umbral bajo
        
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "mitologia", "tecnologia", "humanidad"],
            planos=["tecnico", "simbolico", "historico"],
            capas=["metacognitiva", "mistica", "critica"],
            complejidad=5
        )
        
        agentes = activator.determinar_agentes_activos(contexto, max_agentes=2)
        
        assert len(agentes) <= 2
    
    def test_scoring_coherente(self):
        """Test que el scoring es coherente."""
        activator = SistemaActivacionAgentes(umbral_activacion=0.1)
        
        # Contexto muy afín a Cassandra
        contexto_cassandra = ContextoActivacion(
            temas=["fisica_cuantica", "consciencia", "sistemas_complejos"],
            planos=["tecnico", "sistemico"],
            capas=["metacognitiva", "critica"],
            complejidad=5
        )
        
        # Contexto muy afín a Valis
        contexto_valis = ContextoActivacion(
            temas=["mitologia", "humanidad", "filosofia"],
            planos=["simbolico", "historico", "metaforico"],
            capas=["mistica"],
            complejidad=4
        )
        
        agentes_cassandra = activator.determinar_agentes_activos(contexto_cassandra, max_agentes=1)
        agentes_valis = activator.determinar_agentes_activos(contexto_valis, max_agentes=1)
        
        # Cada contexto debe activar su agente más afín
        assert agentes_cassandra[0] == "cassandra_quark"
        assert agentes_valis[0] == "valis"


class TestIntegracionCompleta:
    """Tests de integración entre DetectorTemasPlanos y SistemaActivacionAgentes."""
    
    def test_flujo_completo_cientifico(self):
        """Test flujo completo con input científico."""
        detector = DetectorTemasPlanos()
        activator = SistemaActivacionAgentes()
        
        texto = "¿Cómo afecta el entrelazamiento cuántico a nuestra comprensión de la consciencia?"
        
        contexto = detector.analizar_conversacion(texto)
        agentes = activator.determinar_agentes_activos(contexto)
        
        assert len(agentes) > 0
        assert "cassandra_quark" in agentes or "multiverse_sim" in agentes
    
    def test_flujo_completo_tecnico(self):
        """Test flujo completo con input técnico."""
        detector = DetectorTemasPlanos()
        activator = SistemaActivacionAgentes()
        
        texto = "Necesito diseñar una arquitectura de microservicios con machine learning"
        
        contexto = detector.analizar_conversacion(texto)
        agentes = activator.determinar_agentes_activos(contexto)
        
        assert len(agentes) > 0
        assert "logos" in agentes
    
    def test_flujo_completo_filosofico(self):
        """Test flujo completo con input filosófico."""
        detector = DetectorTemasPlanos()
        activator = SistemaActivacionAgentes()
        
        texto = "Los mitos antiguos revelan arquetipos universales sobre la naturaleza humana"
        
        contexto = detector.analizar_conversacion(texto)
        agentes = activator.determinar_agentes_activos(contexto)
        
        assert len(agentes) > 0
        assert "valis" in agentes or "mnemosyne" in agentes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
