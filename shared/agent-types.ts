/**
 * Shared types for AI Team Workspace - Agent System
 * Following SOLID principles - Single Responsibility
 */

// ============================================================================
// AGENT TYPES
// ============================================================================

export type AgentType = 
  | "research"
  | "design"
  | "connections"
  | "tracking"
  | "wellness"
  | "impact";

export type AgentStatus = "idle" | "thinking" | "active" | "coordinating";

export interface AgentMetadata {
  name: string;
  description: string;
  color: string;
  icon: string;
  capabilities: string[];
}

export const AGENT_METADATA: Record<AgentType, AgentMetadata> = {
  research: {
    name: "Agente de Investigación",
    description: "Analiza patrones emergentes, detecta tendencias y genera insights profundos",
    color: "#3B82F6", // blue-500
    icon: "🔬",
    capabilities: ["pattern_analysis", "trend_detection", "insight_generation"]
  },
  design: {
    name: "Agente de Diseño",
    description: "Crea estrategias innovadoras y planes de intervención regenerativa",
    color: "#8B5CF6", // violet-500
    icon: "🎨",
    capabilities: ["strategy_creation", "intervention_design", "milestone_planning"]
  },
  connections: {
    name: "Agente de Conexiones",
    description: "Identifica sinergias y mapea alianzas estratégicas entre objetivos",
    color: "#EC4899", // pink-500
    icon: "🤝",
    capabilities: ["synergy_detection", "alliance_mapping", "collaboration_opportunities"]
  },
  tracking: {
    name: "Agente de Seguimiento",
    description: "Monitorea progreso y genera reportes automáticos con métricas de impacto",
    color: "#10B981", // emerald-500
    icon: "📈",
    capabilities: ["progress_monitoring", "report_generation", "metrics_tracking"]
  },
  wellness: {
    name: "Agente de Bienestar",
    description: "Asegura sostenibilidad, detecta riesgo de burnout y recomienda descansos",
    color: "#F59E0B", // amber-500
    icon: "💚",
    capabilities: ["workload_assessment", "burnout_detection", "wellness_recommendations"]
  },
  impact: {
    name: "Agente de Impacto",
    description: "Evalúa impacto social y ambiental, asegura alineación con valores regenerativos",
    color: "#06B6D4", // cyan-500
    icon: "🌍",
    capabilities: ["impact_evaluation", "value_alignment", "regenerative_assessment"]
  }
};

// ============================================================================
// OBJECTIVE TYPES
// ============================================================================

export type ObjectiveDimension = "personal" | "professional" | "vital";
export type ObjectivePriority = "low" | "medium" | "high";
export type ObjectiveStatus = "active" | "paused" | "completed" | "archived";

// ============================================================================
// SYNERGY TYPES
// ============================================================================

export type SynergyType = 
  | "resource_sharing"
  | "skill_overlap"
  | "timeline_alignment"
  | "impact_multiplier"
  | "knowledge_transfer";

export type SynergyStatus = "detected" | "acknowledged" | "active" | "dismissed";

// ============================================================================
// COORDINATION TYPES
// ============================================================================

export type CoordinationCycleType = "daily" | "weekly" | "on_demand";
export type CoordinationStatus = "running" | "completed" | "failed";

// ============================================================================
// CHAT TYPES
// ============================================================================

export type ChatRole = "user" | "agent" | "system";

export interface ChatMessageMetadata {
  keywords?: string[];
  themes?: string[];
  relatedObjectives?: number[];
  confidence?: number;
  agentName?: string;
  agentColor?: string;
}

// ============================================================================
// ORGANIZATIONAL LEVELS
// ============================================================================

export type OrganizationalLevel = "typical" | "living_roles" | "hybrid" | "swarm";

export interface OrganizationalLevelMetadata {
  name: string;
  description: string;
  agentCount: number;
  color: string;
}

export const ORGANIZATIONAL_LEVELS: Record<OrganizationalLevel, OrganizationalLevelMetadata> = {
  typical: {
    name: "Típica",
    description: "6 agentes especializados base",
    agentCount: 6,
    color: "#4A90E2"
  },
  living_roles: {
    name: "Roles Vivos",
    description: "Roles profesionales regenerativos",
    agentCount: 11,
    color: "#7BCA63"
  },
  hybrid: {
    name: "Híbrida",
    description: "Roles híbridos-simbióticos del enjambre",
    agentCount: 17,
    color: "#BD10E0"
  },
  swarm: {
    name: "Enjambre",
    description: "Roles exclusivos SyncEros/S0φIA/AIA",
    agentCount: 12,
    color: "#F5A623"
  }
};
