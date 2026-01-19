/**
 * Hugging Face API Integration Tests
 * Validates that the API key is correctly configured and functional
 */

import { describe, expect, it } from "vitest";
import { callHuggingFace, generateAgentResponse } from "../server/huggingface";

describe("Hugging Face API Integration", () => {
  it("should successfully call Hugging Face API with valid credentials", async () => {
    // Test with a simple prompt
    const response = await callHuggingFace({
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Say hello in one word." },
      ],
      max_tokens: 10,
      temperature: 0.5,
    });

    // Verify response structure
    expect(response).toBeDefined();
    expect(response.choices).toBeDefined();
    expect(response.choices.length).toBeGreaterThan(0);
    expect(response.choices[0].message).toBeDefined();
    expect(response.choices[0].message.content).toBeDefined();
    expect(typeof response.choices[0].message.content).toBe("string");
  }, 30000); // 30 second timeout for API call

  it("should generate agent response successfully", async () => {
    const response = await generateAgentResponse(
      "You are a research agent.",
      "What is AI?",
      [],
      {
        maxTokens: 50,
        temperature: 0.7,
      }
    );

    // Verify response is a non-empty string
    expect(response).toBeDefined();
    expect(typeof response).toBe("string");
    expect(response.length).toBeGreaterThan(0);
  }, 30000);
});
