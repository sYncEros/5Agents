import streamlit as st
import os
from sistema_agentes import SistemaActivacionAgentes, ContextoActivacion
from detector_temas_planos import DetectorTemasPlanos
from motor_sintesis import MotorSintesis
from pathlib import Path

# Configuración general
st.set_page_config(
    page_title="Sistema Transdisciplinario de Análisis",
    layout="wide"
)

st.title("🧠 Sistema Transdisciplinario de Análisis Conversacional")

# Entrada de texto
st.markdown("### 📌 Ingresa una conversación o texto para analizar:")
texto_usuario = st.text_area("Conversación", height=300, placeholder="Pega aquí la conversación o análisis...")

# Parámetros de activación
st.sidebar.header("⚙️ Parámetros de análisis")
nivel_abstraccion = st.sidebar.slider("Nivel de abstracción", 0.0, 1.0, 0.7)
nivel_especulacion = st.sidebar.slider("Nivel de especulación", 0.0, 1.0, 0.6)
nivel_tecnico = st.sidebar.slider("Nivel técnico", 0.0, 1.0, 0.5)

if st.button("🔍 Ejecutar Análisis Transdisciplinario"):
    if not texto_usuario.strip():
        st.warning("⚠️ Debes ingresar un texto para analizar.")
        st.stop()

    # Paso 1: Detección de temas y planos
    detector = DetectorTemasPlanos()
    resultado_deteccion = detector.analizar_conversacion(texto_usuario)

    # Crear contexto para activación
    contexto = ContextoActivacion(
        planos_detectados=[plano.value for plano in resultado_deteccion["planos_activos"]],
        temas_principales=[t.nombre for t in resultado_deteccion["temas_explícitos"]],
        contradicciones=resultado_deteccion["contradicciones_emergentes"],
        bifurcaciones=resultado_deteccion["bifurcaciones_detectadas"],
        nivel_abstraccion=nivel_abstraccion,
        nivel_especulacion=nivel_especulacion,
        nivel_tecnico=nivel_tecnico
    )

    # Paso 2: Activar agentes
    sistema = SistemaActivacionAgentes()
    analisis_agentes = sistema.analizar_con_agentes(texto_usuario, contexto)

    # Paso 3: Síntesis colaborativa
    motor = MotorSintesis()
    sintesis_final = motor.sintetizar_analisis_agentes(analisis_agentes)

    # Mostrar resultados por secciones
    st.success(f"✅ Análisis completado. Nivel de madurez: {sintesis_final.nivel_madurez_sintesis:.2f}")

    # Pestañas de resultados
    tab1, tab2, tab3, tab4 = st.tabs(["🌐 Temas & Planos", "🧠 Agentes", "📊 Síntesis", "📥 Exportar"])

    with tab1:
        st.markdown("### 🌐 Temas Detectados")
        for tema in resultado_deteccion["temas_explícitos"]:
            st.markdown(f"- **{tema.nombre}** (explicitez: {tema.nivel_explicito:.2f}) — planos: {', '.join([p.value for p in tema.planos_activos])}")

        st.markdown("### 💥 Contradicciones")
        st.write(resultado_deteccion["contradicciones_emergentes"])

        st.markdown("### 🌱 Bifurcaciones")
        st.write(resultado_deteccion["bifurcaciones_detectadas"])

    with tab2:
        st.markdown("### 🧠 Agentes Activados")
        for tipo, analisis in analisis_agentes.items():
            with st.expander(f"👤 {tipo.value}"):
                st.markdown("**Hallazgos:**")
                st.write(analisis.hallazgos_principales)
                st.markdown("**Hipótesis:**")
                st.write(analisis.hipotesis_generadas)
                st.markdown("**Metodología:**")
                st.write(analisis.metodologia_sugerida)

    with tab3:
        st.markdown("### 🔄 Hipótesis Cruzadas")
        for h in sintesis_final.hipotesis_cruzadas:
            st.markdown(f"- **{h.enunciado}** (especulación: {h.nivel_especulacion:.2f})")
            st.markdown(f"  - Evidencias: {h.evidencias_convergentes}")
            st.markdown(f"  - Contraargumentos: {h.contraargumentos}")

        st.markdown("### 📌 Paradigmas Emergentes")
        st.write(sintesis_final.paradigmas_emergentes)

    with tab4:
        st.markdown("### 📥 Exportar informe")
        output_path = Path("informe_colaborativo_IA.pdf")

        from generador_pdf import generar_informe_pdf  # Tu generador PDF
        generar_informe_pdf(texto_usuario, analisis_agentes, sintesis_final, output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                label="📄 Descargar PDF del informe",
                data=f,
                file_name="informe_colaborativo_IA.pdf",
                mime="application/pdf"
            )
