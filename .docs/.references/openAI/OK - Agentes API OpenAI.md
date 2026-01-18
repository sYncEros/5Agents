**Agentes**
Aprende a crear agentes con la API de OpenAI.
Los agentes representan **sistemas que realizan tareas de manera inteligente**, que van desde la ejecución de flujos de trabajo simples hasta la búsqueda de objetivos complejos y abiertos.
OpenAI proporciona un **amplio conjunto de primitivas componibles que te permiten compilar agentes**. Esta guía recorre esas primitivas y cómo se unen para formar una sólida plataforma agentica.
**Visión general**
La creación de agentes implica ensamblar componentes en varios dominios, como **modelos, herramientas, conocimiento y memoria, audio y voz, barreras de seguridad y orquestación,** y OpenAI proporciona primitivas componibles para cada uno.
| 
**Dominio**
 | 
**Descripción**
 | 
**Primitivas de OpenAI**
 |
| --- | --- | --- |
| 
[Modelos](https://platform.openai.com/docs/guides/agents#models)
 | 
Inteligencia central capaz de razonar, tomar decisiones y procesar diferentes modalidades.
 | 
[o1](https://platform.openai.com/docs/models/o1), [o3-mini](https://platform.openai.com/docs/models/o3-mini), [GPT-4.5](https://platform.openai.com/docs/models/gpt-4.5-preview), [GPT-4o](https://platform.openai.com/docs/models/gpt-4o)[, GPT-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini)
 |
| 
[Herramientas](https://platform.openai.com/docs/guides/agents#tools)
 | 
Interfaz con el mundo, interacción con el entorno, llamada de funciones, herramientas integradas, etc.
 | 
[Llamada de funciones](https://platform.openai.com/docs/guides/function-calling), [Búsqueda web](https://platform.openai.com/docs/guides/tools-web-search), [Búsqueda de archivos](https://platform.openai.com/docs/guides/tools-file-search), [Uso del equipo](https://platform.openai.com/docs/guides/tools-computer-use)
 |
| 
[Conocimiento y memoria](https://platform.openai.com/docs/guides/agents#knowledge-memory)
 | 
Aumente los agentes con conocimientos externos y persistentes.
 | 
[Almacenes de vectores](https://platform.openai.com/docs/guides/retrieval#vector-stores), [Búsqueda de archivos](https://platform.openai.com/docs/guides/tools-file-search), [Incrustaciones](https://platform.openai.com/docs/guides/embeddings)
 |
| 
[Audio y voz](https://platform.openai.com/docs/guides/agents#audio-and-speech)
 | 
Cree agentes que puedan entender el audio y responder en lenguaje natural.
 | 
[Generación de audio](https://platform.openai.com/docs/guides/audio-generation), [en tiempo real](https://platform.openai.com/docs/guides/realtime), [agentes de audio](https://platform.openai.com/docs/guides/audio-agents)
 |
| 
[Barandillas](https://platform.openai.com/docs/guides/agents#guardrails)
 | 
Prevenir comportamientos irrelevantes, dañinos o indeseables.
 | 
[Moderación](https://platform.openai.com/docs/guides/moderation), Jerarquía de [instrucciones (Python),](https://openai.github.io/openai-agents-python/guardrails/) [Jerarquía de instrucciones (TypeScript)](https://openai.github.io/openai-agents-js/guides/guardrails/)
 |
| 
[Orquestación](https://platform.openai.com/docs/guides/agents#orchestration)
 | 
Desarrolle, implemente, supervise y mejore los agentes.
 | 
[SDK de agentes de Python](https://openai.github.io/openai-agents-python/), SDK de [agentes de TypeScript](https://openai.github.io/openai-agents-js/), [seguimiento](https://platform.openai.com/traces), [evaluaciones](https://platform.openai.com/docs/guides/evals), [ajuste fino](https://platform.openai.com/docs/guides/model-optimization)
 |
| 
[Agentes de voz](https://platform.openai.com/docs/guides/voice-agents)
 | 
Cree agentes que puedan entender el audio y responder en lenguaje natural.
 | 
[API en tiempo real,](https://platform.openai.com/docs/guides/realtime) [compatibilidad con voz en el SDK de agentes de Python](https://openai.github.io/openai-agents-python/voice/quickstart/), [compatibilidad con voz en el SDK de agentes de TypeScript](https://openai.github.io/openai-agents-js/guides/voice-agents/)
 |
**Modelos**
| 
**Modelo**
 | 
**Fortalezas de los agentes**
 |
| --- | --- |
| 
[O3](https://platform.openai.com/docs/models/o3) y [O4-mini](https://platform.openai.com/docs/models/o4-mini)
 | 
Lo mejor para la planificación a largo plazo, las tareas difíciles y el razonamiento.
 |
| 
[GPT-4.1](https://platform.openai.com/docs/models/gpt-4.1)
 | 
Lo mejor para la ejecución de agentes.
 |
| 
[GPT-4.1-mini](https://platform.openai.com/docs/models/gpt-4.1-mini)
 | 
Buen equilibrio entre la capacidad de los agentes y la latencia.
 |
| 
[GPT-4.1-nano](https://platform.openai.com/docs/models/gpt-4.1-nano)
 | 
Lo mejor para baja latencia.
 |
Los grandes modelos de lenguaje (LLM) son el núcleo de muchos sistemas agenticos, responsables de tomar decisiones e interactuar con el mundo. Los modelos de OpenAI soportan una amplia gama de capacidades:
-   **Alta inteligencia:** Capaz de [razonar](https://platform.openai.com/docs/guides/reasoning) y planificar para abordar las tareas más difíciles.
-   **Herramientas:** [Llame a sus funciones](https://platform.openai.com/docs/guides/function-calling) y aproveche las [herramientas integradas de](https://platform.openai.com/docs/guides/tools) OpenAI.
-   **Multimodalidad:** Comprenda de forma nativa texto, imágenes, audio, código y documentos.
-   **Baja latencia:** Soporte para conversaciones [de audio en tiempo real](https://platform.openai.com/docs/guides/realtime) y modelos más pequeños y rápidos.
Para ver comparaciones detalladas de modelos, visite la página de [modelos](https://platform.openai.com/docs/models).
**Herramientas**
| Herramienta | Descripción |
| --- | --- |
| Llamada a funciones | Interactúe con el código definido por el desarrollador. |
| Búsqueda en la web | Obtenga información actualizada de la web. |
| Búsqueda de archivos | Realice búsquedas semánticas en sus documentos. |
| Uso de la computadora | Comprender y controlar una computadora o un navegador. |
| Shell local | Ejecutar comandos en un equipo local. |
Las herramientas permiten a los agentes interactuar con el mundo. OpenAI admite [**llamadas a funciones**](https://platform.openai.com/docs/guides/function-calling) para conectarse con su código y [**herramientas integradas**](https://platform.openai.com/docs/guides/tools) para tareas comunes como búsquedas web y recuperación de datos.
**Conocimiento y memoria**
El conocimiento y la memoria ayudan a los agentes a almacenar, recuperar y utilizar información más allá de sus datos de entrenamiento iniciales. **Los almacenes de vectores** permiten a los agentes buscar sus documentos semánticamente y recuperar información relevante en tiempo de ejecución. Mientras tanto, **las incrustaciones** representan datos de manera eficiente para una recuperación rápida, lo que impulsa soluciones de conocimiento dinámico y memoria de agentes a largo plazo. Puedes integrar tus datos utilizando [los almacenes de vectores](https://platform.openai.com/docs/guides/retrieval#vector-stores) y la [API de incrustaciones de](https://platform.openai.com/docs/guides/embeddings) OpenAI.
**Barandillas**
Las barreras de protección garantizan que sus agentes se comporten de manera segura, coherente y dentro de los límites previstos, lo que es fundamental para las implementaciones de producción. Utilice la [API de moderación](https://platform.openai.com/docs/guides/moderation) gratuita de OpenAI para filtrar automáticamente el contenido inseguro. Controle aún más el comportamiento de su agente aprovechando la [jerarquía de instrucciones](https://openai.github.io/openai-agents-python/guardrails/), que prioriza las indicaciones definidas por el desarrollador y mitiga los comportamientos no deseados de los agentes.
**Orquestación**
La construcción de agentes es un proceso. OpenAI proporciona herramientas para construir, implementar, monitorear, evaluar y mejorar de manera efectiva los sistemas de agentes.
| Fase | Descripción | Primitivas de OpenAI |
| --- | --- | --- |
| Compilación e implementación | Cree agentes rápidamente, aplique barreras de protección y maneje flujos conversacionales con el SDK de agentes. | Agentes SDK Python,&nbsp;Agentes SDK TypeScript |
| Monitor | Observe el comportamiento de los agentes en tiempo real, depure problemas y obtenga información a través del seguimiento. | Trazado |
| Evaluar y mejorar | Mida el rendimiento de los agentes, identifique las áreas de mejora y perfeccione sus agentes. | EvaluacionesPuesta a punto |
**Orquestación de varios agentes**
La orquestación hace referencia al flujo de agentes en la aplicación. ¿Qué agentes se ejecutan, en qué orden y cómo deciden qué sucede a continuación? Hay dos formas principales de orquestar agentes:
1.  Permitir que el LLM tome decisiones: utiliza la inteligencia de un LLM para planificar, razonar y decidir qué pasos tomar en función de eso.
2.  Orquestación a través de código: determinación del flujo de agentes a través de su código.
Puedes mezclar y combinar estos patrones. Cada uno tiene sus propias compensaciones, que se describen a continuación.
**Orquestación a través de LLM**
Un agente es un LLM equipado con instrucciones, herramientas y transferencias. Esto significa que, dada una tarea abierta, el LLM puede planificar de forma autónoma cómo abordará la tarea, utilizando herramientas para realizar acciones y adquirir datos, y utilizando transferencias para delegar tareas a subagentes. Por ejemplo, un agente de investigación podría estar equipado con herramientas como:
-   Búsqueda en la web para encontrar información en línea
-   Búsqueda y recuperación de archivos para buscar a través de datos y conexiones propietarios
-   Uso de la computadora para realizar acciones en una computadora
-   Ejecución de código para hacer análisis de datos
-   Entregas a agentes especializados que son excelentes en planificación, redacción de informes y más.
Este patrón es excelente cuando la tarea es abierta y desea confiar en la inteligencia de un LLM. Las tácticas más importantes aquí son:
1.  Invierte en buenas indicaciones. Deje claro qué herramientas están disponibles, cómo usarlas y dentro de qué parámetros debe operar.
2.  Supervise su aplicación e itere en ella. Vea dónde van mal las cosas y repita sus indicaciones.
3.  Permita que el agente haga introspección y mejore. Por ejemplo, ejecútalo en bucle y deja que se critique a sí mismo; O bien, proporcione mensajes de error y deje que mejore.
4.  Tenga agentes especializados que sobresalgan en una tarea, en lugar de tener un agente de propósito general que se espera que sea bueno en cualquier cosa.
5.  Invierte en [evaluaciones](https://platform.openai.com/docs/guides/evals). Esto le permite capacitar a sus agentes para mejorar y mejorar en las tareas.
**Orquestación a través de código**
Si bien la orquestación a través de LLM es poderosa, la orquestación a través de código hace que las tareas sean más deterministas y predecibles, en términos de velocidad, costo y rendimiento. Los patrones comunes aquí son:
-   Usar [salidas estructuradas](https://platform.openai.com/docs/guides/structured-outputs) para generar datos bien formados que se pueden inspeccionar con el código. Por ejemplo, puede pedirle a un agente que clasifique la tarea en algunas categorías y, a continuación, elegir el siguiente agente en función de la categoría.
-   Encadenar varios agentes transformando la salida de uno en la entrada del siguiente. Puede descomponer una tarea como escribir una publicación de blog en una serie de pasos: investigar, escribir un esquema, escribir la publicación de blog, criticarla y luego mejorarla.
-   Ejecutar el agente que realiza la tarea en un bucle con un agente que evalúa y proporciona comentarios, hasta que el evaluador diga que la salida supera ciertos criterios.while
-   Ejecutar varios agentes en paralelo, por ejemplo, a través de primitivas de Python como . Esto es útil para la velocidad cuando tiene varias tareas que no dependen unas de otras.asyncio.gather
We have a number of examples in [examples/agent\_patterns](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns).