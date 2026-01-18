"""
Agent_Emoción - Análisis de emociones y detección de trauma
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from .base_agents import AgentProfile, BaseAgent


class Valencia(Enum):
    """Valencia emocional."""
    NEGATIVA = "negativa"
    NEUTRAL = "neutral"
    POSITIVA = "positiva"


class Arousal(Enum):
    """Nivel de activación."""
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"


@dataclass
class AnalisisEmocion:
    """Resultado de análisis emocional."""
    texto: str
    valencia: Valencia
    arousal: Arousal
    dominance: float  # 0-1: de sumisión a dominancia
    emocion_primaria: str
    emociones_secundarias: list[str] = field(default_factory=list)
    cues_trauma: list[str] = field(default_factory=list)
    confianza: float = 0.0
    requiere_escalado: bool = False
    recurso_recomendado: str = ""
    
    def to_dict(self) -> dict:
        return {
            "valencia": self.valencia.value,
            "arousal": self.arousal.value,
            "dominance": self.dominance,
            "emocion_primaria": self.emocion_primaria,
            "emociones_secundarias": self.emociones_secundarias,
            "cues_trauma": self.cues_trauma,
            "confianza": self.confianza,
            "requiere_escalado": self.requiere_escalado,
            "recurso": self.recurso_recomendado
        }


class EmociónAgent(BaseAgent):
    """
    Análisis de emociones: valencia/arousal/dominance.
    
    Detecta: cues de trauma, embeddings con KNN para similitud.
    
    USO: clasificación, escalado a humanos si es necesario.
    """
    
    profile = AgentProfile(
        nombre="Emoción",
        rol="Análisis emocional y detección de crisis",
        prompt_base="""Eres un especialista en análisis emocional.
Analiza el texto para:
1. Valencia: negativa / neutral / positiva
2. Arousal: bajo / medio / alto
3. Dominance: sumisión (0) → dominancia (1)
4. Emoción primaria: identifica la principal
5. Emociones secundarias: lista otras presentes
6. Cues de trauma: indicadores de experiencias traumáticas
7. Nivel de riesgo: requiere escalado a humanos?

ESPECIAL ATENCIÓN A:
- Ideación suicida → ESCALADO INMEDIATO
- Abuso / trauma → recursos terapéuticos
- Crisis → pathways a profesionales
""",
        modelo_llm="mistral",
        temperatura=0.7,
        tags=["emociones", "trauma", "crisis"],
        capabilities=["emotion_detection", "crisis_detection", "trauma_cues"]
    )
    
    # Diccionarios de palabras clave
    PALABRAS_CLAVE_EMOCIONES = {
        "alegría": ["feliz", "contento", "alegre", "dicha", "risa"],
        "tristeza": ["triste", "deprimido", "melancolía", "llanto", "dolor"],
        "miedo": ["miedo", "terror", "pánico", "ansiedad", "angustia"],
        "ira": ["furioso", "enojado", "rabia", "cólera", "resentimiento"],
        "asco": ["asco", "repugnancia", "rechazo", "náusea"],
        "sorpresa": ["sorpresa", "asombro", "impactado", "shock"],
    }
    
    CUES_TRAUMA = [
        "trigger", "flashback", "pesadilla", "trauma", "abuso", "violencia",
        "muerte", "perdida", "pánico", "inseguro", "solo", "abandonado"
    ]
    
    INDICADORES_CRISIS = [
        "suicida", "suicidio", "matarme", "acabar con", "ya no puedo",
        "no hay salida", "sin esperanza", "todo es inútil"
    ]
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y retorna emoción dominante."""
        resultado = self.analizar_emociones(input_text)
        if resultado.requiere_escalado:
            return f"⚠️ ESCALADO REQUERIDO: {resultado.emocion_primaria} - {resultado.recurso_recomendado}"
        return f"Emoción: {resultado.emocion_primaria} (valencia: {resultado.valencia.value})"
    
    def analizar_emociones(self, texto: str) -> AnalisisEmocion:
        """
        Análisis emocional multidimensional.
        """
        texto_lower = texto.lower()
        
        # Detectar crisis PRIMERO
        for indicador in self.INDICADORES_CRISIS:
            if indicador in texto_lower:
                return AnalisisEmocion(
                    texto=texto,
                    valencia=Valencia.NEGATIVA,
                    arousal=Arousal.ALTO,
                    dominance=0.1,
                    emocion_primaria="crisis",
                    emociones_secundarias=["depresión", "desesperación"],
                    cues_trauma=["ideación_suicida"],
                    confianza=0.95,
                    requiere_escalado=True,
                    recurso_recomendado="Línea de crisis / Profesional de salud mental"
                )
        
        # Detectar emociones primarias
        emocion_detectada = None
        max_coincidencias = 0
        
        for emocion, palabras_clave in self.PALABRAS_CLAVE_EMOCIONES.items():
            coincidencias = sum(1 for palabra in palabras_clave if palabra in texto_lower)
            if coincidencias > max_coincidencias:
                max_coincidencias = coincidencias
                emocion_detectada = emocion
        
        # Detectar cues de trauma
        cues_detectados = [cue for cue in self.CUES_TRAUMA if cue in texto_lower]
        requiere_escalado = len(cues_detectados) > 0 or emocion_detectada == "tristeza"
        
        # Calcular dimensiones
        valencia = self._calcular_valencia(emocion_detectada or "neutral")
        arousal = self._calcular_arousal(texto_lower, len(cues_detectados))
        
        return AnalisisEmocion(
            texto=texto,
            valencia=valencia,
            arousal=arousal,
            dominance=self._calcular_dominance(emocion_detectada or "neutral"),
            emocion_primaria=emocion_detectada or "neutral",
            emociones_secundarias=[e for e in self.PALABRAS_CLAVE_EMOCIONES.keys() 
                                   if e != emocion_detectada and any(p in texto_lower for p in self.PALABRAS_CLAVE_EMOCIONES[e])],
            cues_trauma=cues_detectados,
            confianza=min(max_coincidencias / 3, 1.0) if max_coincidencias > 0 else 0.3,
            requiere_escalado=requiere_escalado,
            recurso_recomendado="Recursos de apoyo emocional / Profesional" if requiere_escalado else ""
        )
    
    def _calcular_valencia(self, emocion: str) -> Valencia:
        """Valencia basada en emoción."""
        positivas = ["alegría"]
        negativas = ["tristeza", "miedo", "ira", "asco"]
        
        if emocion in positivas:
            return Valencia.POSITIVA
        elif emocion in negativas:
            return Valencia.NEGATIVA
        return Valencia.NEUTRAL
    
    def _calcular_arousal(self, texto: str, trauma_cues: int) -> Arousal:
        """Arousal basado en longitud y cues."""
        if trauma_cues > 2 or len(texto) > 500:
            return Arousal.ALTO
        elif trauma_cues > 0:
            return Arousal.MEDIO
        return Arousal.BAJO
    
    def _calcular_dominance(self, emocion: str) -> float:
        """Dominance 0-1."""
        dominantes = {"ira": 0.8, "alegría": 0.7}
        sumisas = {"miedo": 0.2, "tristeza": 0.3}
        return dominantes.get(emocion, sumisas.get(emocion, 0.5))
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis emocional completo."""
        resultado = self.analizar_emociones(input_text)
        return {
            "agent": self.profile.nombre,
            "analisis": resultado.to_dict()
        }
