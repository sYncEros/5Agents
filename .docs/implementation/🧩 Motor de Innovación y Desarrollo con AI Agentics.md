# 🧩 Motor de Innovación y Desarrollo con AI Agentics

Aplicación modular basada en agentes inteligentes para generar papers académicos a partir de un corpus de documentos, utilizando el framework **CrewAI** y modelado con **Ollama (LLaMA3)**.

---

## 🚀 Características

- Interfaz visual con **Streamlit**.
- Procesamiento de múltiples archivos `.txt` y `.pdf`.
- Identificación automática de **temas principales**.
- Ejecución **paralela** de equipos de agentes para cada tema.
- Generación de artículos científicos completos en **markdown** y **DOCX**.
- Descarga individual o empaquetada en `.zip`.

---

## 🛠️ Requisitos

- Python >= 3.10
- [Ollama](https://ollama.com/) instalado y corriendo localmente.

### 📦 Dependencias

Instala con:

```bash
pip install -r requirements.txt
```

Ejemplo de `requirements.txt`:

```txt
streamlit
python-dotenv
langchain
crewai
crewai-tools
PyPDF2
python-docx
```

---

## 📁 Estructura del proyecto

```
.
├── app.py                  # App principal de Streamlit
├── crew_components/
│   ├── agents.py           # Definición de agentes (orquestador, investigador, etc)
│   └── tasks.py            # Definición de tareas y flujos
├── utils.py                # Funciones auxiliares
├── .env                    # Variables de entorno
├── README.md               # Este archivo
```

---

## ▶️ Uso

1. Ejecuta el servidor de Ollama:

```bash
ollama run llama3
```

2. Inicia la aplicación:

```bash
streamlit run app.py
```

3. Carga tus documentos y deja que los agentes trabajen por ti 🧠🤖

---

## 🧠 Agentes disponibles

| Rol                      | Función principal                                     |
| ------------------------ | ----------------------------------------------------- |
| Director de Orquesta     | Identifica los temas centrales del corpus             |
| Investigador Científico  | Explora literatura y tendencias sobre un tema         |
| Analista de Conocimiento | Conecta corpus con investigación para hallar insights |
| Redactor Científico      | Redacta el paper académico completo                   |

---

## 📤 Salida generada

- Visualización del contenido markdown dentro de la app.
- Descarga individual `.docx` por paper.
- Descarga grupal `.zip` con todos los papers generados.

---

## 🧪 Pruebas recomendadas

- Prueba con corpus técnicos y variados para validar la detección de temas.
- Evalúa papers generados con herramientas de calidad científica (Grammarly, AI detector, etc).

---

## 📬 Contacto

> Proyecto de automatización de flujos cognitivos con IA.
> Desarrollado con ❤️ por [Tu Nombre o Equipo].

---

## 📝 Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
