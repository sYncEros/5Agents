import { z } from "zod";
import { ENV } from "./_core/env";
import { router, protectedProcedure } from "./_core/trpc";
import { storagePut } from "./storage";
import { transcribeAudio } from "./_core/voiceTranscription";

export const uploadRouter = router({
  // Subir archivo a S3
  uploadFile: protectedProcedure
    .input(z.object({
      fileName: z.string(),
      fileType: z.string(),
      fileData: z.string(), // Base64 encoded
    }))
    .mutation(async ({ input, ctx }) => {
      // Decodificar base64
      const buffer = Buffer.from(input.fileData, 'base64');
      const useDataUrl =
        ENV.devDemoMode && (!ENV.forgeApiUrl || !ENV.forgeApiKey);

      if (useDataUrl) {
        const contentType = input.fileType || "application/octet-stream";
        const dataUrl = `data:${contentType};base64,${input.fileData}`;
        return {
          url: dataUrl,
          name: input.fileName,
          type: input.fileType,
          size: buffer.length,
        };
      }
      
      // Generar nombre único para el archivo
      const timestamp = Date.now();
      const randomSuffix = Math.random().toString(36).substring(7);
      const fileKey = `chat-uploads/${ctx.user.id}/${timestamp}-${randomSuffix}-${input.fileName}`;
      
      // Subir a S3
      const { url } = await storagePut(fileKey, buffer, input.fileType);
      
      return {
        url,
        name: input.fileName,
        type: input.fileType,
        size: buffer.length,
      };
    }),

  // Transcribir audio
  transcribeAudio: protectedProcedure
    .input(z.object({
      audioUrl: z.string(),
      language: z.string().optional(),
    }))
    .mutation(async ({ input }) => {
      const result = await transcribeAudio({
        audioUrl: input.audioUrl,
        language: input.language,
      });
      
      if ('error' in result) {
        if (ENV.devDemoMode) {
          return {
            text: "Demo mode: transcription service not configured.",
            language: input.language ?? "unknown",
          };
        }
        throw new Error(result.error);
      }
      
      return {
        text: result.text,
        language: result.language,
      };
    }),
});
