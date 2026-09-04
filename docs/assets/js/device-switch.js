/*
 * Device switcher for the Settings reference (docs/settings/index.md).
 *
 * The reference documents both supported devices: comma four (mici) and
 * comma 3/3X (tici/tizi). Screenshots for both are embedded per panel as
 * .settings-figure-mici / .settings-figure-tici figures. This switcher
 * hides one set; the tables stay shared because the underlying settings
 * are the same params on both devices.
 *
 * Without JS both sets render stacked, so the page still works.
 * The choice persists in localStorage (key: zp-settings-device).
 */
(function () {
  "use strict";

  var STORAGE_KEY = "zp-settings-device";
  var DEFAULT_DEVICE = "mici";

  function apply(device) {
    var tici = device === "tici";
    document.body.classList.toggle("zp-device-tici", tici);
    var switches = document.querySelectorAll("[data-device-switch] button");
    for (var i = 0; i < switches.length; i++) {
      var btn = switches[i];
      var active = (btn.getAttribute("data-device") === device);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    }
  }

  function init() {
    var group = document.querySelector("[data-device-switch]");
    if (!group) return;

    // JS works: mark the page so CSS hides the inactive device's figures.
    document.body.classList.add("zp-device-pick");

    // URL wins over localStorage, so ?device=tici links can be shared.
    var urlDevice = new URLSearchParams(window.location.search).get("device");
    var saved = null;
    try {
      saved = window.localStorage.getItem(STORAGE_KEY);
    } catch (e) { /* storage unavailable */ }
    var device = (saved === "tici" || saved === "mici") ? saved : DEFAULT_DEVICE;
    if (urlDevice === "tici" || urlDevice === "mici") {
      device = urlDevice;
      try {
        window.localStorage.setItem(STORAGE_KEY, device);
      } catch (e) { /* ignore */ }
    }
    apply(device);

    group.addEventListener("click", function (event) {
      var btn = event.target.closest("button[data-device]");
      if (!btn) return;
      device = btn.getAttribute("data-device");
      try {
        window.localStorage.setItem(STORAGE_KEY, device);
      } catch (e) { /* ignore */ }
      apply(device);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
