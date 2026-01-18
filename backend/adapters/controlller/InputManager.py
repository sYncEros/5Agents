# components/controlller/InputManager.py

import streamlit as st


def getUserText():
    st.markdown("### 📌 Ingresa una conversación o texto para analizar:")
    return st.text_area("Conversación", height=300, placeholder="Pega aquí el texto...")
