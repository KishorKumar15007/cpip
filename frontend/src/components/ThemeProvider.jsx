import { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState("dark");
  useEffect(() => { document.documentElement.dataset.theme = theme; }, [theme]);
  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}

export function ThemeToggle() {
  const { theme, setTheme } = useContext(ThemeContext);
  const nextTheme = theme === "dark" ? "light" : "dark";
  return <button className="theme-toggle" type="button" onClick={() => setTheme(nextTheme)}><span aria-hidden="true">{theme === "dark" ? "◐" : "◑"}</span><span>{theme === "dark" ? "Light" : "Dark"}</span></button>;
}
