export type AgentProcessRequest = {
  text: string;
  ritual_opt_in?: boolean;
};

export type AgentProcessResponse = {
  process_id: string;
  agents: Record<string, string>;
  analysis: {
    layers: string[];
    routing: string[];
    guardrails: string[];
    segments: Array<{
      text: string;
      layers: string[];
      emotions: Record<string, number>;
      projections: string[];
      topic: string | null;
      speaker: string | null;
      start_ms: number | null;
      end_ms: number | null;
    }>;
    metadata: Record<string, unknown>;
  };
};

function requiredEnv(name: string): string {
  const value = (import.meta.env[name] ?? "").toString().trim();
  if (!value) {
    throw new Error(
      `Falta configurar ${name}. Crea dashboard/.env y define ${name}.`
    );
  }
  return value;
}

function joinUrl(base: string, path: string): string {
  const b = base.replace(/\/+$/, "");
  const p = path.startsWith("/") ? path : `/${path}`;
  return `${b}${p}`;
}

export function getAgentApiBaseUrl(): string {
  return requiredEnv("VITE_AGENT_API_URL");
}

export async function agentProcess(
  payload: AgentProcessRequest
): Promise<AgentProcessResponse> {
  const base = getAgentApiBaseUrl();
  const res = await fetch(joinUrl(base, "/api/process"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${txt || res.statusText}`);
  }

  return res.json();
}