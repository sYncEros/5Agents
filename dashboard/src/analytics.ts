const analyticsEndpoint = (import.meta.env.VITE_ANALYTICS_ENDPOINT ?? "").trim();
const analyticsWebsiteId = (
  import.meta.env.VITE_ANALYTICS_WEBSITE_ID ?? ""
).trim();

if (typeof document !== "undefined" && analyticsEndpoint && analyticsWebsiteId) {
  const normalizedEndpoint = analyticsEndpoint.replace(/\/+$/, "");
  const existingScript = document.querySelector(
    `script[data-website-id="${analyticsWebsiteId}"]`
  );

  if (!existingScript) {
    const script = document.createElement("script");
    script.defer = true;
    script.src = `${normalizedEndpoint}/umami`;
    script.setAttribute("data-website-id", analyticsWebsiteId);
    document.head.appendChild(script);
  }
}
