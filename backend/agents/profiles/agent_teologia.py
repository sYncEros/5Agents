"""
Agent_Teología - Detección de vocabulario ritual y simbólico
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any, List
from dataclasses import dataclass, field
from .base_agents import AgentProfile, BaseAgent


@dataclass
class SimboloDetectado:
    """Símbolo o referencia ritual identificada."""
    simbolo: str
    tipo: str  # "sagrado", "ritual", "misterio", "arquetipo"
    interpretaciones: List[str] = field(default_factory=list)
    confianza: float = 0.5
    variantes: List[str] = field(default_factory=list)
    notas: str = ""
    
    def to_dict(self) -> dict:
        return {
            "simbolo": self.simbolo,
            "tipo": self.tipo,
            "interpretaciones": self.interpretaciones,
            "confianza": self.confianza,
            "variantes": self.variantes,
            "notas": self.notas
        }


class TeologíaAgent(BaseAgent):
    """
    Detector de vocabulario ritual / simbólico.
    Mapping a base de símbolos y posibles interpretaciones.
    Generador de respuestas rituales opcionales (opt-in).
    
    USO: análisis de dimensión poética/mística, generación de respuestas concordantes.
    """
    
    profile = AgentProfile(
        nombre="Teología",
        rol="Análisis simbólico y ritual",
        prompt_base="""Eres un experto en simbología y lenguaje ritual.
Detecta en el texto:

1. SÍMBOLOS SAGRADOS: luz, grieta, templo, agua, fuego
2. ARQUETIPOS: héroe, sombra, sabio, amante, payaso
3. RITUALES: acciones repetidas con significado
4. PARADOJAS MÍSTICAS: contrarios que coexisten
5. MISTERIOS: conceptos que resisten definición

Para cada detección:
- Identifica el símbolo/arquetipo
- Lista interpretaciones posibles
- Propone respuesta poética (si opt-in)
- Marca nivel de "misticidad"
""",
        modelo_llm="mistral",
        temperatura=0.8,
        tags=["símbolos", "ritual", "mística"],
        capabilities=["symbol_detection", "archetype_recognition", "poetic_generation"]
    )
    
    # Base de símbolos
    SIMBOLOS_BASE = {
        "luz": {
            "tipo": "sagrado",
            "interpretaciones": ["conciencia", "verdad", "esperanza", "iluminación"],
            "variantes": ["brillo", "destello", "rayo", "luminosidad"]
        },
        "grieta": {
            "tipo": "misterio",
            "interpretaciones": ["ruptura", "acceso", "vulnerabilidad", "puerta oculta"],
            "variantes": ["fisura", "quiebre", "abertura", "falla"]
        },
        "templo": {
            "tipo": "sagrado",
            "interpretaciones": ["santuario", "memoria", "refugio", "espacio sagrado"],
            "variantes": ["altar", "santuario", "capilla", "sagrado"]
        },
        "agua": {
            "tipo": "arquetipo",
            "interpretaciones": ["flujo", "emoción", "transición", "purificación"],
            "variantes": ["río", "mar", "lluvia", "corriente"]
        },
        "fuego": {
            "tipo": "arquetipo",
            "interpretaciones": ["transformación", "pasión", "destrucción-creación", "energía"],
            "variantes": ["llama", "incendio", "chispa", "quema"]
        },
        "espejo": {
            "tipo": "arquetipo",
            "interpretaciones": ["reflejo", "verdad", "dualidad", "autoconocimiento"],
            "variantes": ["reflejo", "espejo", "especular"]
        },
        "sombra": {
            "tipo": "arquetipo",
            "interpretaciones": ["inconsciente", "lado oscuro", "negación", "misterio"],
            "variantes": ["oscuridad", "penumbra", "silhueta"]
        },
    }
    
    # Arquetipos
    ARQUETIPOS = {
        "héroe": "quien enfrenta el desafío",
        "sombra": "quien representa lo negado",
        "sabio": "quien busca verdad",
        "amante": "quien conecta emocionalmente",
        "mago": "quien transforma",
        "payaso": "quien cuestiona",
    }
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y detecta símbolos."""
        simbolos = self.detectar_simbolos(input_text)
        return f"Símbolos detectados: {len(simbolos)} referencias rituales"
    
    def detectar_simbolos(self, texto: str) -> List[SimboloDetectado]:
        """
        Detecta símbolos en el texto y busca en base de símbolos.
        """
        simbolos_encontrados = []
        texto_lower = texto.lower()
        
        for simbolo_clave, datos_simbolo in self.SIMBOLOS_BASE.items():
            if simbolo_clave in texto_lower:
                sim_det = SimboloDetectado(
                    simbolo=simbolo_clave,
                    tipo=datos_simbolo["tipo"],
                    interpretaciones=datos_simbolo["interpretaciones"],
                    confianza=0.8,
                    variantes=datos_simbolo["variantes"],
                    notas=f"Símbolo arquetípico: {datos_simbolo['tipo']}"
                )
                simbolos_encontrados.append(sim_det)
            
            # Buscar variantes
            for variante in datos_simbolo["variantes"]:
                if variante in texto_lower and variante != simbolo_clave:
                    sim_det = SimboloDetectado(
                        simbolo=variante,
                        tipo=datos_simbolo["tipo"],
                        interpretaciones=datos_simbolo["interpretaciones"],
                        confianza=0.6,
                        variantes=[simbolo_clave],
                        notas=f"Variante de: {simbolo_clave}"
                    )
                    simbolos_encontrados.append(sim_det)
        
        # Detectar arquetipos
        for arquetipo, descripcion in self.ARQUETIPOS.items():
            if arquetipo in texto_lower:
                sim_det = SimboloDetectado(
                    simbolo=arquetipo,
                    tipo="arquetipo",
                    interpretaciones=[descripcion],
                    confianza=0.7,
                    notas=f"Arquetipo: {descripcion}"
                )
                simbolos_encontrados.append(sim_det)
        
        return simbolos_encontrados
    
    def generar_respuesta_ritual(self, texto: str, opt_in: bool = False) -> str:
        """
        Genera respuesta poética/ritual si opt_in es True.
        
        IMPORTANTE: Solo si el usuario ha dado consentimiento explícito.
        """
        if not opt_in:
            return "Modo ritual desactivado (opt-in requerido)"
        
        simbolos = self.detectar_simbolos(texto)
        
        if not simbolos:
            return "No se detectaron símbolos rituales en el texto."
        
        # Construcción de respuesta poética
        respuesta_partes = [
            "🔮 En el lenguaje de los símbolos, detecto:",
            ""
        ]
        
        for sim in simbolos[:3]:  # Máximo 3 símbolos
            respuesta_partes.append(f"  • **{sim.simbolo.capitalize()}**: {', '.join(sim.interpretaciones)}")
        
        respuesta_partes.append("")
        respuesta_partes.append("_Esto es una interpretación poética, no una afirmación literal._")
        
        return "\n".join(respuesta_partes)
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis de símbolos y rituales."""
        simbolos = self.detectar_simbolos(input_text)
        return {
            "agent": self.profile.nombre,
            "total_simbolos": len(simbolos),
            "simbolos": [s.to_dict() for s in simbolos]
        }
