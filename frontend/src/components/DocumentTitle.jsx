import { useEffect } from "react";

export function DocumentTitle({ title, description }) {
  useEffect(() => {
    document.title = `${title} · CPIP`;
    const tag = document.querySelector('meta[name="description"]');
    if (tag && description) tag.setAttribute("content", description);
  }, [description, title]);
  return null;
}
