import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { finalizeRegistration } from "../api/client";
import { AuthLayout } from "../components/AuthLayout";
import { Button } from "../components/Button";
import { DocumentTitle } from "../components/DocumentTitle";
import { Feedback } from "../components/Feedback";
import { FormField } from "../components/FormField";
import { useAuthStore } from "../store/authStore";

export function UsernameSetupPage() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const navigate = useNavigate();
  const [username, setUsernameValue] = useState("");
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  if (accessToken) return <Navigate to="/dashboard" replace />;
  async function handleSubmit(event) {
    event.preventDefault(); setError(null);
    if (!/^[A-Za-z0-9_][A-Za-z0-9_-]{2,79}$/.test(username.trim())) { setError("Use 3–80 letters, numbers, underscores, or hyphens."); return; }
    setIsSubmitting(true);
    try { const tokens = await finalizeRegistration(username.trim()); useAuthStore.getState().setTokens(tokens); navigate("/dashboard", { replace: true }); } catch (requestError) { setError(requestError.message); } finally { setIsSubmitting(false); }
  }
  return <AuthLayout titleId="username-title"><DocumentTitle title="Choose username" description="Choose your CPIP username." /><div className="auth-copy"><p className="eyebrow">One last step</p><h1 id="username-title">Choose your CPIP username</h1><p>This name identifies your private practice workspace.</p></div><form className="auth-form" onSubmit={handleSubmit} noValidate><FormField id="username" label="Username"><input id="username" name="username" autoComplete="username" required value={username} onChange={(event) => setUsernameValue(event.target.value)} /></FormField>{error ? <Feedback tone="error">{error}</Feedback> : null}<Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Saving username…" : "Continue to dashboard"}</Button></form></AuthLayout>;
}
