# components/controller/ExportSystem.py
import datetime
import traceback
from pathlib import Path
from typing import cast

import streamlit as st
from outputs.generador_outputs import GeneradorOutputs, TipoOutput


def mostrar_opciones_exportacion(sintesis_final, debug: bool = False):
    st.markdown("### 📥 Exportar resultado")

    opciones = [e.name for e in TipoOutput]
    if not opciones:
        st.error("No hay tipos de output disponibles.")
        return

    tipo_output = st.selectbox("Tipo de output", opciones, index=0)
    if not tipo_output:
        st.error("Debe seleccionar un tipo de output válido.")
        return

    try:
        tipo = TipoOutput[cast(str, tipo_output)]
    except Exception:
        st.error("Debe seleccionar un tipo de output válido.")
        return

    try:
        generador = GeneradorOutputs()
        output = generador.generar_output(tipo, sintesis_final)

        # Carpeta de exportación
        carpeta = Path("outputs/exportados")
        carpeta.mkdir(parents=True, exist_ok=True)

        # Nombre con timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = carpeta / f"output_{tipo.value}_{timestamp}.md"

        generador.exportar_output(output, file_path.stem)

        st.markdown("---")
        st.markdown("#### ✅ Resultado generado:")
        st.markdown(output.contenido)

        # Botón de descarga
        if file_path.exists():
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"📄 Descargar {tipo.value.upper()}",
                    data=f,
                    file_name=file_path.name,
                    mime="text/markdown" if tipo.value == "md" else "application/json"
                )

        # Debug info
        if debug:
            st.markdown("#### 🛠 Debug info")
            st.json({
                "tipo": tipo.name,
                "archivo": str(file_path),
                "longitud_contenido": len(output.contenido or ""),
                "timestamp": timestamp
            })

    except Exception as e:
        st.error("❌ Error al generar el output")
        st.text_area("Detalles", traceback.format_exc(), height=200)
