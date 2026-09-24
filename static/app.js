(() => {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("pulse-theme");
  if (savedTheme) root.dataset.theme = savedTheme;

  const themeButton = document.querySelector("[data-theme-toggle]");
  if (themeButton) {
    themeButton.addEventListener("click", () => {
      const next = root.dataset.theme === "light" ? "dark" : "light";
      root.dataset.theme = next;
      localStorage.setItem("pulse-theme", next);
    });
  }

  const textInput = document.querySelector("[data-character-input]");
  const counter = document.querySelector("[data-character-count]");
  const updateCount = () => {
    if (!textInput || !counter) return;
    counter.textContent = textInput.value.length;
    counter.parentElement.style.color = textInput.value.length > 220 ? "var(--warning)" : "var(--accent-2)";
  };
  if (textInput) {
    textInput.addEventListener("input", updateCount);
    updateCount();
  }

  const imageInput = document.querySelector("[data-image-input]");
  const preview = document.querySelector("[data-image-preview]");
  if (imageInput && preview) {
    imageInput.addEventListener("change", () => {
      const [file] = imageInput.files;
      if (!file) return;
      preview.src = URL.createObjectURL(file);
      preview.classList.add("visible");
    });
  }

  document.querySelectorAll("[data-copy-url]").forEach((button) => {
    button.addEventListener("click", async () => {
      const original = button.innerHTML;
      try {
        await navigator.clipboard.writeText(button.dataset.copyUrl);
        button.innerHTML = "<span>✓</span><span>Copied</span>";
        setTimeout(() => (button.innerHTML = original), 1400);
      } catch (_) {
        window.prompt("Copy this link:", button.dataset.copyUrl);
      }
    });
  });
})();
