/**
 * Hugging Face API Integration
 * Provides access to various AI models for agent intelligence
 */

interface HuggingFaceMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface HuggingFaceRequest {
  model?: string;
  messages: HuggingFaceMessage[];
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
}

interface HuggingFaceResponse {
  choices: Array<{
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

/**
 * Default model configuration
 * Using meta-llama/Llama-3.2-3B-Instruct - small, fast, and free
 */
const DEFAULT_MODEL = "meta-llama/Llama-3.2-3B-Instruct";

/**
 * Call Hugging Face Inference API
 */
export async function callHuggingFace(request: HuggingFaceRequest): Promise<HuggingFaceResponse> {
  const apiKey = process.env.HUGGINGFACE_API_KEY;
  
  if (!apiKey) {
    throw new Error("HUGGINGFACE_API_KEY environment variable is not set");
  }

  const model = request.model || DEFAULT_MODEL;
  
  try {
    const response = await fetch(
      `https://router.huggingface.co/v1/chat/completions`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: model,
          messages: request.messages,
          temperature: request.temperature ?? 0.7,
          max_tokens: request.max_tokens ?? 1000,
          stream: false,
        }),
      }
    );

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Hugging Face API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    
    // The new API already returns OpenAI-compatible format
    return data as HuggingFaceResponse;
  } catch (error) {
    console.error("Error calling Hugging Face API:", error);
    throw error;
  }
}

/**
 * Simplified interface for agent interactions
 */
export async function generateAgentResponse(
  systemPrompt: string,
  userMessage: string,
  conversationHistory: HuggingFaceMessage[] = [],
  options?: {
    model?: string;
    temperature?: number;
    maxTokens?: number;
  }
): Promise<string> {
  const messages: HuggingFaceMessage[] = [
    { role: "system", content: systemPrompt },
    ...conversationHistory,
    { role: "user", content: userMessage },
  ];

  const response = await callHuggingFace({
    model: options?.model,
    messages,
    temperature: options?.temperature,
    max_tokens: options?.maxTokens,
  });

  return response.choices[0]?.message.content || "";
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
