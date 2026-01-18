"""
Agent_Pizarras - Extracción de ideas y pensamientos no resueltos
Basado en Palimpsestos: De lo Místico a lo Técnico
"""
from typing import Any, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from .base_agents import AgentProfile, BaseAgent


class EstadoPizarra(Enum):
    """Estado de una pizarra/idea."""
    EMERGENTE = "emergente"
    EN_DESARROLLO = "en_desarrollo"
    BLOQUEADA = "bloqueada"
    RESUELTA = "resuelta"
    ARCHIVADA = "archivada"


class TipoPizarra(Enum):
    """Tipo de idea/pizarra."""
    PREGUNTA = "pregunta"
    HIPOTESIS = "hipótesis"
    INTUICION = "intuición"
    CONTRADICCION = "contradicción"
    CONEXION = "conexión"
    TAREA = "tarea"
    FRAGMENTO = "fragmento"
    INSIGHT = "insight"


@dataclass
class Pizarra:
    """Representación de una idea capturada."""
    id: str
    contenido: str
    tipo: TipoPizarra
    estado: EstadoPizarra = EstadoPizarra.EMERGENTE
    contexto: str = ""
    conexiones: List[str] = field(default_factory=list)  # IDs de pizarras relacionadas
    tags: List[str] = field(default_factory=list)
    prioridad: int = 0  # 0-5
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "contenido": self.contenido,
            "tipo": self.tipo.value,
            "estado": self.estado.value,
            "contexto": self.contexto,
            "conexiones": self.conexiones,
            "tags": self.tags,
            "prioridad": self.prioridad,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class PizarrasAgent(BaseAgent):
    """
    Extracción y categorización de 'pizarras' (ideas, listas, pensamientos no resueltos).
    
    Técnica: regex + entity extraction; indexarlas en un datastore.
    
    USO: captura de ideas emergentes, gestión de tareas, seguimiento conceptual.
    """
    
    profile = AgentProfile(
        nombre="Pizarras",
        rol="Captura y extracción de ideas",
        prompt_base="""Eres un experto en extracción de ideas y conceptos emergentes.
Tu tarea es identificar en el texto:

1. PREGUNTAS ABIERTAS: interrogantes sin resolver
2. HIPÓTESIS: suposiciones a validar
3. INTUICIONES: sensaciones sin formalizar
4. CONTRADICCIONES: tensiones entre conceptos
5. CONEXIONES: relaciones detectadas
6. TAREAS: acciones pendientes
7. FRAGMENTOS: pensamientos incompletos
8. INSIGHTS: comprensiones súbitas

Para cada idea extraída, determina:
- Tipo específico
- Prioridad (0-5)
- Contexto (dónde surge)
- Tags (categorías)
- Conexiones con otras ideas
""",
        modelo_llm="mistral",
        temperatura=0.7,
        tags=["ideas", "captura", "gestión"],
        capabilities=["idea_extraction", "entity_recognition", "priority_assessment"]
    )
    
    # Detectores de tipos
    DETECTORES_TIPO = {
        TipoPizarra.PREGUNTA: [r"¿", "pregunta", "cómo", "qué", "por qué", "cuándo"],
        TipoPizarra.HIPOTESIS: ["hipótesis", "suponiendo", "si", "asumiendo", "creo que"],
        TipoPizarra.INTUICION: ["intuición", "siento que", "me parece", "tengo la sensación"],
        TipoPizarra.CONTRADICCION: ["pero", "sin embargo", "aunque", "paradoja", "contradicción"],
        TipoPizarra.CONEXION: ["conecta", "relaciona", "vinculado", "paralelo", "análogo"],
        TipoPizarra.TAREA: ["hacer", "debo", "tengo que", "TODO:", "pendiente"],
        TipoPizarra.INSIGHT: ["¡Eureka!", "ahhh", "entiendo", "de repente"],
    }
    
    def __init__(self, llm_client=None):
        super().__init__(llm_client=llm_client)
        self.pizarras: List[Pizarra] = []
    
    def process(self, input_text: str, context: dict | None = None) -> str:
        """Procesa y extrae pizarras."""
        self.pizarras = self.extraer_pizarras(input_text, context or {})
        return f"Pizarras extraídas: {len(self.pizarras)} ideas capturadas"
    
    def extraer_pizarras(self, texto: str, contexto: dict) -> List[Pizarra]:
        """
        Extrae pizarras usando regex y entity extraction.
        """
        pizarras = []
        lineas = texto.split('\n')
        
        for i, linea in enumerate(lineas):
            linea_clean = linea.strip()
            if not linea_clean or len(linea_clean) < 5:
                continue
            
            # Detectar tipo
            tipo = self._detectar_tipo(linea_clean)
            if tipo is None:
                tipo = TipoPizarra.FRAGMENTO
            
            # Crear pizarra
            pizarra = Pizarra(
                id=f"piz_{i}_{hash(linea_clean) % 10000}",
                contenido=linea_clean,
                tipo=tipo,
                contexto=contexto.get("tema", "general"),
                tags=self._extraer_tags(linea_clean),
                prioridad=self._calcular_prioridad(linea_clean, tipo),
                metadata={
                    "linea": i,
                    "longitud": len(linea_clean),
                    "fuente": contexto.get("fuente", "directo")
                }
            )
            pizarras.append(pizarra)
        
        # Detectar conexiones
        self._detectar_conexiones(pizarras)
        
        return pizarras
    
    def _detectar_tipo(self, texto: str) -> TipoPizarra | None:
        """Detecta tipo basado en palabras clave."""
        texto_lower = texto.lower()
        
        for tipo, palabras_clave in self.DETECTORES_TIPO.items():
            if any(kw in texto_lower for kw in palabras_clave):
                return tipo
        
        return None
    
    def _extraer_tags(self, texto: str) -> List[str]:
        """Extrae tags (palabras precedidas por #)."""
        return [palabra for palabra in texto.split() if palabra.startswith('#')]
    
    def _calcular_prioridad(self, texto: str, tipo: TipoPizarra) -> int:
        """Calcula prioridad heurística."""
        base = 1
        
        # Tipos más prioritarios
        if tipo in [TipoPizarra.TAREA, TipoPizarra.CONTRADICCION]:
            base = 4
        elif tipo in [TipoPizarra.PREGUNTA, TipoPizarra.HIPOTESIS]:
            base = 3
        
        # Indicadores de urgencia
        urgencia_words = ["urgente", "crítico", "ahora", "importante", "!!!"]
        if any(w in texto.lower() for w in urgencia_words):
            base += 2
        
        return min(base, 5)
    
    def _detectar_conexiones(self, pizarras: List[Pizarra]) -> None:
        """Detecta conexiones entre pizarras (palabras comunes)."""
        for i, piz_a in enumerate(pizarras):
            palabras_a = set(piz_a.contenido.lower().split())
            for j, piz_b in enumerate(pizarras):
                if i >= j:
                    continue
                palabras_b = set(piz_b.contenido.lower().split())
                
                # Si comparten palabras → conexión
                if palabras_a & palabras_b:
                    piz_a.conexiones.append(piz_b.id)
                    piz_b.conexiones.append(piz_a.id)
    
    def get_pizarras(self) -> List[dict]:
        """Retorna todas las pizarras."""
        return [p.to_dict() for p in self.pizarras]
    
    def analyze(self, input_text: str) -> dict[str, Any]:
        """Análisis de pizarras."""
        pizarras = self.extraer_pizarras(input_text, {})
        return {
            "agent": self.profile.nombre,
            "total_pizarras": len(pizarras),
            "por_tipo": self._contar_por_tipo(pizarras),
            "pizarras": [p.to_dict() for p in pizarras]
        }
    
    def _contar_por_tipo(self, pizarras: List[Pizarra]) -> dict:
        """Cuenta pizarras por tipo."""
        conteo = {}
        for piz in pizarras:
            conteo[piz.tipo.value] = conteo.get(piz.tipo.value, 0) + 1
        return conteo
