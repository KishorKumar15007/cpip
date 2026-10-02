import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { login } from "../api/client";
import { useAuthStore } from "../store/authStore";
import { AuthLayout } from "../components/AuthLayout";
import { Button } from "../components/Button";
import { DocumentTitle } from "../components/DocumentTitle";
import { Feedback } from "../components/Feedback";
import { FormField } from "../components/FormField";

export function LoginPage() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const setTokens = useAuthStore((state) => state.setTokens);
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  if (accessToken) {
    return <Navigate to="/dashboard" replace />;
  }

  function updateField(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError(null);
    if (!/^\S+@\S+\.\S+$/.test(form.email) || !form.password) {
      setError("Enter your email address and password.");
      return;
    }
    setIsSubmitting(true);
    try {
      const tokens = await login(form);
      setTokens(tokens);
      navigate(location.state?.from?.pathname || "/dashboard", { replace: true });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return <AuthLayout titleId="login-title"><DocumentTitle title="Sign in" description="Sign in to your CPIP dashboard." /><div className="auth-copy"><p className="eyebrow">Welcome back</p><h1 id="login-title">Sign in to CPIP</h1><p>Continue to your private practice workspace.</p></div>{location.state?.notice ? <Feedback tone="success">{location.state.notice}</Feedback> : null}<form className="auth-form" onSubmit={handleSubmit} noValidate><FormField id="email" label="Email"><input id="email" name="email" type="email" autoComplete="email" required value={form.email} onChange={updateField} /></FormField><FormField id="password" label="Password"><div className="password-input"><input id="password" name="password" type={showPassword ? "text" : "password"} autoComplete="current-password" required value={form.password} onChange={updateField} /><button type="button" className="input-action" onClick={() => setShowPassword((value) => !value)} aria-label={`${showPassword ? "Hide" : "Show"} password`}>{showPassword ? "Hide" : "Show"}</button></div></FormField><button type="button" className="text-button unavailable-control" disabled title="Password reset is not configured yet.">Forgot password? <span>Not available yet</span></button>{error ? <Feedback tone="error">{error}</Feedback> : null}<Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Signing in…" : "Sign in"}</Button></form><div className="auth-divider"><span>Alternative sign-in</span></div><div className="oauth-actions" aria-describedby="oauth-help"><button type="button" className="oauth-button" disabled>Continue with Google <small>Not configured</small></button><button type="button" className="oauth-button" disabled>Continue with GitHub <small>Not configured</small></button></div><p id="oauth-help" className="availability-note">Google, GitHub, and password recovery need backend support before they can be enabled.</p><p className="auth-switch">New to CPIP? <Link to="/signup">Create an account</Link></p></AuthLayout>;
}
