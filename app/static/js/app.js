function initThemeToggle() {
  const btn = document.getElementById("theme-toggle-btn");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";

    // Optimistic UI update
    html.setAttribute("data-theme", next);
    btn.textContent = next === "dark" ? "☀️ Light" : "🌙 Dark";

    const csrfToken = document
      .querySelector('meta[name="csrf-token"]')
      .getAttribute("content");

    try {
      await fetch("/toggle-theme", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
      });
    } catch (err) {
      // Non-fatal: theme still applied locally for this session
      console.warn("Could not save theme preference:", err);
    }
  });
}

document.addEventListener("DOMContentLoaded", initThemeToggle);
