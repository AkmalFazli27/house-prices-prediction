// animate number when scroll to stats-section
(function () {
  const stats = document.querySelector(".stats-section");
  if (!stats) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateStats();
          observer.disconnect();
        }
      });
    },
    { threshold: 0.5 },
  );
});

const statsSection = document.querySelector(".stats-section");
if (statsSection) observer.observe(statsSection);

function animateStats() {
  document.querySelectorAll(".stat-value").forEach((el) => {
    const target = parseFloat(el.textContent);
    // animate from 0 to target
  });
}
