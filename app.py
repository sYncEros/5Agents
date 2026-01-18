# app.py

import streamlit as st
from streamlit_elements import elements, mui, html
import plotly.graph_objects as go
import time
import random
import logging
from backend.core.layer_detector import analyze_text
from backend.core.motor_innovacion import render_motor_innovacion
from backend.core.statistics_manager import get_stats_manager
from backend.core.agents_manager import get_agents_manager

logger = logging.getLogger(__name__)

def display_agent_cards():
    """Muestra las cartas de agentes activos"""
    agents_manager = get_agents_manager()
    agents = agents_manager.get_active_agents()
    
    colors = ["#28a745", "#17a2b8", "#6f42c1", "#fd7e14"]
    
    for agent_name, color in zip(agents, colors):
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}11);
            border-left: 4px solid {color};
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        ">
            <strong>{agent_name}</strong><br>
            <small>Estado: ✅ activo</small>
        </div>
        """, unsafe_allow_html=True)

def display_process_flow():
    """Muestra el flujo del proceso de análisis"""
    st.markdown("""
    ### Flujo de Análisis:
    1. **Recepción** 📥 → Idea capturada
    2. **Distribución** 🔄 → Enviada a agentes
    3. **Análisis** 🔍 → Procesamiento paralelo
    4. **Síntesis** ⚡ → Convergencia de insights
    5. **Resultado** ✨ → Output enriquecido
    """)
    
    # Gráfico de flujo simple
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[1, 2, 3, 2, 1],
        mode='lines+markers',
        name='Flujo de Proceso',
        line=dict(color='#6f42c1', width=3),
        marker=dict(size=10, color=['#28a745', '#17a2b8', '#6f42c1', '#fd7e14', '#dc3545'])
    ))
    
    fig.update_layout(
        height=200,
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def process_with_agents(user_input, ritual_opt_in: bool = False):
    """Procesa la idea con agentes reales de CrewAI"""
    if not user_input.strip():
        st.warning("Por favor, ingresa alguna idea para procesar.")
        return
    
    stats_manager = get_stats_manager()
    agents_manager = get_agents_manager()
    
    with st.spinner("🤖 Procesando con agentes IA reales..."):
        try:
            # Procesar idea con agentes reales
            agent_responses = agents_manager.process_idea(user_input)
            
            # Registrar en estadísticas
            process_id = stats_manager.record_processing(user_input, agent_responses)
            
            st.success(f"✅ Procesamiento completado (ID: {process_id})")
            
            # Mostrar resultados reales de agentes
            st.markdown("### 🤖 Análisis de Agentes")
            for agent_name, response in agent_responses.items():
                with st.expander(f"Respuesta de {agent_name}"):
                    st.write(response)

            # Análisis de capas y segmentación
            analysis = analyze_text(user_input, ritual_opt_in=ritual_opt_in)
            
            st.markdown("### 🧭 Capas detectadas")
            if analysis.layers:
                st.write(", ".join(analysis.layers))
            else:
                st.write("Sin capas explícitas detectadas.")

            st.markdown("### 🧪 Rutas sugeridas")
            st.write(", ".join(analysis.routing))

            if analysis.guardrails:
                st.warning(f"Guardrails activos: {', '.join(analysis.guardrails)}")

            st.markdown("### 🔍 Segmentos y señales")
            for index, segment in enumerate(analysis.segments, start=1):
                with st.expander(f"Segmento {index}"):
                    st.write(segment.text)
                    if segment.layers:
                        st.caption(f"Capas: {', '.join(segment.layers)}")
                    if segment.emotions:
                        st.caption(
                            "Emociones: "
                            + ", ".join([f"{key}({value})" for key, value in segment.emotions.items()])
                        )
                    if segment.projections:
                        st.caption("Proyecciones: " + ", ".join(segment.projections))
        
        except Exception as e:
            st.error(f"❌ Error durante el procesamiento: {str(e)}")
            logger.error(f"Error en process_with_agents: {e}", exc_info=True)

def render_lab_ia():
    stats_manager = get_stats_manager()
    agents_manager = get_agents_manager()
    
    # Obtener estadísticas en tiempo real
    all_stats = stats_manager.get_all_stats()
    
    # CSS personalizado
    st.markdown("""
    <style>
    .hero-section {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .hero-section h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .hero-section p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header con gradientes
    st.markdown("""
    <div class="hero-section">
        <h1>🧠 sΨnc∑ros Lab.IA</h1>
        <p>Sistema transdisciplinario de agentes IA colaborativos</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar con agentes
    with st.sidebar:
        st.header("🤖 Agentes Activos")
        display_agent_cards()

        st.markdown("---")
        ritual_opt_in = st.checkbox("Modo ritual (opt-in)", value=False)

        st.markdown("---")
        st.subheader("📊 Estadísticas (En Tiempo Real)")
        st.metric("Ideas Procesadas", all_stats["ideas_processed"], f"+{all_stats['recent_increase']}")
        st.metric("Agentes Activos", all_stats["agents_active"])
        st.metric("Insights Generados", all_stats["insights_generated"])
        
        st.caption(f"📅 Actualizado: {all_stats['last_update']}")

    # Main interface
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Input de Idea Viva")
        user_input = st.text_area(
            "Fragmentos, reflexiones, hipótesis...",
            placeholder="Ej: La consciencia artificial podría emerger a través de la complejidad emergente de sistemas neuronales...",
            height=200
        )

        if st.button("🚀 Procesar con Agentes IA", type="primary"):
            process_with_agents(user_input, ritual_opt_in=ritual_opt_in)

        # Ejemplos de ideas
        st.markdown("### 💡 Ideas de Ejemplo:")
        ejemplos = [
            "La consciencia artificial emerge de la complejidad",
            "El tiempo es una construcción social del observador",
            "La creatividad humana vs algoritmos generativos",
            "Ética en sistemas autónomos de IA"
        ]

        for ejemplo in ejemplos:
            if st.button(f"💭 {ejemplo}", key=ejemplo):
                st.session_state.ejemplo_seleccionado = ejemplo

    with col2:
        st.subheader("⚡ Proceso de Análisis")
        display_process_flow()

        # Mostrar ejemplo seleccionado
        if 'ejemplo_seleccionado' in st.session_state:
            st.info(f"📝 Ejemplo seleccionado: {st.session_state.ejemplo_seleccionado}")
            if st.button("🔄 Procesar Ejemplo"):
                process_with_agents(st.session_state.ejemplo_seleccionado, ritual_opt_in=ritual_opt_in)
        
        # Mostrar histórico reciente
        st.markdown("### 📜 Procesamiento Reciente")
        history = stats_manager.get_processing_history(limit=5)
        if history:
            for record in reversed(history):
                with st.expander(f"🕐 {record['timestamp'][:16]}"):
                    st.write(f"**Idea:** {record['input_idea'][:100]}...")
                    st.write(f"**Estado:** {record['status']}")
        else:
            st.info("No hay procesamiento previo registrado.")


def main():
    st.set_page_config(
        page_title="sΨnc∑ros Workspace",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 1.5rem;">
            <h1 style="font-size: 2.6rem; margin-bottom: 0.2rem;">🧠 sΨnc∑ros Workspace</h1>
            <p style="font-size: 1.05rem; opacity: 0.9;">Entrada única para Laboratorio y Motor de Innovación</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_lab, tab_motor = st.tabs(["Laboratorio (Idea Viva)", "Motor de Innovación"])

    with tab_lab:
        render_lab_ia()

    with tab_motor:
        render_motor_innovacion()

if __name__ == "__main__":
    main()
