import { Brand } from "./Brand";
import { ThemeToggle } from "./ThemeProvider";

export function AuthLayout({ children, titleId }) {
  return <main className="auth-page min-h-screen"><section className="auth-form-panel" aria-labelledby={titleId}><div className="auth-topline"><Brand /><ThemeToggle /></div>{children}</section><aside className="auth-visual-panel" aria-label="CPIP product overview"><div className="auth-visual-content"><p className="eyebrow">A clearer practice record</p><h2>Turn your solved problems into a learning signal.</h2><p>CPIP connects your competitive-programming history to a focused dashboard built around the work you have actually done.</p><div className="mini-flow" aria-label="Data flow: platform history, CPIP analysis, dashboard"><span>Platform history</span><i aria-hidden="true" /><span>CPIP analysis</span><i aria-hidden="true" /><span>Your dashboard</span></div></div></aside></main>;
}
