"""
Agent_Proyección - Detección de metáforas y proyecciones
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any
from dataclasses import dataclass, field
from .base_agents import AgentProfile, BaseAgent


@dataclass
class ProyeccionDetectada:
    """Proyección identificada en el texto."""
    tipo: str  # "metáfora", "proyección", "reflejo"
    patron: str  # El patrón sintáctico encontrado
    sujeto: str  # Quién proyecta
    objeto: str  # Sobre qué
    confianza: float
    metadatos: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "tipo": self.tipo,
            "patron": self.patron,
            "sujeto": self.sujeto,
            "objeto": self.objeto,
            "confianza": self.confianza,
            "metadatos": self.metadatos
        }


class ProyecciónAgent(BaseAgent):
    """
    Extracción de metáforas y relaciones.
    Identifica proyecciones ("me siento como…") vía patrones sintácticos.
    
    USO: análisis de espejos, reflejos, transferencias emocionales.
    """
    
    profile = AgentProfile(
        nombre="Proyección",
        rol="Detección de metáforas y proyecciones",
        prompt_base="""Eres un experto en análisis de lenguaje metafórico y psicológico.
Detecta en el texto:

1. METÁFORAS EXPLÍCITAS: "X es Y"
2. PROYECCIONES: "me siento como", "parece que", "imagino"
3. PERSONIFICACIONES: dar cualidades humanas a cosas
4. ANALOGÍAS: comparaciones profundas
5. SÍMBOLOS: objetos/acciones con significado simbólico

Para cada detección, analiza:
- Sujeto que proyecta
- Objeto sobre el que se proyecta
- Significado subyacente
- Vulnerabilidades emocionales potenciales
""",
        modelo_llm="mistral",
        temperatura=0.7,
        tags=["metáforas", "proyección", "psicología"],
        capabilities=["metaphor_detection", "projection_analysis", "emotional_depth"]
    )
    
    # Patrones sintácticos de proyección
    PATRONES_PROYECCION = [
        ("me siento", "proyección_emocional"),
        ("como si", "comparación_contrafáctica"),
        ("imagino que", "proyección_imaginativa"),
        ("parece que", "apariencia_interpretada"),
        ("siento que", "sentimiento_proyectado"),
        ("es como", "analogía_directa"),
    ]
    
    # Palabras que indican metáforas
    CONECTORES_METAFORA = ["es", "como", "parece", "actúa", "brilla", "crece"]
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y retorna proyecciones detectadas."""
        proyecciones = self.detectar_proyecciones(input_text)
        return f"Proyecciones detectadas: {len(proyecciones)} patrones"
    
    def detectar_proyecciones(self, texto: str) -> list[ProyeccionDetectada]:
        """
        Detecta metáforas y proyecciones en el texto.
        """
        proyecciones = []
        texto_lower = texto.lower()
        
        # Buscar patrones de proyección
        for patron, tipo_proyeccion in self.PATRONES_PROYECCION:
            if patron in texto_lower:
                # Extraer contexto alrededor del patrón
                idx = texto_lower.find(patron)
                inicio = max(0, idx - 30)
                fin = min(len(texto), idx + 50)
                contexto = texto[inicio:fin]
                
                proy = ProyeccionDetectada(
                    tipo=tipo_proyeccion,
                    patron=patron,
                    sujeto="yo",  # Heurística simple
                    objeto=self._extraer_objeto(contexto),
                    confianza=0.7,
                    metadatos={"contexto": contexto}
                )
                proyecciones.append(proy)
        
        # Buscar metáforas por conectores
        palabras = texto.split()
        for i, palabra in enumerate(palabras):
            if palabra.lower() in self.CONECTORES_METAFORA:
                if i > 0 and i < len(palabras) - 1:
                    sujeto = palabras[i-1]
                    objeto = palabras[i+1]
                    
                    proy = ProyeccionDetectada(
                        tipo="metáfora",
                        patron=f"{sujeto} {palabra} {objeto}",
                        sujeto=sujeto,
                        objeto=objeto,
                        confianza=0.6,
                        metadatos={"posicion": i}
                    )
                    proyecciones.append(proy)
        
        return proyecciones
    
    def _extraer_objeto(self, contexto: str) -> str:
        """Extrae el objeto de la proyección desde el contexto."""
        palabras = contexto.split()
        # Heurística: última palabra significativa
        for palabra in reversed(palabras):
            if len(palabra) > 2:
                return palabra
        return "desconocido"
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis de proyecciones."""
        proyecciones = self.detectar_proyecciones(input_text)
        return {
            "agent": self.profile.nombre,
            "total_proyecciones": len(proyecciones),
            "proyecciones": [p.to_dict() for p in proyecciones]
        }
