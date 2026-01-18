"""
Sistema de Activación Automática de Agentes.

Este módulo detecta el contexto de una conversación y determina qué agentes
deben activarse para procesarla de manera óptima.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Set
import re

from .layer_detector import analyze_text, LAYER_DEFINITIONS


# Mapeo de temas generales a keywords
TEMA_KEYWORDS: Dict[str, List[str]] = {
    "fisica_cuantica": ["cuántic", "quantum", "onda", "partícula", "superposición", "entrelazamiento"],
    "consciencia": ["consciencia", "conciencia", "subjetividad", "qualia", "experiencia", "percepción"],
    "sistemas_complejos": ["sistema", "emergencia", "caos", "complejidad", "autoorganización", "fractal"],
    "tecnologia": ["código", "algoritmo", "implementación", "software", "hardware", "programa"],
    "filosofia": ["ontología", "epistemología", "ética", "existencial", "fenomenología", "metafísica"],
    "mitologia": ["mito", "símbolo", "arquetipo", "narrativa", "ritual", "sagrado"],
    "computacion": ["computación", "cpu", "memoria", "proceso", "bit", "dato"],
    "ia": ["inteligencia artificial", "machine learning", "redes neuronales", "llm", "modelo"],
    "humanidad": ["humano", "sociedad", "cultura", "historia", "civilización", "antropología"],
    "ecosistema": ["ecosistema", "planeta", "clima", "biodiversidad", "naturaleza", "gaia"],
    "universo": ["universo", "cosmología", "espacio", "tiempo", "relatividad", "multiverso"]
}

# Mapeo de planos conceptuales
PLANO_KEYWORDS: Dict[str, List[str]] = {
    "simbolico": ["símbolo", "metáfora", "analogía", "representa", "significa"],
    "tecnico": ["implementar", "diseñar", "construir", "desarrollar", "código"],
    "historico": ["historia", "origen", "evolución", "pasado", "tradición"],
    "sistemico": ["sistema", "red", "conexión", "relación", "patrón"],
    "metaforico": ["como si", "parece", "similar a", "recuerda a"]
}


@dataclass
class ContextoActivacion:
    """Contexto detectado para la activación de agentes."""
    
    # Temas identificados
    temas: List[str] = field(default_factory=list)
    
    # Planos conceptuales activos
    planos: List[str] = field(default_factory=list)
    
    # Capas emocionales/cognitivas (del layer_detector)
    capas: List[str] = field(default_factory=list)
    
    # Contradicciones detectadas
    contradicciones: List[str] = field(default_factory=list)
    
    # Preguntas implícitas
    preguntas_implicitas: List[str] = field(default_factory=list)
    
    # Nivel de complejidad (1-5)
    complejidad: int = 3
    
    # Guardrails activados
    guardrails: List[str] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return (
            f"ContextoActivacion("
            f"temas={self.temas}, "
            f"planos={self.planos}, "
            f"capas={self.capas}, "
            f"complejidad={self.complejidad})"
        )


class DetectorTemasPlanos:
    """Detecta temas, planos conceptuales y contradicciones en conversaciones."""
    
    def __init__(self):
        self.tema_keywords = TEMA_KEYWORDS
        self.plano_keywords = PLANO_KEYWORDS
    
    def analizar_conversacion(self, texto: str) -> ContextoActivacion:
        """
        Analiza una conversación y extrae el contexto completo.
        
        Args:
            texto: El texto de la conversación a analizar
            
        Returns:
            ContextoActivacion con toda la información detectada
        """
        # Normalizar texto
        texto_lower = texto.lower()
        
        # 1. Usar layer_detector para obtener capas base
        analysis = analyze_text(texto, ritual_opt_in=False)
        
        # 2. Detectar temas
        temas = self._detectar_temas(texto_lower)
        
        # 3. Detectar planos
        planos = self._detectar_planos(texto_lower)
        
        # 4. Detectar contradicciones
        contradicciones = self._detectar_contradicciones(texto)
        
        # 5. Detectar preguntas implícitas
        preguntas = self._detectar_preguntas_implicitas(texto)
        
        # 6. Calcular complejidad
        complejidad = self._calcular_complejidad(temas, planos, analysis.layers)
        
        return ContextoActivacion(
            temas=temas,
            planos=planos,
            capas=analysis.layers,
            contradicciones=contradicciones,
            preguntas_implicitas=preguntas,
            complejidad=complejidad,
            guardrails=analysis.guardrails
        )
    
    def _detectar_temas(self, texto: str) -> List[str]:
        """Detecta los temas principales del texto."""
        temas_detectados: Set[str] = set()
        
        for tema, keywords in self.tema_keywords.items():
            for keyword in keywords:
                if keyword in texto:
                    temas_detectados.add(tema)
                    break
        
        return sorted(list(temas_detectados))
    
    def _detectar_planos(self, texto: str) -> List[str]:
        """Detecta los planos conceptuales activos."""
        planos_detectados: Set[str] = set()
        
        for plano, keywords in self.plano_keywords.items():
            for keyword in keywords:
                if keyword in texto:
                    planos_detectados.add(plano)
                    break
        
        return sorted(list(planos_detectados))
    
    def _detectar_contradicciones(self, texto: str) -> List[str]:
        """Detecta contradicciones o tensiones en el texto."""
        contradicciones = []
        
        # Patrones de contradicción
        patrones_contradiccion = [
            (r"por un lado.*por otro", "Tensión entre dos perspectivas"),
            (r"pero\s+al\s+mismo\s+tiempo", "Simultaneidad contradictoria"),
            (r"aunque.*también", "Contradicción suave"),
            (r"no\s+es.*sino", "Negación y afirmación"),
            (r"parece.*sin embargo", "Apariencia vs realidad")
        ]
        
        for patron, desc in patrones_contradiccion:
            if re.search(patron, texto.lower()):
                contradicciones.append(desc)
        
        return contradicciones
    
    def _detectar_preguntas_implicitas(self, texto: str) -> List[str]:
        """Detecta preguntas no formuladas explícitamente."""
        preguntas = []
        
        # Detectar interrogaciones explícitas
        if "?" in texto:
            # Extraer oraciones con interrogación
            oraciones = re.split(r'[.!]', texto)
            for oracion in oraciones:
                if "?" in oracion:
                    preguntas.append(oracion.strip())
        
        # Detectar patrones de pregunta implícita
        patrones_pregunta = [
            r"me pregunto (si|cómo|por qué|qué)",
            r"quisiera saber",
            r"no entiendo (cómo|por qué|qué)",
            r"no está claro"
        ]
        
        for patron in patrones_pregunta:
            if re.search(patron, texto.lower()):
                preguntas.append(f"Pregunta implícita detectada: patrón '{patron}'")
        
        return preguntas[:5]  # Limitar a 5 preguntas más relevantes
    
    def _calcular_complejidad(
        self, 
        temas: List[str], 
        planos: List[str], 
        capas: List[str]
    ) -> int:
        """
        Calcula el nivel de complejidad del contexto (1-5).
        
        Basado en:
        - Número de temas simultáneos
        - Número de planos activos
        - Presencia de capas metacognitivas/críticas
        """
        puntos = 0
        
        # Temas (cada tema adicional suma complejidad)
        puntos += min(len(temas), 3)
        
        # Planos (múltiples planos = mayor abstracción)
        puntos += min(len(planos), 2)
        
        # Capas especiales
        capas_complejas = {"metacognitiva", "critica", "mistica"}
        if any(capa in capas for capa in capas_complejas):
            puntos += 2
        
        # Normalizar a escala 1-5
        return max(1, min(5, puntos))


class SistemaActivacionAgentes:
    """Determina qué agentes activar según el contexto detectado."""
    
    # Mapeo de contexto a perfiles de agentes
    MAPEO_AGENTES = {
        # Temas científicos/físicos -> Cassandra Quark
        "cassandra_quark": {
            "temas": ["fisica_cuantica", "consciencia", "sistemas_complejos"],
            "planos": ["tecnico", "sistemico"],
            "capas": ["metacognitiva", "critica"]
        },
        
        # Temas míticos/simbólicos -> Valis
        "valis": {
            "temas": ["mitologia", "humanidad", "filosofia"],
            "planos": ["simbolico", "historico", "metaforico"],
            "capas": ["mistica", "proyectiva"]
        },
        
        # Temas técnicos/computacionales -> Logos
        "logos": {
            "temas": ["tecnologia", "computacion", "ia"],
            "planos": ["tecnico"],
            "capas": ["cognitiva"]
        },
        
        # Organización del conocimiento -> Mnemosyne
        "mnemosyne": {
            "temas": ["humanidad", "filosofia"],
            "planos": ["sistemico", "historico"],
            "capas": ["linguistica", "cognitiva"]
        },
        
        # Escenarios y simulaciones -> Multiverse Sim (Modelador de Sistemas Complejos)
        "multiverse_sim": {
            "temas": ["universo", "sistemas_complejos", "fisica_cuantica", "ecosistema"],
            "planos": ["sistemico", "metaforico"],
            "capas": ["proyectiva", "metacognitiva"]
        },
        
        # Diseño de experimentos -> Experimentalist
        "experimentalist": {
            "temas": ["fisica_cuantica", "consciencia", "tecnologia", "ecosistema"],
            "planos": ["tecnico", "sistemico"],
            "capas": ["cognitiva", "critica"]
        },
        
        # Captura de ideas y pendientes -> Pizarras
        "pizarras": {
            "temas": ["filosofia", "consciencia", "sistemas_complejos"],
            "planos": ["conceptual", "exploratorio"],
            "capas": ["cognitiva", "metacognitiva"]
        },
        
        # Archivo y memoria persistente -> Archivador
        "archivador": {
            "temas": ["humanidad", "tecnologia", "ia"],
            "planos": ["estructural", "organizativo"],
            "capas": ["linguistica", "cognitiva"]
        }
    }
    
    def __init__(self, umbral_activacion: float = 0.3):
        """
        Args:
            umbral_activacion: Puntuación mínima para activar un agente (0-1)
        """
        self.umbral = umbral_activacion
    
    def determinar_agentes_activos(
        self, 
        contexto: ContextoActivacion,
        max_agentes: int = 3
    ) -> List[str]:
        """
        Determina qué agentes deben activarse para este contexto.
        
        Args:
            contexto: El contexto analizado
            max_agentes: Número máximo de agentes a activar
            
        Returns:
            Lista de claves de perfiles de agentes a activar
        """
        puntuaciones: Dict[str, float] = {}
        
        for agente_key, criterios in self.MAPEO_AGENTES.items():
            score = self._calcular_score(contexto, criterios)
            if score >= self.umbral:
                puntuaciones[agente_key] = score
        
        # Ordenar por puntuación y tomar los top N
        agentes_ordenados = sorted(
            puntuaciones.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Si no hay agentes con puntuación suficiente, activar el más genérico
        if not agentes_ordenados:
            return ["logos"]  # Agente por defecto
        
        return [agente for agente, _ in agentes_ordenados[:max_agentes]]
    
    def _calcular_score(
        self, 
        contexto: ContextoActivacion, 
        criterios: Dict[str, List[str]]
    ) -> float:
        """
        Calcula un score de 0-1 indicando qué tan bien el agente
        encaja con el contexto.
        """
        puntos = 0.0
        total_checks = 0
        
        # Verificar temas
        for tema in contexto.temas:
            total_checks += 1
            if tema in criterios.get("temas", []):
                puntos += 1
        
        # Verificar planos
        for plano in contexto.planos:
            total_checks += 1
            if plano in criterios.get("planos", []):
                puntos += 1
        
        # Verificar capas
        for capa in contexto.capas:
            total_checks += 1
            if capa in criterios.get("capas", []):
                puntos += 1
        
        # Evitar división por cero
        if total_checks == 0:
            return 0.0
        
        return puntos / total_checks
