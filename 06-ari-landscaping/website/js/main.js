/* Ari's Landscaping & Paving — interactions
   Vanilla JS, no dependencies. */

(function () {
  "use strict";

  /* ----- Mobile nav toggle ----- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ----- Before / After sliders ----- */
  document.querySelectorAll(".ba").forEach(function (ba) {
    var frame = ba.querySelector(".ba__frame");
    var after = ba.querySelector(".ba__after");
    var handle = ba.querySelector(".ba__handle");
    var range = ba.querySelector("input[type=range]");
    if (!frame || !after) return;

    function setPos(pct) {
      pct = Math.max(0, Math.min(100, pct));
      after.style.clipPath = "inset(0 0 0 " + pct + "%)";
      if (handle) handle.style.left = pct + "%";
      if (range && Number(range.value) !== Math.round(pct)) range.value = pct;
    }

    function fromEvent(clientX) {
      var rect = frame.getBoundingClientRect();
      setPos(((clientX - rect.left) / rect.width) * 100);
    }

    var dragging = false;
    frame.addEventListener("pointerdown", function (e) { dragging = true; frame.setPointerCapture(e.pointerId); fromEvent(e.clientX); });
    frame.addEventListener("pointermove", function (e) { if (dragging) fromEvent(e.clientX); });
    frame.addEventListener("pointerup", function () { dragging = false; });
    frame.addEventListener("pointercancel", function () { dragging = false; });
    if (range) range.addEventListener("input", function () { setPos(Number(range.value)); });

    setPos(50);
  });

  /* ----- Estimate form (front-end demo handler) ----- */
  var form = document.getElementById("estimate-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var success = document.getElementById("form-success");
      if (success) {
        form.style.display = "none";
        success.style.display = "block";
        success.setAttribute("tabindex", "-1");
        success.focus();
      }
      /* PRODUCTION: POST to the lead-capture endpoint / Make.com webhook here,
         then trigger the instant SMS+email auto-reply (see proposal Section 10). */
    });
  }

  /* ----- Footer year ----- */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();
})();
