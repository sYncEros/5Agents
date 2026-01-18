"""
Agent_Segmentador - Divide texto por actos, temas, turnos
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any, List
from dataclasses import dataclass, field
from datetime import datetime
from .base_agents import AgentProfile, BaseAgent


@dataclass
class Segmento:
    """Representación de un segmento de texto."""
    id: str
    contenido: str
    tipo: str  # "acto", "tema", "turno"
    tema: str = ""
    emocion: str = ""
    speaker: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadatos: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "contenido": self.contenido,
            "tipo": self.tipo,
            "tema": self.tema,
            "emocion": self.emocion,
            "speaker": self.speaker,
            "timestamp": self.timestamp,
            "metadatos": self.metadatos
        }


class SegmentadorAgent(BaseAgent):
    """
    Pipeline de segmentación por NLP: 
    - sentence/paragraph boundary detection
    - topic modeling (LDA/embeddings)
    - rules-based
    
    OUTPUT: array de segmentos con metadatos (tema, emoción, speaker)
    """
    
    profile = AgentProfile(
        nombre="Segmentador",
        rol="Análisis de estructura textual",
        prompt_base="""Eres un experto en análisis de estructura textual.
Tu tarea es segmentar el texto en unidades significativas:
- Por actos/párrafos narrativos
- Por cambios de tema
- Por turnos de conversación

Para cada segmento, identifica:
- Tipo: acto, tema, turno
- Tema principal
- Emoción dominante
- Speaker (si aplicable)
""",
        modelo_llm="mistral",
        temperatura=0.5,
        tags=["segmentación", "análisis", "estructura"],
        capabilities=["sentence_detection", "topic_modeling", "speaker_identification"]
    )
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
        self.segmentos: List[Segmento] = []
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa el texto y retorna resumen de segmentación."""
        self.segmentos = self._segmentar(input_text, context or {})
        return f"Segmentación completada: {len(self.segmentos)} segmentos identificados"
    
    def _segmentar(self, texto: str, contexto: dict) -> List[Segmento]:
        """
        Ejecuta segmentación:
        1. Boundary detection (párrafos/oraciones)
        2. Topic modeling
        3. Speaker extraction si aplica
        """
        segmentos = []
        
        # Boundary detection simple (por párrafos)
        parrafos = texto.split('\n\n')
        
        for i, parrafo in enumerate(parrafos):
            if not parrafo.strip():
                continue
            
            # Crear segmento
            seg = Segmento(
                id=f"seg_{i}",
                contenido=parrafo.strip(),
                tipo="parrafo",
                tema=self._extraer_tema(parrafo, contexto),
                emocion=contexto.get("emocion_dominante", "neutral"),
                speaker=contexto.get("speaker", ""),
                metadatos={
                    "longitud": len(parrafo),
                    "lineas": len(parrafo.split('\n')),
                    "posicion": i
                }
            )
            segmentos.append(seg)
        
        return segmentos
    
    def _extraer_tema(self, texto: str, contexto: dict) -> str:
        """Extrae tema principal (keywords/topic modeling)."""
        # Implementación heurística: palabras clave del contexto
        keywords = contexto.get("keywords", [])
        palabras = texto.lower().split()
        
        for kw in keywords:
            if kw.lower() in palabras:
                return kw
        
        # Default: primera palabra significativa
        return palabras[0] if palabras else "sin_tema"
    
    def get_segmentos(self) -> List[dict]:
        """Retorna array de segmentos procesados."""
        return [seg.to_dict() for seg in self.segmentos]
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis de segmentación."""
        self.segmentos = self._segmentar(input_text, {})
        return {
            "agent": self.profile.nombre,
            "total_segmentos": len(self.segmentos),
            "segmentos": [seg.to_dict() for seg in self.segmentos]
        }
