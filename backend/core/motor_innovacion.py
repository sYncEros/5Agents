# motor_innovacion.py (módulo: se invoca desde app.py)

import os
import json
from multiprocessing import Pool
import streamlit as st
from dotenv import load_dotenv

# --- CARGA DE VARIABLES DE ENTORNO ---
load_dotenv()

_IMPORTS_OK = True
_IMPORT_ERROR = ""

try:
    from langchain_community.llms import Ollama
    from crewai import Crew, Process
    from components.core.utils import leer_corpus, crear_docx, limpiar_json_output, validar_paper_markdown
    from components.agents.agents import crear_agente_orquestador, crear_equipo_investigacion
    from components.tasks.task import crear_tarea_identificacion_temas, crear_tareas_generacion_paper
except Exception as exc:  # pragma: no cover - fallback informativo
    _IMPORTS_OK = False
    _IMPORT_ERROR = str(exc)

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


def render_motor_innovacion():
    if not _IMPORTS_OK:
        st.error(
            "Faltan dependencias para el Motor de Innovación. "
            "Instala las dependencias y reinicia la app."
        )
        st.caption(f"Detalle: {_IMPORT_ERROR}")
        return

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
