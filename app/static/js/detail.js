(function () {
  const sections = document.querySelectorAll(".detail-section");
  const navItems = document.querySelectorAll(".detail-sidebar-item");

  function updateActiveSection() {
    const offset = 150;
    let current = "";
    const lastSection = sections[sections.length - 1];

    if (lastSection) {
      const lastRect = lastSection.getBoundingClientRect();
      if (lastRect.bottom <= window.innerHeight) {
        current = lastSection.id.replace("section-", "");
      }
    }

    if (!current) {
      sections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= offset) {
          current = section.id.replace("section-", "");
        }
      });

      if (!current && sections.length > 0) {
        current = sections[0].id.replace("section-", "");
      }
    }

    navItems.forEach((item) => {
      item.classList.toggle("active", item.dataset.section === current);
    });
  }

  window.addEventListener("scroll", updateActiveSection, { passive: true });
  window.addEventListener("resize", updateActiveSection, { passive: true });
  updateActiveSection();

  document.querySelectorAll('input[type="range"]').forEach((slider) => {
    slider.addEventListener("input", function () {
      const valueEl = document.getElementById(this.id + "-value");
      if (valueEl) valueEl.textContent = this.value;
    });
  });

  const savedScroll = sessionStorage.getItem("detailScrollPos");
  if (savedScroll) {
    window.scrollTo({ top: parseInt(savedScroll, 10) });
    sessionStorage.removeItem("detailScrollPos");
  }

  // Persist prediction card across refresh
  const predCard = document.querySelector(".prediction-card");
  if (predCard) {
    sessionStorage.setItem("detailPrediction", predCard.outerHTML);
  } else if (!document.querySelector(".error-banner")) {
    const saved = sessionStorage.getItem("detailPrediction");
    if (saved) {
      const section = document.querySelector(".detail-content");
      if (section) section.insertAdjacentHTML("beforeend", saved);
    }
  }

  document.querySelector("form")?.addEventListener("submit", function () {
    sessionStorage.removeItem("detailPrediction");
    sessionStorage.setItem("detailScrollPos", window.scrollY);
  });
})();
