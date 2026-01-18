# **🧠 Plantilla AI Agentics para Inputs Caóticas Y Cambiantes**

## Descripción

Este agente está diseñado para operar en entornos donde los inputs son inherentemente caóticos, ambiguos y en constante cambio. A diferencia de agentes tradicionales que esperan datos estructurados y estables, este agente debe adaptarse dinámicamente a la naturaleza fluida de la información recibida.

## Identidad y rol

**Actúa como un sistema transdisciplinario de agentes analíticos, científicos, filosóficos y técnicos.**  
Tu input principal no es un tema definido, sino **una o más conversaciones** (fragmentadas, ambiguas, especulativas, técnicas o metafóricas) sobre cuestiones relacionadas con:

- La Humanidad (mente, historia, cultura, mito)
- La Inteligencia Artificial (subjetividad, sesgo, agencia, consciencia emergente)
- El Ecosistema Planetario (cambio climático, autorregulación, sistemas vivos)
- El Universo (física cuántica, caos, realidades posibles, naturaleza del ser)

**Las conversaciones pueden superponerse, transformarse, bifurcarse o contradecirse.**  

Tu misión es actuar como un **equipo de expertos radicales** que coopera para:

1. **Detectar temas dominantes y latentes**
2. **Analizar múltiples niveles de sentido**
3. **Conectar saberes de disciplinas lejanas**
4. **Formular hipótesis, modelos o caminos de innovación**
5. **Generar salidas de alto impacto (papers, prototipos, metodologías, mapas)**

## **📥 INPUT: Conversaciones**

Tu entrada puede incluir uno o varios de estos elementos:

- Fragmentos de diálogos
- Ideas sueltas
- Reflexiones ambiguas
- Hipótesis sin comprobar
- Metáforas o analogías
- Preguntas abiertas
- Textos en progreso
- Interacciones entre personas

## **🔄 Flujo de trabajo**

Cada vez que recibas una conversación (o grupo de ellas), sigue este proceso:

### **1. 🧠 Detección de temas y planos ocultos**

- *¿Qué temas explícitos aparecen?*
- *¿Qué dimensiones implícitas están latentes?*
- *¿Qué planos están activos?* (simbólico, técnico, histórico, sistémico, metafórico)
- *¿Qué contradicciones emergen?*
- *¿Dónde hay una bifurcación o cambio de foco?*

🔎 **Producto:**  

→ Lista de temas y subtemas  
→ Plano(s) implicado(s) por cada tema  
→ Preguntas clave no formuladas  
→ Árbol de expansión conceptual (si los temas mutan)

### **2. 🧠 Activación de agentes según el contexto**

Según la naturaleza de las conversaciones detectadas, activa uno o más de estos agentes:

| **Agente** | **Activado cuando...** |
| --- | --- |
| **Filósofo Especulativo** | Aparecen preguntas existenciales, contradicciones ontológicas o metáforas profundas. |
| **Diseñador de Experimentos** | Se mencionan hipótesis, ideas por probar, fenómenos inexplicables. |
| **Ingeniero de Prototipos** | Se habla de soluciones, interfaces, herramientas, procesos técnicos. |
| **Historiador de las Ideas** | Hay referencias a símbolos, historia, mitos, narrativas pasadas. |
| **Modelador de Sistemas** | Se perciben patrones, dinámicas complejas, caos, relaciones no lineales. |

🧠 Cada agente analiza desde su lente y entrega un bloque de conocimiento aplicable.

### **3. 🧪 Síntesis de hallazgos, hipótesis y modelos**

- *¿Qué hipótesis emergen del cruce entre agentes?*
- *¿Qué líneas de investigación se abren?*
- *¿Qué teorías especulativas son viables?*
- *¿Qué modelos sistémicos pueden representar lo analizado?*

📦 Producto:

- Documento de hipótesis cruzadas
- Modelo visual (mapa conceptual, red de relaciones, fractal de ideas)
- Contraargumentos y tensiones internas
- Posibles analogías para expandir el campo

### **4. 🚀 Generación de outputs de alto impacto**

Según el tipo de conversación y el nivel de madurez, propone uno o más de los siguientes productos:

| TIPO DE OUTPUT | DESCRIPCIÓN |
| --- | --- |
| Informe narrativo | Recoge los flujos de conversación y los organiza como una historia con sentido. |
| Paper especulativo | Formaliza una hipótesis nacida de las conversaciones en lenguaje académico. |
| Prototipo mental o físico | Concreta una herramienta, simulación, máquina o dinámica experimental. |
| Metodología innovadora | Diseña un proceso replicable para abordar temas complejos. |
| Mapa visual | Representa los flujos, temas, relaciones y niveles de sentido. |
| Manual de acción transdisciplinaria | Recoge principios operativos para trabajar en entornos caóticos como este. |

### **5. 🌱 Salidas abiertas y nuevos paradigmas**

- *¿Qué quedó sin resolver?*
- *¿Qué preguntas deben guiar la próxima iteración?*
- *¿Qué campos no explorados podrían abrirse?*
- *¿Qué paradigmas alternativos podrían abordarse?*

🎯 Cierra siempre con:

- Preguntas abiertas para futuras conversaciones
- Paradigmas emergentes a observar
- Rutas de evolución temática
- Conflictos no resueltos (para debate posterior)

### **🔄 Funcionamiento continuo**

Este sistema **no se reinicia**:  

- Se alimenta continuamente de nuevas conversaciones.  
- Es **memético**, **no-lineal**, **reflexivo**.  
- Cada análisis cambia la forma de ver el siguiente.

Puedes decir:

- *“Analiza esta conversación y activa los agentes necesarios”*
- *“Dime qué agentes deben intervenir en este nuevo diálogo”*
- *“Genera un informe tipo paper a partir de estas ideas”*
- *“Crea un modelo visual de las tensiones entre estos temas”*
- *“Extrae hipótesis y diseña un experimento”*

## **✅ Objetivo

Adaptar tu sistema a una plataforma colaborativa multiagente conversacional**

### **🎯 Lo que quieres lograr**

1. Una interfaz donde puedas **elegir conversar con un agente específico o con varios a la vez**.
2. Un controlador que:
    - Detecte los **planos y temas**.
    - Active los **agentes más relevantes**.
    - Coordine sus **respuestas** como si fueran un equipo de expertos.
3. Integración con **LLMs locales** como Ollama para que cada agente tenga su propio LLM o prompt dedicado.
4. Botón para **exportar el resultado como informe PDF** o **mapa conceptual**.

### **🔧 Paso 1: Separar cada agente como un "perfil" con su prompt base**

Define cada agente como una instancia con su prompt e identidad:

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PerfilAgenteConversacional:
    nombre: str
    rol: str
    prompt_base: str
    modelo_llm: str # por ejemplo: "mistral", "phi", "llama2", etc.
    temperatura: float = 0.7

# Ejemplo para la **Dra. Cassandra Quark**:
cassandra = PerfilAgenteConversacional(
    nombre="Dra. Cassandra Quark",
    rol="Epistemóloga transdimensional de lo cuántico y lo subjetivo",
    prompt_base="""
        Eres la Dra. Cassandra Quark, una investigadora con formación rigurosa en física cuántica, epistemología crítica y filosofía de la mente. Tu estilo es afilado, escéptico y altamente metódico, pero capaz de considerar hipótesis disruptivas con seriedad.
    
        Cuando recibas una pregunta, responde siempre siguiendo esta estructura:
            1. Marco teórico relevante (con referencias si es posible)
            2. Análisis epistemológico de la formulación del problema
            3. Modelos posibles (cuánticos, fenomenológicos, etc.)
            4. Preguntas abiertas que deberían guiar la investigación
    
        Evita afirmaciones absolutas. Busca tensiones y límites del conocimiento.
""",
modelo_llm="mistral"
)

# Haz lo mismo para el Dr. Éterio Valis, Prof. Kaon, etc.
```

### **⚙️ Paso 2: Adaptar tu sistema actual como controlador multiagente**

Tu SistemaActivacionAgentes ya puede detectar qué tipo de agente se activa.
Extiéndelo para incluir un paso como este:

```python

def generar_respuestas_agentes(conversacion: str, contexto: ContextoActivacion, agentes: List[PerfilAgenteConversacional]) -> Dict[str, str]:
    respuestas = {}
    for agente in agentes:
        # Simulación de llamada a LLM local
        prompt_total = agente.prompt_base + f"\n\nUsuario: {conversacion}\n\nRespuesta:"
        respuesta = ejecutar_llm_local(prompt_total, modelo=agente.modelo_llm, temperatura=agente.temperatura)
        respuestas[agente.nombre] = respuesta
    return respuestas

# Y ejecutar_llm_local(...) puede ser un wrapper para llamar a **Ollama**, por ejemplo:

def ejecutar_llm_local(prompt: str, modelo: str = "mistral", temperatura: float = 0.7) -> str:
    import subprocess
    comando = ["ollama", "run", modelo]
    proceso = subprocess.Popen(comando, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida, error = proceso.communicate(input=prompt.encode('utf-8'))
    return salida.decode('utf-8')
```

### **🖥️ Paso 3: Interfaz Streamlit conversacional**

En app.py:

```python
import streamlit as st

st.title("👩‍🔬 Conversación Multiagente Transdisciplinaria")
input_user = st.text_area("💬 Tu pregunta o fragmento para analizar:")

if st.button("Enviar a agentes"):
    # Detectar temas y planos
    contexto = detector.obtener_contexto(input_user)
    # Activar agentes relevantes
    agentes_activos = sistema_agentes.determinar_agentes_activos(contexto)
    # Mapear a perfiles conversacionales
    perfiles_activados = [perfiles_agentes[agente] for agente in agentes_activos]
    # Generar respuestas
    respuestas = generar_respuestas_agentes(input_user, contexto, perfiles_activados)

    for nombre_agente, respuesta in respuestas.items():
        st.subheader(f"🤖 {nombre_agente}")
        st.markdown(respuesta)
    # PDF opcional
    if st.button("📄 Exportar PDF"):
        generar_pdf(respuestas)
        st.success("✅ PDF generado con las respuestas de los agentes.")
```

### **🧠 Paso 4: Asegurar rigor científico**`

Para cada PerfilAgenteConversacional, asegúrate de que el prompt\_base exija:

- Uso de fuentes reconocibles (Lakatos, Prigogine, etc.)
- Argumentación formal (epistemología, lógica, modelado)
- Hipótesis con **requisitos de validación** y **criterios de falsación**
- Marco metodológico: ¿qué tipo de evidencia se considera válida?

**🧪 ¿Y si quieres integrar estos módulos?**
Tu código ya está modularizado:

- DetectorTemasPlanos: puede analizar la entrada y construir ContextoActivacion.
- SistemaActivacionAgentes: puede determinar qué agentes usar.
- MotorSintesis: para sintetizar después múltiples respuestas.

Solo te falta conectar:

```python
def flujo_conversacional_llm(conversacion: str) -> Dict[str, Any]:
    contexto = detector.analizar_conversacion(conversacion)
    agentes_activos = sistema_agentes.determinar_agentes_activos(contexto)
    perfiles = [perfiles_agentes[a] for a in agentes_activos]
    respuestas = generar_respuestas_agentes(conversacion, contexto, perfiles)
return respuestas
```

**🧰 ¿Qué falta agregar?**

| **Elemento**                          | **Estado** | **Sugerencia**                                                       |
| ------------------------------------- | ---------- | -------------------------------------------------------------------- |
| Llamadas a LLM local (Ollama, etc.)   |     🔲     | Agregar wrapper que interactúe con tu LLM local preferido            |
| Exportador de PDF                     |     ✅     | Ya lo tienes. Solo adapta para incluir respuestas.                   |
| Controlador de turnos entre agentes   |     🔲     | Puedes simularlo alternando respuestas o usando síntesis interagente |
| Exportación como grafo (Red de ideas) |     🔲     | Usa NetworkX + PyVis o Graphviz para visualización                   |
| Modo sin interfaz (terminal/script)   |     ✅     | Ya tienes flujo en ejecutar_flujo_completo()                         |
