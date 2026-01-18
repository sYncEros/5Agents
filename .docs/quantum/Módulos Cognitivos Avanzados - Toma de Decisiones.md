# Módulos Cognitivos Avanzados para Agentes de Toma de Decisiones

## 🔮 QuantumLogicModule

Implementa lógica cuántica para representar decisiones ambiguas o superpuestas. Usa proyecciones ortogonales y retículos ortomodulares para modelar proposiciones cognitivas no clásicas.

El agente puede:
• Representar estados mentales como vectores en espacios de Hilbert.
• Colapsar creencias mediante proyecciones.
• Evaluar probabilidades no clásicas de decisiones.
• Combinar proposiciones incompatibles.
• Simular efectos de orden de presentación en juicios.
• Integrarse con otros módulos para decisiones complejas.

**Implementación clave:**

```python
class QuantumLogicModule:
    def __init__(self):
        pass

    def applyProjection(self, psi, P):
        # Colapsa el estado cuántico psi usando la proyección P
        pass

    def computeJoin(self, P, Q):
        # Calcula la unión lógica ortomodular de P y Q
        pass

    def evaluateProbability(self, psi, P):
        # Evalúa la probabilidad no booleana de P dado el estado psi
        pass
```

### Ejemplo de uso

Supón que el agente enfrenta una decisión ambigua:
• Estado inicial: |ψ⟩ = α|A⟩ + β|B⟩ (decisión entre A y B).
• Proyección para A: P_A.

El módulo:

1. Aplica la proyección P_A para colapsar |ψ⟩.
2. Calcula la probabilidad de elegir A como ⟨ψ|P_A|ψ⟩.
3. Si la decisión es incompatible (A vs B), usa lógica ortomodular para evaluar ambas opciones.

### ¿Cómo interactúa con los otros módulos?

• Con el motor de caos: si la decisión es sensible a condiciones iniciales, el caos puede influir en el colapso.
• Con el agente de inferencia social: si la decisión depende de otro individuo, la lógica cuántica puede modelar la incertidumbre social.
• Con el orquestador: se activa en fases de decisión ambigua o contradictoria.

### 🧠🔄 Diagrama Cognitivo

Este esquema te muestra cómo un agente usa lógica cuántica para tomar decisiones en estados ambiguos.

```mermaid
flowchart TD
A [Inicio de decisión ambigua] --> B[Representar estado como vector cuántico |ψ⟩]
B --> C[Aplicar proyecciones para opciones (P_A, P_B)]
C --> D[Calcular probabilidades no clásicas]
D --> E[Colapsar estado según proyección seleccionada]{¿Decisión clara?}
  E -- Sí --> F[Tomar decisión basada en colapso]
  E -- No --> G[Usar lógica ortomodular para evaluar opciones incompatibles]
F --> H[Registrar decisión y actualizar creencias]
G --> H[Registrar decisión y actualizar creencias]
H --> I[Finalizar proceso de decisión]
```

## 🌀 ChaosAnalysisEngine

Analiza la sensibilidad del agente a condiciones iniciales y perturbaciones. Usa conceptos de dinámica caótica para medir imprevisibilidad en decisiones.

El agente puede:
• Calcular exponentes de Lyapunov para evaluar sensibilidad.
• Generar mapas de atractores para visualizar dinámicas.
• Identificar puntos de bifurcación en procesos cognitivos.
• Integrarse con otros módulos para ajustar decisiones basadas en caos.
• Simular efectos de pequeñas perturbaciones en elecciones.
• Evaluar estabilidad de patrones de comportamiento.

### **Implementación clave:**

```python
class ChaosAnalysisEngine:
    def __init__(self):
        pass

    def lyapunovExponent(self, state):
        # Calcula el exponente de Lyapunov para el estado dado
        pass
    def generateAttractorMap(self):
        # Genera un mapa de atractores basado en la dinámica del agente
        pass
```

### **Ejemplo de uso**

Supón que el agente toma decisiones basadas en un conjunto de variables cognitivas:
• Estado inicial: x0.
• Perturbación pequeña: δx.
• Dinámica: x(t+1) = f(x(t)).

El módulo:

1. Calcula el exponente de Lyapunov para evaluar sensibilidad a δx.
2. Genera un mapa de atractores para visualizar la dinámica.
3. Identifica si existen puntos de bifurcación que puedan alterar decisiones futuras.

### **¿Cómo interactúa con los otros módulos?**

• Con el módulo cuántico: si las decisiones son ambiguas, el caos puede influir en el colapso de estados.
• Con el agente de inferencia social: si las decisiones dependen de interacciones sociales, el caos puede modelar la imprevisibilidad social.
• Con el orquestador: se activa en fases de alta incertidumbre o sensibilidad en decisiones

### **🧠🔄 Diagrama Cognitivo**

Este esquema te muestra cómo un agente analiza la sensibilidad caótica en sus decisiones.

```mermaid
flowchart TD
A [Inicio de análisis caótico] --> B[Definir estado cognitivo inicial x0]
B --> C[Aplicar pequeñas perturbaciones δx]
C --> D[Calcular exponente de Lyapunov]
D --> E[Generar mapa de atractores]{¿Alta sensibilidad?}
    E -- Sí --> F[Identificar puntos de bifurcación]
    E -- No --> G[Continuar monitoreando dinámica]
F --> H[Adaptar decisiones basadas en análisis caótico]
G --> H[Adaptar decisiones basadas en análisis caótico]
H --> I[Finalizar análisis y actualizar modelo cognitivo]
```

## 🧍♂️🧍♀️ SelfOtherInferenceAgent + ParameterEstimator

Modela la inferencia social entre el agente y otro individuo. Usa el modelo de inequidad de Fehr-Schmidt y un enfoque bayesiano para ajustar parámetros internos basados en observaciones del otro.

El agente puede:
• Predecir acciones del otro basándose en sus propios parámetros internos (self → other).
• Actualizar sus propios parámetros tras observar al otro (other → self).
• Inferir parámetros óptimos a partir de datos observados.
• Comparar múltiples modelos de inferencia social.
• Simular procesos reales como:

- Empatía computacional.
- Transferencia bayesiana de intenciones.
- Contagio cognitivo y social.

• Ajustar sensibilidad a inequidad propia y ajena.
• Integrarse con otros módulos para decisiones sociales complejas.

### **Implementación clave**

```python
class SelfOtherInferenceAgent:
    def __init__(self):
        pass

    def predictOther(self, selfParams):
        # Predice la acción del otro basándose en los parámetros propios
        pass

    def updateSelf(self, otherParams):
        # Actualiza los parámetros propios tras observar al otro
        pass
class ParameterEstimator:
    def __init__(self):
        pass

    def inferParameters(self, data):
        # Infiero parámetros óptimos a partir de datos observados
        pass

    def compareModels(self):
        # Compara múltiples modelos de inferencia social
        pass
```

### **Componentes del módulo**

1. SelfOtherInferenceAgent

Este agente tiene dos tareas:

• Predicción hacia el otro: usando el propio modelo (p. ej., aversión a la inequidad, sesgo de riesgo), proyecta lo que el otro haría.
• Ajuste hacia uno mismo: al observar al otro, adapta sus propios parámetros mediante aprendizaje o reponderación bayesiana.
Parámetros clave:
• alpha: sensibilidad a la inequidad propia.
• beta: sensibilidad a la inequidad ajena.

1. ParameterEstimator

Este submódulo es como el afinador de un instrumento:
• Recibe datos observados (elecciones del otro, tiempos, resultados).
• Prueba múltiples modelos candidatos.
• Selecciona el que mejor ajusta según criterios como AIC/BIC o verosimilitud bayesiana.

### **📈 Ejemplo de uso**

Supón que el agente ve esto:
• Tú eliges ceder 40 monedas cuando podrías haberte quedado con 80.

El módulo:

1. Predice que, si estuvieras en su lugar, no habrías cedido tanto → inconsistencia.
2. Ajusta beta para aumentar tu sensibilidad social → “quizás soy más empático de lo que creía”.

### **🔄 ¿Cómo interactúa con los otros módulos?**

• Con el motor de caos: si tu conducta es impredecible, el caos alerta de posibles adaptaciones drásticas.
• Con el módulo cuántico: si la decisión está en superposición (“¿ser egoísta o justo?”), el colapso puede depender del output de este agente.
• Con el orquestador: se activa en fases sociales del experimento: “predice lo que haría otro”, “redecide tras ver qué hizo”.

### **🧠🔄 Diagrama Cognitivo**

Este esquema te muestra cómo un agente social razona sobre el otro, ajusta sus parámetros y retroalimenta el proceso.
Un diagrama de flujo en formato Mermaid que representa el circuito cognitivo del módulo de inferencia self–other. Este esquema muestra las fases clave de razonamiento, predicción y actualización del agente:

```mermaid
flowchart TD
A [Inicio de interacción] --> B[Input social observado (acción del otro)]
B --> C[Predice: ¿Qué haría yo en su lugar?]{¿Input ambiguo o contradictorio?}
  C -- Sí --> C1[Activar lógica cuántica para representar superposición]
  C -- No --> D[Predicción directa desde modelo propio]
C1 --> D[Calcula diferencia (error de predicción)]
D --> E[Actualiza parámetros internos.Comparar predicción vs acción observada]
E --> F[Calcula delta de inferencia (error social)]{¿Cambio significativo?}
  F -- Sí --> G[Reentrena modelo self-other]{¿Delta > umbral adaptativo?}
  F -- No --> H[Continúa con modelo actual]
  G -- Sí --> G1[Actualizar parámetros internos (α, β, etc)]
    G1 --> G2[Seleccionar modelo óptimo (ParameterEstimator)]
    G2 --> G3[Refinar auto-modelo con backprop o inferencia bayesiana]
  G -- No --> H[Conservar parámetros actuales]
G1 --> I[Guardar experiencia en memoria episódica]H --> I
H --> I[Registrar en memoria para aprendizaje acumulativo]
I --> J[Actúa o responde]{¿Múltiples episodios similares?}
  J -- Sí --> K[Detectar patrón social → generar nueva heurística]
  J -- No --> L[Esperar más datos]
K --> M[Actualizar modelo heurístico]
L --> M[Actualizar modelo heurístico]
M --> N[Responder o actuar]
```

## **🧠 Descripción de etapas**

• A → B: El agente recibe una acción social observada (e.g., elección del otro).
• B → C: Predice qué haría en su lugar. Si la información es ambigua, activa lógica cuántica.
• C → D: Calcula la diferencia entre predicción y acción observada.
• D → E: Actualiza parámetros internos basándose en el error de predicción.
• E → F: Evalúa si el cambio es significativo para reentrenar el modelo.
• F → G/H: Si es significativo, reentrena y ajusta parámetros; si no, continúa.
• G → I: Guarda la experiencia en memoria episódica para aprendizaje futuro.
• I → J: Decide si actuar o responder basándose en patrones detectados.
• J → K/L: Si hay patrones, genera nuevas heurísticas; si no, espera más datos.
• K/L → M: Actualiza el modelo heurístico según lo aprendido.
• M → N: Finalmente, responde o actúa según el modelo actualizado.
