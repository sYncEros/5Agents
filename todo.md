# 📋 TODO - 5Agents

## 🔴 Tareas Críticas

- [ ] **Probar integración con Ollama**
  - Verificar que Ollama esté instalado (`ollama --version`)
  - Descargar modelos necesarios (`ollama pull mistral`)
  - Ejecutar tests con Ollama: `pytest tests/test_ollama_client.py -v`

## 🟡 Implementación de Features

### Componentes Core del Sistema Multi-Agentes

### Interfaces y Exportación

- [ ] **Refactorizar `app.py` - Integración profesional con tareas de CrewAI**
  - Integrar `ejecutar_equipo_para_tema()` para orquestación paralela de equipos
  - Implementar `Pool` de multiprocessing para ejecutar múltiples temas en paralelo
  - Crear módulo `components/utils.py` con funciones:
    - `leer_corpus()` - Carga archivos TXT/PDF
    - `limpiar_json_output()` - Parsea respuestas JSON del LLM
    - `validar_paper_markdown()` - Valida estructura y calidad de papers
    - `crear_docx()` - Exporta papers a DOCX
  - Implementar `extraer_temas_desde_resultado()` para parsear temas JSON
  - Integrar con `crear_tarea_identificacion_temas()` y `crear_tareas_generacion_paper()`
  - Mostrar resultados con función `mostrar_resultados()`
  - Test: `test_app_refactored.py` (sin mocks, con Ollama real)

- [ ] **Integración Streamlit actualizada**
  - Conectar `app.py` con `ConversationController`
  - Actualizar UI para mostrar respuestas multi-agente
  - Añadir selección manual de agentes (opcional)
  - Mostrar visualización de síntesis y análisis de contexto

- [ ] **Exportador de PDF con respuestas multi-agente**
  - Crear `PDFGenerator` en `components/export/pdf_generator.py`
  - Implementar formato con respuestas de cada agente
  - Incluir síntesis y análisis de contexto
  - Añadir metadatos (timestamp, agentes activados, etc.)
  - Test: `test_pdf_generator.py` (sin mocks)

- [ ] **Generador de grafos/mapas conceptuales**
  - Crear `GraphGenerator` en `components/export/graph_generator.py`
  - Instalar dependencias: `networkx`, `pyvis`
  - Generar grafos interactivos HTML desde síntesis
  - Visualizar relaciones entre temas y respuestas de agentes
  - Test: `test_graph_generator.py` (sin mocks)

### Dashboard y APIs

- [ ] **Dashboard React - Integración completa**
  - Conectar `AgentDashboard.jsx` con backend Python
  - Actualizar fetch para apuntar a Node-RED o API Flask
  - Añadir visualización de respuestas multi-agente
  - Implementar vista de grafo conceptual embebida

## 🟢 Mejoras y Optimización

- [ ] **Mejoras de Calidad de Código (Task.md)**
  - [ ] Evitar hardcoding de slices ([:8000], [:4000]) en tareas
  - [ ] Eliminar duplicaciones en lógica de truncado y formatos
  - [ ] Aplicar principios DRY y SRP a todas las clases
  - [ ] Agregar tipado estricto a funciones de utilidad
  - [ ] Tests para cada clase nueva (minimum 70% coverage)

- [ ] **Arreglar tests fallidos**
  - Mejorar error handling en `ConversationController`
  - Agregar validación de inputs en `process()`
  - Manejar mejor los casos edge (input vacío, agentes inválidos)

- [ ] **Configuración**
  - Mover configuraciones hardcodeadas a `config.toml`
  - Añadir variables de entorno para API keys y URLs
  - Documentar opciones de configuración

- [ ] **Refactoring**
  - Revisar `motor_innovacion.py` y modularizar si es necesario
  - Consolidar definiciones de agentes en un solo lugar
  - Eliminar código duplicado

## 📚 Documentación

- [ ] **Refactorización profesional de código (según Task.md)**
  - [ ] Implementar `TaskConfig` dataclass en tasks para configuración centralizada
  - [ ] Crear utilidades profesionales: `truncar_texto()`, `wrap_seccion()`
  - [ ] Documentar patrones de uso para CrewAI con ejemplos reales
  - [ ] Crear guía: "Cómo crear tareas profesionales sin hardcoding"

- [ ] **Crear guías de uso**
  - Quick start para desarrolladores
  - Guía de configuración de Node-RED
  - Tutorial de creación de nuevos perfiles de agentes

- [ ] **Ejemplos prácticos**
  - Scripts de ejemplo usando los agentes
  - Casos de uso documentados
  - Notebooks interactivos (Jupyter)

## 🔧 Infraestructura

- [ ] **Contenedorización**
  - Dockerfile para backend Python
  - docker-compose.yml para stack completo (Python + Node-RED + Dashboard)

- [ ] **CI/CD**
  - GitHub Actions para tests automáticos
  - Deploy automático del dashboard

## 📝 Notas

**Última actualización:** 16 de enero de 2026
