# crew_compoents/task.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from crewai import Task

# === Configuración por defecto ===
@dataclass(frozen=True)
class TaskConfig:
    max_corpus_chars_identificacion: int = 8000
    max_corpus_chars_sintesis: int = 4000

# === Utilidades ===
def truncar_texto(texto: str, max_chars: int) -> str:
    """Trunca el texto respetando el límite de caracteres, sin cortar palabras."""
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars].rsplit(' ', 1)[0] + "..."

def wrap_seccion(titulo: str, contenido: str) -> str:
    """Formatea secciones con delimitadores estándar."""
    return f"--- {titulo.upper()} ---\n{contenido.strip()}\n--- FIN DE {titulo.upper()} ---\n\n"

# === Tareas ===
def crear_tarea_identificacion_temas(agent, corpus_text: str, config: TaskConfig = TaskConfig()) -> Task:
    """Genera tarea para identificar de 2 a 4 temas principales en el corpus."""
    corpus_recortado = truncar_texto(corpus_text, config.max_corpus_chars_identificacion)
    
    description = (
        "Analiza el siguiente corpus y detecta entre 2 y 4 **temas de investigación principales** claramente presentes en el texto.\n"
        "- Un *tema* debe representar una categoría o enfoque significativo, **no** palabras clave aisladas.\n"
        "- Evita repeticiones, conceptos demasiado amplios o interpretaciones no respaldadas.\n\n"
        f"{wrap_seccion('Corpus (extracto)', corpus_recortado)}"
    )

    expected_output = (
        "Devuelve solo una respuesta en formato JSON, bajo la clave `topics`.\n\n"
        "**Ejemplo:**\n```json\n{\n \"topics\": [\n \"Modelos de lenguaje aplicados a la medicina\",\n \"Ética en inteligencia artificial\"\n ]\n}\n```"
    )
    
    return Task(description=description, expected_output=expected_output, agent=agent)

def crear_tareas_generacion_paper(
    researcher, synthesizer, writer, topic: str, corpus_text: str, config: TaskConfig = TaskConfig()
) -> List[Task]:
    """Genera las tareas de investigación, síntesis y redacción del paper científico."""
    
    corpus_sintesis = truncar_texto(corpus_text, config.max_corpus_chars_sintesis)

    # 1. INVESTIGACIÓN
    task_research = Task(
        description=(
            f"Realiza una investigación exhaustiva sobre el tema: \"{topic}\".\n\n"
            "- Identifica avances recientes\n"
            "- Menciona expertos clave y debates actuales\n"
            "- Detecta vacíos de conocimiento\n"
        ),
        expected_output=(
            "Un informe analítico detallado (mínimo 3 párrafos sustanciales).\n\n"
            "Al final, incluye una sección **BIBLIOGRAFÍA** con 5 referencias completas en formato APA."
        ),
        agent=researcher
    )

    # 2. SÍNTESIS
    task_synthesis = Task(
        description=(
            "Tu misión es **conectar ideas** entre el informe de investigación y el corpus original.\n\n"
            + wrap_seccion("Informe de Investigación", "{context}")
            + wrap_seccion("Corpus Original (extracto)", corpus_sintesis)
            + "Analiza ambos textos y produce una síntesis que evidencie:\n"
            "- Sinergias\n"
            "- Contradicciones\n"
            "- Vacíos de conocimiento\n"
        ),
        expected_output=(
            "Un análisis bien argumentado (mínimo 2 párrafos).\n\n"
            "Al final, incluye una lista de **3 a 5 Oportunidades de Innovación**, claras y fundamentadas."
        ),
        agent=synthesizer,
        context=[task_research]
    )

    # 3. ESCRITURA DEL PAPER
    task_write = Task(
        description=(
            "Tu tarea final es redactar un **paper científico completo** en español usando los siguientes materiales:\n\n"
            + wrap_seccion("Material 1: Informe de Investigación y Bibliografía", "{context[0]}")
            + wrap_seccion("Material 2: Síntesis y Oportunidades de Innovación", "{context[1]}")
            + "Asegúrate de integrar y referenciar el contenido correctamente. Usa estilo académico riguroso."
        ),
        expected_output=(
            "Un artículo completo en formato **markdown**, con las siguientes secciones:\n\n"
            "- Título\n- Abstract\n- Introducción\n- Desarrollo\n- Discusión\n- Conclusión\n- Referencias\n\n"
            "**Importante**: El contenido debe basarse únicamente en los materiales proporcionados."
        ),
        agent=writer,
        context=[task_research, task_synthesis]
    )

    return [task_research, task_synthesis, task_write]