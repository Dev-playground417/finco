// Progressive enhancements. Every page works without this file.
(function () {
  "use strict";

  // Mobile navigation: disclosure button that toggles the main nav below 760px.
  function initNavToggle() {
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.getElementById("site-nav");
    if (!toggle || !nav) return;
    toggle.hidden = false;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("open", open);
    }

    toggle.addEventListener("click", () => {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && nav.classList.contains("open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener("click", (event) => {
      if (nav.classList.contains("open") && !nav.contains(event.target) && !toggle.contains(event.target)) {
        setOpen(false);
      }
    });
  }

  // Theme toggle: follows the OS preference until the user picks one, then remembers it.
  function initThemeToggle() {
    const button = document.querySelector(".theme-toggle");
    if (!button) return;
    const root = document.documentElement;
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    button.hidden = false;

    function isDark() {
      const explicit = root.getAttribute("data-theme");
      return explicit ? explicit === "dark" : media.matches;
    }

    function sync() {
      button.setAttribute("aria-pressed", String(isDark()));
    }

    button.addEventListener("click", () => {
      const next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem("theme", next);
      } catch (e) {
        // Storage unavailable (private mode); the choice lasts for this page only.
      }
      sync();
    });

    media.addEventListener("change", sync);
    sync();
  }

  // Quantity stepper: wraps a number input with −/+ buttons bounded by min/max.
  function initSteppers() {
    document.querySelectorAll("[data-stepper]").forEach((wrapper) => {
      const input = wrapper.querySelector("input[type='number']");
      if (!input) return;
      const min = Number(input.min) || 1;
      const max = Number(input.max) || Infinity;

      const makeButton = (label, text, delta) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "stepper-btn";
        btn.setAttribute("aria-label", label);
        btn.textContent = text;
        btn.addEventListener("click", () => {
          input.value = clamp((Number(input.value) || min) + delta);
          update();
        });
        return btn;
      };

      const clamp = (value) => Math.min(max, Math.max(min, value));
      const minus = makeButton("Decrease quantity", "−", -1);
      const plus = makeButton("Increase quantity", "+", 1);

      function update() {
        const value = Number(input.value) || min;
        minus.disabled = value <= min;
        plus.disabled = value >= max;
      }

      wrapper.prepend(minus);
      wrapper.append(plus);
      wrapper.classList.add("enhanced");
      input.addEventListener("input", update);
      input.addEventListener("change", () => {
        input.value = clamp(Number(input.value) || min);
        update();
      });
      update();
    });
  }

  // Prevent duplicate submissions (e.g. double-clicking "Place order").
  function initSingleSubmit() {
    document.querySelectorAll("form.js-single-submit").forEach((form) => {
      form.addEventListener("submit", (event) => {
        if (form.dataset.submitting) {
          event.preventDefault();
          return;
        }
        form.dataset.submitting = "true";
        const button = form.querySelector("button[type='submit']");
        if (button) {
          button.disabled = true;
          button.textContent = "Placing order…";
        }
      });
    });
    // Re-enable forms restored from the back/forward cache.
    window.addEventListener("pageshow", (event) => {
      if (!event.persisted) return;
      document.querySelectorAll("form.js-single-submit").forEach((form) => {
        delete form.dataset.submitting;
        const button = form.querySelector("button[type='submit']");
        if (button) {
          button.disabled = false;
          button.textContent = "Place order";
        }
      });
    });
  }

  // Apply a <select> (e.g. "Sort by") as soon as it changes; a submit button covers no-JS.
  function initSubmitOnChange() {
    document.querySelectorAll("select.js-submit-on-change").forEach((select) => {
      select.addEventListener("change", () => select.form.requestSubmit());
    });
  }

  initNavToggle();
  initSubmitOnChange();
  initThemeToggle();
  initSteppers();
  initSingleSubmit();
})();
