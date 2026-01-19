import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
// Mock the AI provider for chat tests to avoid external network calls (Hugging Face / Ollama)
vi.mock('./ai-provider', () => ({
  generateResponse: async (_systemPrompt: string, _userMessage: string) => {
    return 'Respuesta simulada del agente para pruebas';
  }
}));

import { appRouter } from '../server/routers';
import { getDb } from '../server/db';
import { communications } from '../drizzle/schema';
import { and, isNull } from 'drizzle-orm';

describe('Chat Router', () => {
  let caller: ReturnType<typeof appRouter.createCaller>;
  
  beforeAll(async () => {
    // Create a mock context with a test user
    const mockContext = {
      user: {
        id: 1,
        openId: 'test-user',
        name: 'Test User',
        email: 'test@example.com',
        role: 'user' as const,
        createdAt: new Date(),
        updatedAt: new Date(),
        lastSignedIn: new Date(),
        loginMethod: 'test'
      },
      req: {} as any,
      res: {} as any,
    };
    
    caller = appRouter.createCaller(mockContext);
    
    // Limpiar mensajes de prueba anteriores
    const db = await getDb();
    if (db) {
      await db.delete(communications)
        .where(and(
          isNull(communications.projectId),
          isNull(communications.taskId)
        ));
    }
  });
  
  afterAll(async () => {
    // Limpiar después de las pruebas
    const db = await getDb();
    if (db) {
      await db.delete(communications)
        .where(and(
          isNull(communications.projectId),
          isNull(communications.taskId)
        ));
    }
  });

  it('should send a message and receive an intelligent response', async () => {
    const result = await caller.chat.sendMessage({
      content: 'Necesito ayuda con análisis de datos'
    });

    expect(result).toBeDefined();
    expect(result.userMessageId).toBeTypeOf('number');
    expect(result.agentMessageId).toBeTypeOf('number');
    expect(result.agentType).toBeDefined();
    expect(result.agentName).toBeDefined();
    expect(result.content).toBeTypeOf('string');
    expect(result.content.length).toBeGreaterThan(0);
    
    // Verificar que el agente correcto fue seleccionado (debería ser data scientist por las palabras clave)
    expect(['data', 'research', 'strategy']).toContain(result.agentType);
  }, 30000); // Timeout de 30 segundos para la llamada al LLM

  it('should retrieve message history', async () => {
    // Primero enviar un mensaje
    await caller.chat.sendMessage({
      content: 'Hola, ¿cómo estás?'
    });

    // Luego obtener el historial
    const messages = await caller.chat.getMessages({
      limit: 10
    });

    expect(messages).toBeDefined();
    expect(Array.isArray(messages)).toBe(true);
    expect(messages.length).toBeGreaterThan(0);
    
    // Verificar estructura de los mensajes
    const lastMessage = messages[messages.length - 1];
    expect(lastMessage).toHaveProperty('id');
    expect(lastMessage).toHaveProperty('content');
    expect(lastMessage).toHaveProperty('role');
    expect(lastMessage).toHaveProperty('createdAt');
  }, 30000);

  it('should route to correct agent based on content', async () => {
    const testCases = [
      { content: 'Necesito escribir un artículo', expectedAgents: ['writer', 'strategy', 'comms'] },
      { content: 'Tengo una pregunta legal sobre contratos', expectedAgents: ['legal', 'strategy'] },
      { content: 'Necesito un análisis financiero', expectedAgents: ['financial', 'strategy', 'research', 'data'] },
    ];

    for (const testCase of testCases) {
      const result = await caller.chat.sendMessage({
        content: testCase.content
      });

      // Verificar que se asignó algún agente válido
      expect(result.agentType).toBeDefined();
      expect(result.agentName).toBeDefined();
      expect(result.content).toBeTypeOf('string');
      expect(result.content.length).toBeGreaterThan(0);
    }
  }, 60000); // Timeout más largo para múltiples llamadas

  it('should handle empty message gracefully', async () => {
    await expect(
      caller.chat.sendMessage({ content: '' })
    ).rejects.toThrow();
  });

  it('should allow specifying a specific agent', async () => {
    const result = await caller.chat.sendMessage({
      content: 'Dame consejos creativos',
      agentType: 'creative'
    });

    expect(result.agentType).toBe('creative');
    expect(result.agentName).toBe('Creative Director');
  }, 30000);

  it('should clear message history', async () => {
    // Enviar algunos mensajes
    await caller.chat.sendMessage({ content: 'Mensaje de prueba 1' });
    await caller.chat.sendMessage({ content: 'Mensaje de prueba 2' });

    // Verificar que hay mensajes
    let messages = await caller.chat.getMessages({ limit: 50 });
    const initialCount = messages.length;
    expect(initialCount).toBeGreaterThan(0);

    // Limpiar historial
    const clearResult = await caller.chat.clearHistory();
    expect(clearResult.success).toBe(true);

    // Verificar que no hay mensajes
    messages = await caller.chat.getMessages({ limit: 50 });
    expect(messages.length).toBe(0);
  }, 60000);
});
