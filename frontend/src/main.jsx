import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { ThemeProvider } from "./components/ThemeProvider";
import { refreshSession } from "./api/client";
import { useAuthStore } from "./store/authStore";
import "./styles.css";

function AuthBootstrap({ children }) {
  const initialized = React.useRef(false);
  const finishInitialization = useAuthStore((state) => state.finishInitialization);
  const setTokens = useAuthStore((state) => state.setTokens);
  React.useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;
    refreshSession().then(setTokens).catch(() => finishInitialization());
  }, [finishInitialization, setTokens]);
  return children;
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
      staleTime: 30_000,
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <AuthBootstrap><App /></AuthBootstrap>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>,
);
