// range slider - live value update + fill track
(function () {
  const slider = document.getElementById("overallqual");
  const value = document.getElementById("overallqual-value");
  if (slider && value) {
    function updateFill() {
      const min = +slider.min || 1;
      const max = +slider.max || 10;
      const pct = ((slider.value - min) / (max - min)) * 100;
      slider.style.background = `linear-gradient(to right, var(--secondary) ${pct}%, var(--outline) ${pct}%)`;
    }
    slider.addEventListener("input", function () {
      value.textContent = this.value;
      updateFill();
    });
    updateFill();
  }

  const savedScroll = sessionStorage.getItem("simpleScrollPos");
  if (savedScroll) {
    window.scrollTo({ top: parseInt(savedScroll, 10) });
    sessionStorage.removeItem("simpleScrollPos");
  }

  // Persist prediction card across refresh
  const predCard = document.querySelector(".prediction-card");
  if (predCard) {
    sessionStorage.setItem("simplePrediction", predCard.outerHTML);
  } else if (!document.querySelector(".error-banner")) {
    const saved = sessionStorage.getItem("simplePrediction");
    if (saved) {
      const section = document.querySelector("section");
      if (section) section.insertAdjacentHTML("beforeend", saved);
    }
  }
}) ();

// form validation + loading state
document.querySelector("form")?.addEventListener("submit", function (e) {
  let valid = true;
  this.querySelectorAll("[required]").forEach((field) => {
    if (!field.value) {
      field.style.borderColor = "var(--error)";
      valid = false;
    } else {
      field.style.borderColor = "";
    }
  });
  if (!valid) {
    e.preventDefault();
    return;
  }
  sessionStorage.removeItem("simplePrediction");
  sessionStorage.setItem("simpleScrollPos", window.scrollY);
  const btn = this.querySelector(".btn-predict");
  btn.disabled = true;
  btn.innerHTML = "Predicting...";
});