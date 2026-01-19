/**
 * Ollama API Integration
 * Provides access to local AI models via Ollama
 * 
 * Installation:
 * 1. Install Ollama: https://ollama.ai/download
 * 2. Pull a model: ollama pull llama3.2
 * 3. Start Ollama service (usually runs automatically)
 * 
 * Default endpoint: http://localhost:11434
 */

interface OllamaMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface OllamaRequest {
  model: string;
  messages: OllamaMessage[];
  temperature?: number;
  stream?: boolean;
}

interface OllamaResponse {
  model: string;
  created_at: string;
  message: {
    role: string;
    content: string;
  };
  done: boolean;
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  eval_count?: number;
}

/**
 * Default Ollama configuration
 */
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || "http://localhost:11434";
const DEFAULT_MODEL = "llama3.2"; // Fast and capable 3B model

/**
 * Check if Ollama is available
 */
export async function isOllamaAvailable(): Promise<boolean> {
  try {
    const response = await fetch(`${OLLAMA_BASE_URL}/api/tags`, {
      method: "GET",
      signal: AbortSignal.timeout(2000), // 2 second timeout
    });
    return response.ok;
  } catch (error) {
    return false;
  }
}

/**
 * Get list of available models in Ollama
 */
export async function getAvailableModels(): Promise<string[]> {
  try {
    const response = await fetch(`${OLLAMA_BASE_URL}/api/tags`);
    if (!response.ok) {
      return [];
    }
    const data = await response.json();
    return data.models?.map((m: any) => m.name) || [];
  } catch (error) {
    console.error("Error fetching Ollama models:", error);
    return [];
  }
}

/**
 * Call Ollama API
 */
export async function callOllama(request: OllamaRequest): Promise<OllamaResponse> {
  const model = request.model || DEFAULT_MODEL;

  try {
    const response = await fetch(`${OLLAMA_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: model,
        messages: request.messages,
        temperature: request.temperature ?? 0.7,
        stream: false,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Ollama API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data as OllamaResponse;
  } catch (error) {
    console.error("Error calling Ollama API:", error);
    throw error;
  }
}

/**
 * Simplified interface for agent interactions
 */
export async function generateAgentResponse(
  systemPrompt: string,
  userMessage: string,
  conversationHistory: OllamaMessage[] = [],
  options?: {
    model?: string;
    temperature?: number;
  }
): Promise<string> {
  const messages: OllamaMessage[] = [
    { role: "system", content: systemPrompt },
    ...conversationHistory,
    { role: "user", content: userMessage },
  ];

  const response = await callOllama({
    model: options?.model || DEFAULT_MODEL,
    messages,
    temperature: options?.temperature,
  });

  return response.message.content || "";
}

/**
 * Extract keywords from text using simple NLP
 * This is a fallback when we don't want to call the API for simple tasks
 */
export function extractKeywords(text: string, limit = 6): string[] {
  const stopwords = new Set([
    "a", "al", "algo", "como", "con", "contra", "cuando", "de", "del", "desde",
    "donde", "el", "ella", "ellas", "ellos", "en", "entre", "era", "eres", "es",
    "esa", "ese", "eso", "esta", "este", "esto", "fue", "fueron", "ha", "han",
    "hasta", "hay", "la", "las", "le", "les", "lo", "los", "más", "muy", "no",
    "para", "pero", "por", "porque", "puede", "que", "qué", "se", "ser", "sin",
    "sobre", "su", "sus", "también", "tan", "te", "tiene", "todo", "un", "una",
    "y", "ya", "the", "this", "that", "with", "into", "from", "were", "have",
    "has", "will", "would", "about", "your", "such", "could", "should"
  ]);

  const tokens = text.toLowerCase().match(/[a-záéíóúñü]+/g) || [];
  const filtered = tokens.filter(token => token.length > 3 && !stopwords.has(token));
  
  // Count frequency
  const frequency = new Map<string, number>();
  filtered.forEach(token => {
    frequency.set(token, (frequency.get(token) || 0) + 1);
  });

  // Sort by frequency and return top N
  return Array.from(frequency.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([word]) => word);
}

/**
 * Estimate confidence score based on response characteristics
 */
export function estimateConfidence(response: string): number {
  const wordCount = response.split(/\s+/).length;
  const hasUncertainty = /quizás|tal vez|posiblemente|probablemente|maybe|perhaps|possibly/i.test(response);
  const hasDefinitiveness = /definitivamente|ciertamente|claramente|obviamente|definitely|certainly|clearly/i.test(response);
  
  let confidence = 0.5; // base
  
  // Longer responses tend to be more confident
  confidence += Math.min(wordCount / 200, 0.3);
  
  // Adjust for language markers
  if (hasDefinitiveness) confidence += 0.15;
  if (hasUncertainty) confidence -= 0.15;
  
  return Math.max(0.1, Math.min(0.95, confidence));
}
