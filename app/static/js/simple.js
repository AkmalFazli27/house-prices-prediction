// range slider - live value update + fill track
(function () {
  const slider = document.getElementById("overallqual");
  const value = document.getElementById("overallqual-value");
  if (slider && value) {
    function updateFill() {
      const min = +slider.min;
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

  const predResult = document.getElementById("prediction-result");
  if (predResult) predResult.scrollIntoView({ behavior: "smooth", block: "center" });
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
  const btn = this.querySelector(".btn-predict");
  btn.disabled = true;
  btn.innerHTML = "Predicting...";
});