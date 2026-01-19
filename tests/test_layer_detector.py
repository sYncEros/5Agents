"""
Tests mínimos para layer_detector (antes palimpsestos.py).
"""
import pytest
from backend.core.layer_detector import analyze_text


class TestLayerDetector:
    """Tests para el detector de capas."""
    
    def test_analyze_text_basico(self):
        """Test análisis básico de texto."""
        texto = "Me siento ansioso por los límites éticos de la IA"
        
        resultado = analyze_text(texto)
        
        # analyze_text retorna una dataclass AnalysisResult
        assert resultado is not None
        assert hasattr(resultado, "layers")
        assert isinstance(resultado.layers, list)
    
    def test_detectar_capa_emocional(self):
        """Test detección de capa emocional."""
        texto = "Me siento muy triste y ansioso por esto"
        
        resultado = analyze_text(texto)
        
        # Debe detectar capa emocional
        assert "emocional" in [c.lower() for c in resultado.layers]
    
    def test_detectar_capa_critica(self):
        """Test detección de capa crítica/ética."""
        texto = "Esto es injusto y plantea problemas éticos profundos"
        
        resultado = analyze_text(texto)
        
        assert "critica" in [c.lower() for c in resultado.layers] or \
               "ética" in str(resultado).lower()
    
    def test_detectar_capa_metacognitiva(self):
        """Test detección de capa metacognitiva."""
        texto = "Pienso que pensar sobre pensar revela límites cognitivos"
        
        resultado = analyze_text(texto)
        
        # Debe detectar metacognición
        assert len(resultado.layers) > 0
    
    def test_texto_vacio(self):
        """Test con texto vacío."""
        resultado = analyze_text("")
        
        # No debe fallar, debe retornar estructura válida
        assert resultado is not None
        assert hasattr(resultado, "layers")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
