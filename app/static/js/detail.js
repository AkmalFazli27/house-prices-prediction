(function () {
  const sections = document.querySelectorAll(".detail-section");
  const navItems = document.querySelectorAll(".detail-sidebar-item");
  let suppressUntil = 0;

  function updateActiveSection() {
    if (Date.now() < suppressUntil) return;

    const mid = window.innerHeight / 2;
    let current = "";

    sections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= mid && rect.bottom >= mid) {
        current = section.id.replace("section-", "");
      }
    });

    if (!current && sections.length > 0) {
      const first = sections[0].getBoundingClientRect();
      current = first.top > mid
        ? sections[0].id.replace("section-", "")
        : sections[sections.length - 1].id.replace("section-", "");
    }

    navItems.forEach((item) => {
      item.classList.toggle("active", item.dataset.section === current);
    });
  }

  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      suppressUntil = Date.now() + 300;
      navItems.forEach((n) => n.classList.toggle("active", n === this));
    });
  });

  window.addEventListener("scroll", updateActiveSection, { passive: true });
  window.addEventListener("resize", updateActiveSection, { passive: true });
  updateActiveSection();

  document.querySelectorAll('input[type="range"]').forEach((slider) => {
    slider.addEventListener("input", function () {
      const valueEl = document.getElementById(this.id + "-value");
      if (valueEl) valueEl.textContent = this.value;
    });
  });
  const predResult = document.getElementById("prediction-result");
  if (predResult) predResult.scrollIntoView({ behavior: "smooth", block: "center" });
})();
