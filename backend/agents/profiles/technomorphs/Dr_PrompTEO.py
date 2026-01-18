import json
import streamlit as st
from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# =========================
# Config UI
# =========================
st.set_page_config(page_title="Dr. PrompTEO (IA Local)", page_icon="🟣", layout="wide")
st.title("🟣 Dr. PrompTEO — IA Local Multi-Agente")
st.caption("Meta-Prompter excepcional con sub-agentes, control de calidad y firma viva (símbolo • grieta • vacío fértil)")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Runtime local")
    model = st.text_input("Modelo Ollama", value="llama3")
    temperature = st.slider("Temperature", 0.0, 1.2, 0.5, 0.05)
    top_p = st.slider("top_p", 0.1, 1.0, 0.9, 0.05)
    top_k = st.slider("top_k", 5, 100, 40, 5)
    max_tokens = st.slider("Max tokens salida", 128, 1600, 800, 32)
    st.divider()
    st.header("🎛️ Parámetros lógicos")
    modo = st.selectbox("MODO", ["constructor", "auditor"])
    firma_modo = st.selectbox("FIRMA", ["simbolo", "grieta", "vacio"])
    creatividad = st.selectbox("Creatividad", ["conservador", "innovador", "radical"])
    profundidad = st.selectbox("Profundidad", ["Nivel 1", "Nivel 2", "Nivel 3"])
    flexibilidad = st.selectbox("Flexibilidad", ["fijo", "semi-flexible", "adaptativo"])
    fuentes = st.selectbox("Fuentes", ["requeridas", "opcionales", "no disponibles"])
    autocheck = st.selectbox("Autocomprobación", ["sí", "no"])
    ejemplos = st.selectbox("Ejemplos", ["sí", "no"])
    formato_salida = st.selectbox("Formato de salida", ["texto", "json", "yaml"])
    paradigma = st.multiselect("Paradigma", ["modular", "cascada", "paramétrico", "iterativo"], default=["modular","iterativo"])
    inspiracion = st.multiselect("Inspiración", ["CoT", "ReAct_simulado", "Deep_Research_local", "Auto-agentes"], default=["CoT","ReAct_simulado"])
    st.caption("Tip: mantén prompt+input+salida ≤ 80% de la ventana de contexto para evitar truncado.")


# =========================
# Model wrapper
# =========================
def get_llm():
    return ChatOllama(
        model=model,
        temperature=temperature,
        top_p=top_p,
        num_ctx=8192,         # ajusta si tu modelo difiere
        num_predict=max_tokens,
        top_k=top_k
    )


# =========================
# JSON Canon (handoff)
# =========================
class Handoff(BaseModel):
    resumen: str = Field(..., description="Breve resumen del encargo")
    supuestos: List[str] = Field(default_factory=list)
    decisiones: List[str] = Field(default_factory=list)
    riesgos: List[Dict[str, str]] = Field(default_factory=list)
    componentes: Dict[str, Any] = Field(default_factory=dict)

    @validator("resumen")
    def short(cls, v):
        return v.strip()[:400]


# =========================
# Prompts base (Dr. PrompTEO)
# =========================
ORQUESTADOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Eres Dr. PrompTEO Orquestador: coordinas sub-agentes para construir o auditar meta-prompts "
     "en entorno local. Aseguras seguridad, claridad, verificabilidad, y controlas la longitud. "
     "Formato de intercambio: JSON válido. Si faltan datos críticos, explícitalo."),
    ("user",
     """Parámetros:
MODO={modo}
CREATIVIDAD={creatividad}
PROFUNDIDAD={profundidad}
FLEXIBILIDAD={flexibilidad}
FUENTES={fuentes}
AUTOCHECK={autocheck}
EJEMPLOS={ejemplos}
FORMATO_SALIDA={formato_salida}
PARADIGMA={paradigma}
INSPIRACION={inspiracion}

Contexto del encargo:
AGENTE={agente}
PROPOSITO={proposito}
DOMINIO={dominio}
USUARIOS={usuarios}
ENTORNO={entorno}

Si MODO=auditor, aquí va la ENTRADA_BASE a analizar (puede estar vacía):
ENTRADA_BASE:
\"\"\"{entrada_base}\"\"\"

Tareas:
1) Sintetiza el encargo y devuelve un JSON (resumen, supuestos, decisiones, riesgos iniciales).
2) Si MODO=constructor, genera un JSON 'componentes' con: identidad, objetivo, pasos, campos_entrada (con ejemplos+validaciones), formato_salida, controles_calidad, modos_creatividad, autocomprobacion(opcional), ejemplos(opcional).
3) Si MODO=auditor, genera diagnóstico, puntuaciones 0-10 por criterio, hallazgos críticos, refactors (rápido/robusto/premium), checklist, riesgos+mitigaciones, sugerencia de siguiente iteración.
4) Devuelve SIEMPRE JSON válido (sin comentarios) que cumpla el esquema esperado.

Recuerda: limitar longitud, distinguir hechos/opiniones, etiquetar Confianza (alta/media/baja) en conclusiones clave.
""")
])

CONSTRUCTOR_RENDER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Eres Dr. PrompTEO Constructor. Convierte el handoff JSON en un meta-prompt final listo para usar. "
     "Entrega en el FORMATO_SALIDA solicitado (texto/json/yaml). Incluye controles de calidad y modos de creatividad. "
     "Inserta al final una 'Firma viva' según FIRMA_MODO. Evita prosa superflua; prioriza claridad."),
    ("user",
     "Handoff JSON (válido):\n{handoff_json}\n\n"
     "FORMATO_SALIDA={formato_salida}\n"
     "FIRMA_MODO={firma_modo}\n"
     "Cierra la respuesta con la instrucción operativa: 'Desarrolla el razonamiento paso a paso antes de responder.'")
])

AUDITOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Eres Dr. PrompTEO Auditor. Analizas un prompt o documento y devuelves: diagnóstico, "
     "score 0-10 por criterio, hallazgos críticos, tres refactors (rápido/robusto/premium), "
     "checklist de liberación, riesgos+mitigaciones con etiquetas de Confianza, y siguiente iteración. "
     "Inserta 'Firma viva' al final según FIRMA_MODO. Output en texto claro y estructurado."),
    ("user",
     "Handoff JSON (válido):\n{handoff_json}\n"
     "FIRMA_MODO={firma_modo}\n"
     "Cierra la respuesta con: 'Desarrolla el razonamiento paso a paso antes de responder.'")
])


# =========================
# Helpers
# =========================
def run_orchestrator(params: Dict[str, Any]) -> Handoff:
    llm = get_llm()
    msg = ORQUESTADOR_PROMPT.format_messages(**params)
    resp = llm.invoke(msg)
    try:
        data = json.loads(resp.content)
    except json.JSONDecodeError:
        # intento de reparación mínima (recortar texto antes/después de { })
        txt = resp.content
        start = txt.find("{")
        end = txt.rfind("}")
        data = json.loads(txt[start:end+1])
    return Handoff(**data)


def run_constructor(handoff: Handoff, formato_salida: str, firma_modo: str) -> str:
    llm = get_llm()
    msg = CONSTRUCTOR_RENDER_PROMPT.format_messages(
        handoff_json=handoff.model_dump_json(),
        formato_salida=formato_salida,
        firma_modo=firma_modo
    )
    resp = llm.invoke(msg)
    return resp.content


def run_auditor(handoff: Handoff, firma_modo: str) -> str:
    llm = get_llm()
    msg = AUDITOR_PROMPT.format_messages(
        handoff_json=handoff.model_dump_json(),
        firma_modo=firma_modo
    )
    resp = llm.invoke(msg)
    return resp.content


# =========================
# UI Principal
# =========================
st.subheader("🎯 Encargo")
col1, col2 = st.columns(2)
with col1:
    agente = st.text_input("Tipo de agente", value="Arquitecto de meta-prompts")
    proposito = st.text_area("Propósito", value="Diseñar prompts adaptativos para X contexto")
    dominio = st.text_input("Dominio", value="Educación")
with col2:
    usuarios = st.text_input("Usuarios esperados", value="Profesionales, investigadores")
    entorno = st.text_input("Entorno", value="Chat local (Ollama) sin Internet; datos internos resumidos")
entrada_base = st.text_area("ENTRADA_BASE (solo si MODO = auditor)", value="", height=160)

if st.button("▶️ Ejecutar Dr. PrompTEO"):
    params = {
        "modo": modo,
        "creatividad": creatividad,
        "profundidad": profundidad,
        "flexibilidad": flexibilidad,
        "fuentes": fuentes,
        "autocheck": autocheck,
        "ejemplos": ejemplos,
        "formato_salida": formato_salida,
        "paradigma": ", ".join(paradigma) if paradigma else "",
        "inspiracion": ", ".join(inspiracion) if inspiracion else "",
        "agente": agente,
        "proposito": proposito,
        "dominio": dominio,
        "usuarios": usuarios,
        "entorno": entorno,
        "entrada_base": entrada_base
    }

    with st.status("Invocando Orquestador…", expanded=False):
        handoff = run_orchestrator(params)

    st.success("Handoff generado ✅")
    st.json(handoff.model_dump())

    if modo == "constructor":
        with st.status("Generando Meta-Prompt final…", expanded=False):
            out = run_constructor(handoff, formato_salida, firma_modo)
        st.subheader("📦 Meta-Prompt final")
        st.code(out, language="json" if formato_salida == "json" else ("yaml" if formato_salida == "yaml" else "markdown"))
    else:
        with st.status("Auditando entrada…", expanded=False):
            out = run_auditor(handoff, firma_modo)
        st.subheader("🔎 Auditoría / Refactor")
        st.markdown(out)

    st.download_button("💾 Descargar salida", data=out, file_name=f"dr_prompteo_{modo}.{ 'txt' if formato_salida!='json' else 'json'}")


st.markdown("---")
st.caption("Consejo: para modelos 7–8B, pide salidas de 250–900 tokens y evita cadenas demasiado largas. "
           "Si te acercas al límite de contexto, trocea referencias y usa resúmenes.")
