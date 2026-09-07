---
title: ICBM
reviewed: 2026-09
---

# Intelligent Cruise Button Management (ICBM)

ICBM is the core system that lets zoompilot safely manage your cruise set
speed through the car's own cruise buttons. On cars without direct
longitudinal control, openpilot cannot command acceleration itself — ICBM
presses the stock cruise buttons for you, at the right moments.

<div class="diagram">
<svg viewBox="0 0 800 210" role="img" aria-label="The ICBM loop: target speed in, servo compares the gap, zoompilot presses the stock cruise buttons, the ECU applies a new set speed, and the readback feeds the servo">
  <defs>
    <marker id="zp-arrow" class="m-dim" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
    <marker id="zp-arrow-a" class="m-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  <rect class="d-box" x="60" y="20" width="180" height="48"/>
  <text class="d-hi" x="150" y="40" text-anchor="middle">target speed</text>
  <text x="150" y="56" text-anchor="middle">curve · zone · SLA</text>
  <rect class="d-box-accent" x="420" y="20" width="200" height="48"/>
  <text class="d-hi" x="520" y="40" text-anchor="middle">ICBM servo</text>
  <text x="520" y="56" text-anchor="middle">gap · pacing · resync</text>
  <line class="d-flow" x1="240" y1="44" x2="416" y2="44"/>
  <text x="328" y="36" text-anchor="middle">gap</text>
  <path class="d-flow-accent" d="M620,44 H660 V164 H624"/>
  <text x="682" y="100" class="d-hi">press</text>
  <rect class="d-box-accent" x="420" y="140" width="200" height="48"/>
  <text class="d-hi" x="520" y="160" text-anchor="middle">cruise button presses</text>
  <text x="520" y="176" text-anchor="middle">tap · hold</text>
  <line class="d-flow" x1="420" y1="164" x2="306" y2="164"/>
  <text x="363" y="156" text-anchor="middle">set speed ±</text>
  <rect class="d-box" x="100" y="140" width="200" height="48"/>
  <text class="d-hi" x="200" y="160" text-anchor="middle">stock cruise ECU</text>
  <text x="200" y="176" text-anchor="middle">your car, unmodified</text>
  <path class="d-flow-accent" d="M200,140 V104 H520 V72"/>
  <text x="360" y="98" text-anchor="middle">new set speed readback</text>
</svg>
</div>

## What it does for you

- **Restores your speed exactly.** The servo presses until the ECU's
  readback matches the target speed.
- **Hands control back instantly.** Press a cruise button yourself in the
  middle of an adjustment, and zoompilot stops and gives you control
  straight away.
- **Feels natural on big changes.** For large speed changes, ICBM holds
  the button down the way you would.
- **Stays quiet when you act.** Button presses are suppressed while you
  are pressing yours, and pacing adapts to how far the target speed is.

## Design details

ICBM is a servo loop over the button interface, with per-brand actuation
profiles. The full design record is in
[ICBM design notes](../technical/icbm.md); the way ICBM shares the set
speed with SLA is in
[Cruise arbiter](../technical/cruise-arbiter.md).
