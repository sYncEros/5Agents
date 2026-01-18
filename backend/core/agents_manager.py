# agents_manager.py
"""
Gestor de agentes con llamadas reales a CrewAI.
Reemplaza los resultados simulados con respuestas auténticas de agentes.
"""

import logging
from typing import Dict, List
from langchain_community.llms import Ollama
from crewai import Crew, Agent, Task, Process

logger = logging.getLogger(__name__)


class AgentsManager:
    """Orquesta agentes reales de CrewAI para procesar ideas."""
    
    def __init__(self, model: str = "ollama/llama3"):
        """
        Inicializa el gestor de agentes.
        
        Args:
            model: Modelo Ollama a usar (por defecto llama3)
        """
        self.model = model
        self.llm = None
        self._initialize_llm()
        self.agents_config = self._setup_agents_config()
    
    def _initialize_llm(self):
        """Inicializa la conexión con Ollama."""
        try:
            self.llm = Ollama(model=self.model)
            logger.info(f"LLM inicializado: {self.model}")
        except Exception as e:
            logger.error(f"Error al inicializar LLM: {e}")
            raise
    
    def _setup_agents_config(self) -> Dict[str, Dict]:
        """Define configuración de los 4 agentes principales."""
        return {
            "🔬 Científico": {
                "role": "Analista Científico",
                "goal": "Realizar un análisis empírico riguroso identificando marcos teóricos, "
                       "metodologías y necesidades de validación experimental.",
                "backstory": "Eres un investigador científico experimentado con expertise en "
                           "método científico, lógica formal y pensamiento crítico."
            },
            "🎨 Creativo": {
                "role": "Pensador Creativo e Innovador",
                "goal": "Explorar perspectivas artísticas, metafóricas y divergentes que amplíen "
                       "la comprensión convencional de la idea.",
                "backstory": "Especialista en pensamiento lateral, síntesis creativa y generación "
                           "de nuevas perspectivas que desafían lo establecido."
            },
            "🧠 Filósofo": {
                "role": "Filósofo Reflexivo",
                "goal": "Analizar las implicaciones ontológicas, epistemológicas y existenciales "
                       "de la idea desde múltiples tradiciones filosóficas.",
                "backstory": "Filósofo con expertise en metafísica, epistemología y filosofía "
                           "aplicada, capaz de conectar ideas con principios fundamentales."
            },
            "💻 Técnico": {
                "role": "Ingeniero Técnico Estratégico",
                "goal": "Evaluar la factibilidad técnica, complejidad de implementación y "
                       "viabilidad con tecnologías actuales.",
                "backstory": "Ingeniero con experiencia en arquitectura de sistemas, evaluación "
                           "de tecnologías y gestión de complejidad técnica."
            }
        }
    
    def _create_agent(self, agent_name: str) -> Agent:
        """Crea un agente específico con su configuración."""
        config = self.agents_config[agent_name]
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm=self.llm,
            allow_delegation=False,
            verbose=False
        )
    
    def _create_analysis_task(self, agent: Agent, idea: str, agent_name: str) -> Task:
        """Crea una tarea de análisis para un agente específico."""
        return Task(
            description=(
                f"Analiza la siguiente idea desde tu perspectiva como {agent_name}:\n\n"
                f"IDEA: {idea}\n\n"
                f"Proporciona un análisis detallado, estructurado y práctico. "
                f"Sé específico y fundamenta tu perspectiva."
            ),
            agent=agent,
            expected_output=f"Análisis completo desde la perspectiva de {agent_name}",
        )
    
    def process_idea(self, idea: str) -> Dict[str, str]:
        """
        Procesa una idea con todos los agentes en paralelo.
        
        Args:
            idea: La idea a analizar
            
        Returns:
            Dict con respuestas de cada agente
        """
        if not idea or not idea.strip():
            raise ValueError("La idea no puede estar vacía")
        
        results = {}
        errors = {}
        
        logger.info(f"Procesando idea: {idea[:50]}...")
        
        # Procesar con cada agente
        for agent_name in self.agents_config.keys():
            try:
                agent = self._create_agent(agent_name)
                task = self._create_analysis_task(agent, idea, agent_name)
                
                # Ejecutar crew individual para cada agente
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False
                )
                
                output = crew.kickoff()
                results[agent_name] = str(output).strip()
                logger.info(f"✓ {agent_name} completó análisis")
                
            except Exception as e:
                error_msg = f"Error en análisis de {agent_name}: {str(e)}"
                logger.error(error_msg)
                errors[agent_name] = error_msg
                results[agent_name] = f"[Error en procesamiento: {str(e)}]"
        
        if errors:
            logger.warning(f"Se encontraron {len(errors)} errores durante el procesamiento")
        
        return results
    
    def get_active_agents(self) -> List[str]:
        """Retorna lista de agentes activos."""
        return list(self.agents_config.keys())
    
    def get_agents_count(self) -> int:
        """Retorna número de agentes disponibles."""
        return len(self.agents_config)


# Instancia global
_agents_manager = None


def get_agents_manager(model: str = "ollama/llama3") -> AgentsManager:
    """Retorna la instancia global del gestor de agentes."""
    global _agents_manager
    if _agents_manager is None:
        _agents_manager = AgentsManager(model=model)
    return _agents_manager
