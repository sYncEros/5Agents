/**
 * File Upload System
 * Handles multiple file types: PDF, DOCX, TXT, CSV, JSON, images
 * Following Single Responsibility Principle
 */

import multer from "multer";
import path from "path";
import fs from "fs/promises";
import { nanoid } from "nanoid";

export interface UploadedFile {
  id: string;
  originalName: string;
  mimeType: string;
  size: number;
  path: string;
  uploadedAt: Date;
}

// Storage configuration
const UPLOAD_DIR = path.join(process.cwd(), "uploads");

// Ensure upload directory exists
export async function ensureUploadDir() {
  try {
    await fs.access(UPLOAD_DIR);
  } catch {
    await fs.mkdir(UPLOAD_DIR, { recursive: true });
  }
}

// Configure multer storage
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    await ensureUploadDir();
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const uniqueId = nanoid();
    const ext = path.extname(file.originalname);
    cb(null, `${uniqueId}${ext}`);
  },
});

// File filter
const fileFilter: multer.Options["fileFilter"] = (req, file, cb) => {
  const allowedMimes = [
    // Documents
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "text/plain",
    "text/markdown",
    // Data
    "text/csv",
    "application/json",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    // Images
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
  ];

  if (allowedMimes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error(`File type ${file.mimetype} not allowed`));
  }
};

// Multer instance
export const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB max
  },
});

/**
 * Process uploaded file and extract metadata
 */
export async function processUploadedFile(file: any): Promise<UploadedFile> {
  const uploadedFile: UploadedFile = {
    id: nanoid(),
    originalName: file.originalname,
    mimeType: file.mimetype,
    size: file.size,
    path: file.path,
    uploadedAt: new Date(),
  };

  return uploadedFile;
}

/**
 * Extract text content from various file types
 */
export async function extractTextContent(filePath: string, mimeType: string): Promise<string> {
  try {
    // Plain text files
    if (mimeType === "text/plain" || mimeType === "text/markdown") {
      return await fs.readFile(filePath, "utf-8");
    }

    // JSON files
    if (mimeType === "application/json") {
      const content = await fs.readFile(filePath, "utf-8");
      return JSON.stringify(JSON.parse(content), null, 2);
    }

    // CSV files
    if (mimeType === "text/csv") {
      return await fs.readFile(filePath, "utf-8");
    }

    // For other types, return placeholder
    // TODO: Implement PDF, DOCX extraction using external libraries
    return `[Content extraction for ${mimeType} not yet implemented]`;
  } catch (error) {
    console.error("Error extracting text content:", error);
    return "[Error extracting content]";
  }
}

/**
 * Delete uploaded file
 */
export async function deleteUploadedFile(filePath: string): Promise<void> {
  try {
    await fs.unlink(filePath);
  } catch (error) {
    console.error("Error deleting file:", error);
  }
}

/**
 * Get file type category
 */
export function getFileCategory(mimeType: string): "document" | "data" | "image" | "unknown" {
  if (mimeType.startsWith("image/")) return "image";
  if (mimeType.includes("pdf") || mimeType.includes("word") || mimeType.includes("text")) {
    return "document";
  }
  if (mimeType.includes("json") || mimeType.includes("csv") || mimeType.includes("excel")) {
    return "data";
  }
  return "unknown";
}
