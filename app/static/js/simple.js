(function () {
  const slider = document.getElementById("overallqual");
  const value = document.getElementById("overallqual-value");
  if (slider && value) {
    slider.addEventListener("input", function () {
      value.textContent = this.value;
    });
  }
});
