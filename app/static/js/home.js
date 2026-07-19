// animate number when scroll to stats-section
(function () {
  const stats = document.querySelector(".stats-section");
  if (!stats) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounters();
          observer.disconnect();
        }
      });
    },
    { threshold: 0.4 },
  );

  observer.observe(stats);

  function animateCounters() {
    document.querySelectorAll(".stat-value").forEach((el) => {
      const target = parseFloat(el.textContent);
      if (isNaN(target)) return;

      const duration = 1200;
      const start = performance.now();

      function step(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);

        // ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = eased * target;

        // format: integer or 2 decimal
        el.textContent =
          target % 1 === 0
            ? Math.round(current)
            : current.toFixed(target.toString().split(".")[1]?.length || 2);
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
}) ();