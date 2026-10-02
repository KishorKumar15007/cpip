import { Feedback, LoadingState } from "./Feedback";

export { LoadingState };
export function ErrorState({ message, onRetry }) { return <Feedback tone="error" onAction={onRetry}>{message}</Feedback>; }
export function EmptyState({ message }) { return <Feedback>{message}</Feedback>; }
