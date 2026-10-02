import { Link } from "react-router-dom";

export function Brand({ compact = false }) {
  return <Link className="brand" to="/home" aria-label="CP Intelligence Platform home"><span className="brand-mark" aria-hidden="true">CP</span><span className="brand-copy"><strong>CPIP</strong>{!compact ? <small>Competitive Programming Intelligence</small> : null}</span></Link>;
}
