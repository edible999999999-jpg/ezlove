import { request } from "./request";

export function wxLogin(code) {
  return request({ url: "/auth/wx-login", method: "POST", data: { code }, noAuth: true });
}

export function devLogin() {
  return request({ url: "/auth/dev-login", method: "POST", noAuth: true });
}

export function refreshToken(refresh_token) {
  return request({ url: "/auth/refresh", method: "POST", data: { refresh_token }, noAuth: true });
}
