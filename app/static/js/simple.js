// range slider - live value update
(function () {
  const slider = document.getElementById("overallqual");
  const value = document.getElementById("overallqual-value");
  if (slider && value) {
    slider.addEventListener("input", function () {
      value.textContent = this.value;
    });
  }
});

// form validation
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
  if (!valid) e.preventDefault();
});
