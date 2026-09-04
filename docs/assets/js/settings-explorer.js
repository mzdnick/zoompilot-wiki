/*
 * Settings explorer UI (docs/settings/explorer.md).
 *
 * Renders window.ZP_SETTINGS (docs/assets/js/settings-data.js) as a
 * searchable, filterable card grid. The canonical reference with full
 * notes stays docs/settings/index.md; every card links there. Without
 * JS the page shows the fallback links.
 */
(function () {
  "use strict";

  var mount = document.getElementById("zp-settings-explorer");
  var panels = window.ZP_SETTINGS;
  if (!mount || !panels) return;

  var state = { q: "", panel: "All" };

  /* Runtime-built hrefs bypass MkDocs link rewriting. Resolve the
   * reference page from a real markdown link on this page (the
   * noscript fallback carries one) instead of guessing a path. */
  var refBase = "";
  var refLink = mount.querySelector("noscript a");
  if (refLink) {
    refBase = refLink.getAttribute("href");
    if (refBase.indexOf("#") !== -1) {
      refBase = refBase.slice(0, refBase.indexOf("#"));
    }
  }

  mount.innerHTML = "";
  mount.className = "zp-explorer";

  /* controls */
  var controls = document.createElement("div");
  controls.className = "zp-explorer-controls";

  var search = document.createElement("input");
  search.type = "search";
  search.className = "zp-explorer-search";
  search.placeholder = "Search settings…";
  search.setAttribute("aria-label", "Search settings");

  var chips = document.createElement("div");
  chips.className = "zp-explorer-chips";
  chips.setAttribute("role", "tablist");
  var names = ["All"].concat(
    panels.map(function (p) { return p.panel; }),
  );
  names.forEach(function (name) {
    var chip = document.createElement("button");
    chip.type = "button";
    chip.className = "zp-explorer-chip";
    chip.textContent = name;
    chip.setAttribute("aria-pressed", name === "All" ? "true" : "false");
    chip.addEventListener("click", function () {
      state.panel = name;
      chips.querySelectorAll(".zp-explorer-chip").forEach(function (c) {
        c.setAttribute("aria-pressed", "false");
      });
      chip.setAttribute("aria-pressed", "true");
      render();
    });
    chips.appendChild(chip);
  });

  controls.appendChild(search);
  controls.appendChild(chips);
  mount.appendChild(controls);

  var count = document.createElement("p");
  count.className = "zp-explorer-count";
  mount.appendChild(count);

  var grid = document.createElement("div");
  grid.className = "zp-explorer-grid";
  mount.appendChild(grid);

  function card(item, panel) {
    var card = document.createElement("a");
    card.className = "zp-explorer-card";
    card.href = refBase + "#" + panel.anchor;
    var head = document.createElement("span");
    head.className = "zp-explorer-panel";
    head.textContent = panel.panel;
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
    card.appendChild(head);
    card.appendChild(name);
    card.appendChild(vals);
    card.appendChild(def);
    card.appendChild(note);
    return card;
  }

  function render() {
    var q = state.q.trim().toLowerCase();
    var shown = 0;
    grid.innerHTML = "";
    panels.forEach(function (panel) {
      if (state.panel !== "All" && state.panel !== panel.panel) return;
      panel.items.forEach(function (item) {
        if (
          q &&
          (item.name + " " + item.note + " " + item.values)
            .toLowerCase()
            .indexOf(q) === -1
        ) {
          return;
        }
        grid.appendChild(card(item, panel));
        shown++;
      });
    });
    count.textContent =
      shown === 0
        ? "No settings match. The full reference may word it differently."
        : shown + (shown === 1 ? " setting" : " settings") +
          (state.panel === "All" ? "" : " in " + state.panel);
  }

  search.addEventListener("input", function () {
    state.q = search.value;
    render();
  });

  render();
})();
