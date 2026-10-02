import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { getSubmissions } from "../api/client";
import { Brand } from "../components/Brand";
import { Button } from "../components/Button";
import { DocumentTitle } from "../components/DocumentTitle";
import { Feedback, LoadingState } from "../components/Feedback";
import { ThemeToggle } from "../components/ThemeProvider";
import { useAuthStore } from "../store/authStore";

const upcoming = ["Rating history", "Topic and difficulty patterns", "Practice activity"];

export function DashboardPage() {
  const clearAuth = useAuthStore((state) => state.clearAuth);
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const submissionsQuery = useQuery({ queryKey: ["submissions"], queryFn: getSubmissions });
  function handleLogout() { queryClient.removeQueries({ queryKey: ["submissions"] }); clearAuth(); navigate("/login", { replace: true }); }
  return <div className="dashboard-page"><DocumentTitle title="Dashboard" description="Your CPIP practice dashboard." /><header className="dashboard-header"><div className="container dashboard-nav"><Brand compact /><div className="dashboard-actions"><ThemeToggle /><Button type="button" variant="quiet" onClick={handleLogout}>Log out</Button></div></div></header><main className="container dashboard-main"><section className="dashboard-intro"><p className="eyebrow">Your CPIP workspace</p><h1>A home for the practice you have actually done.</h1><p>Dashboard analytics will appear here as each Phase 2 capability is built from your synced data.</p></section><section className="smoke-section" aria-labelledby="connection-title"><div><p className="eyebrow">Live connection</p><h2 id="connection-title">Submission history</h2><p>This panel verifies the authenticated FastAPI connection without inventing analytics values.</p></div>{submissionsQuery.isPending ? <LoadingState label="Loading recent submissions" /> : null}{submissionsQuery.isError ? <Feedback tone="error" onAction={submissionsQuery.refetch}>Unable to load submissions: {submissionsQuery.error.message}</Feedback> : null}{submissionsQuery.isSuccess && submissionsQuery.data.length === 0 ? <Feedback>Your account has no synced submissions yet. Sync data before this connection panel can show a result.</Feedback> : null}{submissionsQuery.isSuccess && submissionsQuery.data.length > 0 ? <Feedback tone="success">Connected securely. {submissionsQuery.data.length} recent submission{submissionsQuery.data.length === 1 ? "" : "s"} reached this React Query component.</Feedback> : null}</section><section className="upcoming-section" aria-labelledby="upcoming-title"><div className="section-intro"><p className="eyebrow">Dashboard foundation</p><h2 id="upcoming-title">Built to receive real analytics.</h2><p>These sections intentionally wait for their approved backend and UI tasks.</p></div><div className="upcoming-grid">{upcoming.map((title) => <article className="upcoming-card" key={title}><span>Planned</span><h3>{title}</h3><p>No data is shown until this feature has a defined, verified source.</p></article>)}</div></section></main></div>;
}
