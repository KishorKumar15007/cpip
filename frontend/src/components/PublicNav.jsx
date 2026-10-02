import { Link } from "react-router-dom";
import { Brand } from "./Brand";
import { Button } from "./Button";
import { ThemeToggle } from "./ThemeProvider";

export function PublicNav() {
  return <header className="public-header"><nav className="public-nav container" aria-label="Primary navigation"><Brand /><div className="public-nav-links"><a href="#features">Features</a><a href="#how-it-works">How it works</a><ThemeToggle /><Button to="/login" variant="secondary">Sign in</Button><Button to="/signup" className="nav-cta">Create account</Button></div></nav></header>;
}
