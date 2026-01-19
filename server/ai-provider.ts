/**
 * Unified AI Provider
 * Automatically detects and uses available AI providers:
 * 1. Ollama (local, free, no limits) - Priority
 * 2. Hugging Face (cloud, requires API key) - Fallback
 */

import * as ollama from "./ollama";
import * as huggingface from "./huggingface";

export interface AIMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface AIProviderInfo {
  provider: "ollama" | "huggingface" | "none";
  available: boolean;
  models?: string[];
}

let cachedProvider: "ollama" | "huggingface" | null = null;
let lastCheck: number = 0;
const CACHE_DURATION = 60000; // 1 minute

/**
 * Detect which AI provider is available
 */
export async function detectProvider(): Promise<AIProviderInfo> {
  // Return cached result if recent
  const now = Date.now();
  if (cachedProvider && (now - lastCheck) < CACHE_DURATION) {
    return {
      provider: cachedProvider,
      available: true,
    };
  }

  // If a Hugging Face API key is present, prefer it (useful for CI or when Ollama models differ)
  const hasHFKey = !!process.env.HUGGINGFACE_API_KEY;
  if (hasHFKey) {
    cachedProvider = "huggingface";
    lastCheck = now;
    console.log("[AI Provider] Using Hugging Face API (preferred because HUGGINGFACE_API_KEY is set)");
    return {
      provider: "huggingface",
      available: true,
    };
  }

  // Check Ollama (local, free) as a fallback when Hugging Face key is not provided
  const ollamaAvailable = await ollama.isOllamaAvailable();
  if (ollamaAvailable) {
    const models = await ollama.getAvailableModels();
    cachedProvider = "ollama";
    lastCheck = now;
    console.log(`[AI Provider] Using Ollama with models: ${models.join(", ")}`);
    return {
      provider: "ollama",
      available: true,
      models,
    };
  }

  // No provider available
  cachedProvider = null;
  console.warn("[AI Provider] No AI provider available. Install Ollama or set HUGGINGFACE_API_KEY");
  return {
    provider: "none",
    available: false,
  };
}

/**
 * Generate AI response using available provider
 */
export async function generateResponse(
  systemPrompt: string,
  userMessage: string,
  conversationHistory: AIMessage[] = [],
  options?: {
    temperature?: number;
    maxTokens?: number;
  }
): Promise<string> {
  const providerInfo = await detectProvider();

  if (!providerInfo.available) {
    throw new Error(
      "No AI provider available. Please install Ollama (https://ollama.ai) or set HUGGINGFACE_API_KEY environment variable."
    );
  }

  try {
    if (providerInfo.provider === "ollama") {
      return await ollama.generateAgentResponse(
        systemPrompt,
        userMessage,
        conversationHistory,
        {
          temperature: options?.temperature,
        }
      );
    } else {
      return await huggingface.generateAgentResponse(
        systemPrompt,
        userMessage,
        conversationHistory,
        {
          temperature: options?.temperature,
          maxTokens: options?.maxTokens,
        }
      );
    }
  } catch (error) {
    console.error(`[AI Provider] Error with ${providerInfo.provider}:`, error);
    throw error;
  }
}

/**
 * Extract keywords from text (provider-independent)
 */
export function extractKeywords(text: string, limit = 6): string[] {
  return ollama.extractKeywords(text, limit);
}

/**
 * Estimate confidence score (provider-independent)
 */
export function estimateConfidence(response: string): number {
  return ollama.estimateConfidence(response);
}

/**
 * Force refresh provider detection
 */
export function refreshProvider(): void {
  cachedProvider = null;
  lastCheck = 0;
}
