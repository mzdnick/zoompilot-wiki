---
title: Settings explorer
hide:
  - navigation
---

# Settings explorer

Every on-device setting as a card: accepted values, default, and a
one-clause note. Type to search, or filter by panel. Cards link into
the [Settings reference](index.md), which stays canonical — it holds
the full notes, the Mazda seeding story, and where each default comes
from.

<div id="zp-settings-explorer" markdown="0">
<noscript>

The explorer needs JavaScript. The same content lives in the plain
[Settings reference](index.md): [Steering](index.md#steering),
[Cruise](index.md#cruise), [Models](index.md#models),
[Visuals](index.md#visuals), [Toggles](index.md#toggles),
[Device](index.md#device), [Software](index.md#software), and
[Developer](index.md#developer).

</noscript>
</div>

## Where the data comes from

The card data is generated from the reference tables in
`contrib/gen-settings-data.py`. The reference is canonical: edit it,
run the script, and commit the regenerated
`docs/assets/js/settings-data.js`. Cards show the reference wording,
with long notes clamped; the reference carries the full picture and
every "why".
