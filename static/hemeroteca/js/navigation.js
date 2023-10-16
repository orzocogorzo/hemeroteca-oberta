window.addEventListener("DOMContentLoaded", () => {
  const nav = document.querySelector(".site-navigation");
  const burger = nav.querySelector(".burger");
  burger.addEventListener("click", show);

  function show() {
    if (nav.classList.contains("open")) {
      nav.classList.remove("open");
      document.body.removeEventListener("click", hide, true);
    } else {
      nav.classList.add("open");
      document.body.addEventListener("click", hide, true);
    }
  }

  function hide(ev) {
    if (nav.contains(ev.target) || nav === ev.target) return;
    ev.preventDefault();
    ev.stopPropagation();
    nav.classList.remove("open");
    document.body.removeEventListener("click", hide, true);
  }
});
