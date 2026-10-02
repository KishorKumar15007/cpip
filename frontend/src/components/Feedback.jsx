import { Button } from "./Button";

export function Feedback({ actionLabel = "Try again", children, onAction, tone = "neutral" }) {
  return <div className={`feedback feedback-${tone}`} role={tone === "error" ? "alert" : "status"}><p>{children}</p>{onAction ? <Button type="button" variant="quiet" onClick={onAction}>{actionLabel}</Button> : null}</div>;
}

export function LoadingState({ label }) {
  return <div className="loading-state" role="status"><span className="loading-mark" aria-hidden="true" />{label}</div>;
}
