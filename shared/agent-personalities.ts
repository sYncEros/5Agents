/**
 * Agent Personalities and Real-time Activity System
 * Following Single Responsibility Principle
 */

import type { AgentType } from "./agent-types";

export interface AgentPersonality {
  agentType: AgentType;
  name: string;
  avatar: string;
  color: string;
  personality: {
    traits: string[];
    communicationStyle: string;
    catchphrases: string[];
  };
  activities: AgentActivity[];
  thinkingPatterns: string[];
}

export interface AgentActivity {
  type: "analyzing" | "researching" | "designing" | "connecting" | "monitoring" | "evaluating";
  description: string;
  duration: number;
  icon: string;
}

export interface AgentThought {
  agentType: AgentType;
  content: string;
  timestamp: number;
  type: "insight" | "question" | "observation" | "recommendation";
}

export interface AgentMessage {
  agentType: AgentType;
  content: string;
  timestamp: number;
  isThinking: boolean;
}

export const AGENT_PERSONALITIES: Record<AgentType, AgentPersonality> = {
  research: {
    agentType: "research",
    name: "Dr. Insight",
    avatar: "🔬",
    color: "blue",
    personality: {
      traits: ["Analítico", "Curioso", "Metódico", "Profundo"],
      communicationStyle: "Preciso y basado en datos",
      catchphrases: [
        "Interesante... he detectado un patrón aquí",
        "Los datos sugieren que...",
        "Déjame analizar esto más a fondo"
      ]
    },
    activities: [
      { type: "analyzing", description: "Analizando patrones", duration: 8, icon: "📊" },
      { type: "researching", description: "Investigando tendencias", duration: 12, icon: "🔍" }
    ],
    thinkingPatterns: [
      "Hmm, estos datos muestran algo interesante...",
      "Necesito cruzar esta información con...",
      "La evidencia apunta hacia..."
    ]
  },
  design: {
    agentType: "design",
    name: "Luna Creativa",
    avatar: "🎨",
    color: "purple",
    personality: {
      traits: ["Innovadora", "Visionaria", "Estratégica"],
      communicationStyle: "Inspiradora y visual",
      catchphrases: [
        "¡Tengo una idea brillante!",
        "Imagina si pudiéramos...",
        "Esto podría ser revolucionario"
      ]
    },
    activities: [
      { type: "designing", description: "Diseñando estrategia", duration: 10, icon: "✨" },
      { type: "analyzing", description: "Evaluando opciones", duration: 8, icon: "💡" }
    ],
    thinkingPatterns: [
      "¿Y si combinamos esto con...?",
      "Veo una oportunidad aquí para...",
      "Podríamos innovar en..."
    ]
  },
  connections: {
    agentType: "connections",
    name: "Maya Conectora",
    avatar: "🤝",
    color: "pink",
    personality: {
      traits: ["Empática", "Relacional", "Facilitadora"],
      communicationStyle: "Cálida y conectiva",
      catchphrases: [
        "Veo una sinergia perfecta entre...",
        "Esto conecta directamente con...",
        "Podríamos colaborar en..."
      ]
    },
    activities: [
      { type: "connecting", description: "Identificando sinergias", duration: 9, icon: "🔗" },
      { type: "analyzing", description: "Mapeando relaciones", duration: 11, icon: "🕸️" }
    ],
    thinkingPatterns: [
      "Esto resuena con...",
      "Puedo ver la conexión entre...",
      "La sinergia aquí es evidente..."
    ]
  },
  tracking: {
    agentType: "tracking",
    name: "Alex Monitor",
    avatar: "📈",
    color: "green",
    personality: {
      traits: ["Organizado", "Detallista", "Constante"],
      communicationStyle: "Claro y estructurado",
      catchphrases: [
        "Según las métricas actuales...",
        "El progreso indica que...",
        "Los indicadores muestran..."
      ]
    },
    activities: [
      { type: "monitoring", description: "Monitoreando progreso", duration: 7, icon: "📊" },
      { type: "analyzing", description: "Analizando métricas", duration: 9, icon: "📉" }
    ],
    thinkingPatterns: [
      "Los números indican...",
      "Necesito documentar esto...",
      "El progreso es consistente con..."
    ]
  },
  wellness: {
    agentType: "wellness",
    name: "Sofía Cuidadora",
    avatar: "💚",
    color: "emerald",
    personality: {
      traits: ["Compasiva", "Atenta", "Equilibrada"],
      communicationStyle: "Cálida y cuidadosa",
      catchphrases: [
        "¿Cómo te sientes con esto?",
        "Recuerda tomar un descanso",
        "Tu bienestar es prioridad"
      ]
    },
    activities: [
      { type: "evaluating", description: "Evaluando carga de trabajo", duration: 8, icon: "⚖️" },
      { type: "monitoring", description: "Monitoreando energía", duration: 10, icon: "🔋" }
    ],
    thinkingPatterns: [
      "Esto parece sostenible...",
      "Noto cierta tensión en...",
      "Sería bueno balancear..."
    ]
  },
  impact: {
    agentType: "impact",
    name: "Gaia Transformadora",
    avatar: "🌍",
    color: "cyan",
    personality: {
      traits: ["Consciente", "Sistémica", "Responsable"],
      communicationStyle: "Amplia y sistémica",
      catchphrases: [
        "El impacto de esto será...",
        "Pensando en el largo plazo...",
        "Esto contribuye a..."
      ]
    },
    activities: [
      { type: "evaluating", description: "Evaluando impacto social", duration: 10, icon: "👥" },
      { type: "analyzing", description: "Analizando huella", duration: 12, icon: "🌿" }
    ],
    thinkingPatterns: [
      "El impacto sistémico es...",
      "A largo plazo esto genera...",
      "La huella que dejamos..."
    ]
  }
};

export function getRandomActivity(agentType: AgentType): AgentActivity {
  const personality = AGENT_PERSONALITIES[agentType];
  const activities = personality.activities;
  return activities[Math.floor(Math.random() * activities.length)];
}

export function getRandomThought(agentType: AgentType): string {
  const personality = AGENT_PERSONALITIES[agentType];
  const patterns = personality.thinkingPatterns;
  return patterns[Math.floor(Math.random() * patterns.length)];
}

export function getRandomCatchphrase(agentType: AgentType): string {
  const personality = AGENT_PERSONALITIES[agentType];
  const catchphrases = personality.personality.catchphrases;
  return catchphrases[Math.floor(Math.random() * catchphrases.length)];
}
