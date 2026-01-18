# AIAgents - Task

## 🔧 Objetivos de mejora

Refactorizar el código proporcionado para mejorar su **calidad, claridad y mantenibilidad**, alineadas con principios como **DRY**, **responsabilidad única** y **evitar ambigüedad contextual**.

1. **Eliminar duplicaciones y fragmentación de lógica.**
2. **Claridad y separación de responsabilidades** (cada tarea tiene su lógica bien delimitada).
3. **Uso más limpio del formato de texto dinámico** (str.format() vs. f-strings con placeholders).
4. **Evitar el hardcoding de slices ([:8000], [:4000])** fuera de contexto.
5. **Autoexplicatividad sin necesidad de comentarios extensos.**

### ✅ VERSIÓN REFACTORIZADA

#### `crew_components/tasks.py`

```python
from crewai import Task

def crear_tarea_identificacion_temas(agent, corpus_text, max_chars=8000):
    """Tarea para identificar entre 2 y 4 temas principales de un corpus."""
    description = (
        "Analiza el siguiente corpus y detecta entre 2 y 4 temas de investigación principales que estén claramente presentes en el texto.\n"
        "Un 'tema' debe representar una categoría o enfoque significativo del contenido, no palabras clave aisladas.\n"
        "Evita repeticiones, conceptos demasiado amplios o interpretaciones no respaldadas por el texto.\n\n"
        f"CORPUS (extracto):\n{corpus_text[:max_chars]}"
    )
    expected_output = (
        'Devuelve solo una respuesta en formato JSON, bajo la clave "topics".\n'
        'Ejemplo:\n{\n "topics": [\n "Modelos de lenguaje aplicados a la medicina",\n "Ética en inteligencia artificial"\n ]\n}'
    )
    return Task(description=description, expected_output=expected_output, agent=agent)

def _generar_sintesis_contexto(corpus_text, max_chars=4000):
   return f"--- CORPUS ORIGINAL (extracto) ---\n{corpus_text[:max_chars]}\n--- FIN DEL CORPUS ---\n\n"

def crear_tareas_generacion_paper(researcher, synthesizer, writer, topic, corpus_text):
    """Crea las tres tareas secuenciales: investigación, síntesis y escritura final."""

    # 1. Investigación
    investigacion = Task(
        description=(
            f'Realiza una investigación exhaustiva sobre: "{topic}". '
            "Identifica avances recientes, expertos clave, debates actuales y vacíos de conocimiento."
        ),
        expected_output=(
            "Un informe analítico detallado (mínimo 3 párrafos sustanciales). "
            "Al final, incluye una sección '**BIBLIOGRAFÍA**' con 5 referencias completas en formato APA."
        ),
        agent=researcher
    )

    # 2. Síntesis (con informe anterior + corpus)
    sintesis = Task(
        description=(
            "Tu misión es conectar ideas. A continuación tienes el informe de investigación y un extracto del corpus original. "
            "Tu trabajo es encontrar sinergias, contradicciones y vacíos de conocimiento entre ambos.\n\n"
            "--- INFORME DE INVESTIGACIÓN ---\n{context}\n--- FIN DEL INFORME ---\n\n"
            f"{_generar_sintesis_contexto(corpus_text)}"
            "Analiza ambos textos y produce tu síntesis."
        ),
        expected_output=(
            "Un análisis de síntesis bien argumentado (mínimo 2 párrafos). "
            "Al final, incluye una lista de 3 a 5 **'Oportunidades de Innovación'** concretas y bien fundamentadas que surjan de tu análisis."
        ),
        agent=synthesizer,
        context=[investigacion]
    )

    # 3. Escritura de paper (con ambos contextos anteriores)
    escritura = Task(
        description=(
            "Tu tarea final es escribir un paper científico completo en español. "
            "Utiliza OBLIGATORIAMENTE los siguientes materiales:\n\n"
            "--- MATERIAL 1: INFORME DE INVESTIGACIÓN Y BIBLIOGRAFÍA ---\n{context[0]}\n--- FIN DEL MATERIAL 1 ---\n\n"
            "--- MATERIAL 2: SÍNTESIS Y OPORTUNIDADES DE INNOVACIÓN ---\n{context[1]}\n--- FIN DEL MATERIAL 2 ---\n\n"
            "Usando estos materiales, redacta el paper. Asegúrate de incluir las referencias de la bibliografía en la sección final. "
            "Tu respuesta final DEBE ser únicamente el paper en formato markdown."
        ),
        expected_output=(
            "Un artículo científico completo en formato markdown, con Título, Abstract, Introducción, Desarrollo, Discusión, Conclusión y Referencias. "
            "Cada sección debe ser sustancial y estar directamente basada en los materiales proporcionados."
        ),
        agent=writer,
        context=[investigacion, sintesis]
    )
    return [investigacion, sintesis, escritura]
```

### 📌 Cambios clave explicados

| Mejora | Descripción |
| :--- | :--- |
| **Funciones auxiliares** | `_generar_sintesis_contexto` encapsula la lógica de corte del corpus. Facilita cambios futuros. |
| **Evita hardcoding innecesario** | Parámetros como `max_chars` son ahora ajustables desde la llamada. |
| **Claridad de roles** | Cada tarea tiene un nombre descriptivo (`investigacion`, `sintesis`, `escritura`) que refleja su propósito. |
| **Estructura limpia y reutilizable** | Textos largos están claramente organizados y las plantillas contextuales están bien delimitadas. |
| **No duplicación de lógica** | No se repite la estructura del texto ni su segmentación de corpus. |

### **✅ Ventajas adicionales**

- Listo para escalar: fácil añadir más tareas si decides expandir el pipeline.
- Transparente para debugging.
- Sustituible o testeable en partes (cada tarea es fácilmente aislable para pruebas unitarias o mocks).

---

### Versión Profesional y Completa

Perfecto. Vamos a convertir tu código en una **versión de producción profesional**, con una estructura clara, reutilizable, altamente mantenible y completamente alineada con principios como **SRP**, **DRY**, y **clean architecture**.

### ✅ ENFOQUE PROFESIONAL

Este rediseño incluye:

1. **Tipado estricto y uso de dataclasses** donde aplica.
2. **Separación de constantes, lógica de contexto y tareas.**
3. **Reutilización de lógica de truncado/formatos.**
4. **Uso de plantilla de texto multisección clara (markdown-style).**
5. **Formateo profesional de texto multilínea.**
6. **Preparado para testeo e integración en sistemas más grandes.**

#### 📦 ARCHIVO: `crew_components/tasks.py`

```python
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
```

### 📐 ¿Qué logras con esta versión?

| Ventaja | Detalle |
| :--- | :--- |
| **Profesionalismo** | Estructura clara, documentación implícita, nombres expresivos. |
| **Escalabilidad** | Fácil agregar más tareas, secciones o formatos de salida. |
| **Mantenibilidad** | Todo configurable desde `TaskConfig`, reusable en tests. |
| **Compatibilidad con tests** | Funciones puras, sin efectos colaterales. |
| **Separación de capas** | Lógica de truncado, formato de secciones y creación de tareas, todo modular. |

**🧪 ¿Quieres que te incluya también...?**

- ✅ Tests unitarios (pytest)
- ✅ Integración con Streamlit como frontend para lanzar tareas
- ✅ Versión REST con FastAPI para invocar estas tareas como endpoints

Solo dime qué necesitas a continuación.

---

### ✅ CAMBIOS CLAVE IMPLEMENTADOS

#### 🔧 ARQUITECTURA Y CALIDAD

| Mejora | Detalle |
| :--- | :--- |
| ✅ **Separación de responsabilidades** | Separación clara entre carga de corpus, procesamiento, UI y lógica de ejecución. |
| ✅ **Tipado estricto y validaciones defensivas** | Evita errores silenciosos y mejora el debugging. |
| ✅ **Mensajes de error robustos** | Para debugging más claro y tolerancia a errores de LLM. |
| ✅ **Variables y funciones con nombres semánticos** | Mejora la legibilidad profesional. |
| ✅ **Diseño extensible** | Lista para incorporar logs, métricas, trazas o control de errores más avanzado. |

#### 📦 CÓDIGO REFACTORIZADO: `app.py`

```python
import os
import json
from multiprocessing import Pool
import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from crewai import Crew, Process

# --- CARGA DE VARIABLES DE ENTORNO ---
load_dotenv()

# --- IMPORTACIONES LOCALES ---
from utils import leer_corpus, crear_docx, limpiar_json_output, validar_paper_markdown
from crew_components.agents import crear_agente_orquestador, crear_equipo_investigacion
from crew_components.tasks import crear_tarea_identificacion_temas, crear_tareas_generacion_paper

# --- CREW INDIVIDUAL POR TEMA ---
def ejecutar_equipo_para_tema(args):
    topic, corpus_text = args
    print(f"🚀 Iniciando equipo para el tema: {topic}")
    
    # Instanciamos LLM por proceso (necesario para multiprocessing seguro)
    llm = Ollama(model="ollama/llama3")
    
    researcher, synthesizer, writer = crear_equipo_investigacion(llm)
    tasks = crear_tareas_generacion_paper(researcher, synthesizer, writer, topic, corpus_text)
    
    crew = Crew(
        agents=[researcher, synthesizer, writer],
        tasks=tasks,
        process=Process.sequential
    )
    
    resultado_paper = crew.kickoff()
    print(f"✅ Equipo para '{topic}' ha finalizado.")
    
    return {
        "topic": topic,
        "paper": str(resultado_paper).strip()
    }

# --- UI PRINCIPAL ---
def main():
    st.set_page_config(page_title="Motor de Innovación Modular", page_icon="🧩", layout="wide")

    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h1 style='font-size: 2.8rem;'>🧩 Motor de Innovación y Desarrollo</h1>
        <p style='font-size: 1.2rem;'>Aplicación modular temática para generar papers usando AI Agentics en paralelo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("1. Sube tu corpus de documentos")
    archivos = st.file_uploader(
        "Arrastra o selecciona tus archivos (TXT, PDF):",
        type=["txt", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if st.button("🤖 Analizar y Generar en Paralelo"):
        if not archivos:
            st.error("⚠️ Por favor, sube al menos un archivo para analizar.")
            return

        st.markdown("---")
        st.subheader("🔬 Proceso Orquestado en Curso...")
        
        with st.status("Iniciando la misión...", expanded=True) as status:
            corpus = leer_corpus(archivos)
            
            if not corpus.strip():
                st.error("❌ El corpus está vacío o no se pudo leer.")
                return

            status.update(label="🔎 Director de Investigación analizando temas principales...")
            
            try:
                llm = Ollama(model="ollama/llama3")
                orquestador = crear_agente_orquestador(llm)
                tarea_temas = crear_tarea_identificacion_temas(orquestador, corpus)
                
                crew_temas = Crew(agents=[orquestador], tasks=[tarea_temas], process=Process.sequential)
                resultado_temas = crew_temas.kickoff()
                
                temas = extraer_temas_desde_resultado(resultado_temas)
                
                if not temas:
                    st.error("❌ No se pudieron identificar temas válidos en el corpus.")
                    return
                
                status.update(label=f"📚 Temas identificados: {', '.join(temas)}. Lanzando equipos en paralelo...")
                
            except Exception as e:
                st.error(f"Error al identificar temas: {e}")
                return

            # --- Ejecución en paralelo de equipos ---
            try:
                argumentos = [(tema, corpus) for tema in temas]
                with Pool(processes=len(temas)) as pool:
                    resultados = pool.map(ejecutar_equipo_para_tema, argumentos)
                
                st.session_state.final_results = resultados
                status.update(label="✅ ¡Misión completada! Todos los equipos han finalizado.", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"❌ Error durante la ejecución paralela de los equipos: {e}")
                return

    # --- Visualización de resultados ---
    if 'final_results' in st.session_state:
        mostrar_resultados(st.session_state.final_results)

# --- UTILIDADES DE PARSEO ---
def extraer_temas_desde_resultado(resultado_raw: str) -> list[str]:
    try:
        cleaned_str = limpiar_json_output(str(resultado_raw))
        data = json.loads(cleaned_str)
        raw_topics = data.get("topics", [])
    except Exception as e:
        raise ValueError(f"Error al interpretar la respuesta del orquestador: {e}")
        
    temas = []
    for item in raw_topics:
        if isinstance(item, str):
            temas.append(item)
        elif isinstance(item, dict):
            if 'name' in item:
                temas.append(item['name'])
            elif 'topic' in item:
                temas.append(item['topic'])
                
    return [t for t in temas if isinstance(t, str) and t.strip()]

def mostrar_resultados(resultados: list[dict]):
    st.markdown("---")
    st.subheader("🎉 Resultados de los Equipos de Investigación")
    
    for resultado in resultados:
        tema = resultado.get("topic", "Tema desconocido")
        contenido = resultado.get("paper", "").strip()
        
        with st.expander(f"📄 Paper sobre: **{tema}**", expanded=True):
            st.markdown(contenido)
            
            if not validar_paper_markdown(contenido):
                st.warning("⚠️ El contenido generado no cumple con los criterios mínimos de calidad.")
                continue
                
            try:
                archivo_docx = crear_docx(contenido)
                st.download_button(
                    label=f"📥 Descargar Paper sobre '{tema}'",
                    data=archivo_docx,
                    file_name=f"paper_{tema.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"download_{tema}"
                )
            except Exception as e:
                st.error(f"❌ Error al generar el archivo DOCX: {e}")

if __name__ == "__main__":
    main()
```

### 🧱 Mejoras para Producción

Si estás preparando este código para un sistema más amplio, considera lo siguiente:

| Mejora | Beneficio |
| :--- | :--- |
| **Logs (loguru)** | Mejor trazabilidad de errores y rendimiento en producción. |
| **Tests (pytest)** | Seguridad ante refactorizaciones futuras. |
| **Resiliencia (tenacity)** | Manejo de reintentos automático ante fallos de LLM. |
| **Persistencia** | Guardar resultados en base de datos o almacenamiento local. |
| **Containers (Docker)** | Despliegue profesional y reproducible. |

---

### ✅ Refactorización de Agentes (`crew_components/agents.py`)

Para llevar esto a un **nivel profesional**, aquí tienes una versión mejorada con tipado, docstrings y separación de responsabilidades.

#### 📦 ARCHIVO: `crew_components/agents.py`

```python
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
```

### 📌 Próximos pasos sugeridos

1. **Tests unitarios**: Validar la configuración de agentes.
2. **Configuración externa**: Mover prompts y roles a `agents_config.json`.
3. **Selector de perfiles**: Permitir elegir tipos de expertos desde la UI.
