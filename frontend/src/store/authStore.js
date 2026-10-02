import { create } from "zustand";

export const useAuthStore = create((set) => ({
  accessToken: null,
  refreshToken: null,
  setTokens: ({ access_token: accessToken, refresh_token: refreshToken }) =>
    set({ accessToken, refreshToken }),
  clearAuth: () => set({ accessToken: null, refreshToken: null }),
}));
