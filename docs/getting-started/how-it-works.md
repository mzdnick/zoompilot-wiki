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
forward camera, the FSC (forward sensing camera). A neural network
model reads that camera and the planners turn its output into actuator
requests. The car's own computers do the physical work: the EPS motor
turns the wheel, and the powertrain control module (PCM) manages
speed.

<div class="diagram">
<svg viewBox="0 0 800 260" role="img" aria-label="Module diagram: the Mazda forward camera, the FSC, feeds the driving model on the comma device. The lateral planner and torque controller steer the Mazda EPS. The longitudinal planner sends a set speed to the MRCC radar, which drives the PCM for gas and brakes; under alpha long the planner drives the PCM directly. Radar, blind-spot monitors, and speed signs feed in. Self-tune learns the EPS motor. The driver supervises and can brake or cancel at any time.">
  <defs>
    <marker id="zp-arrow" class="m-dim" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
    <marker id="zp-arrow-a" class="m-acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z"/></marker>
  </defs>
  <rect class="d-box" x="20" y="84" width="100" height="48"/>
  <text class="d-hi" x="70" y="104" text-anchor="middle">FSC</text>
  <text x="70" y="120" text-anchor="middle">forward camera</text>
  <line class="d-flow" x1="124" y1="108" x2="186" y2="108"/>
  <text x="155" y="101" text-anchor="middle">road view</text>
  <rect class="d-box" x="190" y="84" width="130" height="48"/>
  <text class="d-hi" x="255" y="104" text-anchor="middle">driving model</text>
  <text x="255" y="120" text-anchor="middle">vision</text>
  <line class="d-flow" x1="324" y1="96" x2="346" y2="56"/>
  <line class="d-flow" x1="324" y1="120" x2="346" y2="160"/>
  <rect class="d-box" x="350" y="32" width="140" height="48"/>
  <text class="d-hi" x="420" y="52" text-anchor="middle">lateral planner</text>
  <text x="420" y="68" text-anchor="middle">where in the lane</text>
  <line class="d-flow" x1="494" y1="56" x2="551" y2="56"/>
  <rect class="d-box" x="555" y="32" width="115" height="48"/>
  <text class="d-hi" x="612" y="52" text-anchor="middle">torque controller</text>
  <text x="612" y="68" text-anchor="middle">7 learned bands</text>
  <line class="d-flow" x1="674" y1="56" x2="701" y2="56"/>
  <rect class="d-box" x="705" y="32" width="80" height="48"/>
  <text class="d-hi" x="745" y="52" text-anchor="middle">EPS</text>
  <text x="745" y="68" text-anchor="middle">steering</text>
  <rect class="d-box" x="350" y="136" width="140" height="48"/>
  <text class="d-hi" x="420" y="156" text-anchor="middle">longitudinal planner</text>
  <text x="420" y="172" text-anchor="middle">how fast, how far</text>
  <line class="d-flow" x1="494" y1="160" x2="551" y2="160"/>
  <rect class="d-box" x="555" y="136" width="110" height="48"/>
  <text class="d-hi" x="610" y="156" text-anchor="middle">MRCC radar</text>
  <text x="610" y="172" text-anchor="middle">stock cruise</text>
  <line class="d-flow" x1="669" y1="160" x2="691" y2="160"/>
  <rect class="d-box" x="695" y="136" width="90" height="48"/>
  <text class="d-hi" x="740" y="156" text-anchor="middle">PCM</text>
  <text x="740" y="172" text-anchor="middle">gas · brakes</text>
  <path class="d-flow-accent" style="stroke-dasharray: 5 4" d="M420,188 V212 H740 V188"/>
  <text x="580" y="206" text-anchor="middle">alpha long</text>
  <path class="d-flow-accent" d="M745,84 V104 H612 V84"/>
  <text x="678" y="98" text-anchor="middle">learns your motor</text>
  <line class="d-flow" x1="222" y1="150" x2="222" y2="136"/>
  <text x="222" y="162" text-anchor="middle">radar · blind spots · speed signs</text>
  <line class="d-lane" x1="20" y1="232" x2="785" y2="232"/>
  <text x="402" y="252" text-anchor="middle">you: supervise · brake or cancel ends it</text>
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

With stock software, Mazda's radar cruise ECU — the MRCC radar —
controls speed. openpilot sends it a target and the ECU executes.
zoompilot adds its cruise features on top of this: curve slowdowns,
speed-limit awareness, and a [cruise arbiter](../technical/cruise-arbiter.md)
that keeps your set speed yours. Dismiss a speed-limit change once,
and it stays dismissed until the limit on the road actually changes.

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
