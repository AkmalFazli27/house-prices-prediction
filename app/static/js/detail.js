(function () {
  const sections = document.querySelectorAll(".detail-section");
  const navItems = document.querySelectorAll(".detail-sidebar-item");

  function updateActiveSession() {
    let current = '';
    sections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= 150) {
        current = section.id.replace("section-", "");
      }
    });

    if (!current && sections.length > 0) {
        const last = sections[sections.length - 1];
        current = last.id.replace('section-', '');
    }
    navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.section === current);
    })
  }

  window.addEventListener('scroll', updateActiveSession, { passive: true});
  window.addEventListener('resize', updateActiveSession, { passive: true});
  updateActiveSession();
});
