(function () {
  function initBackToTop() {
    var button = document.getElementById("back-to-top");
    if (!button) return;

    var showAfterPx = 350;
    var autoHideAfterMs = 1800;
    var ticking = false;
    var hideTimerId = null;

    function getScrollTop() {
      return (
        window.pageYOffset ||
        (document.documentElement && document.documentElement.scrollTop) ||
        0
      );
    }

    function isInteractingWithButton() {
      return button.matches(":hover") || document.activeElement === button;
    }

    function setFocusable(isFocusable) {
      if (isFocusable) {
        button.removeAttribute("tabindex");
        button.removeAttribute("aria-hidden");
      } else {
        button.setAttribute("tabindex", "-1");
        button.setAttribute("aria-hidden", "true");
      }
    }

    function clearAutoHideTimer() {
      if (hideTimerId) {
        clearTimeout(hideTimerId);
        hideTimerId = null;
      }
    }

    function scheduleAutoHide() {
      clearAutoHideTimer();
      hideTimerId = setTimeout(function () {
        var scrollTop = getScrollTop();
        if (scrollTop <= showAfterPx) return;
        if (isInteractingWithButton()) return;
        button.classList.remove("is-visible");
        setFocusable(false);
      }, autoHideAfterMs);
    }

    function setVisibility() {
      ticking = false;
      var scrollTop = getScrollTop();

      if (scrollTop > showAfterPx) {
        button.classList.add("is-visible");
        setFocusable(true);
        scheduleAutoHide();
      } else {
        button.classList.remove("is-visible");
        setFocusable(false);
        clearAutoHideTimer();
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

    button.addEventListener("mouseenter", function () {
      clearAutoHideTimer();
    });
    button.addEventListener("mouseleave", function () {
      if (button.classList.contains("is-visible")) scheduleAutoHide();
    });
    button.addEventListener("focus", function () {
      clearAutoHideTimer();
    });
    button.addEventListener("blur", function () {
      if (button.classList.contains("is-visible")) scheduleAutoHide();
    });

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
