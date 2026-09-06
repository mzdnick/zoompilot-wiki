/*
 * Settings cards (docs/settings/index.md).
 *
 * Renders window.ZP_SETTINGS (docs/assets/js/settings-data.js — the
 * canonical data) as card grids inside each panel section, and wires
 * the search bar and panel chips above them. The page opens on the
 * first panel (Steering); the chips show one panel at a time. A search
 * covers every panel whatever the chip shows. Filtering hides cards in
 * place; a panel with no hits collapses, heading and screenshots
 * included. Panel anchors (#cruise, #device, …) select that panel on
 * load and on hashchange. Without JS the cards do not render; the page
 * carries a noscript pointer to the release sources.
 */
(function () {
  "use strict";

  var panels = window.ZP_SETTINGS;
  var controls = document.getElementById("zp-settings-controls");
  var count = document.getElementById("zp-settings-count");
  if (!panels || !controls) return;

  var state = { q: "", panel: panels[0].panel };

  /* the panel named by a #hash, or null — panel anchors equal the
   * panel headings' ids, which the data carries as "anchor" */
  function panelFromHash() {
    var id = location.hash.slice(1);
    var name = null;
    panels.forEach(function (p) {
      if (p.anchor === id) name = p.panel;
    });
    return name;
  }

  /* per-panel card mounts + the elements that make up each section
   * (heading, screenshots, intro), so a filtered-out panel can
   * collapse entirely */
  var mounts = {};
  var sections = {};
  document.querySelectorAll(".zp-panel-cards").forEach(function (mount) {
    var name = mount.getAttribute("data-panel");
    mounts[name] = mount;
    var els = [mount];
    var el = mount.previousElementSibling;
    while (el && el.tagName !== "H2") {
      els.push(el);
      el = el.previousElementSibling;
    }
    if (el) els.push(el);
    sections[name] = els;
  });

  function card(item) {
    var el = document.createElement("div");
    el.className = "zp-explorer-card";
    var name = document.createElement("strong");
    name.textContent = item.name;
    var vals = document.createElement("code");
    vals.textContent = item.values;
    var def = document.createElement("span");
    def.className = "zp-explorer-def";
    def.textContent = "default: " + item.def;
    var note = document.createElement("span");
    note.className = "zp-explorer-note";
    note.textContent = item.note;
    el.appendChild(name);
    el.appendChild(vals);
    el.appendChild(def);
    el.appendChild(note);
    return el;
  }

  panels.forEach(function (panel) {
    var mount = mounts[panel.panel];
    if (!mount) return;
    panel.items.forEach(function (item) {
      mount.appendChild(card(item));
    });
  });

  var search = document.createElement("input");
  search.type = "search";
  search.className = "zp-explorer-search";
  search.placeholder = "Search all panels…";
  search.setAttribute("aria-label", "Search settings in every panel");

  var chips = document.createElement("div");
  chips.className = "zp-explorer-chips";
  chips.setAttribute("role", "tablist");
  panels.map(function (p) { return p.panel; })
    .forEach(function (name) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "zp-explorer-chip";
      chip.textContent = name;
      chip.setAttribute("aria-pressed", name === state.panel ? "true" : "false");
      chip.addEventListener("click", function () {
        state.panel = name;
        chips.querySelectorAll(".zp-explorer-chip").forEach(function (c) {
          c.setAttribute("aria-pressed", "false");
        });
        chip.setAttribute("aria-pressed", "true");
        apply();
      });
      chips.appendChild(chip);
    });

  controls.appendChild(search);
  controls.appendChild(chips);

  function setPressedChip() {
    chips.querySelectorAll(".zp-explorer-chip").forEach(function (c) {
      c.setAttribute("aria-pressed", c.textContent === state.panel ? "true" : "false");
    });
  }

  function scrollToPanel() {
    var anchor = null;
    panels.forEach(function (p) {
      if (p.panel === state.panel) anchor = p.anchor;
    });
    var el = anchor && document.getElementById(anchor);
    if (el) el.scrollIntoView();
  }

  function apply() {
    var q = state.q.trim().toLowerCase();
    var searching = q.length > 0;
    var shown = 0;
    panels.forEach(function (panel) {
      var mount = mounts[panel.panel];
      if (!mount) return;
      var panelShown = 0;
      panel.items.forEach(function (item, i) {
        var hit = !q ||
          (item.name + " " + item.note + " " + item.values)
            .toLowerCase()
            .indexOf(q) !== -1;
        mount.children[i].hidden = !hit;
        if (hit) panelShown++;
      });
      /* a query spans every panel; a chip shows one panel */
      var panelVisible =
        (searching || state.panel === panel.panel) && panelShown > 0;
      (sections[panel.panel] || []).forEach(function (el) {
        el.hidden = !panelVisible;
      });
      if (panelVisible) shown += panelShown;
    });
    if (count) {
      count.textContent = shown === 0
        ? "No settings match. The reference wording may differ."
        : searching
          ? shown + (shown === 1 ? " setting" : " settings") +
            " matching \u201C" + state.q.trim() + "\u201D, all panels"
          : shown + (shown === 1 ? " setting" : " settings") +
            " in " + state.panel;
    }
  }

  search.addEventListener("input", function () {
    state.q = search.value;
    apply();
  });

  /* cross-page links target panels directly (faq #toggles,
   * troubleshooting #device), so the browser's own anchor scroll can
   * run while the section is still hidden — re-scroll once shown */
  var hashPanel = panelFromHash();
  if (hashPanel) state.panel = hashPanel;
  setPressedChip();
  apply();
  if (hashPanel) {
    window.setTimeout(scrollToPanel, 150);
  }

  window.addEventListener("hashchange", function () {
    var name = panelFromHash();
    if (!name) return;
    state.panel = name;
    setPressedChip();
    apply();
    scrollToPanel();
  });
})();
