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
<svg viewBox="0 0 800 232" role="img" aria-label="One drive: the road camera and driving model see, the planners choose where in the lane and how fast, radar, blind-spot monitors, and speed signs feed the plan, the plan drives the EPS motor and the gas and brakes, self-tune learns your motor's response, and you supervise and can brake or cancel at any time">
  <defs>
    <marker id="zp-arrow" class="m-dim" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
    <marker id="zp-arrow-a" class="m-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  <rect class="d-box" x="30" y="40" width="180" height="64"/>
  <text class="d-hi" x="120" y="62" text-anchor="middle">sees</text>
  <text x="120" y="80" text-anchor="middle">road camera</text>
  <text x="120" y="96" text-anchor="middle">driving model</text>
  <line class="d-flow" x1="214" y1="72" x2="250" y2="72"/>
  <rect class="d-box" x="254" y="40" width="200" height="64"/>
  <text class="d-hi" x="354" y="62" text-anchor="middle">plans</text>
  <text x="354" y="80" text-anchor="middle">where in the lane</text>
  <text x="354" y="96" text-anchor="middle">how fast, how far</text>
  <line class="d-flow" x1="458" y1="72" x2="494" y2="72"/>
  <rect class="d-box" x="498" y="40" width="232" height="64"/>
  <text class="d-hi" x="614" y="62" text-anchor="middle">acts</text>
  <text x="614" y="80" text-anchor="middle">EPS motor</text>
  <text x="614" y="96" text-anchor="middle">gas · brakes</text>
  <line class="d-flow" x1="354" y1="136" x2="354" y2="108"/>
  <text x="354" y="152" text-anchor="middle">radar · blind spots · speed signs</text>
  <path class="d-flow-accent" d="M614,108 V172 H400 V108"/>
  <text x="606" y="166" text-anchor="end">learns your motor</text>
  <line class="d-lane" x1="30" y1="204" x2="730" y2="204"/>
  <text x="380" y="224" text-anchor="middle">you: supervise · brake or cancel ends it</text>
</svg>
</div>

zoompilot rewrites how this pipeline drives a Mazda — and the work
keeps reaching deeper into the stack.

## What a fork means

openpilot by comma.ai is the base. sunnypilot extends it with more
features and car-specific tuning. zoompilot takes sunnypilot and tunes
it for one brand: Mazda. The full lineage and credits are on
[What is zoompilot?](about.md).

zoompilot's Mazda-specific work today spans steering, cruise, sensors,
and the experimental alpha longitudinal. The sections below take them
in turn.

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
