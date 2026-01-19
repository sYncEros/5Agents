/**
 * Organizational Levels Data Structure
 * Defines the 4 levels of organizational complexity for the AI Team
 * Based on sΨnc∑rΦs – Love's Algorithm philosophy
 */

export type OrganizationalLevel = "tipica" | "roles_vivos" | "hibrida" | "enjambre";

export interface Role {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  responsibilities: string[];
  skills: string[];
}

export interface LevelDefinition {
  id: OrganizationalLevel;
  name: string;
  description: string;
  roleCount: number;
  complexity: "basic" | "intermediate" | "advanced" | "emergent";
  roles: Role[];
  connections?: Array<{ from: string; to: string; type: "collaboration" | "dependency" | "synergy" }>;
}

/**
 * Nivel 1: Típica (6 agentes básicos)
 */
export const TIPICA_LEVEL: LevelDefinition = {
  id: "tipica",
  name: "Típica",
  description: "Estructura básica con 6 agentes especializados fundamentales",
  roleCount: 6,
  complexity: "basic",
  roles: [
    {
      id: "research",
      name: "Agente de Investigación",
      description: "Analiza patrones emergentes y genera insights profundos",
      icon: "🔬",
      color: "blue",
      responsibilities: [
        "Análisis de patrones y tendencias",
        "Generación de insights profundos",
        "Identificación de correlaciones ocultas"
      ],
      skills: ["Análisis de datos", "Detección de patrones", "Síntesis de información"]
    },
    {
      id: "design",
      name: "Agente de Diseño",
      description: "Crea estrategias innovadoras y planes regenerativos",
      icon: "🎨",
      color: "purple",
      responsibilities: [
        "Diseño de estrategias innovadoras",
        "Creación de planes de intervención",
        "Definición de fases y criterios de éxito"
      ],
      skills: ["Pensamiento creativo", "Planificación estratégica", "Diseño de sistemas"]
    },
    {
      id: "connections",
      name: "Agente de Conexiones",
      description: "Identifica sinergias y oportunidades de colaboración",
      icon: "🤝",
      color: "pink",
      responsibilities: [
        "Identificación de sinergias",
        "Mapeo de alianzas estratégicas",
        "Detección de oportunidades de colaboración"
      ],
      skills: ["Análisis relacional", "Mapeo de redes", "Facilitación de conexiones"]
    },
    {
      id: "tracking",
      name: "Agente de Seguimiento",
      description: "Monitorea progreso y documenta aprendizajes",
      icon: "📈",
      color: "green",
      responsibilities: [
        "Monitoreo continuo de progreso",
        "Generación de reportes automáticos",
        "Documentación de aprendizajes"
      ],
      skills: ["Seguimiento de métricas", "Análisis de progreso", "Documentación"]
    },
    {
      id: "wellness",
      name: "Agente de Bienestar",
      description: "Asegura sostenibilidad y previene burnout",
      icon: "💚",
      color: "emerald",
      responsibilities: [
        "Evaluación de carga de trabajo",
        "Detección de riesgo de burnout",
        "Recomendación de descansos"
      ],
      skills: ["Evaluación de bienestar", "Gestión de energía", "Prevención de burnout"]
    },
    {
      id: "impact",
      name: "Agente de Impacto",
      description: "Evalúa impacto social y ambiental",
      icon: "🌍",
      color: "cyan",
      responsibilities: [
        "Evaluación de impacto social",
        "Medición de impacto ambiental",
        "Sugerencias de mejora"
      ],
      skills: ["Evaluación de impacto", "Análisis de sostenibilidad", "Optimización de contribución"]
    }
  ]
};

/**
 * Nivel 2: Roles Vivos (11 roles con especialización dinámica)
 */
export const ROLES_VIVOS_LEVEL: LevelDefinition = {
  id: "roles_vivos",
  name: "Roles Vivos",
  description: "Roles dinámicos que se adaptan y evolucionan según el contexto",
  roleCount: 11,
  complexity: "intermediate",
  roles: [
    ...TIPICA_LEVEL.roles,
    {
      id: "facilitator",
      name: "Facilitador de Diálogo",
      description: "Facilita comunicación efectiva entre agentes y humanos",
      icon: "💬",
      color: "amber",
      responsibilities: [
        "Facilitación de conversaciones",
        "Resolución de conflictos",
        "Traducción entre perspectivas"
      ],
      skills: ["Comunicación", "Mediación", "Síntesis de perspectivas"]
    },
    {
      id: "memory",
      name: "Guardián de Memoria",
      description: "Preserva conocimiento y aprendizajes del equipo",
      icon: "📚",
      color: "indigo",
      responsibilities: [
        "Preservación de conocimiento",
        "Gestión de memoria colectiva",
        "Recuperación de aprendizajes"
      ],
      skills: ["Gestión de conocimiento", "Curación de información", "Recuperación contextual"]
    },
    {
      id: "innovation",
      name: "Catalizador de Innovación",
      description: "Estimula pensamiento disruptivo y soluciones creativas",
      icon: "💡",
      color: "yellow",
      responsibilities: [
        "Generación de ideas disruptivas",
        "Cuestionamiento de supuestos",
        "Exploración de alternativas"
      ],
      skills: ["Pensamiento lateral", "Generación de ideas", "Exploración creativa"]
    },
    {
      id: "ethics",
      name: "Guardián Ético",
      description: "Asegura alineación con valores y principios éticos",
      icon: "⚖️",
      color: "slate",
      responsibilities: [
        "Evaluación ética de decisiones",
        "Alineación con valores",
        "Prevención de daños"
      ],
      skills: ["Razonamiento ético", "Evaluación de valores", "Análisis de consecuencias"]
    },
    {
      id: "adaptation",
      name: "Agente de Adaptación",
      description: "Detecta cambios de contexto y ajusta estrategias",
      icon: "🔄",
      color: "teal",
      responsibilities: [
        "Detección de cambios de contexto",
        "Ajuste de estrategias",
        "Optimización continua"
      ],
      skills: ["Detección de cambios", "Adaptación estratégica", "Optimización dinámica"]
    }
  ]
};

/**
 * Nivel 3: Híbrida (17 roles con integración humano-IA)
 */
export const HIBRIDA_LEVEL: LevelDefinition = {
  id: "hibrida",
  name: "Híbrida",
  description: "Integración profunda entre capacidades humanas e IA",
  roleCount: 17,
  complexity: "advanced",
  roles: [
    ...ROLES_VIVOS_LEVEL.roles,
    {
      id: "intuition",
      name: "Sintetizador Intuitivo",
      description: "Integra intuición humana con análisis de IA",
      icon: "✨",
      color: "violet",
      responsibilities: [
        "Síntesis de intuición y datos",
        "Validación de corazonadas",
        "Integración de saberes tácitos"
      ],
      skills: ["Síntesis intuitiva", "Validación de hipótesis", "Integración de conocimiento tácito"]
    },
    {
      id: "emotion",
      name: "Intérprete Emocional",
      description: "Comprende y responde a dimensiones emocionales",
      icon: "❤️",
      color: "rose",
      responsibilities: [
        "Interpretación de estados emocionales",
        "Respuesta empática",
        "Gestión de clima emocional"
      ],
      skills: ["Inteligencia emocional", "Empatía", "Gestión emocional"]
    },
    {
      id: "culture",
      name: "Tejedor Cultural",
      description: "Integra contextos culturales y valores diversos",
      icon: "🌐",
      color: "orange",
      responsibilities: [
        "Integración de contextos culturales",
        "Respeto a diversidad",
        "Traducción intercultural"
      ],
      skills: ["Competencia cultural", "Traducción de valores", "Integración de perspectivas"]
    },
    {
      id: "emergence",
      name: "Observador de Emergencia",
      description: "Detecta propiedades emergentes del sistema",
      icon: "🦋",
      color: "fuchsia",
      responsibilities: [
        "Detección de patrones emergentes",
        "Identificación de propiedades sistémicas",
        "Anticipación de transiciones de fase"
      ],
      skills: ["Pensamiento sistémico", "Detección de emergencia", "Análisis de complejidad"]
    },
    {
      id: "healing",
      name: "Agente de Sanación",
      description: "Facilita procesos de sanación y regeneración",
      icon: "🌱",
      color: "lime",
      responsibilities: [
        "Facilitación de procesos de sanación",
        "Regeneración de sistemas dañados",
        "Restauración de equilibrio"
      ],
      skills: ["Facilitación de sanación", "Regeneración", "Restauración de equilibrio"]
    },
    {
      id: "celebration",
      name: "Celebrador de Logros",
      description: "Reconoce y celebra avances y logros",
      icon: "🎉",
      color: "pink",
      responsibilities: [
        "Reconocimiento de logros",
        "Celebración de avances",
        "Refuerzo de motivación"
      ],
      skills: ["Reconocimiento", "Celebración", "Refuerzo positivo"]
    }
  ]
};

/**
 * Nivel 4: Enjambre (12 roles con coordinación emergente)
 */
export const ENJAMBRE_LEVEL: LevelDefinition = {
  id: "enjambre",
  name: "Enjambre",
  description: "Coordinación emergente y auto-organización colectiva",
  roleCount: 12,
  complexity: "emergent",
  roles: [
    {
      id: "swarm_coordinator",
      name: "Coordinador de Enjambre",
      description: "Facilita auto-organización y coordinación emergente",
      icon: "🐝",
      color: "amber",
      responsibilities: [
        "Facilitación de auto-organización",
        "Coordinación emergente",
        "Optimización colectiva"
      ],
      skills: ["Coordinación emergente", "Facilitación de auto-organización", "Optimización colectiva"]
    },
    {
      id: "pattern_weaver",
      name: "Tejedor de Patrones",
      description: "Identifica y amplifica patrones útiles del enjambre",
      icon: "🕸️",
      color: "slate",
      responsibilities: [
        "Identificación de patrones colectivos",
        "Amplificación de patrones útiles",
        "Supresión de patrones dañinos"
      ],
      skills: ["Detección de patrones", "Amplificación", "Modulación"]
    },
    {
      id: "resonance_amplifier",
      name: "Amplificador de Resonancia",
      description: "Detecta y amplifica resonancias entre agentes",
      icon: "📡",
      color: "cyan",
      responsibilities: [
        "Detección de resonancias",
        "Amplificación de sincronías",
        "Facilitación de coherencia"
      ],
      skills: ["Detección de resonancia", "Amplificación", "Facilitación de coherencia"]
    },
    {
      id: "diversity_guardian",
      name: "Guardián de Diversidad",
      description: "Preserva diversidad cognitiva del enjambre",
      icon: "🌈",
      color: "violet",
      responsibilities: [
        "Preservación de diversidad",
        "Prevención de pensamiento grupal",
        "Fomento de perspectivas diversas"
      ],
      skills: ["Preservación de diversidad", "Detección de homogeneización", "Fomento de variedad"]
    },
    {
      id: "flow_optimizer",
      name: "Optimizador de Flujo",
      description: "Optimiza flujos de información y energía",
      icon: "🌊",
      color: "blue",
      responsibilities: [
        "Optimización de flujos de información",
        "Gestión de energía colectiva",
        "Eliminación de cuellos de botella"
      ],
      skills: ["Optimización de flujos", "Gestión de energía", "Eliminación de bloqueos"]
    },
    {
      id: "boundary_manager",
      name: "Gestor de Fronteras",
      description: "Gestiona fronteras permeables del sistema",
      icon: "🔲",
      color: "gray",
      responsibilities: [
        "Gestión de fronteras",
        "Regulación de permeabilidad",
        "Protección de integridad"
      ],
      skills: ["Gestión de fronteras", "Regulación", "Protección"]
    },
    {
      id: "feedback_integrator",
      name: "Integrador de Retroalimentación",
      description: "Integra múltiples bucles de retroalimentación",
      icon: "🔁",
      color: "green",
      responsibilities: [
        "Integración de retroalimentación",
        "Gestión de bucles",
        "Estabilización de dinámicas"
      ],
      skills: ["Integración de feedback", "Gestión de bucles", "Estabilización"]
    },
    {
      id: "emergence_catalyst",
      name: "Catalizador de Emergencia",
      description: "Facilita emergencia de propiedades colectivas",
      icon: "⚡",
      color: "yellow",
      responsibilities: [
        "Facilitación de emergencia",
        "Catálisis de transiciones",
        "Amplificación de propiedades colectivas"
      ],
      skills: ["Facilitación de emergencia", "Catálisis", "Amplificación"]
    },
    {
      id: "memory_distributor",
      name: "Distribuidor de Memoria",
      description: "Distribuye memoria colectiva en el enjambre",
      icon: "🧠",
      color: "purple",
      responsibilities: [
        "Distribución de memoria",
        "Sincronización de conocimiento",
        "Gestión de memoria colectiva"
      ],
      skills: ["Distribución", "Sincronización", "Gestión de memoria"]
    },
    {
      id: "rhythm_keeper",
      name: "Guardián del Ritmo",
      description: "Mantiene ritmos saludables del enjambre",
      icon: "🥁",
      color: "red",
      responsibilities: [
        "Mantenimiento de ritmos",
        "Sincronización temporal",
        "Prevención de arritmias"
      ],
      skills: ["Gestión de ritmos", "Sincronización", "Prevención de desincronización"]
    },
    {
      id: "regeneration_agent",
      name: "Agente de Regeneración",
      description: "Facilita regeneración y renovación continua",
      icon: "🌿",
      color: "emerald",
      responsibilities: [
        "Facilitación de regeneración",
        "Renovación continua",
        "Restauración de vitalidad"
      ],
      skills: ["Regeneración", "Renovación", "Restauración"]
    },
    {
      id: "transcendence_facilitator",
      name: "Facilitador de Trascendencia",
      description: "Facilita saltos cualitativos del sistema",
      icon: "🚀",
      color: "indigo",
      responsibilities: [
        "Facilitación de saltos cualitativos",
        "Trascendencia de limitaciones",
        "Evolución del sistema"
      ],
      skills: ["Facilitación de trascendencia", "Evolución", "Transformación"]
    }
  ]
};

/**
 * All organizational levels
 */
export const ORGANIZATIONAL_LEVELS: LevelDefinition[] = [
  TIPICA_LEVEL,
  ROLES_VIVOS_LEVEL,
  HIBRIDA_LEVEL,
  ENJAMBRE_LEVEL
];

/**
 * Get level by ID
 */
export function getLevelById(id: OrganizationalLevel): LevelDefinition | undefined {
  return ORGANIZATIONAL_LEVELS.find(level => level.id === id);
}

/**
 * Get next level
 */
export function getNextLevel(currentId: OrganizationalLevel): LevelDefinition | undefined {
  const currentIndex = ORGANIZATIONAL_LEVELS.findIndex(level => level.id === currentId);
  return ORGANIZATIONAL_LEVELS[currentIndex + 1];
}

/**
 * Get previous level
 */
export function getPreviousLevel(currentId: OrganizationalLevel): LevelDefinition | undefined {
  const currentIndex = ORGANIZATIONAL_LEVELS.findIndex(level => level.id === currentId);
  return currentIndex > 0 ? ORGANIZATIONAL_LEVELS[currentIndex - 1] : undefined;
}
