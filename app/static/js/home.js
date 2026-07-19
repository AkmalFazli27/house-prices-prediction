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

const statsSection = document.querySelector('.stats-section');
if (statsSection) observer.observe(statsSection);
