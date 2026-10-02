import { useAuthStore } from "../store/authStore";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

async function parseResponse(response) {
  const body = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = typeof body?.detail === "string" ? body.detail : "Request failed.";
    const error = new Error(detail);
    error.status = response.status;
    throw error;
  }

  return body;
}

export async function apiRequest(path, options = {}, canRefresh = true) {
  const { accessToken } = useAuthStore.getState();
  const headers = new Headers(options.headers);

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (response.status === 401 && canRefresh && path !== "/auth/refresh") {
    try {
      const refreshed = await apiRequest(
        "/auth/refresh",
        {
          method: "POST",
        },
        false,
      );
      useAuthStore.getState().setTokens(refreshed);
      return apiRequest(path, options, false);
    } catch {
      useAuthStore.getState().clearAuth();
    }
  }

  return parseResponse(response);
}

export function login(credentials) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  }, false);
}

export function refreshSession() {
  return apiRequest("/auth/refresh", { method: "POST" }, false);
}

export function logout() {
  return apiRequest("/auth/logout", { method: "POST" }, false);
}

export function finalizeRegistration(username) {
  return apiRequest("/auth/register/finalize", { method: "POST", body: JSON.stringify({ username }) }, false);
}

export function register(account) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify(account),
  }, false);
}

export function getSubmissions() {
  return apiRequest("/submissions");
}

export function triggerSync(platform) {
  return apiRequest(`/sync/${platform}`, { method: "POST" });
}
