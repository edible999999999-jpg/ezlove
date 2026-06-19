// Production API base URL - set before deploying mini-program
const PROD_API_BASE = "";

export const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8001/api/v1"
    : PROD_API_BASE + "/api/v1";
