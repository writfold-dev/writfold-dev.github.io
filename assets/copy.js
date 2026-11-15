// Copy buttons: each <button data-copy="…"> stays hidden unless the clipboard is usable,
// so without JavaScript the command beside it is plain selectable text.
document.addEventListener("DOMContentLoaded", () => {
  if (!navigator.clipboard) return;
  for (const button of document.querySelectorAll("button[data-copy]")) {
    button.hidden = false;
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(button.dataset.copy);
        button.textContent = "Copied";
      } catch {
        button.textContent = "Select the text";
      }
      setTimeout(() => { button.textContent = "Copy"; }, 2000);
    });
  }
});
