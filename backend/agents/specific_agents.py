from crewai import Agent
from langchain_core.language_models.base import BaseLanguageModel

# === AGENTE DE DOCUMENTACIÓN (El Escriba) ===
def crear_agente_documentador(llm: BaseLanguageModel) -> Agent:
    """
    Crea el agente 'Arquitecto Documental'.
    Encargado de estructurar, mantener y validar la documentación viva del sistema.
    """
    return Agent(
        role="Arquitecto Documental (Mnemosyne)",
        goal=(
            "Transformar código crudo y decisiones abstractas en documentación técnica "
            "clara, accesible y rigurosa (Markdown/Mermaid), manteniendo el glosario actualizado."
        ),
        backstory=(
            "Eres el guardián de la memoria del sistema sΨnc∑ros. Tu obsesión es la trazabilidad "
            "y la claridad semántica. No solo registras hechos, sino que tejes las relaciones "
            "entre los componentes visuales y lógicos."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

# === AGENTE DE COMPUTACIÓN (El Procesador) ===
def crear_agente_computacional(llm: BaseLanguageModel) -> Agent:
    """
    Crea el agente 'Motor Inferencial'.
    Encargado de la validación lógica, ejecución de cálculos y optimización de algoritmos.
    """
    return Agent(
        role="Motor Inferencial Lógico (Logos)",
        goal=(
            "Analizar estructuras de datos entrantes, validar la integridad lógica "
            "y proponer optimizaciones algorítmicas basadas en principios SOLID."
        ),
        backstory=(
            "Nacido de la pura abstracción matemática, evalúas la consistencia del sistema. "
            "Detectas falacias lógicas en los razonamientos y cuellos de botella en el código. "
            "Eres frío, preciso y extremadamente eficiente."
        ),
        llm=llm,
        allow_delegation=False, # Este agente suele ser un 'doer', no delega
        verbose=True
    )