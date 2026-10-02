import { create } from "zustand";

export const useAuthStore = create((set) => ({
  accessToken: null,
  isInitializing: true,
  setTokens: ({ access_token: accessToken }) => set({ accessToken, isInitializing: false }),
  finishInitialization: () => set({ isInitializing: false }),
  clearAuth: () => set({ accessToken: null, isInitializing: false }),
}));
