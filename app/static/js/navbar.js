(function () {
  const toggle = document.getElementById("nav-toggle");
  const menu = document.getElementById("nav-menu");
  if (!toggle || !menu) return;

  function setOpen(open) {
    menu.classList.toggle("hidden", !open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".icon-open")?.classList.toggle("hidden", open);
    toggle.querySelector(".icon-close")?.classList.toggle("hidden", !open);
  }

  toggle.addEventListener("click", () => {
    setOpen(menu.classList.contains("hidden"));
  });

  document.addEventListener("click", (e) => {
    const nav = document.querySelector(".navbar");
    if (nav && !nav.contains(e.target)) setOpen(false);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });

  setOpen(false);
})();
