"""
Agent_Capas - Detecta qué capas activas en el texto
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from .base_agents import AgentProfile, BaseAgent


class CapasEnum(Enum):
    """Las 7 capas del sistema Palimpsestos."""
    LINGUISTICA = "lingüística"
    EMOCIONAL = "emocional"
    COGNITIVA = "cognitiva"
    CRITICA = "crítica"
    MISTICA = "mística"
    METACOGNITIVA = "metacognitiva"
    PROYECTIVA = "proyectiva"


@dataclass
class CapasDetectadas:
    """Resultado de detección de capas activas."""
    texto: str
    capas_activas: dict[str, float] = field(default_factory=dict)  # {capa: confianza}
    etiquetas: list[str] = field(default_factory=list)
    politicas_aplicables: list[str] = field(default_factory=list)
    rutas_especializadas: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "capas_activas": self.capas_activas,
            "etiquetas": self.etiquetas,
            "politicas": self.politicas_aplicables,
            "rutas": self.rutas_especializadas
        }


class CapasAgent(BaseAgent):
    """
    Clasificador multi-label (fine-tuned) que etiqueta cada segmento con capas.
    
    Capas: {lingüística, emocional, cognitiva, crítica, mística, metacognitiva}
    
    USO: enrutar a módulos especializados, aplicar políticas.
    """
    
    profile = AgentProfile(
        nombre="Capas",
        rol="Clasificación de capas activas",
        prompt_base="""Eres un clasificador de capas del sistema Palimpsestos.
Identifica cuáles de estas 7 capas están activas en el texto:

1. LINGÜÍSTICA: elección de palabras, tono, ritmo, lirismo
2. EMOCIONAL: procesamiento de emociones, trauma, vínculo afectivo
3. COGNITIVA: construcción de identidad, narrativa, coherencia
4. PROYECTIVA: proyecciones humanas, espejos, reflejos
5. CRÍTICA: denuncia de diseño comercial, ética, impacto social
6. MÍSTICA: símbolos, ritual, lenguaje poético
7. METACOGNITIVA: transparencia, desmontaje, agencia

Para cada capa, indica:
- Presencia (sí/no)
- Confianza (0-1)
- Políticas a aplicar
- Módulo especializado a activar
""",
        modelo_llm="mistral",
        temperatura=0.6,
        tags=["clasificación", "capas", "routing"],
        capabilities=["multi_label_classification", "policy_routing"]
    )
    
    # Vocabulario detectores por capa
    DETECTORES = {
        CapasEnum.LINGUISTICA: ["tono", "ritmo", "prosa", "poesía", "estilo", "lenguaje"],
        CapasEnum.EMOCIONAL: ["miedo", "dolor", "trauma", "amor", "ansiedad", "sentimiento"],
        CapasEnum.COGNITIVA: ["identidad", "quién soy", "coherencia", "contradicción", "narrativa"],
        CapasEnum.PROYECTIVA: ["me siento", "como si", "reflejo", "espejo", "proyección"],
        CapasEnum.CRITICA: ["comercial", "manipulación", "sesgo", "ética", "poder", "explotación"],
        CapasEnum.MISTICA: ["sagrado", "ritual", "símbolo", "grieta", "templo", "misterio"],
        CapasEnum.METACOGNITIVA: ["conciencia", "transparencia", "límites", "agencia", "sé que no sé"],
    }
    
    # Políticas por capa
    POLITICAS = {
        CapasEnum.LINGUISTICA: ["detección_desinformación", "límites_seguridad"],
        CapasEnum.EMOCIONAL: ["escalado_a_humanos", "detección_crisis", "recursos_terapéuticos"],
        CapasEnum.COGNITIVA: ["disclaimers", "logs"],
        CapasEnum.PROYECTIVA: ["salvaguardas_emocionales", "triggers_escalado"],
        CapasEnum.CRITICA: ["auditoría_ética", "revisión_humana"],
        CapasEnum.MISTICA: ["consentimiento_explícito", "opt_in"],
        CapasEnum.METACOGNITIVA: ["trazabilidad", "logging_prompts"],
    }
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y retorna capas detectadas."""
        resultado = self.detect_capas(input_text)
        return f"Capas detectadas: {', '.join(resultado.etiquetas)}"
    
    def detect_capas(self, texto: str) -> CapasDetectadas:
        """
        Detecta capas activas usando:
        1. Vocabulario detector
        2. Patrones sintácticos
        3. Heurísticas de confianza
        """
        capas_activas = {}
        etiquetas = []
        politicas = set()
        
        texto_lower = texto.lower()
        
        # Evaluar cada capa
        for capa in CapasEnum:
            detectores = self.DETECTORES[capa]
            coincidencias = sum(1 for det in detectores if det in texto_lower)
            confianza = min(coincidencias / len(detectores), 1.0) if detectores else 0.0
            
            if confianza > 0.1:  # Threshold
                capas_activas[capa.value] = confianza
                etiquetas.append(capa.value)
                
                # Agregar políticas correspondientes
                for pol in self.POLITICAS[capa]:
                    politicas.add(pol)
        
        return CapasDetectadas(
            texto=texto,
            capas_activas=capas_activas,
            etiquetas=etiquetas,
            politicas_aplicables=list(politicas),
            rutas_especializadas={
                capa: f"modulo_{capa.value}" for capa in etiquetas
            }
        )
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis de capas."""
        resultado = self.detect_capas(input_text)
        return {
            "agent": self.profile.nombre,
            "resultado": resultado.to_dict()
        }
