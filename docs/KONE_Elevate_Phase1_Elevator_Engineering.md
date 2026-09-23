# PHASE 1 — ELEVATOR ENGINEERING & PHYSICAL SYSTEM

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

---

## How to Read This Chapter Set

Almost everything in the three chapters that follow is **general elevator and electrical-engineering knowledge** — the physics of traction, how a variable-frequency drive works, how a permanent-magnet synchronous motor is controlled, how door and brake systems typically fail. This knowledge applies across the elevator industry; it is not a disclosure of KONE's internal designs. Where something is genuinely specific to a named KONE product or service, or where the project's own source documents made a claim, it is labeled as such. Four labels are used:

- **PUBLICLY DOCUMENTED** — stated by KONE (or another named vendor) in public materials cited in the project's own research roadmap.
- **GENERAL ELEVATOR INDUSTRY KNOWLEDGE** — standard mechanical/electrical engineering, true of traction elevators broadly, not exclusive to any one manufacturer. This is the label for the large majority of this chapter set.
- **PROJECT ASSUMPTION** — an inference this book makes to keep the material concrete, clearly flagged as such.
- **Research Gap / Proprietary Information** — called out explicitly, in its own box, wherever the true answer is internal to KONE (or another OEM) and not publicly available. Nothing is invented to fill these gaps.

**A scope decision, stated up front:** the project's roadmap leaves "which elevator architecture" as an open question, but nearly every piece of engineering material in the source documents — the motor, drive, traction sheave, rope, and counterweight discussion; the sensor list; the fault examples — describes a **traction elevator**, and specifically one consistent with a modern **gearless, permanent-magnet-motor machine** (the dominant architecture in KONE's current flagship products). *[PROJECT ASSUMPTION]* This chapter set follows that implied scope: traction elevators get full depth, other architectures (hydraulic, MRL-as-a-variant-of-traction, etc.) are covered at the level needed for contrast and completeness.

## What You Will Be Able to Answer After Phase 1

1. How does a modern traction elevator work, end to end?
2. What are its major mechanical components, and what does each one do?
3. How does the motor actually move the car?
4. How does the drive control the motor?
5. How does the controller know where the elevator is?
6. How do doors operate?
7. How does the brake work?
8. What can fail in each subsystem?
9. What physical symptoms does each failure create?
10. What sensors can observe those symptoms?
11. What alarms might be generated?
12. Why can one fault produce many alarms?
13. Why can one alarm have many possible root causes?
14. Why can a mechanical fault appear as an electrical fault?
15. Why does all of this matter for autonomous fault isolation and RCA?

---
---

# CHAPTER 1 — ELEVATOR FUNDAMENTALS, ARCHITECTURE & OPERATING PRINCIPLES

## 1.1 What Is an Elevator, and Why Do Different Architectures Exist?

At its simplest, an elevator is a machine that moves a platform (the **car**) vertically along fixed guides, on demand, safely and repeatably. Everything else — motors, ropes, sensors, controllers — exists to make that one sentence true under real-world constraints: variable load (an empty car vs. a full one), variable travel distance (a two-floor building vs. a sixty-floor tower), strict positioning accuracy (the car floor must land within millimeters of the landing floor), and, above all, an extremely high safety bar, because failure modes can be lethal. *[GENERAL ELEVATOR INDUSTRY KNOWLEDGE]*

Different elevator architectures exist because no single mechanism is efficient across all of those constraints simultaneously. A short building with modest traffic doesn't need the same machine as a 60-story tower; a small freight lift doesn't need the same precision-leveling system as a hospital bed elevator. The architecture is chosen to match rise (building height), speed, load, duty cycle, and space/cost constraints.

## 1.2 Elevator Classifications

*[GENERAL ELEVATOR INDUSTRY KNOWLEDGE throughout this section]*

| Architecture | How it moves the car | Machine room | Typical rise/speed | Typical use |
|---|---|---|---|---|
| **Geared traction** | Motor drives the sheave through a reduction gearbox | Often a dedicated machine room | Low–mid rise, moderate speed | Older/mid-rise buildings; being phased out in new installs in favor of gearless |
| **Gearless traction** | Motor drives the sheave directly, no gearbox | Machine room or machine-room-less | Mid–high rise, high speed | Modern default for most passenger elevators, including most current KONE products |
| **Machine-room-less (MRL)** | A compact gearless machine mounted in the hoistway itself | None — machine is in the shaft | Low–high rise | Common in new builds; saves building space |
| **Hydraulic** | A fluid-filled piston (ram) pushes the car directly, no ropes/counterweight in the traditional sense | Machine room with pump unit, often at the base | Low rise only (a handful of floors) | Low-rise buildings where a hoistway-top machine isn't practical |
| **Vacuum / pneumatic** | Air-pressure differential moves a sealed cab | None | Very low rise, low traffic | Niche residential installs |

Within these mechanical architectures, elevators are also classified by **use case** — passenger, freight/goods (higher load capacity, different door and finish requirements), high-rise vs. low/mid-rise (different rope, drive-power, and speed requirements), and hospital/service elevators (larger cars for beds/gurneys, different door timing and load-sensing tolerances, often higher duty cycles).

**Traction is the architecture this book focuses on**, because it is the one built from a rope-and-sheave-and-counterweight system whose *physics* — not just its control electronics — is central to how faults manifest and get confused with one another. That physics is the subject of §1.5, and it is the foundation the whole project's RCA reasoning rests on.

> **RCA CONNECTION:** Different architectures fail differently. A hydraulic elevator has no rope-slip or counterweight-imbalance failure mode at all, but has pump and hydraulic-fluid failure modes a traction elevator doesn't. Any fault-tree or Bayesian prior this project builds is architecture-specific — it should not be assumed to transfer to a hydraulic or pneumatic installation without re-derivation.

## 1.3 The Complete Traction-Elevator Operating Cycle

This is the single most important sequence in Chapter 1 — everything in Chapters 2 and 3 is a deeper look at one link in this chain.

```
Passenger requests a floor (hall call / car call)
        ↓
Controller determines the movement plan
        ↓
Controller commands the drive
        ↓
Drive releases the brake and commands the motor
        ↓
Motor generates torque
        ↓
Traction sheave rotates
        ↓
Ropes/belts transmit motion (friction-based grip, not a rigid link)
        ↓
Car and counterweight move in opposite directions
        ↓
Position/speed feedback reports location continuously
        ↓
Controller compares actual vs. commanded motion, corrects in real time
        ↓
Elevator decelerates approaching the target floor
        ↓
Elevator enters the leveling zone (fine positioning)
        ↓
Brake re-engages and holds the car
        ↓
Door system receives permission and opens
```

Walking through each stage:

**Request → plan.** A hall call (button at a landing) or car call (button inside the car) registers with the controller. In a single-car system the "plan" is simple (go there next, in this order); in multi-car systems the controller also decides *which* car should answer, but that dispatch logic is outside this chapter's scope.

**Plan → drive command.** The controller doesn't move the motor directly. It sends a **motion profile** — a target speed curve over time (accelerate, run at rated speed, decelerate, creep into position) — to the drive, which is the component actually responsible for realizing that profile electrically.

**Brake release, then torque.** Before the motor is asked to move the car, the brake — which is engaged by default (a fail-safe, spring-applied design covered in §1.4 and in depth in Chapter 3) — must release. The drive then commands the motor to produce torque in the required direction.

**Torque → sheave rotation → rope motion.** The motor's rotating shaft turns the traction sheave (directly, in a gearless machine). The ropes sit in grooves around the sheave and move with it **because of friction**, not because they are rigidly attached — this is the single most consequential fact in elevator physics, and §1.5 explains why.

**Rope motion → car and counterweight.** The car hangs from one end of the rope system; a counterweight (roughly balancing the car plus a fraction of rated load) hangs from the other, over the sheave. As the car goes up, the counterweight goes down, and vice versa — this balancing dramatically reduces how much torque the motor needs to supply for a given amount of motion.

**Continuous feedback.** An encoder (almost always on the motor shaft, sometimes supplemented by an independent absolute-position reference in the hoistway) reports position and speed many times per second. The controller uses this to run a **closed-loop** correction: compare the commanded profile to the actual behavior, and continuously adjust.

**Deceleration and leveling.** As the car nears its target floor, the controller commands the speed profile back down. A separate, more precise **leveling zone** sensor (distinct from the main encoder in many designs) takes over for the final few centimeters, because the accuracy needed to align the car floor with the landing floor is tighter than the main position loop typically needs to guarantee elsewhere in the run.

**Stop, hold, unlock.** Once stopped and confirmed level, the brake re-engages *before* the drive removes holding torque — because the sheave-rope friction alone is not considered a safe way to hold a stationary, loaded car. Only after the brake is confirmed engaged **and** the car is confirmed level within tolerance does the door system receive permission to unlock and open.

> **Why This Matters to KONE Elevate RCA:** This chain is the backbone of every fault episode the system will ever investigate. A fault episode is, structurally, "something in this chain didn't happen the way it was supposed to" — and the further downstream the observed symptom is, the more upstream candidate causes there are to weigh. A leveling-accuracy complaint, for instance, could originate at the encoder, the brake, the rope, or the sheave — all of which sit upstream of "leveling" in this chain. Understanding the chain is what lets the RCA Agent's hypothesis generation be *elevator-informed* rather than a generic pattern match over alarm codes.

## 1.4 Mechanical Architecture: The Components That Make Motion Possible

This section explains *what each component is, where it sits, what it does, why it's necessary, and what it interacts with* — the functional picture. Chapter 3 picks these same components back up and asks *what happens when each one degrades*, in full failure-mode depth, so this section deliberately does not repeat that analysis.

**Motor.** Converts electrical energy into rotational torque. In a modern gearless traction elevator, it is a permanent-magnet synchronous motor (PMSM — see Chapter 2), directly coupled to the sheave.

**Machine.** The general term for the motor + sheave + (if present) brake, assembled as one unit — "the machine" in elevator terminology usually refers to this whole drive unit, not the motor alone.

**Traction sheave.** The grooved wheel the ropes wrap around. Its groove profile and surface condition determine how much friction is available to grip the ropes — this is the physical heart of "traction."

**Ropes / coated belts.** Traditionally steel wire ropes; increasingly, flat coated-steel-cord belts (thinner, lighter, allow smaller sheaves) in modern machines. They transmit the sheave's rotation into linear car/counterweight motion, purely via friction against the sheave.

**Car and car frame.** The car is the passenger cabin; the car frame (or "sling") is the structural steel frame that actually carries the load and connects to the ropes, guide shoes, and safety gear. The decorative cabin the passenger sees is mounted inside this frame.

**Counterweight.** A mass, connected to the opposite end of the rope system from the car, sized to roughly balance the car's own weight plus a fraction (commonly around 40–50% of rated load, though the exact figure is a design and code choice) of rated capacity. *[GENERAL ELEVATOR INDUSTRY KNOWLEDGE]* Its purpose is purely to reduce the net torque the motor must supply — without it, the motor would have to lift the full weight of the car on every upward trip.

**Guide rails and guide shoes.** Vertical steel rails run the length of the hoistway; guide shoes (or rollers, in higher-speed installations) mounted on the car frame and counterweight ride along them, constraining motion to a straight vertical line and resisting horizontal sway.

**Brake.** A fail-safe, normally-engaged mechanical brake — spring-applied, electrically released (covered in depth in Chapter 3). It is not a "stopping" brake in the automotive sense so much as a **holding** brake: its job is to guarantee the car cannot move when it isn't supposed to.

**Governor and safety gear.** An overspeed-protection pair: the governor is a speed-sensing device (mechanically linked to car motion, often via its own separate rope) that detects excessive descending speed; safety gear is a mechanical device on the car frame that, when triggered (usually by the governor), physically clamps onto the guide rails to stop the car. Covered at the physical/behavioral level in Chapter 3 §3.4; the standards and certification treatment comes later in the research book.

**Buffers.** Shock-absorbing devices at the bottom of the hoistway (and sometimes the top), a last-resort mechanical safeguard if a car or counterweight were to travel beyond its normal limits.

**Landing system.** The set of fixed references (mechanical or sensor-based) that tell the elevator where each floor actually is in physical space — this is what the leveling-zone sensing in §1.3 ultimately references.

**Door system.** Introduced here as an interacting component (it must be locked before the car may move, and unlocked/opened only under specific conditions), covered in full depth in Chapter 3 §3.1.

```
              MECHANICAL ENERGY FLOW
              (traction elevator, gearless)

   Electrical energy
          │
          ▼
        MOTOR  ───────────► generates torque
          │
          ▼
   TRACTION SHEAVE  ◄────── BRAKE (holds sheave when disengaged from motion)
          │  (friction grip on ropes)
          ▼
      ROPES / BELTS
       ╱          ╲
      ▼            ▼
     CAR      COUNTERWEIGHT
      │             │
      ▼             ▼
  GUIDE SHOES ◄── GUIDE RAILS ──► GUIDE SHOES
   (car)                          (counterweight)
```

> **Why This Matters to KONE Elevate RCA:** Every one of these components appears as either a row in Chapter 3's failure matrix or a node in a future fault tree. The "interacts with" relationships noted above (brake↔sheave, guide shoes↔rails, ropes↔sheave friction) are exactly the relationships that let one component's failure masquerade as another's — which is the whole reason a simple fault-code lookup is insufficient and a structured, evidence-weighing RCA layer has a job to do.

## 1.5 The Physics of Traction

This section is short, but it is arguably the single most important piece of engineering intuition in the whole project.

**Traction, precisely.** The ropes are not bolted to the sheave. They sit in grooves and are held against it purely by friction, under the tension created by the weight of the car and counterweight on either side. "Traction" is the name for this friction-based grip. It's a deliberate design choice, not a limitation: because the connection is frictional rather than rigid, an overspeed or over-tension condition can cause the rope to *slip* against the sheave rather than transmitting damaging force indefinitely — traction is, in a sense, a built-in mechanical fuse, but it also means grip can degrade gradually (sheave-groove wear, rope surface wear, contamination) before it fails outright.

**Counterweight and net torque.** Because the counterweight roughly balances the car plus a design fraction of rated load, the motor mostly only has to overcome the *difference* between the two sides, plus friction and acceleration — not the full weight of the car. This is why elevator motors can be far smaller than a naive "lift this much weight" calculation would suggest.

**Torque, current, and load — the relationship that matters most for this project.** In a modern PMSM under field-oriented control (explained fully in Chapter 2), motor torque is approximately proportional to the torque-producing component of current:

**T ≈ k · I_q**

(torque T is approximately proportional to the torque-producing current component I_q, with k a motor-specific constant). The drive doesn't need to know *why* more torque is required at a given moment — it simply supplies whatever current the control loop calculates is needed to hit the commanded speed/position profile. That means **current rises whenever more torque is needed, for any reason at all** — a heavier-than-usual load, a stiffer-than-usual mechanical resistance, or an actual electrical fault all look the same from the current sensor's point of view at first glance.

> **KEY CONCEPT:** A mechanical problem can look exactly like an electrical problem, because the electrical system's job is to react to mechanical reality, not to independently know what "normal" should be for a given moment.

Worked through explicitly:

```
Mechanical obstruction / added resistance
        ↓
Increased resistance to motion
        ↓
Controller's control loop must command more torque
        to hold the commanded speed/position profile
        ↓
More torque requires more current (T ≈ k · I_q)
        ↓
Drive's current sensor reads an elevated / abnormal value
        ↓
Drive may raise an "overcurrent" fault
```

> **COMMON MISCONCEPTION:** "High motor current means the motor has failed." In reality, elevated current is *evidence consistent with* many different causes — a genuine motor winding fault is only one of them, and often not the most likely one. Chapter 2 §2.5 works through this specific example (motor overcurrent) as a full differential-diagnosis case, because it is foundational to everything the project's RCA logic later needs to do.

> **Why This Matters to KONE Elevate RCA:** This one principle — that a downstream electrical signature can be the *effect* of an upstream mechanical cause — is the physical justification for the entire project. If fault codes mapped one-to-one onto root causes, there would be no reasoning problem left to solve. Because they don't, evidence must be weighed, not looked up.

---
---

# CHAPTER 2 — ELEVATOR ELECTRICAL, DRIVE & MOTION-CONTROL SYSTEM

Chapter 1 established *what physically has to happen* for an elevator to move safely. This chapter explains *how electrical signals make that happen* — the chain from building power, through the drive and motor, to actual controlled motion, and back through sensor feedback to a controller that continuously corrects itself.

## 2.1 The Electrical / Control Chain, End to End

```
Electrical supply (building power, 3-phase AC)
        ↓
DRIVE  (rectifies AC → regulates a DC bus → synthesizes new AC for the motor)
        ↓
MOTOR  (converts electrical energy to torque)
        ↓
TRACTION SYSTEM  (sheave → ropes → car/counterweight — Chapter 1)
        ↓
ELEVATOR MOTION
        ↓
FEEDBACK  (encoder, sensors)
        ↓
CONTROLLER  (compares actual to commanded, issues correction)
        ↺ (loop closes back to the drive)
```

This is a **closed-loop** system throughout: nothing in it is "set and forget." Every stage is continuously measured and corrected, which is exactly why sensor data is so central to this project — the elevator is, by design, already instrumented to know when its own behavior deviates from what was commanded. The project's job is to interpret *why* it deviated.

## 2.2 The Elevator Controller: How the System "Decides"

*[GENERAL ELEVATOR INDUSTRY KNOWLEDGE]* The controller is the system's decision-making center — typically PLC-based or a comparable embedded industrial controller, running as a **state machine**: at any moment, the elevator is in one defined state (idle, accelerating, running, decelerating, leveling, door-open, door-closing, fault, inspection, etc.), and transitions between states only happen when specific, defined conditions are met.

Its main functional blocks:

- **Main control board** — runs the core logic/state machine and coordinates everything else.
- **I/O modules** — the physical interface to sensors, switches, and outputs (door motors, indicator lights, relays).
- **Safety controller** — a distinct, often independently-certified logic path that monitors the safety chain (door locks, governor/safety-gear state, overtravel limits) and can halt motion regardless of what the main control logic wants. This separation — safety logic kept apart from general control logic — is a foundational industry safety pattern, and it is the same principle this project's own "AI stays outside the safety-control loop" boundary mirrors at the software-architecture level.
- **Drive interface** — the communication link (whether a dedicated bus or discrete I/O) between the controller (which decides *where to go*) and the drive (which decides *how to get the motor there electrically*).
- **Communication buses** — internal links to door controllers, dispatch systems (in multi-car installations), and often an external/cloud-facing connection for monitoring.
- **Event logging** — a running record of state transitions, faults, and (in most modern systems) some sensor history — this log is one of the primary evidence sources the RCA Agent described in the project proposal will draw on.
- **Fault-code generation** — the controller (and/or drive) raises a coded alarm when it detects a defined abnormal condition. Section 6 of the roadmap already established the central theme this project is built around: **a fault code names a *symptom the controller detected*, not necessarily the thing that caused it.**

> **Why This Matters to KONE Elevate RCA:** The controller's own event log is one of the project's primary evidence sources — but it's evidence of *when the controller noticed something*, in the controller's own vocabulary (fault codes), not a diagnosis. Everything from here forward in this project is about closing that gap responsibly.

## 2.3 The VFD / VVVF Drive

The drive (Variable Frequency Drive / Variable Voltage Variable Frequency) is the component that actually converts fixed building power into the precisely variable electrical signal the motor needs to move exactly as commanded.

```
AC input (building supply, fixed frequency/voltage)
        ↓
RECTIFIER      converts AC → DC
        ↓
DC BUS         smoothed, stored DC energy (also receives regenerated energy — see below)
        ↓
INVERTER       IGBTs switch the DC bus on/off rapidly (PWM)
               to synthesize a new, variable-frequency, variable-voltage 3-phase AC waveform
        ↓
MOTOR
```

| Component | Function | What can fail | Sensor signature if it fails | Possible alarm | Could be confused with |
|---|---|---|---|---|---|
| **Rectifier** | AC → DC conversion | Diode/device failure, connection issue | DC-bus voltage anomaly, possible input current imbalance | Drive fault, undervoltage/overvoltage | Power-quality issue from the building supply itself |
| **DC bus** | Stores/smooths DC energy; buffers regenerated energy | Capacitor degradation (aging), overvoltage from unmanaged regen | DC-bus voltage ripple or drift outside normal range | Overvoltage/undervoltage fault | Chopper/braking-resistor fault (see below) |
| **Inverter (IGBTs)** | Switches DC bus to synthesize the motor's AC supply, via **PWM** (Pulse-Width Modulation — rapidly turning the output on and off so that the *average* voltage over time approximates the desired waveform) | Device (IGBT) short/open failure, gate-driver failure, thermal degradation | Abnormal current waveform, current imbalance across phases, drive over-temperature | Drive fault / IGBT fault / drive overcurrent | Motor winding fault — both can present as an abnormal current signature "at the motor" |
| **Gate drivers** | Precisely switch each IGBT on/off on command | Drift, component failure | Erratic switching pattern, secondary current distortion | Drive fault | Inverter/IGBT failure directly |
| **Current sensors** | Measure actual phase current for the closed-loop control | Calibration drift, sensor failure | Reported current inconsistent with other evidence (e.g., no corresponding torque/motion effect) | May not alarm directly — often shows up as control-loop misbehavior | A genuine electrical fault, since it *looks* like abnormal current whether or not the current is actually abnormal |
| **Voltage sensors** | Monitor DC bus and/or output voltage for the control loop and protection logic | Drift, failure | Voltage readings inconsistent with expected bus behavior | Overvoltage/undervoltage fault | Rectifier or DC-bus issue |
| **Braking resistor / chopper** | Dissipates excess energy that flows *back* into the DC bus during regenerative conditions (see below), preventing overvoltage | Resistor burnout, chopper switching failure | DC-bus overvoltage specifically during deceleration/overhauling-load conditions | Overvoltage fault, specifically correlated with braking/regen events | A DC-bus or rectifier fault occurring at other times |

**Regenerative braking, explained plainly.** Sometimes the mechanical system is trying to turn the motor *faster* than the drive is commanding — for example, a heavily-loaded car descending (gravity is helping it along) or a lightly-loaded car ascending (the heavier counterweight is "winning"). In these situations the motor briefly acts more like a generator than a motor, and energy flows *back* from the motor into the DC bus rather than out of it. If that energy isn't dealt with, the DC bus voltage would climb dangerously — which is exactly what the braking resistor/chopper exists to prevent, by burning the excess energy off as heat (some modern drives instead feed it back into the building's electrical system). The related formula, useful for intuition: **P = T · ω** (power equals torque times rotational speed) — during an overhauling condition, the mechanical system is *delivering* power to the motor shaft rather than the motor delivering power to the load, and that power has to go somewhere electrically.

> **JUDGE QUESTION:** *"If the drive can already detect an internal IGBT self-test failure and raise a fault code, why do you need an AI layer at all for a drive fault?"* Because the drive's self-test tells you the drive found something wrong with *itself* — it does not tell you whether an apparently unrelated overcurrent event five seconds earlier was the *cause* of that internal stress, or a coincidence, or evidence pointing at a completely different subsystem. The fault code is one piece of evidence; root-cause determination is a reasoning step over several pieces of evidence together.

> **Why This Matters to KONE Elevate RCA:** Nearly every "alarm" in this chapter's table can, in isolation, point to several different underlying causes — which is precisely why the project's design principle is to combine multiple evidence sources (§2.5 works through this in full for the single most common and most ambiguous case: motor overcurrent) rather than trust any single fault code.

## 2.4 PMSM and Motor Control

**What a PMSM is.** A Permanent Magnet Synchronous Motor uses permanent magnets embedded in the rotor (the rotating part) instead of an electromagnet, paired with a stator (the stationary part) whose windings produce a rotating magnetic field when energized in the right sequence. The rotor "follows" that rotating field — hence *synchronous*. PMSMs are the dominant choice for modern gearless elevator machines because they deliver high torque at low speed efficiently, without needing a reduction gearbox. *[GENERAL ELEVATOR INDUSTRY KNOWLEDGE]*

**Field-Oriented Control (FOC), explained in plain language first.** In a simple DC motor, you can directly and independently adjust two separate things: how strong the magnetic field is, and how much current flows to produce turning force (torque). AC motors don't offer that same direct handle by default, because the current in each of the three phase windings is constantly changing direction as the motor spins. FOC is a control technique that mathematically transforms the three changing AC phase currents into two much simpler, non-rotating equivalent quantities. Once the drive is working with these two simplified quantities instead of the three raw phase currents, it can control torque almost as directly as a DC motor would allow — adjusting a single, clean "torque-demand" signal many times per second.

**The technical mechanism.** The transformation is done in two mathematical steps commonly known as the Clarke transform (three-phase currents → two stationary-frame components) and the Park transform (stationary frame → a rotating reference frame locked to the rotor's own electrical angle, which is why continuous, accurate position feedback — the encoder — is essential to FOC: without knowing the rotor's instantaneous electrical angle precisely, the transform's rotating frame drifts out of alignment with the real motor). In this rotating frame, current is split into two components:

- **I_d** — the field-producing (flux) component
- **I_q** — the torque-producing component

As established in §1.5, torque is approximately proportional to I_q, which is what allows the drive to translate "I need this much torque, right now" directly into "I need this much I_q current, right now" — and then regulate it in a fast closed loop.

**Why this matters for elevator ride quality.** This is what lets a modern elevator produce smooth, precisely controlled torque throughout start, constant-speed travel, and the fine deceleration needed for accurate floor leveling, instead of the rougher motion a simpler AC control scheme would produce.

The relationship between command and reality, restated as a loop:

```
Motor command (from controller's motion profile)
        ↓
Drive translates command into required I_q (via FOC)
        ↓
Actual motor behavior (torque, resulting motion)
        ↓
Sensor feedback (encoder: speed/position; current sensors)
        ↓
Controller/drive compares actual vs. commanded
        ↓
Correction issued
        ↺ (loop repeats, many times per second)
```

> **Why This Matters to KONE Elevate RCA:** Because FOC depends on accurate encoder feedback, an encoder problem doesn't just cause a "position" symptom — it can degrade torque control quality itself, producing current and motion signatures that look like a motor or drive problem. This is one of the clearest examples in the whole project of why fault isolation has to consider the *dependency structure* between subsystems, not treat each sensor in isolation.

## 2.5 Worked Example: Reasoning Through "Motor Overcurrent"

This is the single most important worked example in Phase 1. The roadmap calls out this exact reasoning chain as the project's motivating problem, and it becomes a foundational reference case for the RCA chapters later in the book.

**The starting fact:** the drive reports an overcurrent condition. That is the *entire* content of the fault code. Everything below is what a properly evidence-weighing system — human or AI — has to consider before concluding anything.

---

**Cause 1 — Mechanical jam / obstruction**
- *Physical mechanism:* something physically resists the car's motion (debris, a binding component, a jammed door interfering with motion permission logic).
- *Expected sensor behavior:* current rises in a pattern correlated with position/attempted motion, not with any electrical anomaly; vibration signature often changes too.
- *Expected electrical behavior:* drive's own internal self-test and component-health checks come back clean.
- *Expected alarm:* overcurrent, possibly alongside a stalled-motion or position-deviation alarm.
- *Evidence supporting:* current elevated specifically during motion attempts, drive self-test clean, no clear pattern of a fault when stationary.
- *Evidence contradicting:* if current is elevated even during commanded-stationary periods, this cause becomes less likely.
- *How a technician differentiates it:* physical inspection of the travel path, correlating exactly when in the motion cycle current rose.

**Cause 2 — Brake drag**
- *Physical mechanism:* the brake fails to fully release (wear, misadjustment, coil issue — see Chapter 3 §3.2), adding continuous mechanical resistance.
- *Expected sensor behavior:* current elevated specifically correlated with brake-release timing; possible position drift.
- *Expected electrical behavior:* clean drive self-test.
- *Expected alarm:* overcurrent, possibly a brake-related fault if the brake system has its own monitoring.
- *Evidence supporting:* elevated current tightly correlated with brake-release events across multiple trips; brake-timing telemetry (if available) shows a deviation.
- *Evidence contradicting:* if elevated current appears regardless of brake state, this becomes less likely.
- *How a technician differentiates it:* checking brake-timing/torque telemetry alongside current, or a physical brake-release check.

**Cause 3 — Excessive load**
- *Physical mechanism:* the car is loaded beyond, or near, rated capacity.
- *Expected sensor behavior:* current elevated proportionally to a load-sensor reading (if the system has one), consistent across similar trips at similar loads.
- *Expected electrical behavior:* clean.
- *Expected alarm:* overcurrent, possibly an overload alarm if load-sensing exists independently.
- *Evidence supporting:* correlates directly with load-sensor data.
- *Evidence contradicting:* elevated current with a normal/low load reading rules this out.
- *How a technician differentiates it:* directly checking load data, if available, before assuming a mechanical or electrical fault.

**Cause 4 — Rope/traction issue**
- *Physical mechanism:* significant rope or sheave-groove wear reduces available friction, requiring more compensating torque, or in severe cases causing rope slip.
- *Expected sensor behavior:* current elevated under load, possibly with a position/speed deviation if slip is occurring; vibration signature may show a wear pattern.
- *Expected electrical behavior:* clean.
- *Expected alarm:* overcurrent and/or position-deviation.
- *Evidence supporting:* correlates with load-dependent severity and, if slip is present, a position-vs-commanded mismatch.
- *Evidence contradicting:* no position deviation and no correlation with rope-wear indicators (e.g., recent inspection history) makes this less likely.
- *How a technician differentiates it:* physical rope/sheave inspection, maintenance-history check for wear indicators.

**Cause 5 — Motor winding problem**
- *Physical mechanism:* insulation breakdown or a partial short in the motor's own windings.
- *Expected sensor behavior:* current imbalance across the three phases, possibly independent of load or motion state; elevated motor temperature.
- *Expected electrical behavior:* the drive's own internal checks may flag an inconsistency specifically traceable to the motor rather than the drive.
- *Expected alarm:* overcurrent, motor-temperature fault.
- *Evidence supporting:* phase-current imbalance present even under light or no load; temperature trend independent of external mechanical factors.
- *Evidence contradicting:* balanced phase currents and normal temperature make this unlikely.
- *How a technician differentiates it:* phase-balance measurement, insulation resistance testing.

**Cause 6 — Cable / wiring problem**
- *Physical mechanism:* a loose connection or partial short in the motor cabling.
- *Expected sensor behavior:* intermittent or erratic current readings, sometimes correlated with vibration (a loose connection worsening under motion-induced vibration).
- *Expected electrical behavior:* possible intermittent drive fault rather than a consistent one.
- *Expected alarm:* overcurrent, possibly an intermittent/erratic fault pattern in the log.
- *Evidence supporting:* an inconsistent, non-repeatable pattern across otherwise-similar trips.
- *Evidence contradicting:* a highly consistent, repeatable pattern argues against a loose connection specifically.
- *How a technician differentiates it:* physical inspection and connection testing.

**Cause 7 — Drive / IGBT fault**
- *Physical mechanism:* device degradation or failure inside the drive itself (see §2.3).
- *Expected sensor behavior:* abnormal current waveform or phase imbalance traceable to the drive side, elevated drive (not motor) temperature.
- *Expected electrical behavior:* the drive's own self-test/diagnostics are the most direct evidence here.
- *Expected alarm:* drive fault / IGBT fault, in addition to or instead of a generic overcurrent code.
- *Evidence supporting:* drive self-test fails or flags an internal fault; drive-side temperature anomaly.
- *Evidence contradicting:* a clean drive self-test with an otherwise mechanically-explicable current pattern argues against this.
- *How a technician differentiates it:* drive diagnostic self-test results, drive-side temperature and voltage telemetry.

**Cause 8 — Incorrect VFD parameters**
- *Physical mechanism:* the drive's configuration (e.g., current limits, motor parameter settings) doesn't match the actual motor/installation, causing the control loop to command more current than the real situation needs.
- *Expected sensor behavior:* a persistent, systematic elevated-current pattern present from installation or from a recent parameter change, not tied to any specific mechanical event.
- *Expected electrical behavior:* clean hardware self-test, since nothing is physically broken.
- *Expected alarm:* overcurrent, often more of a "nuisance trip" pattern than a hard fault.
- *Evidence supporting:* correlates in time with a known configuration/parameter change; consistent across all trips regardless of load or mechanical state.
- *Evidence contradicting:* a sudden onset with no configuration change nearby argues against this.
- *How a technician differentiates it:* reviewing configuration history and comparing current parameters against the motor's actual nameplate/design values.

---

> **COMMON MISCONCEPTION:** "High motor current means the motor has failed." As the table above shows, motor winding failure is only one of at least eight plausible causes, and in practice often not the most common one. Treating "overcurrent" as synonymous with "motor fault" is exactly the kind of shortcut this project exists to replace with evidence-weighed reasoning.

> **Why This Matters to KONE Elevate RCA:** This table *is*, in miniature, what a fault-tree node and its Bayesian evidence-weighting look like in practice. Every cause has a distinct evidence signature; the project's later RCA chapters formalize exactly this kind of reasoning — generate the plausible causes, predict what evidence each would produce, compare that prediction against what was actually observed, and rank accordingly.

---
---

# CHAPTER 3 — ELEVATOR SUBSYSTEMS, FAILURE MODES & SENSOR EVIDENCE

Chapters 1 and 2 explained how an elevator is supposed to work. This chapter asks the question the whole project is built around: **when something goes wrong, how does that show up, and to whom (which sensor, which alarm)?** It works through the door, brake, and rope/traction subsystems in failure-mode depth, covers the safety-related mechanical components at a physical level, builds a complete sensor dictionary, and closes with the two artifacts every later RCA chapter will build on: a master failure-to-evidence matrix and a set of fully worked causal chains.

## 3.1 The Door System

*[GENERAL ELEVATOR INDUSTRY KNOWLEDGE throughout]* The door system is worth taking seriously on its own, not as an afterthought to the traction system — it is mechanically simpler than the main drive, but it fails *often* (doors cycle every trip, sometimes dozens of times an hour) and its failure signatures are some of the most commonly confused in the entire elevator.

**Components:**

- **Door operator / door motor** — a dedicated (usually smaller) motor that drives door motion, separate from the main traction motor.
- **Door belt** — transmits the door motor's motion to the door panel(s).
- **Rollers and tracks** — guide the door panel(s) along their travel path.
- **Door lock / door interlock** — a safety-critical component that must confirm "locked" before the elevator is permitted to move, and that gates whether the doors can be commanded open.
- **Photo-eye** — an optical beam (or array of beams) across the door opening; interruption is interpreted as an obstruction and triggers reopening.
- **Light curtain** — a denser array of optical sensors than a simple photo-eye, providing finer obstruction detection across more of the door opening.
- **Safety edge** — a physical, contact-based obstruction sensor (a sensitive strip along the door's leading edge) as a complement to the optical systems.
- **Door encoder** — tracks door-panel position/speed for closed-loop door-motion control, analogous to the main motor's encoder.
- **Open/close limit sensors** — confirm the door has reached its fully-open or fully-closed position.

**Failure-mode table:**

| Failure | Physical mechanism | Observable symptom | Sensor evidence | Possible alarm | Alternative causes to rule out |
|---|---|---|---|---|---|
| **Roller wear** | Rollers degrade, increasing friction along the track | Slower / noisier door movement | Elevated door-motor current, longer cycle time | Door timeout | Door motor weakness, track misalignment |
| **Photo-eye drift** | Optical alignment or sensitivity drifts over time | Repeated reopening with no visible obstruction | Photo-eye state instability across multiple cycles, no correlation with a real object | Door obstruction / door fault | A genuine (real) obstruction |
| **Encoder drift** | Door encoder signal degrades or loses calibration | Door position appears incorrect to the controller | Door-position-vs-commanded deviation | Encoder fault | Belt slippage producing a similar mismatch |
| **Lock-contact instability** | Lock/interlock contact wear or misalignment | Repeated reopening, or failure to confirm "locked" | Lock-state signal instability | Door-lock fault, safety-circuit-open | Photo-eye or general obstruction symptoms |
| **Obstruction (genuine)** | A real physical object blocks the door path | Door fails to close, single well-correlated event | Photo-eye/safety-edge triggers exactly at the obstruction, clears when removed | Door obstruction | Photo-eye drift (this is the pair the project's own illustrative scenario is built on) |
| **Belt problems** | Wear, stretch, or slippage in the door belt | Inconsistent panel synchronization or speed | Door-motor current pattern change, position mismatch between panels (on center-opening doors) | Door fault, door-close timeout | Roller wear, motor weakness |
| **Motor problems** | Door-motor winding/mechanical wear (a smaller-scale version of the main-motor failure modes in Ch. 2) | Weak or inconsistent door movement | Elevated/erratic door-motor current | Door fault, door-close timeout | Obstruction, belt/roller issues |
| **Track problems** | Misalignment or debris in the door track | Binding, uneven door motion | Elevated current at specific points in the door's travel, repeatable position | Door timeout | Roller wear |

> **ENGINEERING EXAMPLE:** This is the exact cascade the project's own idea proposal uses as its illustrative scenario: debris blocks a door → photo-eye/safety-edge correctly detects an obstruction → the door repeatedly fails to close → a door-close timeout is raised → because the door never confirms locked, the safety circuit remains open → because the safety circuit is open, the drive is inhibited from starting → several distinct alarms are raised, all downstream of one physical cause. The project's proposal is explicit that this specific example is illustrative, not a verified KONE service case — but the *pattern* (one physical event, several downstream alarms) is exactly what alarm correlation exists to recognize.

> **Why This Matters to KONE Elevate RCA:** The photo-eye-drift vs. genuine-obstruction pair is arguably the hardest, most realistic ambiguity in the entire door subsystem — both produce nearly identical alarm signatures in a single event; only the *pattern across repeated events* (intermittent and object-independent vs. tied to one specific removable cause) separates them. This is a strong candidate for one of the project's canonical fault scenarios.

## 3.2 The Brake System

**Components and behavior.** The elevator brake is an **electromechanical, spring-applied, electrically-released** device: springs hold the brake engaged by default; an electromagnetic coil, when energized, pulls the brake open (releases it) against that spring force. This is a deliberate fail-safe design — if electrical power is lost for any reason, the brake defaults to *engaged*, not released. *[GENERAL ELEVATOR INDUSTRY KNOWLEDGE]* Key monitored parameters include brake coil health, brake wear (lining thickness), brake torque (holding force), brake timing (how quickly it engages/releases), and — in more modern systems — a periodic brake self-test.

**How a brake problem can look like a motor or position problem.** This is worth walking through explicitly, because it is one of the clearest real-world instances of the principle established in §1.5.

```
Brake fails to fully release (wear, misadjustment, or coil issue)
        ↓
Continuous mechanical resistance/drag persists during travel
        ↓
Motor must produce more torque than the commanded profile expects,
        for the entire trip, not just at one moment
        ↓
Elevated current — correlated specifically with brake-release timing
        ↓
In severe cases: abnormal motion behavior, or slight position drift
        while the car is supposed to be held stationary
        ↓
Possible outcomes: "overcurrent" alarm, a brake-specific fault
        (if monitored), or a subtle "leveling deviation" that looks,
        at first glance, like an encoder or leveling-sensor problem
```

The key diagnostic move that separates brake drag from a pure motor/drive issue is **correlation with brake state**: if elevated current tracks tightly with brake-release/engage events across many trips, the brake — not the motor — is the more likely primary cause.

> **Why This Matters to KONE Elevate RCA:** The brake is a **safety-relevant** component in its own right (it's one of the mechanisms directly responsible for holding a stationary car), so a brake-drag pattern in the evidence isn't just "one more possible cause of overcurrent" — it should carry a genuinely elevated diagnostic priority, independent of how common it turns out to be statistically, because the cost of missing a degrading brake is higher than the cost of missing, say, minor rope wear.

## 3.3 The Rope and Traction System

| Element | Normal operation | Degradation mechanism | Observable effect | Sensor evidence | Possible alarm | Diagnostic confusion |
|---|---|---|---|---|---|---|
| **Steel ropes** | Uniform tension and wear across all ropes | Fatigue, corrosion, wire breakage over time | Uneven load sharing, vibration | Vibration signature change, tension-sensor deviation (if fitted) | Position deviation; safety-related alarm if severe | Sheave wear, counterweight imbalance |
| **Coated belts** | Uniform tension, intact coating | Coating wear, cord fatigue | Similar to ropes, generally lower vibration signature when healthy | Vibration/tension deviation | Position deviation | Similar to rope wear |
| **Traction sheave** | Groove profile provides consistent, sufficient friction | Groove wear reduces available friction | Rope slip under higher loads specifically | Speed/position mismatch vs. commanded profile, load-dependent | Position/overspeed-underspeed deviation | Rope wear, counterweight imbalance |
| **Rope tension** | Balanced across all ropes | Individual rope stretch/wear diverges from the others | Uneven load distribution | Tension-sensor deviation between ropes (if individually monitored) | Position deviation, vibration alarm | Sheave wear |
| **Rope/sheave slip** | Should not occur in normal operation | Insufficient traction (wear, contamination, or severe overload) | Car moves less than commanded for the torque applied | Position-vs-commanded mismatch, especially under high load | Position deviation, overspeed protection involvement in extreme cases | Encoder fault (also produces a position-vs-commanded mismatch, but from a different origin) |
| **Counterweight imbalance** | Roughly balances car + design fraction of rated load | Incorrect weighting for current usage pattern, or a component failure in the counterweight assembly | Direction-dependent torque/current asymmetry beyond what load explains | Current asymmetry between up-travel and down-travel | Motor overcurrent (direction-dependent) | Straightforward motor fault, if direction isn't considered |

> **Why This Matters to KONE Elevate RCA:** Several rows in this table produce *the same kind of* alarm (position deviation, overcurrent) as encoder faults and brake drag. Distinguishing between them depends on secondary signatures — direction-dependence, load-dependence, and time trend (gradual wear vs. sudden onset) — which is exactly the kind of multi-evidence reasoning a single fault code cannot carry on its own.

## 3.4 Safety-Related Mechanical Components

This section covers what these components physically *are* and *do* — not the certification standards that govern them, which belong to a later phase of this book.

- **Overspeed governor.** A speed-sensing device, mechanically linked to car motion, that detects when descending speed exceeds a defined threshold. On triggering, it typically acts on the safety gear.
- **Safety gear.** A mechanical clamping device on the car frame that, when triggered, grips the guide rails to arrest motion. This is a mechanical, not electronic, last line of defense — deliberately independent of the elevator's normal control electronics.
- **UCMP / UCM (Unintended Car Movement Protection).** A system specifically addressing the scenario where the car moves away from a floor with the doors open when it should not — a distinct and serious hazard class from "the car moved too fast," which is what the governor/safety-gear pair addresses.
- **ACOP (Ascending Car Overspeed Protection).** Addresses the specific case of an ascending overspeed condition, complementing the governor/safety-gear system which historically focused more on descending overspeed.
- **Buffers.** Passive, mechanical shock absorbers at the extremes of travel — a final layer of protection if a car or counterweight were to travel beyond its intended limits.

> **JUDGE QUESTION:** *"Doesn't a safety-gear or governor event need the fastest possible AI response?"* No — and this is worth being explicit and confident about. These are exactly the events that must remain entirely outside the AI system's reach in real time, per the project's own stated safety boundary: they are handled by independent, hardware-level, fail-safe mechanisms that do not and should not wait on — or depend on — any software layer, AI or otherwise. The RCA Agent's role with respect to these components is strictly after-the-fact: helping a technician understand, from telemetry, why a safety-related event occurred, never intervening in whether or how it occurs.

## 3.5 Sensor & Telemetry Dictionary

A note before the tables: **exact sampling rates for these signals are not stated anywhere in the project's source material, and this book does not invent them.** *[Research Gap / Proprietary Information]* Where a general, defensible statement can be made about relative sampling needs (e.g., that a current or vibration signal, which captures fast electromechanical dynamics, needs to be sampled far more frequently than a door-cycle duration or ambient-temperature reading, which changes slowly), it is included as general engineering reasoning — not as a specific claimed number.

**A. Electrical signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Motor current | Torque demand, indirectly; varies smoothly with load and motion phase | Spikes, sustained elevation, phase imbalance | Central evidence for nearly every mechanical *and* electrical fault (Ch. 2 §2.5) — but on its own cannot distinguish *which* cause | Load data, brake state, drive temperature, vibration |
| Motor voltage | Applied voltage to the motor windings | Deviation from expected drive-commanded value | Drive/inverter health | DC-bus voltage, current |
| Phase current (per-phase) | Should be balanced across the three phases | Imbalance between phases | Motor winding issues specifically (a whole-motor current reading alone can't see this) | Motor temperature |
| DC-bus voltage | Stable, within a regulated band | Overvoltage (often regen-related) or undervoltage (supply-related) | Rectifier, chopper/braking-resistor, and supply-quality issues | Braking/regen events, input power quality |
| Drive temperature | Rises modestly with duty cycle, stays within rated range | Sustained elevation independent of ambient conditions | Drive/IGBT-side faults, specifically distinguished from motor-side faults | Motor temperature (for comparison), ambient temperature |
| Motor temperature | Rises with duty cycle and load | Sustained elevation, especially without a corresponding duty-cycle explanation | Motor winding issues | Current, drive temperature, duty cycle/usage |
| Power quality (building supply) | Stable voltage/frequency within expected tolerance | Sags, harmonics, imbalance | Supply-side issues masquerading as elevator-side faults | DC-bus behavior |

**B. Mechanical signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Vibration | Low, consistent baseline during normal travel | Elevated or changed frequency content | Rope/sheave wear, bearing wear, mechanical looseness — but cannot on its own say *which* component without correlation | Rope tension, current, travel phase |
| Acceleration | Follows the commanded motion profile smoothly | Jerky or inconsistent profile-tracking | Control-loop quality issues, which can stem from encoder, motor, or mechanical causes | Encoder signal quality, current |
| Brake torque / timing | Consistent engage/release timing and holding torque | Slow release, weak holding torque, timing drift | Brake wear/drag specifically | Motor current (during brake-transition moments) |
| Rope tension (where instrumented) | Balanced across ropes | Divergence between individual ropes | Rope wear/stretch | Vibration |
| Motor speed | Tracks the commanded profile closely | Deviation from commanded profile | A very general signal — many causes can produce a speed deviation | Position, current, encoder health |

**C. Position / motion signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Rotary/absolute encoder | Precise, continuous position/speed reference | Signal noise, dropout, or drift | Encoder faults directly — but a position error *caused by* an encoder fault looks identical, from the position data alone, to a real mechanical position error (e.g., rope slip) | Independent leveling-sensor reading, vibration |
| Position sensor(s) | Confirms car location in the hoistway | Deviation from encoder-predicted position | Cross-checks the encoder; disagreement between the two narrows the fault to one or the other | Encoder |
| Leveling/floor sensors | Confirms precise floor alignment at stop | Small but consistent offset at stop | Leveling-specific issues, often distinct in pattern from general position drift | Brake timing, rope condition |

**D. Door signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Door position | Tracks the door's commanded travel | Deviation from expected position at a given time | Belt, roller, track, or door-motor issues | Door-motor current, door encoder |
| Door-cycle duration | Consistent across similar trips | Lengthening over time (wear) or sudden change (fault/obstruction) | A general symptom shared by many door-subsystem faults | Door-motor current, photo-eye state |
| Door-motor current | Smooth, predictable profile | Elevated or erratic | Door-motor or mechanical-resistance (roller/track) issues | Door-cycle duration |
| Door-lock state | Confirms locked/unlocked reliably | Instability or failure to confirm | Lock/interlock issues — safety-relevant | Safety-circuit state |
| Photo-eye state | Clear except during genuine passage/obstruction | Instability or flicker across cycles with no consistent physical cause | Distinguishes genuine obstruction from photo-eye degradation, *if* pattern is examined across multiple cycles | Door-cycle duration, lock state |

**E. Environmental signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Machine-room temperature | Within equipment-rated range | Sustained elevation | Context for interpreting drive/motor temperature readings — a hot machine room can explain elevated component temperatures that would otherwise look alarming | Drive/motor temperature |
| Humidity | Within equipment-rated range | Elevated, sustained | Context for electrical/insulation-related degradation risk over time | Long-term maintenance/failure trends |
| Ambient temperature (car/hoistway) | Building-normal range | Extremes | Rarely a direct fault cause on its own; mostly contextual | Machine-room temperature |

**F. Operational / usage signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Trips (count) | Accumulates with usage | N/A directly — used as a rate/context signal | Usage-intensity context for wear-based failure priors | Running hours, door cycles |
| Starts/stops | Accumulates with usage | N/A directly | Same as above | Motor duty-cycle wear |
| Travel distance | Accumulates with usage | N/A directly | Wear-based prior context | Rope/sheave wear likelihood |
| Door cycles | Accumulates with usage | N/A directly | Door-component wear-based prior context | Roller/belt wear likelihood |
| Running hours | Accumulates with usage | N/A directly | General equipment-age/wear context | All wear-based failure priors |

**G. Load-related signals**

| Signal | Measures / normal behavior | Abnormal signature | Helps identify / limits | Correlate with |
|---|---|---|---|---|
| Load / passenger information | Reflects actual car loading per trip | N/A directly — used as a context signal | Rules load in or out as an explanation for elevated current | Motor current, direction-dependent current asymmetry |

> **KEY CONCEPT:** A sensor doesn't report a cause — it reports a physical quantity. Every fault-isolation step in this project depends on the gap between "what did the sensor measure" and "what does that measurement imply," which is never a one-to-one mapping.

> **Why This Matters to KONE Elevate RCA:** This dictionary — and specifically its "correlate with" column — is the practical seed of the project's evidence-retrieval and multi-signal reasoning design. Almost no signal here is individually diagnostic; nearly every one becomes meaningfully diagnostic only in combination with at least one other.

## 3.6 Master Failure → Evidence Matrix

This matrix draws together every subsystem covered across all three chapters. It is intended to become a working reference for the fault-tree and FMEA work in later phases of this book.

| Component | Failure Mode | Physical Effect | Observable Symptom | Sensor Evidence | Related Alarms | Possible Confusing Causes | Diagnostic Importance |
|---|---|---|---|---|---|---|---|
| **Motor** | Winding insulation breakdown / partial short | Uneven electromagnetic behavior, possible overheating | Uneven running, possible overheating | Phase-current imbalance, elevated motor temperature, current ripple | Overcurrent, motor-temperature fault | Mechanical jam, brake drag (both raise current without a winding fault) | High — costly component; cheaper causes must be ruled out first |
| **IGBT / drive** | Device degradation or short circuit | Miscontrolled or interrupted motor current | Jerky motion, drive trip, elevator out of service | Drive fault code, DC-bus anomaly, drive-temperature spike | Drive fault, drive trip | Motor-side fault (symptom appears "at the motor") | High — stops service entirely; also a costly part |
| **Brake** | Worn lining or misadjusted gap/timing | Incomplete release or drag | Dragging sensation, current elevation, possible position drift while held | Elevated current at brake-release moments, brake-torque/timing deviation | Overcurrent, brake fault, position deviation | Motor/traction fault (manifests as "extra load") | High — safety-relevant component |
| **Traction sheave** | Groove wear | Reduced friction | Rope slip under higher loads | Speed/position mismatch under load | Position/overspeed-underspeed deviation | Rope wear, counterweight imbalance | Medium–high |
| **Rope / belt** | Wear, fatigue, uneven elongation | Uneven load sharing, possible slip | Vibration, position drift, uneven wear pattern | Vibration-signature change, tension deviation | Position deviation, safety alarm if severe | Sheave wear, counterweight imbalance | High — safety-relevant, inspection-governed |
| **Counterweight** | Imbalance (incorrect weighting or component failure) | Direction-dependent load asymmetry | Direction-dependent current asymmetry | Current asymmetry up vs. down, vibration | Overcurrent (direction-dependent) | A simple motor fault, if direction isn't considered | Medium |
| **Encoder** | Drift, contamination, connector fault | Inaccurate position/speed feedback | Rough control response, leveling inaccuracy | Signal noise/dropout, position-vs-commanded deviation, speed-feedback inconsistency | Encoder fault, leveling deviation | Drive tuning issue, mechanical position issue (e.g., rope slip) | High — feeds the entire closed-loop system |
| **Door motor** | Winding/mechanical wear | Slow, weak, or inconsistent door movement | Increased cycle time | Elevated door-motor current | Door fault, door-close timeout | Obstruction, belt/roller issue | Medium |
| **Door rollers** | Wear or misalignment | Increased friction | Slow/noisy door movement | Elevated current, longer cycle | Door timeout | Belt wear, track misalignment | Low–medium |
| **Door belt** | Wear, stretch, or slip | Inconsistent panel synchronization | Uneven door motion | Current-pattern change, panel position mismatch | Door fault, door-close timeout | Roller wear, motor weakness | Medium |
| **Photo-eye** | Misalignment, contamination, drift | False obstruction detection | Repeated reopening without a real obstruction | Photo-eye state instability across cycles | Door obstruction, door fault | A genuine obstruction (this exact confusion is the project's own worked example) | High — central to the project's own motivating case |
| **Door lock / interlock** | Contact wear or misalignment | Unreliable lock-state confirmation | Repeated reopening, failure to confirm locked | Lock-state instability, safety-circuit-open indication | Door-lock fault, safety-circuit-open | Photo-eye/obstruction symptoms | Very high — directly gates motion permission |
| **Position / leveling system** | Sensor drift or contamination | Imprecise floor alignment | Car stops slightly off-level | Leveling-sensor deviation, consistent small position offset | Leveling deviation / re-leveling event | Encoder drift, brake timing, rope stretch | Medium–high |
| **Safety system (governor / safety-gear sensing)** | Contact degradation or misadjustment | False trips, or (worse) failure to trip when needed | Unexpected safety-chain-open events, or no response during test | Safety-chain state change, governor switch signal | Safety-circuit trip, safety-chain fault | Unrelated electrical noise (false trips); nothing symptomatic in normal operation (missed trips) | Highest — always human/qualified-technician territory, never resolved by the AI layer alone |

> **Why This Matters to KONE Elevate RCA:** This is, functionally, the seed of the project's static knowledge base — the artifact the roadmap describes building out further into full fault trees and FMEA tables. Every fault-tree node in later chapters should trace back to a row here.

## 3.7 Engineering Connection Map

The general causal pattern behind every row above:

```
PHYSICAL COMPONENT
        ↓
FAILURE MODE
        ↓
PHYSICAL EFFECT
        ↓
OBSERVABLE SYMPTOM
        ↓
SENSOR SIGNATURE
        ↓
EVENT / ALARM
        ↓
POSSIBLE SECONDARY EFFECTS
        ↓
POTENTIAL ROOT CAUSES (to weigh, not assume)
```

**Worked example 1 — IGBT / drive fault**
IGBT junction degrades → localized overheating / switching failure → drive reports an internal fault, or motor current becomes erratic → abnormal current ripple plus a drive-temperature/fault flag → **"Drive fault"** alarm → secondary effects: elevator taken out of service, possibly repeated fault-reset attempts logged → root causes to weigh: the IGBT itself, but also upstream DC-bus anomalies or cooling/ventilation issues that could have *caused* the overheating in the first place.

**Worked example 2 — Mechanical jam**
A foreign object or binding component enters the travel path → abnormal resistance to motion → the motor must produce more torque than the commanded profile expects → current rises above the load-adjusted expected value, vibration signature changes → **"Overcurrent"** and/or abnormal-motion alarm → secondary effects: possible drive trip, possible safety-circuit involvement if severe → root cause: the physical obstruction, distinguished from a drive/motor fault by a clean drive self-test.

**Worked example 3 — Brake drag**
Brake fails to fully release → continuous mechanical resistance during travel → motor works harder than the load alone would explain → current elevated specifically correlated with brake-release timing, possible position drift → **"Overcurrent"**, **"brake fault"**, or a subtle **"leveling deviation"** → secondary effects: accelerated wear on both brake and motor if unaddressed → root cause: the brake mechanism, distinguished by checking brake-timing/torque telemetry alongside current.

**Worked example 4 — Door photo-eye degradation**
Photo-eye alignment drifts or the lens degrades → intermittent false-obstruction readings → the door repeatedly reopens with no real obstruction → cycle time increases, photo-eye state becomes unstable across cycles → **"Door obstruction"** and **"door timeout"** alarms, potentially several in sequence → secondary effects: if the door never successfully completes its cycle, a downstream safety-circuit-open and drive-start-inhibited condition can follow — precisely the project's own motivating cascade → root cause: photo-eye hardware degradation, distinguished from a genuine obstruction by the *pattern* across repeated events, not any single event.

**Worked example 5 — Encoder fault**
Encoder signal degrades (contamination, connector issue, component wear) → position/speed feedback to the controller becomes inaccurate → the closed-loop correction is now acting on wrong information → car behavior becomes rough, or leveling becomes imprecise → **"Encoder fault"** and/or **"leveling deviation"** → secondary effects: because the entire motion-control loop depends on this feedback, a bad encoder can indirectly produce anomalies that look like motor or drive problems → root cause: the encoder itself, distinguished by checking whether the encoder's own internal signal-consistency checks fail even when commanded and drive-reported values otherwise look normal.

> **ONE-LINE TAKEAWAY:** One physical failure can generate several distinct alarms, and one alarm can be the downstream effect of several distinct physical failures — which is exactly the asymmetry an evidence-weighing RCA layer exists to resolve.

---
---

# PHASE 1 CONCLUSION

### What We Now Understand

We now have a complete, first-principles picture of the physical system this project is diagnosing: how a traction elevator moves a car (Chapter 1), how that motion is electrically commanded and continuously corrected (Chapter 2), and how the door, brake, rope/traction, and safety subsystems each fail — and what evidence each failure leaves behind (Chapter 3). We have a working sensor dictionary spanning seven categories of signals, and a master failure-to-evidence matrix spanning fourteen components, both built to become direct inputs to later RCA work.

### The Critical Diagnostic Insight

Two ideas, established repeatedly and from different directions across all three chapters, now stand as this project's foundational premise:

**Fault code ≠ root cause.** A fault code — "overcurrent," "door obstruction," "encoder fault" — names a symptom the controller detected, in the controller's own limited vocabulary. It does not name what caused that symptom. Chapter 2's motor-overcurrent worked example showed at least eight physically distinct causes converging on the exact same fault code.

**Sensor evidence must be interpreted in context.** No single signal in the Chapter 3 dictionary is, by itself, uniquely diagnostic. Motor current means almost nothing without knowing brake state, load, and travel phase. A position deviation means something different depending on whether it correlates with encoder health, brake timing, or rope condition. Evidence only becomes informative in combination — which is precisely why the project's architecture treats diagnosis as a multi-source, multi-hypothesis reasoning problem rather than a fault-code lookup table.

### Bridge to Phase 2

Everything in Phase 1 has been about a *single* fault, considered on its own — one motor overcurrent event, one door obstruction, one brake-drag episode. But Chapter 3's own worked examples already showed that one physical failure can cascade into *several* alarms in quick succession (the door-photo-eye example is the clearest case: obstruction detection → door timeout → safety-circuit-open → drive-start-inhibited, four alarms from one cause). Phase 2 must now study how fault codes and alarms are actually structured and generated, how multiple related alarms can be correlated into a single fault episode rather than treated as independent events, and how to distinguish a **primary** alarm (the one closest to the true cause) from a **consequential** alarm (a downstream symptom of that same cause) — the exact diagnostic evidence a technician, or an RCA Agent, needs before root-cause reasoning can even begin.

---

*This concludes Phase 1 of the KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis Master Research Book: Chapters 1 through 3. Ready for Phase 2 whenever you are.*
