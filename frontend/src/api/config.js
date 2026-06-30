// Production API base URL - set before deploying mini-program
const PROD_API_BASE = "";

export const MEDIA_BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8001"
    : PROD_API_BASE || "";

export const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8001/api/v1"
    : PROD_API_BASE + "/api/v1";

export function getFullUrl(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${MEDIA_BASE_URL}${url}`;
}
