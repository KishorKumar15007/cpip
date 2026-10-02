export function FormField({ error, id, label, children, hint }) {
  const helpId = hint || error ? `${id}-help` : undefined;
  return <div className="form-field"><label htmlFor={id}>{label}</label>{children}{(hint || error) ? <p id={helpId} className={error ? "field-error" : "field-hint"}>{error || hint}</p> : null}</div>;
}
