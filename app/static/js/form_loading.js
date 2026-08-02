(function () {
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function (event) {
      if (event.defaultPrevented) return;

      const button = form.querySelector(".btn-predict");
      if (!button || button.disabled) return;

      button.disabled = true;
      button.setAttribute("aria-busy", "true");

      const label = button.querySelector(".btn-label");
      const idleIcon = button.querySelector(".btn-predict-icon");
      const spinner = button.querySelector(".btn-predict-spinner");

      if (label) label.textContent = "Predicting...";
      if (idleIcon) idleIcon.classList.add("hidden");
      if (spinner) spinner.classList.remove("hidden");
    });
  });
})();
