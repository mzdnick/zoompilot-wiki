---
title: How zoompilot works
reviewed: 2026-09
---

# How zoompilot works

This page follows one drive from camera to wheels, and shows what
zoompilot changes on the way. No prior openpilot knowledge needed.

## The stack, in one picture

openpilot is software that runs on a comma device. The device sits on
the car's camera harness and watches the road through the car's
forward camera. A neural network model reads that camera and the
planners turn its output into actuator requests. The car's own
computers do the physical work: the EPS motor turns the wheel, and the
powertrain control module (PCM) manages speed.

<div class="diagram">
<svg viewBox="0 0 800 188" role="img" aria-label="Pipeline: road camera feeds the driving model, the model feeds the lateral and longitudinal planners, the lateral planner drives the EPS motor through a torque controller, the longitudinal planner drives the PCM, and a self-tune loop runs from the EPS motor back to the torque controller">
  <defs>
    <marker id="zp-arrow" class="m-dim" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
    <marker id="zp-arrow-a" class="m-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  <rect class="d-box" x="20" y="80" width="120" height="48"/>
  <text class="d-hi" x="80" y="100" text-anchor="middle">road camera</text>
  <text x="80" y="116" text-anchor="middle">car harness</text>
  <line class="d-flow" x1="140" y1="104" x2="166" y2="104"/>
  <rect class="d-box" x="170" y="80" width="120" height="48"/>
  <text class="d-hi" x="230" y="100" text-anchor="middle">driving model</text>
  <text x="230" y="116" text-anchor="middle">neural network</text>
  <line class="d-flow" x1="290" y1="92" x2="316" y2="60"/>
  <line class="d-flow" x1="290" y1="116" x2="316" y2="148"/>
  <rect class="d-box-accent" x="320" y="36" width="170" height="48"/>
  <text class="d-hi" x="405" y="56" text-anchor="middle">lateral planner</text>
  <text x="405" y="72" text-anchor="middle">where in the lane</text>
  <rect class="d-box" x="320" y="124" width="170" height="48"/>
  <text class="d-hi" x="405" y="144" text-anchor="middle">longitudinal planner</text>
  <text x="405" y="160" text-anchor="middle">how fast, how far</text>
  <line class="d-flow-accent" x1="490" y1="60" x2="526" y2="60"/>
  <rect class="d-box-accent" x="530" y="36" width="140" height="48"/>
  <text class="d-hi" x="600" y="56" text-anchor="middle">torque controller</text>
  <text x="600" y="72" text-anchor="middle">7 learned bands</text>
  <line class="d-flow-accent" x1="670" y1="60" x2="700" y2="60"/>
  <rect class="d-box-accent" x="704" y="36" width="80" height="48"/>
  <text class="d-hi" x="744" y="56" text-anchor="middle">EPS</text>
  <text x="744" y="72" text-anchor="middle">motor</text>
  <line class="d-flow" x1="490" y1="148" x2="526" y2="148"/>
  <rect class="d-box" x="530" y="124" width="140" height="48"/>
  <text class="d-hi" x="600" y="144" text-anchor="middle">PCM</text>
  <text x="600" y="160" text-anchor="middle">gas · brakes</text>
  <path class="d-flow-accent" d="M744,88 V104 H640 V88"/>
  <text x="692" y="119" text-anchor="middle">self-tune measures it</text>
</svg>
</div>

Everything zoompilot changes happens in the middle: the planners, the
controllers, and what the car's sensors are allowed to say.

## What a fork means

openpilot by comma.ai is the base. sunnypilot extends it with more
features and car-specific tuning. zoompilot takes sunnypilot and tunes
it for one brand: Mazda. The full lineage and credits are on
[What is zoompilot?](about.md).

zoompilot's Mazda-specific work falls into four areas: steering, cruise,
sensors, and the experimental alpha longitudinal. The sections below
take them in turn.

## Steering: asking the motor for torque

The electric power steering (EPS) motor is what turns the front wheels.
openpilot does not move the steering wheel directly — it asks the EPS
for a torque, many times a second, and the motor delivers what it can.

Two facts about the 2022+ Mazda EPS motor shaped zoompilot's steering
work:

- **The motor is stronger than stock openpilot assumes.** openpilot
  caps its request at one conservative value for all speeds. The motor
  can deliver about 44% more where it matters, and zoompilot asks for
  it. See [Steering improvements](../features/steering.md).
- **The motor behaves differently at every speed.** Its output scale
  even drops from 1200 to 800 counts near 32 mph. One fixed tune cannot
  fit both parking lots and highways.

zoompilot's answer is the **speed-bin learner**. Driving is sorted into
seven speed bands, from parking speeds to highway. For each band,
[self-tune](../reference/glossary.md) measures two numbers — the torque
gain and the friction — and keeps a separate tune per band. Fresh
installs start from a tune learned on a real CX-5, then refine it to
your motor.

The motor's firmware also decides what zoompilot may do. The 2022+
CX-5 motor is the only one granted lateral from 0 mph, and it is the
key that unlocks alpha longitudinal. That check is the
[steer-to-zero flag](../technical/mazda-fingerprinting.md), and it is
why [EPS swaps](eps-swap.md) work: an older Mazda with that motor gets
the same treatment.

## Speed: who owns the gas and brakes

With stock software, Mazda's own radar cruise ECU controls speed.
openpilot sends it a target and the ECU executes. zoompilot adds its
cruise features on top of this: curve slowdowns, speed-limit awareness,
and a [cruise arbiter](../technical/cruise-arbiter.md) that keeps your
set speed yours. Dismiss a speed-limit change once, and it stays
dismissed until the limit on the road actually changes.

[Alpha longitudinal](../features/alpha-longitudinal.md) removes the
middleman: zoompilot's own planner drives gas and brakes directly. That
is the experimental mode. It comes with a hard trade-off — the radar
goes dark, and with it AEB and forward collision alerts. Read that
page before enabling it.

## Sensors: what the car already knows

The CX-5 carries sensors that the stock openpilot port ignores.
zoompilot wires them in. The forward radar reports up to four cars
ahead. The blind-spot monitor data backs the safety checks on
automatic lane changes. The LKAS camera reads speed-limit signs and
feeds [Speed-Limit Assist](../features/speed-limit-assist.md). See
[Sensor readouts](../features/sensor-readouts.md).

## The driver's part

You stay in the loop. Engage with the stock steering-wheel cruise
controls while driving; on 2022+ EPS Mazdas, steering help is
available from 0 mph. The device's driver-monitoring camera watches
your attention, and warns then disengages if it loses you. Brake or
press cancel, and the car is fully yours again. Read the
[safety page](../safety.md) before your first drive.

## Where to go next

- [Supported cars](supported-cars.md) — which Mazdas have the motor
  this page is about
- [Install](install.md) — put zoompilot on a comma device
- [First drive](first-drive.md) — recommended settings
- [Features](../features/steering.md) — what each change does on the road
- [Technical notes](../technical/index.md) — the measurement record
  behind every claim on this page
