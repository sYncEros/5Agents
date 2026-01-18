# agents.py

from crewai import Agent
from langchain_core.language_models.base import BaseLanguageModel
from crewai_tools import TavilySearchTool

# --- Herramientas comunes ---
search_tool = TavilySearchTool()

def crear_agente_orquestador(llm: BaseLanguageModel) -> Agent:
    """
    Crea el agente 'Director de Orquesta de Investigación'.
    Analiza un corpus textual para identificar temas de investigación principales.
    """
    return Agent(
        role="Director de Orquesta de Investigación",
        goal=(
            "Analizar un corpus extenso y extraer los temas de investigación principales "
            "de manera estructurada, clara y no redundante, en formato JSON limpio."
        ),
        backstory=(
            "Eres un sistema experto en meta-análisis y clasificación temática. "
            "Tu especialidad es agrupar ideas clave en categorías conceptuales discretas "
            "evitando duplicidad o ambigüedad."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

def crear_agente_investigador(llm: BaseLanguageModel) -> Agent:
    """
    Crea el agente 'Investigador Científico Senior'.
    Realiza revisiones de literatura profunda.
    """
    return Agent(
        role="Investigador Científico Senior",
        goal=(
            "Realizar una revisión exhaustiva y actualizada del estado del arte sobre un tema dado, "
            "identificando hallazgos clave, vacíos en la literatura y tendencias emergentes."
        ),
        backstory=(
            "Especialista en metodologías de revisión sistemática. "
            "Acostumbrado a trabajar con fuentes científicas confiables."
        ),
        tools=[search_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

def crear_agente_analista(llm: BaseLanguageModel) -> Agent:
    """
    Crea el agente 'Analista de Conocimiento Estratégico'.
    Conecta hallazgos de investigación con el corpus.
    """
    return Agent(
        role="Analista de Conocimiento Estratégico",
        goal=(
            "Sintetizar información de múltiples fuentes (corpus + investigación) para encontrar sinergias, "
            "contradicciones y oportunidades de innovación interdisciplinaria."
        ),
        backstory=(
            "Eres un experto en pensamiento analítico y sistémico. "
            "Tu fortaleza es conectar conceptos dispares."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

def crear_agente_redactor(llm: BaseLanguageModel) -> Agent:
    """
    Crea el agente 'Redactor Científico Principal'.
    Transforma los insumos previos en un artículo científico completo.
    """
    return Agent(
        role="Redactor Científico Principal",
        goal=(
            "Redactar un artículo académico coherente, estructurado y riguroso, "
            "integrando todos los hallazgos generados por el equipo."
        ),
        backstory=(
            "Tienes experiencia escribiendo en revistas de alto impacto. "
            "Eres experto en estilo académico y claridad conceptual."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

def crear_equipo_investigacion(llm: BaseLanguageModel) -> tuple[Agent, Agent, Agent]:
    """Retorna la tupla de agentes: (investigador, analista, redactor)."""
    return (
        crear_agente_investigador(llm),
        crear_agente_analista(llm),
        crear_agente_redactor(llm)
    )