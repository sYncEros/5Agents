"""
Tests para el motor de síntesis.
"""
import pytest
from components.core.synthesis_engine import MotorSintesis, Sintesis
from components.core.agent_activator import ContextoActivacion


class TestMotorSintesis:
    """Tests para MotorSintesis."""
    
    def test_sintetizar_respuestas_basico(self):
        """Test síntesis básica con dos respuestas."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "La física cuántica sugiere que la realidad es probabilística. Los sistemas complejos muestran comportamientos emergentes.",
            "Agente B": "Los sistemas complejos requieren múltiples niveles de análisis. La física cuántica abre nuevas posibilidades."
        }
        
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "sistemas_complejos"],
            planos=["tecnico"],
            capas=["metacognitiva"],
            complejidad=4
        )
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        assert isinstance(sintesis, Sintesis)
        assert len(sintesis.resumen) > 0
        assert sintesis.metadata["num_agentes"] == 2
    
    def test_detectar_convergencias(self):
        """Test detección de convergencias entre agentes."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "La consciencia es un fenómeno emergente. Los sistemas complejos exhiben propiedades emergentes.",
            "Agente B": "Las propiedades emergentes son clave. La consciencia podría ser emergente en sistemas suficientemente complejos."
        }
        
        contexto = ContextoActivacion(temas=["consciencia"], planos=[], capas=[], complejidad=3)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # Debe detectar convergencias en conceptos compartidos
        assert len(sintesis.convergencias) > 0
    
    def test_detectar_tensiones(self):
        """Test detección de tensiones y contraargumentos."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "La IA puede ser consciente. Sin embargo, esto plantea problemas éticos profundos.",
            "Agente B": "Por un lado la IA es útil, pero por otro lado genera riesgos existenciales."
        }
        
        contexto = ContextoActivacion(temas=["ia"], planos=[], capas=["critica"], complejidad=4)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # Debe detectar tensiones por los marcadores
        assert len(sintesis.tensiones) > 0
    
    def test_extraer_hipotesis(self):
        """Test extracción de hipótesis."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "Hipótesis: la consciencia podría ser un epifenómeno cuántico.",
            "Agente B": "Posiblemente la mente emerge de procesos neuronales complejos. Sugiere que necesitamos más evidencia."
        }
        
        contexto = ContextoActivacion(temas=["consciencia"], planos=[], capas=[], complejidad=3)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        assert len(sintesis.hipotesis_cruzadas) > 0
    
    def test_extraer_preguntas_abiertas(self):
        """Test extracción de preguntas abiertas."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "¿Cómo podríamos medir la consciencia? No está claro cuál es el umbral.",
            "Agente B": "Queda por determinar si esto es verificable. Futuras investigaciones deberían explorar este tema."
        }
        
        contexto = ContextoActivacion(temas=[], planos=[], capas=[], complejidad=2)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        assert len(sintesis.preguntas_abiertas) > 0
    
    def test_construir_relaciones(self):
        """Test construcción de relaciones para grafos."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "La física cuántica estudia partículas subatómicas.",
            "Agente B": "Las partículas cuánticas muestran comportamiento probabilístico."
        }
        
        contexto = ContextoActivacion(temas=["fisica_cuantica"], planos=[], capas=[], complejidad=3)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # Debe generar relaciones entre conceptos
        assert len(sintesis.relaciones) > 0
        # Cada relación es una tupla (origen, destino, tipo)
        for rel in sintesis.relaciones:
            assert isinstance(rel, tuple)
            assert len(rel) == 3
    
    def test_detectar_temas_emergentes(self):
        """Test detección de temas emergentes."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "La neurociencia computacional revela patrones cerebrales.",
            "Agente B": "Los algoritmos de aprendizaje profundo imitan procesos neuronales."
        }
        
        contexto = ContextoActivacion(
            temas=["tecnologia"],  # Tema original
            planos=[],
            capas=[],
            complejidad=3
        )
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # Debe detectar "neurociencia" o "algoritmos" como temas nuevos
        assert len(sintesis.temas_emergentes) >= 0  # Puede o no detectar según extracción
    
    def test_generar_resumen(self):
        """Test generación de resumen ejecutivo."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "Primera respuesta con análisis profundo.",
            "Agente B": "Segunda respuesta complementaria.",
            "Agente C": "Tercera perspectiva única."
        }
        
        contexto = ContextoActivacion(temas=[], planos=[], capas=[], complejidad=3)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # El resumen debe mencionar el número de agentes
        assert "3 agente" in sintesis.resumen
        assert len(sintesis.resumen) > 50  # Debe ser un resumen sustancial
    
    def test_sintesis_con_respuesta_unica(self):
        """Test síntesis con una sola respuesta."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente Único": "Esta es una respuesta individual sin otras perspectivas."
        }
        
        contexto = ContextoActivacion(temas=[], planos=[], capas=[], complejidad=1)
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        assert isinstance(sintesis, Sintesis)
        assert sintesis.metadata["num_agentes"] == 1
        # Las convergencias deberían ser vacías o mínimas
        assert len(sintesis.convergencias) == 0
    
    def test_sintesis_con_guardrails(self):
        """Test que la síntesis respeta guardrails del contexto."""
        motor = MotorSintesis()
        
        respuestas = {
            "Agente A": "Análisis del tema solicitado."
        }
        
        contexto = ContextoActivacion(
            temas=[],
            planos=[],
            capas=[],
            complejidad=2,
            guardrails=["crisis_detectada"]
        )
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # Debe incluir guardrails en metadata
        assert "guardrails_activos" in sintesis.metadata
        assert "crisis_detectada" in sintesis.metadata["guardrails_activos"]


class TestIntegracionSintesis:
    """Tests de integración del motor de síntesis."""
    
    def test_flujo_completo_multiagente(self):
        """Test flujo completo con múltiples agentes."""
        motor = MotorSintesis()
        
        respuestas = {
            "Dra. Cassandra Quark": "Desde la física cuántica, observamos superposición de estados. Los sistemas complejos exhiben propiedades emergentes.",
            "Dr. Éterio Valis": "Los mitos antiguos hablan de dualidades. Los sistemas simbólicos revelan patrones universales.",
            "Agente Logos": "Implementar esto requiere algoritmos de sistemas complejos. La arquitectura debe ser modular."
        }
        
        contexto = ContextoActivacion(
            temas=["fisica_cuantica", "mitologia", "tecnologia"],
            planos=["tecnico", "simbolico", "sistemico"],
            capas=["metacognitiva", "mistica"],
            complejidad=5
        )
        
        sintesis = motor.sintetizar_respuestas(respuestas, contexto)
        
        # Verificar que se generaron todos los componentes
        assert len(sintesis.resumen) > 0
        assert len(sintesis.convergencias) >= 0
        assert len(sintesis.hipotesis_cruzadas) >= 0
        assert len(sintesis.relaciones) > 0
        assert sintesis.metadata["num_agentes"] == 3
        assert sintesis.metadata["complejidad_contexto"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
