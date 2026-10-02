import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { register } from "../api/client";
import { AuthLayout } from "../components/AuthLayout";
import { Button } from "../components/Button";
import { DocumentTitle } from "../components/DocumentTitle";
import { Feedback } from "../components/Feedback";
import { FormField } from "../components/FormField";
import { useAuthStore } from "../store/authStore";

export function SignupPage() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [requestError, setRequestError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  if (accessToken) return <Navigate to="/dashboard" replace />;
  const updateField = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  function validate() {
    const next = {};
    if (!form.username.trim()) next.username = "Choose a username.";
    if (!/^\S+@\S+\.\S+$/.test(form.email)) next.email = "Enter a valid email address.";
    if (!form.password) next.password = "Enter a password.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }
  async function handleSubmit(event) {
    event.preventDefault(); setRequestError(null);
    if (!validate()) return;
    setIsSubmitting(true);
    try { await register({ username: form.username.trim(), email: form.email.trim(), password: form.password }); navigate("/login", { replace: true, state: { notice: "Account created. You can sign in now." } }); } catch (error) { setRequestError(error.message); } finally { setIsSubmitting(false); }
  }
  return <AuthLayout titleId="signup-title"><DocumentTitle title="Create account" description="Create a CPIP account for your private practice workspace." /><div className="auth-copy"><p className="eyebrow">Start your workspace</p><h1 id="signup-title">Create your CPIP account</h1><p>Your dashboard starts with an account and the data you choose to connect.</p></div><form className="auth-form" onSubmit={handleSubmit} noValidate><FormField id="username" label="Username" error={errors.username}><input id="username" name="username" autoComplete="username" required value={form.username} onChange={updateField} aria-describedby={errors.username ? "username-help" : undefined} /></FormField><FormField id="signup-email" label="Email" error={errors.email}><input id="signup-email" name="email" type="email" autoComplete="email" required value={form.email} onChange={updateField} aria-describedby={errors.email ? "signup-email-help" : undefined} /></FormField><FormField id="signup-password" label="Password" error={errors.password} hint="Your password is sent only to the existing CPIP registration endpoint."><div className="password-input"><input id="signup-password" name="password" type={showPassword ? "text" : "password"} autoComplete="new-password" required value={form.password} onChange={updateField} aria-describedby="signup-password-help" /><button type="button" className="input-action" onClick={() => setShowPassword((value) => !value)} aria-label={`${showPassword ? "Hide" : "Show"} password`}>{showPassword ? "Hide" : "Show"}</button></div></FormField>{requestError ? <Feedback tone="error">{requestError}</Feedback> : null}<Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Creating account…" : "Create account"}</Button></form><p className="auth-switch">Already have an account? <Link to="/login">Sign in</Link></p></AuthLayout>;
}
