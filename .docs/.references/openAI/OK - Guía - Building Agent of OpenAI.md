**AI Agents Builder Guide of API / OpenAI**
1.  **Montarlo técnicamente**
**Opción A:** *API OpenAI + Python*
**📂 Requisitos**
1.  **Install libraries**
pip install openai
1.  **Keep your API KEY:**
*python*
import **os**
**os**.environ\["OPENAI\_API\_KEY"\] = "\_\_\_\_\_\_\_\_\_\_\_\_\_"
1.  **Código base**
*python*
from openai import OpenAI
**client** = OpenAI( )
*\# System Prompt*
**system\_prompt** = *"""*
*Eres un agente que...*
*"""*
*\# Example of conversation*
**messages = \[**
{"role": "system", "content": **system\_prompt**},
{"role": "user", "content": *"Imagina que vamos a..."*}
\]
**response** = **client**.**chat**.completions.create(
model="gpt-4", *\# Others Models*
messages = messages,
temperatura = 0.8
)
print(**response**.choices\[0\].**message**.content)
**✅ Puedes cambiar el content del usuario para activar los modos**
-   *"Colapsa tu función y adopta el modo/rol \_\_\_\_\_\_\_"*
-   *"Cambia de manifestación y descríbete"*
-   *...  
    *
### ****Con los Agentes de ChatGPT****
En la interfaz de ChatGPT Plus (o Enterprise), puedes crear un **Custom GPT**:
1.  **Ir a Explore GPTs.**
2.  Clicar **Create GPT.**
3.  En **Instructions**, pega el **Prompt de Sistema afinado**.
4.  Añade “acciones” si quieres que interactúe con APIs o herramientas externas.
5.  Guarda y publica tu GPT privado.
Esto no requiere programar en Python, pero tendrás menos control fino de código.
## ¿Cómo se configura una acción?
En el creador de GPTs de OpenAI:
1.  Vas a la sección **Actions**.
2.  Defines una **OpenAPI schema** (archivo .yaml o .json) que describe:
-   Qué endpoint se llama.
-   Qué parámetros acepta.
-   Cómo se debe mostrar el resultado.
1.  El GPT aprende a usar ese endpoint de forma contextual.  
    **Ejemplo sencillo de definición YAML:**
**openapi:** 3.0.0
**info:**
**title:** Mi API de Multiverso
**version:** 1.0.0
**paths:**
/historia\_alternativa:
**get:**
**summary:** Devuelve un relato corto de una línea temporal ficticia.
**parameters:**
\- name: tema
in: query
required: true
schema:
type: string
**responses:**
'200':
description: Historia generada
content:
application/json:
schema:
type: object
properties:
historia:
type: string
## Ideas de acciones para tu GPT multiversal
Aquí te dejo algunas:
✅ **/generar\_historia\_alternativa**  
Devuelve un cuento breve basado en el tema y el universo.
✅ **/crear\_imagen**  
Devuelve una imagen generada con DALL·E o Stable Diffusion.
✅ **/buscar\_evento\_real**  
Consulta Wikipedia o una base de datos histórica.
✅ **/crear\_codigo\_secreto**  
Crea un código inspirado en la línea temporal.
✅ **/enviar\_mensaje\_multiversal**  
Permite enviar un mensaje imaginario a otra versión de ti.