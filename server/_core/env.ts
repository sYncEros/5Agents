const parseBoolean = (value: string | undefined) =>
  value === "true" || value === "1";

const parseNumber = (value: string | undefined, fallback: number) => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

const parseRole = (value: string | undefined) =>
  value === "admin" ? "admin" : "user";

export const ENV = {
  appId: process.env.VITE_APP_ID ?? "",
  cookieSecret: process.env.JWT_SECRET ?? "",
  databaseUrl: process.env.DATABASE_URL ?? "",
  oAuthServerUrl: process.env.OAUTH_SERVER_URL ?? "",
  ownerOpenId: process.env.OWNER_OPEN_ID ?? "",
  isProduction: process.env.NODE_ENV === "production",
  forgeApiUrl: process.env.BUILT_IN_FORGE_API_URL ?? "",
  forgeApiKey: process.env.BUILT_IN_FORGE_API_KEY ?? "",
  devAuthBypass: parseBoolean(process.env.DEV_AUTH_BYPASS),
  devAuthUserId: parseNumber(process.env.DEV_AUTH_USER_ID, 1),
  devAuthUserOpenId: process.env.DEV_AUTH_USER_OPEN_ID ?? "dev-user",
  devAuthUserName: process.env.DEV_AUTH_USER_NAME ?? "Dev User",
  devAuthUserEmail: process.env.DEV_AUTH_USER_EMAIL ?? "dev@example.com",
  devAuthUserRole: parseRole(process.env.DEV_AUTH_ROLE),
  devDemoMode: parseBoolean(process.env.DEV_DEMO_MODE),
};
