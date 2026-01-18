"""
Controlador de Flujo Conversacional.

Orquesta el flujo completo del sistema multi-agente:
1. Detectar contexto
2. Activar agentes relevantes
3. Generar respuestas con LLMs
4. Sintetizar resultados
"""
from __future__ import annotations

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time

from .agent_activator import DetectorTemasPlanos, SistemaActivacionAgentes, ContextoActivacion
from .synthesis_engine import MotorSintesis, Sintesis
from components.llm.ollama_client import OllamaClient
from components.llm.profiles import AGENT_PROFILES

@dataclass
class ResultadoConversacion:
    """Resultado completo del procesamiento conversacional."""
    
    # Input original
    input: str
    
    # Contexto detectado
    contexto: ContextoActivacion
    
    # Agentes activados
    agentes_activados: List[str]
    
    # Respuestas individuales
    respuestas: Dict[str, str]
    
    # Síntesis
    sintesis: Sintesis
    
    # Tiempos
    tiempo_total: float
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el resultado a diccionario para serialización."""
        return {
            "input": self.input,
            "contexto": {
                "temas": self.contexto.temas,
                "planos": self.contexto.planos,
                "capas": self.contexto.capas,
                "complejidad": self.contexto.complejidad,
                "contradicciones": self.contexto.contradicciones,
                "preguntas_implicitas": self.contexto.preguntas_implicitas,
                "guardrails": self.contexto.guardrails
            },
            "agentes_activados": self.agentes_activados,
            "respuestas": self.respuestas,
            "sintesis": {
                "resumen": self.sintesis.resumen,
                "hipotesis_cruzadas": self.sintesis.hipotesis_cruzadas,
                "convergencias": self.sintesis.convergencias,
                "tensiones": self.sintesis.tensiones,
                "preguntas_abiertas": self.sintesis.preguntas_abiertas,
                "temas_emergentes": self.sintesis.temas_emergentes,
                "relaciones": self.sintesis.relaciones
            },
            "metadata": {
                "tiempo_total": self.tiempo_total,
                "timestamp": self.timestamp
            }
        }


class ConversationController:
    """
    Orquestador del flujo conversacional multi-agente.
    
    Ejemplo de uso:
        controller = ConversationController()
        resultado = controller.process("¿Puede una IA ser consciente?")
        print(resultado.sintesis.resumen)
    """
    
    def __init__(
        self,
        ollama_base_url: str = "http://localhost:11434",
        umbral_activacion: float = 0.3,
        max_agentes: int = 3,
        verbose: bool = False
    ):
        """
        Args:
            ollama_base_url: URL del servidor Ollama
            umbral_activacion: Puntuación mínima para activar agentes
            max_agentes: Número máximo de agentes a activar
            verbose: Si mostrar logs de progreso
        """
        self.ollama = OllamaClient(base_url=ollama_base_url)
        self.detector = DetectorTemasPlanos()
        self.activator = SistemaActivacionAgentes(umbral_activacion=umbral_activacion)
        self.synthesizer = MotorSintesis()
        
        self.max_agentes = max_agentes
        self.verbose = verbose
        
        # Verificar disponibilidad de Ollama
        if not self.ollama.is_available():
            print("⚠️  Advertencia: Ollama no está disponible. Las respuestas fallarán.")
            print("   Asegúrate de que Ollama esté corriendo: ollama serve")
    
    def process(
        self,
        user_input: str,
        agentes_manuales: Optional[List[str]] = None
    ) -> ResultadoConversacion:
        """
        Procesa una entrada del usuario a través del sistema multi-agente.
        
        Args:
            user_input: Texto de entrada del usuario
            agentes_manuales: Lista opcional de agentes a usar (omite detección automática)
            
        Returns:
            ResultadoConversacion con todo el análisis
        """
        inicio = time.time()
        
        # 1. Detectar contexto
        if self.verbose:
            print("🔍 Detectando contexto...")
        
        contexto = self.detector.analizar_conversacion(user_input)
        
        if self.verbose:
            print(f"   Temas: {contexto.temas}")
            print(f"   Planos: {contexto.planos}")
            print(f"   Complejidad: {contexto.complejidad}/5")
        
        # 2. Activar agentes (manual o automático)
        if agentes_manuales:
            agentes_keys = agentes_manuales
            if self.verbose:
                print(f"🎯 Agentes seleccionados manualmente: {agentes_keys}")
        else:
            if self.verbose:
                print("🤖 Activando agentes automáticamente...")
            
            agentes_keys = self.activator.determinar_agentes_activos(
                contexto,
                max_agentes=self.max_agentes
            )
            
            if self.verbose:
                print(f"   Agentes activados: {agentes_keys}")
        
        # 3. Generar respuestas
        if self.verbose:
            print("💬 Generando respuestas...")
        
        respuestas = {}
        for key in agentes_keys:
            profile = AGENT_PROFILES.get(key)
            if not profile:
                print(f"⚠️  Agente '{key}' no encontrado en AGENT_PROFILES")
                continue
            
            if self.verbose:
                print(f"   → {profile.nombre}...")
            
            # Construir prompt
            prompt = profile.build_prompt(user_input)
            
            try:
                # Generar respuesta
                respuesta = self.ollama.generate(
                    prompt=prompt,
                    model=profile.modelo_llm,
                    temperature=profile.temperatura,
                    max_tokens=profile.max_tokens
                )
                respuestas[profile.nombre] = respuesta
                
                if self.verbose:
                    print(f"      ✓ Respuesta generada ({len(respuesta)} chars)")
                    
            except Exception as e:
                print(f"      ✗ Error generando respuesta: {e}")
                respuestas[profile.nombre] = f"[Error: {str(e)}]"
        
        # 4. Sintetizar
        if self.verbose:
            print("🧪 Sintetizando respuestas...")
        
        sintesis = self.synthesizer.sintetizar_respuestas(respuestas, contexto)
        
        if self.verbose:
            print(f"   Hipótesis: {len(sintesis.hipotesis_cruzadas)}")
            print(f"   Convergencias: {len(sintesis.convergencias)}")
            print(f"   Tensiones: {len(sintesis.tensiones)}")
        
        # 5. Construir resultado
        tiempo_total = time.time() - inicio
        timestamp = time.time()
        
        resultado = ResultadoConversacion(
            input=user_input,
            contexto=contexto,
            agentes_activados=agentes_keys,
            respuestas=respuestas,
            sintesis=sintesis,
            tiempo_total=round(tiempo_total, 2),
            timestamp=timestamp
        )
        
        if self.verbose:
            print(f"\n✅ Procesamiento completado en {tiempo_total:.2f}s")
        
        return resultado
    
    def process_multiple(
        self,
        inputs: List[str],
        agentes_manuales: Optional[List[str]] = None
    ) -> List[ResultadoConversacion]:
        """
        Procesa múltiples inputs en secuencia.
        
        Args:
            inputs: Lista de textos de entrada
            agentes_manuales: Lista opcional de agentes a usar para todos
            
        Returns:
            Lista de ResultadoConversacion
        """
        resultados = []
        
        for i, user_input in enumerate(inputs):
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"Procesando entrada {i+1}/{len(inputs)}")
                print(f"{'='*60}")
            
            resultado = self.process(user_input, agentes_manuales)
            resultados.append(resultado)
        
        return resultados
    
    def listar_agentes_disponibles(self) -> Dict[str, Dict[str, str]]:
        """
        Lista todos los agentes disponibles con su información.
        
        Returns:
            Diccionario {key: {nombre, rol, modelo}}
        """
        agentes_info = {}
        
        for key, profile in AGENT_PROFILES.items():
            agentes_info[key] = {
                "nombre": profile.nombre,
                "rol": profile.rol,
                "modelo": profile.modelo_llm,
                "temperatura": profile.temperatura
            }
        
        return agentes_info
    
    def verificar_sistema(self) -> Dict[str, Any]:
        """
        Verifica el estado del sistema completo.
        
        Returns:
            Diccionario con estado de cada componente
        """
        return {
            "ollama": {
                "disponible": self.ollama.is_available(),
                "url": self.ollama.base_url,
                "modelos": self.ollama.list_models() if self.ollama.is_available() else []
            },
            "agentes": {
                "disponibles": len(AGENT_PROFILES),
                "lista": list(AGENT_PROFILES.keys())
            },
            "configuracion": {
                "umbral_activacion": self.activator.umbral,
                "max_agentes": self.max_agentes,
                "verbose": self.verbose
            }
        }
