(() => {
  const key = "writfold-theme";
  const root = document.documentElement;
  const valid = value => value === "light" || value === "paper-dark";
  let theme = "system";
  try {
    const saved = localStorage.getItem(key);
    if (valid(saved)) theme = saved;
  } catch { /* System remains usable when storage is unavailable. */ }
  if (valid(theme)) root.dataset.theme = theme;

  document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("theme");
    const source = document.querySelector(".wordmark picture source");
    const metas = document.querySelectorAll('meta[name="theme-color"]');
    function apply() {
      if (valid(theme)) root.dataset.theme = theme;
      else delete root.dataset.theme;
      source.media = theme === "system" ? "(prefers-color-scheme: light)" : theme === "light" ? "all" : "not all";
      for (const meta of metas) {
        meta.content = theme === "paper-dark" ? "#151d19" : theme === "light" || meta.media.includes("light") ? "#f7f8f4" : "#101922";
      }
      select.value = theme;
    }
    apply();
    select.addEventListener("change", () => {
      theme = valid(select.value) ? select.value : "system";
      apply();
      try {
        if (theme === "system") localStorage.removeItem(key);
        else localStorage.setItem(key, theme);
      } catch { /* The current page still honors the selected theme. */ }
    });
    select.closest("label").hidden = false;
  });
})();
