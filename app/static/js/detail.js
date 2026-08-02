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
      let below = null;
      sections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        if (rect.top > mid && (!below || rect.top < below.rect.top)) {
          below = { id: section.id.replace("section-", ""), rect };
        }
      });
      if (below) {
        current = below.id;
      } else {
        let last = sections[0];
        sections.forEach((section) => {
          const rect = section.getBoundingClientRect();
          if (rect.bottom > 0 && rect.top < window.innerHeight) {
            last = section;
          }
        });
        current = last.id.replace("section-", "");
      }
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
