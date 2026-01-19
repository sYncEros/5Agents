import type { CreateExpressContextOptions } from "@trpc/server/adapters/express";
import type { User } from "../../drizzle/schema";
import { ENV } from "./env";
import { sdk } from "./sdk";

export type TrpcContext = {
  req: CreateExpressContextOptions["req"];
  res: CreateExpressContextOptions["res"];
  user: User | null;
};

export async function createContext(
  opts: CreateExpressContextOptions
): Promise<TrpcContext> {
  if (ENV.devAuthBypass) {
    const now = new Date();
    const user: User = {
      id: ENV.devAuthUserId,
      openId: ENV.devAuthUserOpenId,
      name: ENV.devAuthUserName,
      email: ENV.devAuthUserEmail,
      loginMethod: "dev",
      role: ENV.devAuthUserRole,
      createdAt: now,
      updatedAt: now,
      lastSignedIn: now,
    };

    return {
      req: opts.req,
      res: opts.res,
      user,
    };
  }

  let user: User | null = null;

  try {
    user = await sdk.authenticateRequest(opts.req);
  } catch (error) {
    // Authentication is optional for public procedures.
    user = null;
  }

  return {
    req: opts.req,
    res: opts.res,
    user,
  };
}
