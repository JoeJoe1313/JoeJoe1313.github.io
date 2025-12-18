(function () {
  function initBackToTop() {
    var button = document.getElementById("back-to-top");
    if (!button) return;

    var showAfterPx = 350;
    var ticking = false;

    function setVisibility() {
      ticking = false;
      var scrollTop =
        window.pageYOffset ||
        (document.documentElement && document.documentElement.scrollTop) ||
        0;

      if (scrollTop > showAfterPx) {
        button.classList.add("is-visible");
      } else {
        button.classList.remove("is-visible");
      }
    }

    window.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        (window.requestAnimationFrame || setTimeout)(setVisibility, 0);
      },
      { passive: true }
    );

    setVisibility();

    button.addEventListener("click", function (event) {
      event.preventDefault();
      try {
        window.scrollTo({ top: 0, behavior: "smooth" });
      } catch (err) {
        window.scrollTo(0, 0);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBackToTop);
  } else {
    initBackToTop();
  }
})();
