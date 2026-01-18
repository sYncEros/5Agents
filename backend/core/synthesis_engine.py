"""
Motor de Síntesis para respuestas multi-agente.

Este módulo sintetiza las respuestas de múltiples agentes, generando:
- Hipótesis cruzadas
- Contraargumentos y tensiones
- Preguntas abiertas
- Mapas conceptuales
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import re

from .agent_activator import ContextoActivacion


@dataclass
class Sintesis:
    """Resultado de la síntesis de múltiples respuestas."""
    
    # Hipótesis cruzadas emergentes
    hipotesis_cruzadas: List[str] = field(default_factory=list)
    
    # Puntos de convergencia entre agentes
    convergencias: List[str] = field(default_factory=list)
    
    # Contraargumentos y tensiones
    tensiones: List[Dict[str, str]] = field(default_factory=list)
    
    # Preguntas abiertas para futuras iteraciones
    preguntas_abiertas: List[str] = field(default_factory=list)
    
    # Temas emergentes no detectados inicialmente
    temas_emergentes: List[str] = field(default_factory=list)
    
    # Relaciones entre conceptos (para grafos)
    relaciones: List[Tuple[str, str, str]] = field(default_factory=list)  # (origen, destino, tipo)
    
    # Resumen ejecutivo
    resumen: str = ""
    
    # Metadatos
    metadata: Dict[str, Any] = field(default_factory=dict)


class MotorSintesis:
    """Sintetiza respuestas de múltiples agentes en conocimiento estructurado."""
    
    def __init__(self):
        # Keywords para detectar convergencias
        self.convergencia_patterns = [
            r"coincid",
            r"acuerdo",
            r"ambos.*sugieren",
            r"tanto.*como",
            r"en común"
        ]
        
        # Keywords para detectar tensiones
        self.tension_patterns = [
            r"sin embargo",
            r"pero",
            r"contrariamente",
            r"mientras que",
            r"por otro lado",
            r"a diferencia de"
        ]
        
        # Keywords para hipótesis
        self.hipotesis_markers = [
            "podría ser que",
            "hipótesis",
            "posiblemente",
            "quizás",
            "sugiere que",
            "indica que",
            "parece que"
        ]
    
    def sintetizar_respuestas(
        self,
        respuestas: Dict[str, str],
        contexto: ContextoActivacion
    ) -> Sintesis:
        """
        Sintetiza respuestas de múltiples agentes.
        
        Args:
            respuestas: Diccionario {nombre_agente: respuesta}
            contexto: Contexto original de activación
            
        Returns:
            Sintesis con análisis cruzado
        """
        sintesis = Sintesis()
        
        # 1. Extraer conceptos clave de cada respuesta
        conceptos_por_agente = self._extraer_conceptos(respuestas)
        
        # 2. Detectar convergencias
        sintesis.convergencias = self._detectar_convergencias(conceptos_por_agente)
        
        # 3. Detectar tensiones y contraargumentos
        sintesis.tensiones = self._detectar_tensiones(respuestas)
        
        # 4. Generar hipótesis cruzadas
        sintesis.hipotesis_cruzadas = self._generar_hipotesis_cruzadas(
            respuestas, conceptos_por_agente
        )
        
        # 5. Identificar preguntas abiertas
        sintesis.preguntas_abiertas = self._extraer_preguntas_abiertas(respuestas)
        
        # 6. Detectar temas emergentes
        sintesis.temas_emergentes = self._detectar_temas_emergentes(
            conceptos_por_agente, contexto
        )
        
        # 7. Construir relaciones para grafos
        sintesis.relaciones = self._construir_relaciones(conceptos_por_agente)
        
        # 8. Generar resumen ejecutivo
        sintesis.resumen = self._generar_resumen(respuestas, sintesis)
        
        # 9. Metadatos
        sintesis.metadata = {
            "num_agentes": len(respuestas),
            "agentes_activos": list(respuestas.keys()),
            "complejidad_contexto": contexto.complejidad,
            "guardrails_activos": contexto.guardrails
        }
        
        return sintesis
    
    def _extraer_conceptos(
        self, 
        respuestas: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """Extrae conceptos clave de cada respuesta."""
        conceptos_por_agente = {}
        
        for agente, respuesta in respuestas.items():
            # Extraer sustantivos y frases clave
            # Simplificado: palabras de 5+ letras que aparecen con frecuencia
            palabras = re.findall(r'\b[a-záéíóúñ]{5,}\b', respuesta.lower())
            
            # Contar frecuencias
            frecuencias = defaultdict(int)
            for palabra in palabras:
                frecuencias[palabra] += 1
            
            # Tomar las más frecuentes (conceptos clave)
            conceptos = [
                palabra for palabra, freq in 
                sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
            
            conceptos_por_agente[agente] = conceptos
        
        return conceptos_por_agente
    
    def _detectar_convergencias(
        self,
        conceptos_por_agente: Dict[str, List[str]]
    ) -> List[str]:
        """Detecta conceptos mencionados por múltiples agentes."""
        convergencias = []
        
        # Contar cuántos agentes mencionan cada concepto
        concepto_counts = defaultdict(list)
        for agente, conceptos in conceptos_por_agente.items():
            for concepto in conceptos:
                concepto_counts[concepto].append(agente)
        
        # Convergencia = concepto mencionado por 2+ agentes
        for concepto, agentes in concepto_counts.items():
            if len(agentes) >= 2:
                agentes_str = ", ".join(agentes)
                convergencias.append(
                    f"'{concepto}' mencionado por: {agentes_str}"
                )
        
        return convergencias[:5]  # Top 5 convergencias
    
    def _detectar_tensiones(
        self,
        respuestas: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """Detecta contraargumentos y tensiones entre respuestas."""
        tensiones = []
        
        # Buscar patrones de tensión en cada respuesta
        for agente, respuesta in respuestas.items():
            for pattern in self.tension_patterns:
                matches = re.finditer(pattern, respuesta.lower())
                for match in matches:
                    # Extraer contexto alrededor del patrón
                    inicio = max(0, match.start() - 100)
                    fin = min(len(respuesta), match.end() + 100)
                    contexto = respuesta[inicio:fin].strip()
                    
                    tensiones.append({
                        "agente": agente,
                        "tipo": "contraargumento_interno",
                        "contexto": contexto[:200]  # Limitar longitud
                    })
        
        return tensiones[:5]  # Top 5 tensiones
    
    def _generar_hipotesis_cruzadas(
        self,
        respuestas: Dict[str, str],
        conceptos_por_agente: Dict[str, List[str]]
    ) -> List[str]:
        """Genera hipótesis emergentes del cruce de respuestas."""
        hipotesis = []
        
        # Buscar oraciones que contengan marcadores de hipótesis
        for agente, respuesta in respuestas.items():
            for marker in self.hipotesis_markers:
                if marker in respuesta.lower():
                    # Extraer la oración completa
                    sentences = re.split(r'[.!?]', respuesta)
                    for sentence in sentences:
                        if marker in sentence.lower():
                            hipotesis.append(
                                f"[{agente}] {sentence.strip()}"
                            )
        
        # Generar hipótesis de convergencia
        agentes_list = list(respuestas.keys())
        if len(agentes_list) >= 2:
            # Buscar conceptos compartidos
            conceptos_compartidos = set(conceptos_por_agente[agentes_list[0]])
            for agente in agentes_list[1:]:
                conceptos_compartidos &= set(conceptos_por_agente[agente])
            
            if conceptos_compartidos:
                conceptos_str = ", ".join(list(conceptos_compartidos)[:3])
                hipotesis.append(
                    f"Hipótesis de convergencia: Los conceptos {conceptos_str} "
                    f"parecen ser centrales según múltiples perspectivas"
                )
        
        return hipotesis[:7]  # Top 7 hipótesis
    
    def _extraer_preguntas_abiertas(
        self,
        respuestas: Dict[str, str]
    ) -> List[str]:
        """Extrae preguntas abiertas de las respuestas."""
        preguntas = []
        
        for agente, respuesta in respuestas.items():
            # Buscar interrogaciones explícitas
            sentences = re.split(r'[.!]', respuesta)
            for sentence in sentences:
                if "?" in sentence:
                    preguntas.append(f"[{agente}] {sentence.strip()}")
            
            # Buscar patrones de pregunta implícita
            patterns = [
                r"queda por (determinar|resolver|investigar|entender)",
                r"no está claro",
                r"sería interesante (explorar|investigar|considerar)",
                r"futuras investigaciones deberían"
            ]
            
            for pattern in patterns:
                if re.search(pattern, respuesta.lower()):
                    # Extraer contexto
                    match = re.search(pattern, respuesta.lower())
                    if match:
                        inicio = max(0, match.start() - 50)
                        fin = min(len(respuesta), match.end() + 100)
                        contexto = respuesta[inicio:fin].strip()
                        preguntas.append(f"[{agente}] ...{contexto}...")
        
        return preguntas[:10]  # Top 10 preguntas
    
    def _detectar_temas_emergentes(
        self,
        conceptos_por_agente: Dict[str, List[str]],
        contexto_original: ContextoActivacion
    ) -> List[str]:
        """Detecta temas que emergen pero no estaban en el contexto inicial."""
        todos_conceptos = set()
        for conceptos in conceptos_por_agente.values():
            todos_conceptos.update(conceptos)
        
        # Filtrar conceptos que no estaban en los temas originales
        temas_originales_str = " ".join(contexto_original.temas).lower()
        
        temas_nuevos = [
            concepto for concepto in todos_conceptos
            if concepto not in temas_originales_str
        ]
        
        return temas_nuevos[:8]  # Top 8 temas emergentes
    
    def _construir_relaciones(
        self,
        conceptos_por_agente: Dict[str, List[str]]
    ) -> List[Tuple[str, str, str]]:
        """
        Construye relaciones entre conceptos para grafos.
        
        Returns:
            Lista de tuplas (concepto_origen, concepto_destino, tipo_relacion)
        """
        relaciones = []
        
        # Crear relaciones entre conceptos del mismo agente
        for agente, conceptos in conceptos_por_agente.items():
            for i, concepto1 in enumerate(conceptos[:5]):  # Limitar para eficiencia
                for concepto2 in conceptos[i+1:6]:
                    relaciones.append((
                        concepto1,
                        concepto2,
                        f"co-mencionado_por_{agente}"
                    ))
        
        # Crear relaciones entre agentes (convergencias)
        agentes_list = list(conceptos_por_agente.keys())
        for i, agente1 in enumerate(agentes_list):
            for agente2 in agentes_list[i+1:]:
                conceptos_comunes = (
                    set(conceptos_por_agente[agente1]) & 
                    set(conceptos_por_agente[agente2])
                )
                for concepto in list(conceptos_comunes)[:3]:
                    relaciones.append((
                        agente1,
                        agente2,
                        f"convergen_en_{concepto}"
                    ))
        
        return relaciones[:20]  # Top 20 relaciones más relevantes
    
    def _generar_resumen(
        self,
        respuestas: Dict[str, str],
        sintesis: Sintesis
    ) -> str:
        """Genera un resumen ejecutivo de la síntesis."""
        partes = []
        
        # Intro
        num_agentes = len(respuestas)
        agentes_str = ", ".join(respuestas.keys())
        partes.append(
            f"Se consultaron {num_agentes} agente(s): {agentes_str}."
        )
        
        # Convergencias
        if sintesis.convergencias:
            partes.append(
                f"\n**Convergencias:** {len(sintesis.convergencias)} concepto(s) "
                "mencionados por múltiples agentes, indicando puntos de acuerdo."
            )
        
        # Tensiones
        if sintesis.tensiones:
            partes.append(
                f"\n**Tensiones:** {len(sintesis.tensiones)} contraargumento(s) "
                "o matiz(ces) detectado(s)."
            )
        
        # Hipótesis
        if sintesis.hipotesis_cruzadas:
            partes.append(
                f"\n**Hipótesis emergentes:** {len(sintesis.hipotesis_cruzadas)} "
                "hipótesis derivadas del análisis cruzado."
            )
        
        # Preguntas abiertas
        if sintesis.preguntas_abiertas:
            partes.append(
                f"\n**Preguntas abiertas:** {len(sintesis.preguntas_abiertas)} "
                "cuestión(es) que requieren exploración adicional."
            )
        
        return " ".join(partes)
