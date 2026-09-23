# PHASE 6 — ALARM CORRELATION, TIME-SERIES SIGNAL PROCESSING & ANOMALY DETECTION

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

Labels: **[PROJECT SOURCE]**, **[ESTABLISHED ENGINEERING KNOWLEDGE]** (signal processing, statistics, and the classical anomaly-detection literature — the label for nearly everything in this chapter, none of it elevator- or KONE-exclusive), **[EXTERNAL RESEARCH]**, **[ENGINEERING INFERENCE]**, **[ASSUMPTION]**, **[NOT PUBLICLY ESTABLISHED]**. No production sampling rates, thresholds, or algorithm choices are claimed as KONE's actual implementation anywhere below — where a specific number appears, it is illustrative, and labeled as such.

**A scope boundary stated up front and held throughout:** this chapter does **not** discuss LLMs, retrieval-augmented generation, agents, or generative AI architecture. Those belong to a later phase. This chapter's job is narrower and, in a real sense, more foundational: turning raw, noisy, asynchronous elevator signals into the clean, structured, trustworthy evidence Phase 5's reasoning framework assumed was already available.

**The central question of this chapter:** *how do we obtain, clean, correlate, and interpret the real-world time-dependent evidence required to perform the reasoning Phase 5 described?*

**The central principle:** **good RCA requires good evidence, and good evidence requires understanding the temporal and signal characteristics of the elevator.**

---

## From Phase 5 to Phase 6

Phase 5 answered *how an RCA system should reason.* It did not answer where the evidence that reasoning depends on actually comes from, or whether it can be trusted.

```
RCA hypothesis
     ↓
What evidence would support it?
     ↓
Where can that evidence be found?
     ↓
How is the signal represented?
     ↓
Is the signal clean?
     ↓
When did it change?
     ↓
What other events occurred around it?
     ↓
Is the observed change abnormal?
     ↓
Can the evidence be trusted?
```

**Phase 5 was the reasoning framework. Phase 6 is evidence intelligence** — the discipline that makes Phase 5's "current↑," "vibration↑," and "drive self-test normal" into things that were actually, correctly, trustworthily measured, not assumed.

---

# Part I — Time-Series Foundations

## 8.1 What Is Time-Series Data?

*[ESTABLISHED ENGINEERING KNOWLEDGE]* A **time series** is a sequence of **observations**, each tied to a **timestamp**, typically collected at some **sampling interval** (the time between observations) or equivalently a **sampling frequency** (observations per second). Related vocabulary: a **signal** is the continuous physical quantity being measured (motor current, vibration); a **measurement** is one sampled value of it; a **state** is the elevator's current operating condition (idle, accelerating, door-open); an **event** is a discrete, named occurrence (a trip, a fault); a **sequence** is an ordered run of observations or events; a **trend** is a slow, sustained directional change; **noise** is random, non-informative variation; **drift** is a slow, systematic shift in a signal's baseline over time (distinct from noise, which doesn't accumulate directionally); a **transient** is a brief, temporary deviation that resolves on its own; **steady state** is stable, unchanging behavior; and an **operating cycle** is one complete repeatable sequence (a full door open-close cycle; a full floor-to-floor trip).

Elevator examples of each: motor current over time is a time series with a trend during acceleration, noise from normal electrical switching, and a transient spike if a door briefly catches. Cab speed over time follows a repeatable operating cycle (accelerate → constant speed → decelerate → level). Vibration over time is mostly noise around a low baseline during healthy operation, with drift appearing gradually as a bearing or rope wears.

**Why an elevator is naturally a time-dependent system:** almost nothing about an elevator is meaningfully described by a single instantaneous number. "Motor current is 12 amps" means something different during acceleration than during constant-speed travel than while stationary — the *sequence* of values, not any single value, is what carries diagnostic information, which is precisely why this entire chapter exists.

## 8.2 Continuous Signals vs. Event Data

Two fundamentally different data types, both required:

**Continuous / sampled telemetry** — current, voltage, temperature, vibration, position, speed: values that exist and change at every moment, captured at a sampling rate.

**Event data** — a drive trip, a door timeout, a safety event, an encoder fault, a controller state transition: discrete occurrences, each with a timestamp but no meaningful "value" between occurrences.

**Why both are required, not either alone:** an alarm alone — *"motor overcurrent"* — tells you an event happened. It says nothing about *how* it developed. The telemetry — *"motor current increased gradually over the previous three seconds before crossing threshold"* — tells a materially different diagnostic story than *"current spiked instantaneously."* **Alarm + pre-event trend + operating context** is categorically more informative than the alarm alone, and this difference (gradual vs. sudden onset) is exactly the kind of signal Chapter 7 §7.17's Dynamic Bayesian Network discussion was built to use.

## 8.3 Sampling

*[ESTABLISHED ENGINEERING KNOWLEDGE]* **Sampling frequency** is how often a signal is measured; **sampling interval** is the time between measurements (its reciprocal). The **Nyquist concept**: to accurately capture a signal's fastest-changing component, you must sample at *more than twice* the frequency of that component — sampling slower than this risks **aliasing**, where a fast-changing signal is misread as a slower, different pattern because the samples simply missed the in-between detail. **Under-sampling** misses real fast dynamics; **over-sampling** wastes bandwidth/storage without adding useful information beyond a point. **Sensor bandwidth** is the range of frequencies a given sensor can physically capture at all — sampling faster than a sensor's own bandwidth allows doesn't recover detail the sensor was never capable of measuring.

**Why different elevator signals plausibly need different sampling rates:** a slow-changing signal like machine-room temperature, which meaningfully changes over minutes, needs nowhere near the sampling rate of a vibration signal, whose diagnostically-useful content lives in oscillations occurring many times per second. **Actual production sampling rates depend on the elevator/control system and are not assumed here** — no specific KONE rate is claimed anywhere in this book. **[NOT PUBLICLY ESTABLISHED]**

## 8.4 Resampling and Time Alignment

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Data from multiple sensors rarely arrives perfectly synchronized: different sensors may have different native sampling frequencies, different timestamps, occasional missing points, small clock differences between subsystems, transmission latency, and generally asynchronous acquisition. Standard techniques: **resampling** (converting a signal to a common, shared sampling rate), **interpolation** (filling in estimated values between real samples), **aggregation** (summarizing many fast samples into fewer, coarser ones to match a slower signal), and **timestamp alignment/synchronization** (correcting for known clock offsets before comparing signals).

**Why this matters for causal reasoning specifically:** consider three readings — motor current at 10:31:01.120, vibration at 10:31:01.180, alarm at 10:31:01.210. If these timestamps come from three different subsystems with even small, unaccounted-for clock offsets, the *apparent* ordering (current first, then vibration, then the alarm) could be an artifact of the offsets rather than the true physical sequence — and Chapter 7 §7.13's entire causal-graph reasoning depends on ordering being real, not an alignment error. **Incorrect time alignment can manufacture a false temporal relationship that downstream reasoning would then treat as genuine evidence.**

## 8.5 Signal Quality

| Signal Quality Problem | What It Looks Like | Possible Cause | Diagnostic Risk |
|---|---|---|---|
| Missing data | Gaps in the record | Communication interruption, sensor offline | Absence mistaken for a true "normal" reading (Ch.7 §7.26's exact distinction) |
| Sensor dropout | Sudden loss of a signal mid-stream | Connector/power issue | Investigation loses a needed evidence source mid-episode |
| Stuck values | Identical reading repeated many times | Sensor frozen, not actually re-measuring | A real change is invisible; system believes "stable" when it isn't |
| Spikes | A single extreme outlier value | Transient electrical noise, sensor glitch | Mistaken for a genuine, meaningful event |
| Saturation / clipping | Value pinned at a sensor's max/min limit | Signal genuinely exceeded sensor range | True magnitude of a real event is underrepresented |
| Drift (sensor-side) | Gradual baseline shift unrelated to equipment | Sensor calibration degrading | Mistaken for genuine equipment degradation |
| Noise | High-frequency, low-magnitude random variation | Normal electrical/mechanical noise floor | Can mask a real but subtle fault signature |
| Communication gaps | Irregular timestamp spacing | Network/bus issues | Breaks resampling/alignment assumptions |
| Duplicated timestamps | Two readings, same timestamp | Logging error | Ambiguous ordering for causal reasoning |
| Impossible / out-of-range values | Physically implausible readings | Sensor fault, transmission corruption | Must be filtered, never reasoned over as real |

> **DATA QUALITY WARNING:** Bad data must never be treated as genuine equipment behavior. Every subsequent stage in this chapter — filtering, feature extraction, anomaly detection, alarm correlation — inherits whatever quality problems weren't caught here. This table's row order roughly tracks how early in the pipeline each problem needs to be caught.

---

# Part II — Signal Processing Fundamentals

## 8.6 Filtering

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Raw sensor signals contain noise that can obscure the underlying pattern worth reasoning about.

| Filter | Purpose | Mathematical Intuition | Elevator Application |
|---|---|---|---|
| **Moving average** | Smooth short-term noise | Replace each point with the average of a surrounding window | Smoothing a noisy current reading before trend analysis |
| **Median filter** | Smooth noise while preserving sharp edges | Replace each point with the median (not mean) of a surrounding window | Removing spike noise without blurring a genuine step-change |
| **Low-pass filter** | Keep slow variation, remove fast noise | Attenuates frequencies above a cutoff | Isolating a temperature trend from fast electrical noise |
| **High-pass filter** | Keep fast variation, remove slow drift | Attenuates frequencies below a cutoff | Isolating vibration content from a slow-changing baseline |
| **Band-pass filter** | Keep a specific frequency range | Combines low-pass and high-pass | Isolating a specific mechanical vibration frequency band of interest |
| **Savitzky-Golay** | Smooth while preserving higher-order signal shape (peaks, curvature) | Local polynomial fitting instead of simple averaging | Preserving a genuine current-rise shape that a plain moving average would round off |

**Excessive filtering can remove the fault signature itself, not just the noise.** A fault that manifests as a brief, sharp transient — a momentary current spike as an obstruction is first contacted — is exactly the kind of feature an aggressive low-pass or moving-average filter will smooth away. Filtering should never be applied blindly; it should be chosen with an explicit understanding of what frequency/timescale the fault signature of interest actually lives at.

## 8.7 Basic Statistical Features

| Feature | Meaning | Elevator Example | Diagnostic Value |
|---|---|---|---|
| Mean | Central tendency | Average motor current over a trip | Baseline reference |
| Median | Middle value, robust to outliers | Typical door-cycle time, ignoring rare outliers | Robust baseline |
| Variance / std. dev. | Spread around the mean | Vibration variability during travel | Detects increased inconsistency |
| RMS | "Effective magnitude" of an oscillating signal | Motor current, vibration | Captures energy content a simple mean would understate |
| Min / max | Extreme values in a window | Peak door-motor current during closing | Flags outlier events |
| Peak | Single largest magnitude | Peak vibration during a transient | Detects sharp events |
| Peak-to-peak | Difference between max and min | Current swing during acceleration | Detects instability/oscillation |
| Crest factor | Peak divided by RMS | Ratio for vibration signals | High crest factor suggests sharp, impulsive events (e.g., an impact) rather than smooth variation |

## 8.8 RMS in Depth

**Definition:** for a signal sampled as x₁, x₂, ..., xₙ over a window, **RMS = √( (x₁² + x₂² + ... + xₙ²) / n )** — the square root of the mean of the squared values.

**Why RMS specifically, rather than a plain average, for signals like current and vibration:** many of these signals oscillate around zero or vary rapidly in both directions — a plain average can understate or even cancel out a signal's true magnitude (an AC current waveform averages close to zero over a full cycle despite carrying real energy). Squaring before averaging removes the sign-cancellation problem and weights larger excursions more heavily, so RMS captures the signal's genuine "effective size" in a way a simple mean cannot.

**Limitation, stated plainly: RMS alone does not identify the cause.** An elevated RMS current value is consistent with every one of the nine candidate causes in Chapter 7 §7.7.1's motor-overcurrent fault tree — RMS is a feature, not a diagnosis, exactly the distinction §8.33 formalizes for every technique in this chapter.

## 8.9 Frequency-Domain Analysis

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Every signal discussed so far has been viewed in the **time domain** — value against time. The **frequency domain** instead asks: *what oscillating components, at what frequencies and strengths, make up this signal?* The **Fourier Transform** (computed in practice via the **FFT**, Fast Fourier Transform algorithm) converts a time-domain signal into its frequency-domain representation — conceptually, decomposing a complex signal into the sum of simple sine waves at different frequencies, and reporting how much energy exists at each.

Useful vocabulary: the **dominant frequency** (the strongest single frequency component), **harmonics** (energy at whole-number multiples of a fundamental frequency, common in electrical/mechanical rotating systems), **spectral energy** (how energy is distributed across the frequency range), **frequency shifts** (a dominant frequency moving over time, potentially indicating a changing rotational speed or a developing mechanical issue), and **sidebands** (extra frequency components appearing just above and below a dominant frequency, often associated with periodic mechanical modulation — e.g., a rotating component with a localized defect striking something once per revolution).

> **KEY CONCEPT:** Two signals can look nearly identical in the time domain (same RMS, same peak) and be completely different in the frequency domain — one dominated by a single clean frequency, the other spread across many. This is precisely why frequency-domain analysis adds real diagnostic value beyond §8.7's time-domain statistical features: it can distinguish signal *character*, not just signal *magnitude*.

## 8.10 Cross-Correlation and Lag Analysis

*[ESTABLISHED ENGINEERING KNOWLEDGE]* **Cross-correlation** measures how similar two signals are to each other as one is shifted in time relative to the other — the **lag** at which the correlation is strongest tells you the most likely time offset between related events in the two signals.

**Example:** motor current increases, and vibration increases roughly 150ms later. Cross-correlation, computed across many such episodes, can quantify this consistently and precisely — confirming both *that* the two signals tend to move together and *by roughly how much one lags the other*.

**What cross-correlation can, and cannot, tell you:** it can establish that two signals are statistically related and estimate their typical time offset. **It cannot, by itself, prove that one causes the other** — this is Chapter 7 §7.13's correlation-vs-causation distinction, restated at the signal-processing level rather than the event level. A consistent 150ms lag is *consistent with* current genuinely driving a vibration response through a real physical mechanism; it's also consistent with both being driven by some third, unmeasured factor. The physical justification (as established throughout Chapters 1–3) is what turns a strong cross-correlation into credible causal evidence, not the correlation coefficient alone.

## 8.11 Temporal Correlation

A lighter-weight relative of §8.10: simple **event ordering** — did A happen before B? — plus **time windows** (how close together, in absolute terms), **lead/lag relationships**, and **event proximity**. Examples: motor current rise → overcurrent alarm; door current increase → door timeout; encoder instability → position fault.

**Limitations of purely temporal reasoning, restated from Chapter 4 §4.12 and now given its signal-processing grounding:** ordering alone cannot distinguish genuine causation from independent coincidence or a shared unobserved cause. Temporal correlation is a necessary ingredient for alarm correlation (§8.19) but never a sufficient one on its own.

---

# Part III — Elevator-Specific Signal Applications

## 8.12 Motor Current Signature Analysis (MCSA)

*[ESTABLISHED ENGINEERING KNOWLEDGE — MCSA is a well-established industrial technique across rotating machinery generally, not elevator- or KONE-specific]* MCSA is the practice of analyzing a motor's electrical current — in both time and frequency domain — to infer information about its mechanical and electrical condition, on the principle that mechanical problems (load variation, bearing wear, misalignment) and electrical problems (winding faults) each tend to leave characteristic imprints on the current waveform, because the motor's electrical behavior is physically coupled to its mechanical behavior (Ch.1 §1.5's core principle, revisited at the signal-processing level).

Motor current can reflect load changes (current tracks commanded torque, §7.14's T ≈ k·I_q relationship), mechanical abnormalities (periodic load variation from a defective rotating component shows up as sidebands around the fundamental electrical frequency, §8.9), motor faults (asymmetric or unstable current patterns from winding degradation), and drive behavior (current shaped by the specific switching/control characteristics of the drive itself, Ch.2 §2.3).

**This book does not claim any particular current pattern uniquely identifies a specific KONE fault.** Signatures are **contextual evidence** — precisely the point Chapter 2 §2.5 and Chapter 7 §7.15 made repeatedly with the nine-cause motor-overcurrent example: current alone, however sophisticated the signal processing applied to it, cannot resolve which of nine physically distinct causes is responsible. What MCSA genuinely adds is a richer, more discriminating *version* of the current evidence — combined with speed, load, vibration, temperature, and event history, it narrows the hypothesis space further than a raw threshold crossing alone ever could.

## 8.13 Vibration Analysis

*[ESTABLISHED ENGINEERING KNOWLEDGE]* Vibration is characterized by **amplitude** (how large the oscillation is), **frequency** (how fast it oscillates), and derived features already introduced in §8.7–§8.9: RMS, peak, frequency spectrum, harmonics. **Transient vibration** is a brief event (an impact, a sudden mechanical catch); **envelope analysis** extracts the slower-varying "envelope" of a fast oscillating signal, often revealing periodic impact patterns (e.g., from a damaged rotating component) that raw amplitude alone obscures.

Elevator components with vibration relevance: the motor, bearings, the traction machine generally, the sheave, other rotating components, and the door mechanism (which has its own, lower-magnitude vibration character during operation).

**Vibration patterns can indicate abnormalities but are rarely sufficient alone for definitive RCA** — consistent with every component-level fault-tree branch across Chapters 3, 4, and 7 that listed vibration as *one* piece of supporting evidence among several, never a standalone conclusion.

## 8.14 Door-Cycle Analysis

A door cycle: **open command → opening motion → fully open → dwell → closing motion → fully closed → lock confirmation.**

Signals and features worth analyzing across this cycle: cycle time (total or per-phase), motor current (throughout the cycle, not just peak), position (door-panel position over time), acceleration (smoothness of motion), repeated reopenings (count and pattern across cycles — the key signal for the photo-eye-degradation-vs-genuine-obstruction distinction, Ch.4 §4.9), closing-force behavior, lock timing, and photo-eye state (stability across many cycles, not just presence/absence at one moment).

**How abnormal door-cycle patterns can help distinguish candidate causes, without claiming deterministic identification:** an elevated but *consistent* cycle time with elevated door-motor current suggests mechanical resistance (rollers, track); reopening events with *no* consistent positional pattern and *normal* motor current suggest a sensing issue (photo-eye); a position-vs-commanded mismatch specifically suggests the encoder branch; lock-state instability specifically implicates the interlock. None of these patterns *proves* a specific cause on its own — they narrow the live hypothesis set from §7.7.2's fault tree, which is precisely the evidence-generation role this whole chapter exists to serve.

## 8.15 Encoder and Position Analysis

Relevant signals: the **position signal** itself, derived **speed** and **acceleration**, the **stopping point**, **leveling accuracy**, **position deviation** (actual vs. commanded), and **feedback consistency** (does the position signal behave the way the commanded motion profile predicts it should, moment to moment).

**The core analytical move:** compare the **expected trajectory** (what the commanded motion profile predicts position/speed should be, at each moment) against the **observed trajectory** (what the encoder and any independent position reference actually report). Deviations between the two — and, critically, whether an *independent* leveling sensor agrees or disagrees with the main encoder — is exactly the diagnostic check Chapter 3 §3.7 and Chapter 7 §7.7.3/§7.34 relied on to separate a genuine encoder fault from a genuine mechanical motion problem.

**Why position behavior connects to multiple subsystems, not just the encoder:** the encoder reports position, but position is *actually determined* by the motor (Ch.1–2), the controller's interpretation of that signal (Ch.2 §2.2), the traction system's actual mechanical behavior (Ch.1 §1.5, Ch.3 §3.3), and the brake's holding/release timing (Ch.3 §3.2) — a position-analysis pipeline that only looks at the encoder in isolation is structurally incapable of resolving which of these four is actually responsible for an observed deviation.

---

# Part IV — Alarm Management and Correlation

## 8.16 Alarm Flooding

*[ESTABLISHED ENGINEERING KNOWLEDGE]* An **alarm flood** is a large number of alarms generated within a short period. This is dangerous for human operators specifically because volume itself degrades judgment — when many alarms arrive nearly simultaneously, a human (or a naive automated system) has limited capacity to recognize that they share one underlying cause, and tends to process each as an independent, equally-weighted problem.

**Concrete elevator example, reused from Chapter 4 §4.6:** one initiating problem (a mechanical obstruction) produces motor overcurrent + drive trip + position deviation + leveling fault + a service-needed alarm — five distinct alarms from one physical cause. An operator (or an unprepared system) may interpret these as five independent failures requiring five independent investigations, rather than recognizing the single upstream story.

## 8.17 Alarm Rationalization

*[ESTABLISHED ENGINEERING KNOWLEDGE — ISA-18.2 and EEMUA 191 are established industrial alarm-management standards, developed for process-industry control systems generally, not for elevators specifically]* Alarm rationalization is the discipline of reviewing an alarm system to ensure every alarm serves a genuine purpose: has a clear **priority**, reflects genuine **severity** and **consequence**, and produces an actionable **operator response** — rather than accumulating **duplicate alarms** (multiple alerts for the same underlying condition), **nuisance alarms** (frequent, low-value alerts that train operators to ignore alarms generally), **low-value alarms**, **persistent alarms** (alarms that stay active without providing new information), and **stale alarms** (long-active conditions no longer meaningfully "alerting" anyone). ISA-18.2 (an American National Standards Institute/ISA standard) and EEMUA 191 (a UK-originated engineering-practice guideline) are the two most commonly cited industrial frameworks for this discipline — cited here as established reference points for the general practice, not as elevator-specific requirements.

## 8.18 Alarm Suppression

**The concept:** deliberately filtering or suppressing certain alarms — most defensibly, consequential alarms already explained by an already-identified primary event — to reduce operator noise. **The real risk:** suppressing an alarm that turns out to carry independent diagnostic value, or suppressing during a state where the "expected" consequential pattern doesn't actually hold (e.g., a maintenance mode or a startup/shutdown sequence, where normal alarm-suppression logic built for steady-state operation may not correctly apply).

**This book does not describe, recommend, or provide any operational instruction for disabling, bypassing, or suppressing safety-relevant alarms.** The discussion here is strictly about diagnostic-layer alarm-management noise reduction — deciding which *already-explained* consequential alarms merit separate operator attention versus which are adequately represented by the primary event — never about safety-chain alarms specifically (Ch.4 §4.7-G, Ch.7 §7.7.6), which this book treats as categorically outside any suppression discussion.

## 8.19 Alarm Correlation

This is one of the central sections of the chapter.

```
Multiple alarms
     ↓
Group by time
     ↓
Group by subsystem
     ↓
Analyze causal relationships
     ↓
Identify likely initiating event
     ↓
Classify consequential alarms
```

**Worked example**, the canonical sequence from earlier phases, now walked through as a correlation process rather than assumed as given:

```
10:31:01   Motor current ↑
10:31:02   Overcurrent alarm
10:31:02   Drive trip
10:31:03   Position deviation
10:31:04   Safety-related event
```

Grouped by time (all within a ~3-second window) and checked against known subsystem relationships (Ch.4 §4.6's cascade patterns, Ch.7 §7.13's causal graphs — a drive trip is a documented protective response to overcurrent; a mid-travel stop plausibly produces a position/leveling discrepancy; an unconfirmed safe/leveled state plausibly withholds normal-operation permission), this set of five raw alarms transforms into **one probable incident chain** rather than five unrelated problems.

**But correlation must not force unrelated events into one cluster.** If a sixth alarm — say, an unrelated door-lock instability on a different car — happened to fall within the same time window purely by coincidence, a correlation process that merges *anything* temporally close would incorrectly fold it into this incident. The physical-plausibility check (§8.20) is what prevents this.

## 8.20 Temporal vs. Causal Correlation

| Relationship | Meaning | Diagnostic Strength |
|---|---|---|
| **Temporal correlation only** | Events occur close together in time, with no known physical mechanism connecting them | Weak — suggestive at best, easily coincidental |
| **Causal correlation** | One event plausibly contributes to another through a known, physically-justified mechanism | Strong — the basis for a defensible primary/consequential claim |
| **Both present** | Temporal proximity *and* physical plausibility | Strongest — this is the standard this book's cascade examples meet |

**Example of both present:** motor current↑ → drive overcurrent has both temporal proximity and direct physical plausibility (Ch.2 §2.3's protective-trip mechanism). **Example of temporal-only:** a temperature reading rising and a door alarm occurring within the same minute may be temporally close purely by chance, with no known mechanism connecting a machine-room temperature trend to door-lock behavior — this pairing should **not** be treated as one incident chain merely because the timestamps are close.

## 8.21 Alarm Clustering

Several general approaches, each with real trade-offs: **fixed time windows** (simple, but a poor fit if incident duration varies widely); **sliding windows** (more flexible, more computationally continuous); **event sequence patterns** (matching against known cascade "shapes" like Ch.4 §4.6's worked examples — precise when a known pattern matches, blind to novel cascades); **subsystem grouping** (cluster alarms sharing a plausible subsystem relationship, per Ch.4 §4.7's taxonomy); **similarity-based clustering** (grouping alarms with similar characteristics generally); **causal-graph-based clustering** (using §7.13's explicit mechanism knowledge directly, the most physically-grounded but most knowledge-intensive option); and **state-aware clustering** (accounting for the elevator's current operating state, §8.31, before deciding whether two alarms' proximity is meaningful).

## 8.22 Primary vs. Consequential Alarm Detection

Directly extending Chapter 4's foundational distinction into an explicit, repeatable procedure:

**The diagnostic problem, precisely stated:** given an observed alarm set {A1, A2, A3, A4}, which is **initiating**, which are **consequential**, and — importantly — could any be **independent** (unrelated to the others despite temporal proximity)?

```
Collect alarms
     ↓
Sort chronologically
     ↓
Group by incident window
     ↓
Map subsystem relationships (Ch.4 §4.7)
     ↓
Check known causal relationships (§8.20, Ch.7 §7.13)
     ↓
Compare telemetry (does the physical evidence support the
     proposed causal story, not just the timing?)
     ↓
Identify likely initiating event
     ↓
Retain uncertainty where the evidence doesn't cleanly resolve it
```

This is a **conceptual algorithm**, not yet an implemented AI agent — that architectural specification is deliberately deferred to a later phase of this book, consistent with this chapter's explicit scope boundary (front matter).

---

# Part V — Anomaly Detection

## 8.23 What Is an Anomaly?

**Anomaly = behavior significantly different from expected behavior.** *[ESTABLISHED ENGINEERING KNOWLEDGE]* Several distinct flavors:

- **Point anomaly** — a single observation, unusual in isolation (one extreme current spike).
- **Contextual anomaly** — normal in one context, abnormal in another (§8.24's entire subject — high current is fine during acceleration, suspicious while idle).
- **Collective anomaly** — no single point looks unusual, but a *sequence* of points together does (a subtly-but-consistently elevated pattern across many trips).
- **Transient anomaly** — brief, self-resolving.
- **Persistent anomaly** — sustained, doesn't self-resolve.
- **Regime change** — the signal's whole underlying "normal" shifts to a new baseline (not necessarily itself a fault — could reflect a genuine change in usage pattern, load profile, or a legitimate configuration change).

## 8.24 Baseline Behavior

Anomaly detection is fundamentally a comparison against "normal" — which makes defining normal the load-bearing step. Elevator "normal" behavior plausibly varies with **load**, **direction** (up vs. down — Ch.3 §3.3's counterweight-asymmetry reasoning applies directly here), **floor/travel distance**, **time of day** (usage-pattern effects), **temperature** (Ch.3 §3.5-E's environmental context), **operating mode**, **elevator age**, and **maintenance condition**.

**A single global threshold may be inadequate** precisely because of this variability — a current level that's perfectly normal for a fully-loaded car traveling up ten floors may be genuinely anomalous for an empty car making a one-floor trip. §8.31 develops this into an explicit operating-state framework.

## 8.25 Statistical Baseline Methods: Z-score, MAD, EWMA, CUSUM, Control Charts

| Method | Core Idea | Mechanism | Best Detects | Elevator Example | Key Limitation |
|---|---|---|---|---|---|
| **Z-score** | How many standard deviations from the mean | z = (x − μ) / σ | Point anomalies against a stable baseline | A single current reading far outside its usual range | Assumes a roughly stable, well-behaved baseline; sensitive to outliers corrupting μ and σ themselves; struggles under non-stationary (naturally changing) behavior |
| **MAD** (Median Absolute Deviation) | A more robust version of the same idea | median(\|xᵢ − median(x)\|), often used to form a "modified z-score" | Same as Z-score, but more reliably in the presence of outliers | A noisy vibration signal with occasional spikes that would otherwise distort a standard-deviation-based threshold | Still assumes a roughly stable baseline period to compute the reference statistics from |
| **EWMA** (Exponentially Weighted Moving Average) | A smoothed trend that weights recent data more heavily | EWMAₜ = λ·xₜ + (1−λ)·EWMAₜ₋₁ | Gradual drift | Motor temperature or door-cycle time creeping upward over weeks | Trade-off between λ (responsiveness) and noise robustness — high λ reacts fast but noisily, low λ is smooth but slow to flag real change |
| **CUSUM** (Cumulative Sum) | Accumulates small persistent deviations from a target over time | Sₜ = max(0, Sₜ₋₁ + (xₜ − target − k)), alarm when Sₜ exceeds a threshold h | Small, persistent shifts too subtle for a simple threshold | Door closing time increasing by a fraction of a second per week — individually invisible, cumulatively real | Requires choosing a reference/slack value (k) and decision threshold (h), both of which shape sensitivity |
| **Control charts** | Visualize a process against statistically-derived control limits | Center line + upper/lower control limits, watching for out-of-control patterns, trends, or runs | Process-level deviations, borrowed from industrial quality-control practice | Tracking whether a fleet-wide metric (e.g., average brake-release timing) stays within its historically normal range | Designed originally for manufacturing process control; applying it to equipment condition monitoring is a reasonable adaptation, not its original purpose |

**Why CUSUM specifically matters for the door-degradation case:** a gradually increasing door-closing time is exactly the "small persistent deviation" pattern CUSUM is designed to catch earlier than a simple threshold would — by the time a fixed threshold is crossed, the degradation may already be well advanced; CUSUM's accumulation mechanism can flag the trend while it's still small.

## 8.26 Changepoint Detection

A **changepoint** is the specific time at which a signal's underlying statistical behavior changes — a new baseline mean, a new variance, or a change in the signal's overall distribution.

```
Normal current
     ↓
[CHANGEPOINT]
     ↓
A new, different, persistent baseline
```

Changes can be **abrupt** (a sudden step, e.g., current jumping to a new sustained level the moment an obstruction appears) or **gradual** (a slow ramp, e.g., wear-driven drift), and can affect the **mean** (the average level shifts), the **variance** (the signal becomes more/less noisy without necessarily shifting on average), or the full **distribution** (a more complex change in shape). **Bayesian Online Changepoint Detection (BOCPD)**, introduced conceptually: maintains a running probability distribution over "how long has it been since the last changepoint" (the *run length*), updated as each new observation arrives — allowing a real-time, online estimate of changepoint probability without needing to see the whole future signal in advance, which is exactly the operational constraint a real diagnostic system faces (it has to decide *now*, using only data available *now*).

## 8.27 Classical Multivariate/ML Methods: Isolation Forest, One-Class SVM, PCA

| Method | Core Idea | Mechanism | Elevator Application | Key Limitation |
|---|---|---|---|---|
| **Isolation Forest** | Anomalies are easier to isolate than normal points | An ensemble of random trees; each randomly splits the feature space; anomalies get isolated in fewer splits on average (short "path length" = anomalous) | Flagging unusual combinations across several engineered features (e.g., current + vibration + temperature together) | Needs meaningful feature engineering first — doesn't inherently understand time-series structure unless temporal features are explicitly built in; less interpretable than a simple threshold |
| **One-Class SVM** | Learn the boundary enclosing "normal" | A kernel-based decision boundary separating normal from everything else | Flagging multivariate operating points outside the normal operating envelope | Computationally expensive at scale; kernel/parameter choice matters a great deal; doesn't scale gracefully to very high dimensions or very large datasets |
| **PCA** (Principal Component Analysis) | Correlated sensors can be represented in fewer effective dimensions | Finds directions of maximum variance in multivariate data; reconstructs from a reduced set of components; large reconstruction error/residual signals a deviation from the normal correlation structure | Specifically useful because elevator signals (current, vibration, temperature) are *correlated* with each other during normal operation — PCA captures how they normally move *together* | The reduced-dimension representation assumes the normal correlation structure is roughly linear and stable; a genuine but benign change in operating pattern can look identical to a fault under pure PCA reconstruction error |

## 8.28 Deep Learning Methods: Autoencoders, LSTM Autoencoders, Temporal CNN/Transformer, VAE

```
Input → Encoder → Latent (compressed) representation → Decoder → Reconstructed signal
                                                              ↓
                                              Reconstruction error → Anomaly score
```

| Method | Core Idea | Temporal Awareness | Data Requirement | Elevator Application | Key Limitation |
|---|---|---|---|---|---|
| **Standard autoencoder** | Learn to reconstruct normal data; poor reconstruction flags anomalies | None built in — treats each input as an independent snapshot | Moderate — enough normal examples to learn the reconstruction task | Flagging unusual instantaneous multivariate readings | No sense of sequence; threshold selection is non-trivial; can produce false positives on legitimate but rare normal variation |
| **LSTM autoencoder** | Same idea, with recurrent layers modeling temporal sequence | **Explicit** — learns what "normal, given recent history" looks like | Higher — needs enough sequential normal examples | Detecting when a signal's *trajectory*, not just its instantaneous value, deviates from expectation (directly serving Ch.7 §7.17's DBN motivation) | More training data and compute than a standard autoencoder; harder to interpret why a given sequence was flagged |
| **Temporal CNN** | Convolutional layers capturing local temporal patterns | Local/short-range | Moderate–high | Efficient detection of short-duration pattern anomalies | Less naturally suited to very long-range dependencies than a Transformer |
| **Transformer** | Self-attention capturing longer-range temporal dependencies | Long-range, without RNN sequential bottleneck | High — generally the most data- and compute-hungry option here | Relating a current anomaly to a relevant event from well before the immediate window | Substantial data/compute requirements; hardest of this group to interpret and validate rigorously |
| **VAE** (Variational Autoencoder) | A probabilistic latent representation instead of a fixed point | Depends on architecture (can be combined with recurrent/temporal layers) | Similar to standard autoencoder, plus probabilistic-modeling considerations | Uncertainty-aware anomaly scoring — how *likely* is this input under the learned normal distribution, not just how far off the reconstruction is | Probabilistic framing adds genuine value but also genuine complexity over a plain autoencoder |

**Explain why advanced models should only be introduced if they materially outperform simpler baselines** — this is the roadmap's own explicit recommendation, and it's worth stating the reasoning, not just the rule: every method in this table requires substantially more data, more compute, and more validation effort than §8.25's statistical methods, and — critically for a hackathon-stage project with synthetic, physics-grounded data rather than large labeled real-world datasets (§8.42) — the deep-learning methods' main advantage (learning subtle patterns from abundant data) is precisely the resource this project does not currently have in quantity.

## 8.29 Self-Supervised and Contrastive Learning

**Why this category matters given the data problem stated throughout this book:** labeled elevator fault data is scarce and proprietary OEM information isn't public (Ch.4 §4.23) — self-supervised methods are specifically designed for exactly this situation, learning useful representations of *normal* data from largely **unlabeled** examples, without ever needing an explicit "this is a fault" label.

Approaches include **contrastive learning** (similar operating states are pulled together in representation space; genuinely different states are pushed apart — e.g., different normal door cycles should end up represented similarly to each other, while a genuinely abnormal cycle should end up represented differently, learned without ever being told explicitly which cycles were abnormal), **masked reconstruction** (hide part of a signal, train a model to predict the hidden part from context — a signal segment the model struggles to predict is a candidate anomaly), and **predictive/representation learning** more generally (learning representations useful for downstream tasks without task-specific labels).

**Data assumptions worth being explicit about:** these methods still require a reasonably large volume of *normal* operational data to learn useful representations from — they reduce the need for *labeled fault* data specifically, not the need for data generally. **No production performance claim is made for any of these techniques in this book** — they are introduced as a technically appropriate response to the data-scarcity problem, not as a validated solution to it.

## 8.30 Multi-Signal (Multivariate) Anomaly Detection

**Why individual-sensor anomaly detection is insufficient, restated concretely:** "motor current abnormal," alone, is consistent with load, mechanical resistance, an electrical issue, or a purely transient event — genuinely ambiguous on its own. **"Motor current abnormal + vibration abnormal + temperature normal + drive diagnostics normal"** is a materially stronger evidence set — it's consistent with fewer of Chapter 7 §7.7.1's nine candidate causes, and inconsistent with several others (a genuine drive/IGBT fault would be expected to show *abnormal*, not normal, drive diagnostics).

This is the signal-processing-layer justification for §7.14's entire Bayesian evidence-combination framework: **multivariate evidence is not simply "more evidence" — it's evidence that discriminates between hypotheses in a way single-signal evidence structurally cannot.**

## 8.31 Context-Aware Anomaly Detection and Elevator Operating States

**Why the same raw value may be normal in one context and abnormal in another:** high motor current during acceleration is expected and healthy; the same current level during steady-state constant-speed travel is a meaningfully different (and more concerning) signal. High door current during active closing is expected; the same current while the door is supposed to be stationary is not.

A conceptual state machine, useful for scoping which baseline applies at any given moment: **idle → door opening → door open → door closing → acceleration → constant-speed travel → deceleration → leveling → stopped → emergency/protective state → (where relevant) maintenance mode.** **This exact state machine is not claimed as KONE's proprietary implementation** — it's a reasonable, general engineering decomposition of what any traction elevator's operating cycle plausibly involves (consistent with Ch.1 §1.3's operating-cycle chapter), offered as a conceptual scaffold for state-aware baseline selection, not a confirmed internal architecture.

> **Why This Matters to KONE Elevate RCA:** State-awareness is what makes §8.24's baseline problem tractable — rather than one global "normal" for motor current, the system needs (at minimum) a separate normal-behavior model per operating state, which is a direct, practical design requirement flowing out of this section.

---

# Part VI — From Signal to Evidence

## 8.32 Feature Engineering

**How raw signals become diagnostic features**, two worked examples:

```
Raw current waveform
   → RMS (§8.8) → Peak → Variance → Frequency features (§8.9)
   → Trend → Changepoint (§8.26)

Raw door-cycle signal
   → Cycle time → Acceleration profile → Closing time
   → Reopen count → Lock delay
```

| Raw Signal | Derived Features | Potential Diagnostic Meaning |
|---|---|---|
| Motor current | RMS, peak, variance, dominant frequency, trend | Load level, mechanical resistance, electrical health, gradual vs. sudden onset |
| Vibration | RMS, peak, crest factor, spectral energy, envelope | Mechanical wear signatures, transient impacts |
| Door-cycle signal | Cycle time, reopen count, closing force profile, lock delay | Obstruction vs. sensing issue vs. mechanical wear (§8.14) |
| Position/encoder | Position-vs-commanded deviation, speed consistency | Leveling accuracy, feedback trustworthiness (§8.15) |

## 8.33 The Signal → Feature → Evidence Framework

```
RAW SIGNAL → CLEAN SIGNAL → FEATURE → ANOMALY → CONTEXT → DIAGNOSTIC EVIDENCE
```

**Anomaly detection does NOT equal root-cause diagnosis — stated once here, and meant to govern every technique in this chapter.** *"Motor current is anomalous"* is not equivalent to *"the motor has failed."* Every one of §8.25–§8.29's methods, however sophisticated, produces exactly one thing: a signal that some feature deviates from expectation. None of them, individually or collectively, identify *why*. That "why" step is Chapter 7's job entirely — this chapter's entire contribution is making sure the "what deviated, how, and how confidently" handoff to that reasoning is as clean and trustworthy as possible.

## 8.34 False Positives, False Negatives, and Detection Latency

**False positive:** normal behavior flagged as abnormal → unnecessary inspection → wasted technician time. **False negative:** a real abnormality missed → missed degradation → possible service interruption. **Threshold selection is inescapably a trade-off, and an engineering/business one, not a purely technical one** — a more sensitive threshold catches more real problems but generates more false alarms (risking the alarm-flooding/nuisance-alarm problems of §8.16–§8.17); a less sensitive threshold reduces noise at the cost of missing genuine early-stage degradation.

**Detection latency** — the time from an event occurring to an alert actually being generated (data collection delay + processing time + reporting delay) — is a related, separate trade-off: **faster detection is not automatically better if it comes at the cost of dramatically increased false alarms.** A detector tuned to react instantly to any deviation will, by construction, react to noise as readily as to real signal.

## 8.35 Anomaly Detection vs. Fault Detection vs. Root Cause Analysis

The final, precise three-way distinction this Part has been building toward:

**Anomaly detection:** *"Behavior differs from expected."* An anomaly may turn out to be benign, unknown, sensor-related, purely operational/environmental, genuine early degradation, or an actual fault — the term itself makes no claim about which.

**Fault detection:** *"A known, defined failure condition is likely present"* — a narrower, more committed claim than a bare anomaly, requiring the deviation to match a recognized failure pattern (Ch.4 §4.7's taxonomy).

**Root cause analysis:** *"Why does this abnormal behavior occur?"* — the full evidence-weighed, multi-hypothesis reasoning process Chapter 7 built in depth.

**ANOMALY ≠ FAULT ≠ ROOT CAUSE.** Example, stated once more for emphasis: *Anomaly* — motor current increased. *Fault detection* — this matches the "overcurrent" category. *RCA* — likely mechanical resistance caused increased torque demand (one ranked hypothesis among several, per Ch.7 §7.15). **Anomaly detection is evidence generation for RCA — it is not RCA itself, and this chapter's output feeds Chapter 7's process rather than replacing any part of it.**

---

# Part VII — Worked End-to-End Examples

## 8.36 Worked Example 1: Mechanical Obstruction — Full Signal Pipeline

**Scenario:** a mechanical obstruction develops during operation.

```
Normal motor current
     ↓
Small current increase (below any threshold — a changepoint, not yet an alarm)
     ↓
Vibration increase (correlated in time and, per §8.20, physically
     plausible given the same developing mechanical cause)
     ↓
Acceleration deviation (motion profile no longer tracks the
     commanded trajectory precisely)
     ↓
Current spike (crosses the defined threshold)
     ↓
Overcurrent alarm generated
     ↓
Drive trip (protective response)
     ↓
Position deviation (mid-travel stop, no confirmed floor position)
```

**Pipeline stages applied:**

1. **Signal preprocessing** (§8.4–§8.5) — confirm current and vibration timestamps are aligned; confirm no sensor-quality issue explains the readings.
2. **Feature extraction** (§8.32) — RMS and trend on current; RMS and spectral content on vibration.
3. **Anomaly detection** (§8.25–§8.26) — CUSUM or a changepoint method flags the *early*, small, gradual current increase before it would cross a naive fixed threshold; a Z-score or threshold method flags the later, sharper spike.
4. **Temporal alignment** (§8.4, §8.11) — confirm the current-rise-then-vibration-rise ordering, checked against known clock offsets.
5. **Alarm correlation** (§8.19) — group the overcurrent alarm, drive trip, and position deviation into one incident window.
6. **Primary/consequential classification** (§8.22) — overcurrent identified as the earliest, physically-plausible initiating alarm; drive trip and position deviation classified as consequential.
7. **Evidence creation** (§8.47) — package the anomaly (pre-alarm current trend), the vibration correlation, the clean drive self-test (if checked), and the alarm chronology into one structured evidence object.
8. **Handoff to RCA** — this evidence package becomes the input to exactly the Chapter 7 §7.32 worked example this chapter's introduction promised to feed. **This chapter does not perform the final root-cause ranking itself** — that's Chapter 7's job, already demonstrated there using evidence of exactly this shape.

## 8.37 Worked Example 2: Door Degradation

**Scenario:** the door mechanism gradually becomes more resistant over time (e.g., accumulating roller wear).

```
Door-cycle time gradually increases (over days/weeks — a slow trend)
     ↓
Motor current gradually increases (correlated with the same trend)
     ↓
Variance in cycle time increases (growing inconsistency, not just a shifted average)
     ↓
Changepoint/drift detected (§8.26, or EWMA/CUSUM per §8.25)
     ↓
Repeated reopen events begin appearing (as resistance approaches
     a threshold where the door occasionally fails to fully close in time)
     ↓
Door timeout alarm
```

**How EWMA + CUSUM + door-cycle features + event correlation could detect this degradation, conceptually:** EWMA smooths the noisy cycle-time signal into a clear trend line; CUSUM accumulates the small week-over-week increase, flagging the drift well before any single reading would cross a fixed threshold; door-cycle feature extraction (§8.14, §8.32) confirms the pattern is specifically tied to resistance (current rising alongside cycle time, not reopen events driven by photo-eye instability, which would show a different signature — Ch.4 §4.9); event correlation confirms the eventual timeout alarms are downstream of this same gradual trend, not an independent, sudden problem. **No claim is made that KONE's production systems currently deploy this specific combination** — this is a demonstration of the reasoning, not a description of a confirmed implementation.

## 8.38 Worked Example 3: Intermittent Encoder Issue

**Scenario:** an encoder connection is marginal, producing occasional, brief instability.

```
Normal position signal
     ↓
Occasional feedback instability (brief, sub-second glitches)
     ↓
Short-duration position deviation (self-resolving each time)
     ↓
Repeated position-related events, spread irregularly over days
     ↓
The condition is not present during any single physical inspection
     (Ch.4 §4.13's intermittent-fault problem, restated at the
     signal-processing layer)
     ↓
Historical reconstruction becomes essential
```

**Why event logs + time-series data + cross-correlation + operating context can reveal a pattern no single inspection would:** each individual glitch is brief and, viewed in isolation, easily dismissed as sensor noise. Reviewed together — as a time series of many such brief events, cross-correlated against, say, vibration levels (a marginal connector might only fail under specific vibration conditions) or temperature (thermal expansion affecting a marginal connection) — a genuine pattern can emerge that no single moment-in-time reading, and no single technician visit, would ever surface. This is the concrete, technical justification for why Chapter 5's historical-evidence emphasis (§5.16) and Chapter 4's intermittent-fault discussion (§4.13) both matter as much as they do: some faults are, structurally, only visible in aggregate.

---

# Part VIII — Choosing Methods Responsibly

## 8.39 A Signal-Processing Decision Guide

A conceptual guide, not an absolute rule:

```
What type of signal is this?

Slow-changing            → statistical trend methods (EWMA, CUSUM)
Periodic/oscillatory     → frequency-domain analysis (FFT)
Transient                → time-domain/event analysis
Multivariate             → PCA / multivariate methods
A temporal sequence      → temporal models (LSTM-AE, Temporal CNN, Transformer)
Baseline poorly known    → general anomaly detection (statistical or ML)
A known, named signature → supervised/classification methods (requires labeled examples this project largely lacks — §8.42)
```

## 8.40 Algorithm Selection Matrix

| Method | Data Requirement | Temporal Awareness | Interpretability | Computational Cost | Elevator Use Case | Recommended Baseline? |
|---|---|---|---|---|---|---|
| Fixed threshold | Minimal | None | Highest | Lowest | Simple, well-understood limits (e.g., a hard current ceiling) | **Yes** |
| Z-score | Low | None | High | Low | Point anomalies against a stable baseline | **Yes** |
| MAD | Low | None | High | Low | Same, more outlier-robust | **Yes** |
| EWMA | Low | Weak (trend-only) | High | Low | Gradual drift (temperature, door-cycle time) | **Yes** |
| CUSUM | Low | Weak (trend-only) | High | Low | Small, persistent shifts | **Yes** |
| Control charts | Low–moderate | None | High | Low | Fleet-level trend monitoring | **Yes** |
| Changepoint detection (incl. BOCPD) | Moderate | Moderate | Moderate | Moderate | Identifying when behavior genuinely shifted | **Yes** |
| Isolation Forest | Moderate | None (unless engineered in) | Moderate | Moderate | Multivariate point anomalies | Moderate — needs feature engineering |
| One-Class SVM | Moderate | None | Low–moderate | Moderate–high | Multivariate boundary learning | Moderate |
| PCA | Moderate | None | Moderate | Low–moderate | Correlated multivariate telemetry | Moderate — good fit but needs stable correlation structure |
| Autoencoder | High | None | Low | Moderate–high | Multivariate reconstruction-based anomaly scoring | Requires stronger justification |
| LSTM autoencoder | High | Strong | Low | High | Sequence-aware anomaly detection | Requires stronger justification |
| Temporal CNN | High | Moderate–strong | Low | High | Short-range temporal patterns | Requires stronger justification |
| Transformer | Very high | Strong (long-range) | Lowest | Highest | Long-range dependency modeling | Requires stronger justification |
| VAE | High | Depends on architecture | Low | High | Uncertainty-aware anomaly scoring | Requires stronger justification |
| BOCPD | Moderate | Strong | Moderate | Moderate | Online changepoint probability | Moderate — a genuinely good fit worth prioritizing among the "advanced" tier |
| Self-supervised (general) | Moderate–high, but unlabeled | Depends on task design | Low–moderate | Moderate–high | Learning from abundant unlabeled normal data | Requires stronger justification |
| Contrastive learning | Moderate–high, but unlabeled | Depends on task design | Low | Moderate–high | Distinguishing normal-variant clusters without labels | Requires stronger justification |

**Strong baseline methods:** fixed threshold, Z-score, MAD, EWMA, CUSUM, control charts, changepoint detection. **Advanced methods requiring stronger justification:** everything from Isolation Forest downward — not because they're worse, but because their added complexity needs to be earned by demonstrated added value over the baseline tier, not assumed.

## 8.41 Why Simple Baselines Matter First

The roadmap's own explicit recommendation, defended here on its merits: given this project's **small, synthetic dataset** (rather than large labeled production data), **explainability requirements** (a confidence-scored, auditable conclusion is the whole point of this project — a black-box deep model actively undermines that goal), real **compute constraints** at hackathon scale, genuine **validation difficulty** without labeled ground truth, the **false-positive cost** discussed in §8.34, and the general maintenance-domain preference for interpretable, auditable tools over opaque ones — a simple, well-validated baseline that clearly works is worth more, scientifically and practically, than a sophisticated model whose behavior nobody on the team can fully explain or trust. **This is critical for scientific credibility specifically**: establishing a simple baseline's measurable performance *first*, then testing whether an advanced model materially improves on it, is the methodologically sound order of operations — reversing it (starting with the most sophisticated model available) is a common and avoidable mistake.

## 8.42 Data Scarcity and Synthetic Signals

Restating and extending Chapter 4 §4.23 and Chapter 7 §7.40's research gaps at the signal-processing layer specifically: **few publicly available real elevator datasets** exist; **labeled faults are scarce**; proprietary OEM telemetry is not public; elevator faults are, in the aggregate, **rare events**, producing severe **class imbalance** in any dataset that does exist; and real-world **maintenance records may themselves be incomplete**. This has direct implications for supervised learning (insufficient labeled examples to train reliably), anomaly detection generally (baseline "normal" data is available, but confirmed-fault examples to validate against are not), validation (no large held-out labeled test set to measure real-world performance against), and transfer learning (a model trained on a different domain's data may not transfer cleanly to elevator-specific signal characteristics).

**How synthetic data may be used, conceptually:** simulated motor-current abnormalities, simulated vibration increases, synthetic door-cycle degradation, and simulated encoder deviations, each constructed from the physics-grounded reasoning established across Chapters 1–3 of this book (Understanding Report §K's stated validation strategy). **Synthetic data is demonstration data, never production validation data — this distinction must never be blurred.** A method that performs well against synthetic scenarios has demonstrated that its *reasoning process* behaves as designed; it has not demonstrated real-world diagnostic accuracy, which can only be established against real, labeled field data this project does not currently have.

## 8.43 The Data Quality Chain

```
DATA QUALITY
     ↓
SIGNAL QUALITY
     ↓
FEATURE QUALITY
     ↓
DETECTION QUALITY
     ↓
EVIDENCE QUALITY
     ↓
RCA QUALITY
```

**Poor data produces poor features, which produce poor anomaly detection, which produces poor diagnostic evidence, which produces poor RCA** — no stage in Chapter 7's careful reasoning framework can compensate for evidence that was corrupted, misaligned, or mislabeled at this chain's first link. This is one of the key operating principles of the whole research book: **sophistication in reasoning (Chapter 7) cannot substitute for rigor in evidence collection (this chapter)** — the two are complementary, sequential dependencies, not interchangeable investments.

---

# Part IX — Architecture Handoff

## 8.44 Why This Matters to the RCA System

This chapter produces structured evidence of a specific shape: **that** an anomaly was detected, **when** the signal changed, the **magnitude** of the deviation, its **duration**, the **affected signal** and **affected operating state**, any **correlated signals**, any **correlated alarms**, the relevant **temporal relationships**, and a **confidence/quality** rating for the observation itself (distinct from Chapter 7's diagnostic confidence — this is confidence in the *measurement*, not yet in any *cause*). This evidence is what feeds directly into the RCA reasoning framework Chapter 7 already built and demonstrated. **This chapter does not design the AI agent architecture that would consume this evidence** — that remains deliberately deferred to a later phase.

## 8.45 The Master Signal-to-RCA Pipeline

```
RAW TELEMETRY
     ↓
QUALITY CHECK              (§8.5)
     ↓
TIME ALIGNMENT              (§8.4)
     ↓
FILTERING                    (§8.6)
     ↓
FEATURE EXTRACTION             (§8.7–§8.9, §8.32)
     ↓
BASELINE COMPARISON              (§8.24, §8.31)
     ↓
ANOMALY DETECTION                  (§8.25–§8.29)
     ↓
TEMPORAL ANALYSIS                    (§8.10–§8.11)
     ↓
ALARM CORRELATION                      (§8.19–§8.21)
     ↓
PRIMARY/CONSEQUENTIAL CLASSIFICATION     (§8.22)
     ↓
DIAGNOSTIC EVIDENCE                        (§8.47)
     ↓
RCA ENGINE (Chapter 7)
```

## 8.46 The Master Alarm-Correlation Pipeline

A companion pipeline, specifically for discrete alarm/event streams rather than continuous telemetry:

```
ALARM STREAM
     ↓
TIMESTAMP NORMALIZATION
     ↓
INCIDENT WINDOW
     ↓
ALARM CLUSTERING              (§8.21)
     ↓
SUBSYSTEM MAPPING               (Ch.4 §4.7)
     ↓
TEMPORAL RELATIONSHIPS            (§8.11)
     ↓
CAUSAL RELATIONSHIPS                (§8.20, Ch.7 §7.13)
     ↓
PRIMARY EVENT CANDIDATE
     ↓
CONSEQUENTIAL EVENTS
     ↓
EVIDENCE PACKAGE
```

**The output of this pipeline should be framed as "likely causal event chain," never "guaranteed root cause."** Alarm correlation narrows and structures the evidence; it does not, by itself, conclude anything — that remains Chapter 7's job, fed by this pipeline's output.

## 8.47 The Evidence Package

A structured evidence package, conceptually, carries: **timestamp**, **signal** (which one), **baseline** (what "normal" was being compared against), **observed value**, **deviation** (magnitude/direction from baseline), **duration**, **operating state** (§8.31), **related signals** (§8.30's multivariate context), **related alarms**, **event sequence**, **signal quality** (§8.5's assessment), **anomaly score**, and **source** (provenance — which sensor, which method produced this evidence).

**Why this is more useful to downstream RCA than raw telemetry:** every field above corresponds directly to something Chapter 7's reasoning process needs and would otherwise have to re-derive from scratch — handing raw, unstructured telemetry to a reasoning layer forces it to also solve every problem this chapter exists to solve, defeating the purpose of separating evidence-generation from evidence-reasoning as distinct, independently-improvable stages.

## 8.48 Limitations

Honestly stated: noisy sensors, missing data, asynchronous timestamps, non-stationary operation (genuine, non-faulty behavior changes over time — wear, seasonal effects, usage-pattern shifts), changing load, environmental effects, the inherent rarity of real faults, false positives, false negatives, concept drift (the definition of "normal" itself changing over time, requiring baseline models to be periodically revisited), sensor faults masquerading as equipment faults, correlated signals risking the double-counting problem (Ch.7 §7.16), insufficient sampling for some fault types, and unknown failure modes no fault tree in this book yet represents. **Each of these can mislead diagnosis if not explicitly accounted for** — which is precisely why this chapter treats evidence generation as a discipline in its own right, not a solved preliminary step.

## 8.49 Research Gaps

Limited real elevator datasets; limited labeled fault signatures; unknown proprietary sampling rates (§8.3); limited public OEM alarm mappings (Ch.4 §4.23); uncertain signal-to-fault relationships beyond the general engineering reasoning established in Chapters 1–3; genuine difficulty establishing causal relationships with confidence from observational data alone (§8.10, Ch.7 §7.13); difficulty validating anomaly thresholds without real fault-labeled data; and the practical difficulty of distinguishing sensor anomalies from genuine equipment anomalies (§8.5) without independent cross-checks. **Known**: the general methods and their trade-offs, taught throughout this chapter. **Unknown**: their real-world calibrated performance on actual KONE equipment and data. **Assumed**: a modern gearless traction elevator's general signal characteristics, consistent with Chapters 1–3's stated scope. **Illustrative**: every specific number in this chapter's worked examples and tables.

---

# Judge Questions

**1. Why can't you just use thresholds?** *Concise:* Thresholds miss gradual drift and context-dependence (§8.24–§8.26). *Detailed:* A fixed threshold treats every operating state identically and can't detect a slow trend before it crosses the line. *Evidence:* §8.25's CUSUM/EWMA comparison. *Assumptions:* None. *Tested:* Whether "we use AI" masks an actual understanding of threshold limitations. *Avoid:* Dismissing thresholds entirely — they remain a valid, recommended baseline (§8.40) for genuinely simple cases.

**2. Why do you need time-series analysis?** *Concise:* Because elevator state is inherently temporal (§8.1) — a single snapshot rarely carries enough information. *Detailed:* The whole gradual-vs-sudden distinction (§7.17, §8.37) depends on it. *Evidence:* Multiple worked examples. *Assumptions:* None. *Tested:* Basic grounding. *Avoid:* A generic answer without the gradual/sudden example.

**3. Why does sampling rate matter?** *Concise:* Under-sampling a fast signal risks aliasing — missing real dynamics entirely (§8.3). *Detailed:* Nyquist reasoning, plus why different elevator signals need different rates. *Evidence:* Standard signal-processing theory. *Assumptions:* No specific KONE rate claimed. *Tested:* Whether the team understands this isn't just "more data is better." *Avoid:* Inventing a specific sampling number.

**4. What happens if sensors have different sampling rates?** *Concise:* Resampling/alignment is required before comparison (§8.4). *Detailed:* Interpolation, aggregation, timestamp synchronization. *Evidence:* — *Assumptions:* — *Tested:* Whether multi-sensor integration challenges are understood, not assumed away. *Avoid:* Assuming all signals arrive pre-aligned.

**5. How do you synchronize signals?** *Concise:* Timestamp normalization and clock-offset correction before any cross-signal comparison (§8.4). *Detailed:* The false-temporal-relationship risk if this is skipped. *Evidence:* — *Assumptions:* — *Tested:* Whether misalignment risk is taken seriously. *Avoid:* Treating this as a trivial step.

**6. What is aliasing?** *Concise:* A fast signal misread as a slower, different pattern due to under-sampling (§8.3). *Detailed:* Nyquist's "more than twice the frequency" rule. *Evidence:* Standard signal theory. *Assumptions:* — *Tested:* A direct definitional check. *Avoid:* Confusing aliasing with simple noise.

**7. Why filter the signal?** *Concise:* To remove noise obscuring the underlying pattern (§8.6). *Detailed:* Different filters for different noise/signal characteristics. *Evidence:* §8.6's table. *Assumptions:* — *Tested:* Whether filter choice is understood as signal-specific, not generic. *Avoid:* "To clean the data" without specifying how or why a specific filter fits.

**8. Can filtering hide a fault?** *Concise:* Yes — excessive filtering can smooth away exactly the transient a fault signature depends on (§8.6). *Detailed:* A sharp, brief current spike is exactly what an aggressive low-pass filter removes. *Evidence:* Direct engineering reasoning. *Assumptions:* — *Tested:* Whether the team has considered filtering's own failure mode, not just its benefit. *Avoid:* Presenting filtering as risk-free.

**9. What is RMS?** *Concise:* The square root of the mean of squared values — an "effective magnitude" measure (§8.8). *Detailed:* Full formula and why it beats a plain average for oscillating signals. *Evidence:* Standard signal theory. *Assumptions:* — *Tested:* Whether the formula can be stated, not just the acronym. *Avoid:* Confusing RMS with peak or average.

**10. Why use FFT?** *Concise:* To see what frequency components make up a signal, not just its magnitude (§8.9). *Detailed:* Two signals with identical RMS can differ completely in frequency content. *Evidence:* §8.9's KEY CONCEPT box. *Assumptions:* — *Tested:* Whether time-domain vs. frequency-domain is genuinely understood. *Avoid:* "FFT finds patterns" without the specific time/frequency distinction.

**11. What is motor current signature analysis?** *Concise:* Analyzing current's time- and frequency-domain content to infer mechanical/electrical condition (§8.12). *Detailed:* Physically coupled to load and mechanical state via Ch.1's T≈k·Iq relationship. *Evidence:* Established industrial technique, not elevator-specific. *Assumptions:* No KONE-specific signature claimed. *Tested:* Whether MCSA is understood as contextual evidence, not a standalone diagnosis. *Avoid:* Claiming a specific pattern uniquely identifies a specific fault.

**12. How can vibration help diagnosis?** *Concise:* As one of several correlated signals narrowing the hypothesis space, not a standalone conclusion (§8.13). *Detailed:* Amplitude, frequency, envelope analysis — each adds discriminating power in combination with other evidence. *Evidence:* §7.7's fault trees, throughout. *Assumptions:* — *Tested:* Whether vibration is treated as one input among several. *Avoid:* "Vibration tells you what's wrong" alone.

**13. How can door-cycle analysis help?** *Concise:* Distinguishing obstruction, mechanical resistance, sensing issues, and motor problems by their distinct cycle-feature signatures (§8.14). *Detailed:* Cycle time + current + reopen pattern together, not any one alone. *Evidence:* Ch.4 §4.9's differential table. *Assumptions:* — *Tested:* Specific, concrete application, not generality. *Avoid:* Vague "it helps."

**14. Why is encoder data important?** *Concise:* It's the foundation of the whole closed-loop motion-control system (Ch.2 §2.4) — degraded encoder data degrades everything downstream. *Detailed:* Expected-vs-observed trajectory comparison, cross-checked against an independent leveling sensor. *Evidence:* Ch.3 §3.7, Ch.7 §7.34. *Assumptions:* — *Tested:* Whether the encoder's structural centrality is understood. *Avoid:* Treating it as just one more sensor.

**15. What is cross-correlation?** *Concise:* Measuring how similar two signals are at various time lags (§8.10). *Detailed:* Identifies both relatedness and typical time offset. *Evidence:* Standard signal theory. *Assumptions:* — *Tested:* Definitional accuracy. *Avoid:* Confusing with simple correlation (no lag).

**16. Does correlation prove causation?** *Concise:* No (§8.10, Ch.7 §7.13). *Detailed:* Three explanations for correlation — genuine causation, shared unobserved cause, coincidence. *Evidence:* — *Assumptions:* — *Tested:* Whether this principle survives repetition across chapters without erosion. *Avoid:* Any hedge that sounds like "usually, yes."

**17. What is alarm flooding?** *Concise:* Many alarms generated in a short period, risking misinterpretation as independent problems (§8.16). *Detailed:* The five-alarms-from-one-obstruction example. *Evidence:* — *Assumptions:* — *Tested:* Whether the concrete example is ready. *Avoid:* A definition with no example.

**18. Why is alarm correlation important?** *Concise:* It transforms an alarm flood into one probable incident chain instead of several false independent investigations (§8.19). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this connects back to Ch.4's original motivation. *Avoid:* Losing the thread back to why this matters at all.

**19. How do you identify the primary alarm?** *Concise:* Earliest in the incident window, physically plausible as an initiating cause (§8.22). *Detailed:* The explicit algorithm — chronological sort, subsystem mapping, causal-relationship check. *Evidence:* — *Assumptions:* — *Tested:* Whether "earliest" alone (without the plausibility check) is mistakenly given as the full answer. *Avoid:* "Whichever came first," unqualified.

**20. How do you distinguish consequential alarms?** *Concise:* By confirming a documented causal mechanism connects them to the primary event (§8.20). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same discipline as Q19, applied to the "rest" of the chain. *Avoid:* Assuming everything not primary is automatically consequential without checking.

**21. What if two unrelated faults occur simultaneously?** *Concise:* The physical-plausibility check should prevent incorrectly merging them (§8.19's "must not force unrelated events into one cluster," Ch.7 §7.28). *Detailed:* A real, acknowledged risk of any correlation system. *Evidence:* — *Assumptions:* — *Tested:* Whether the false-positive side of correlation has been considered. *Avoid:* Assuming correlation always gets this right.

**22. What is anomaly detection?** *Concise:* Identifying behavior that differs from expectation (§8.23). *Detailed:* Several distinct types — point, contextual, collective, transient, persistent, regime-change. *Evidence:* — *Assumptions:* — *Tested:* Definitional precision. *Avoid:* Conflating anomaly with fault.

**23. Is an anomaly automatically a fault?** *Concise:* No (§8.35). *Detailed:* An anomaly may be benign, sensor-related, environmental, or genuine — the term alone doesn't say which. *Evidence:* — *Assumptions:* — *Tested:* The single most important distinction in this whole Part — expect it to recur. *Avoid:* Any answer implying automatic equivalence.

**24. What is the difference between anomaly detection and RCA?** *Concise:* Detection says something looks unusual; RCA explains why (§8.35). *Detailed:* Anomaly detection is evidence generation for RCA, not RCA itself. *Evidence:* — *Assumptions:* — *Tested:* Whether the chapter-to-chapter handoff is understood. *Avoid:* Treating anomaly detection as sufficient on its own.

**25. Why use Z-score?** *Concise:* Simple, interpretable point-anomaly detection against a stable baseline (§8.25). *Detailed:* z=(x−μ)/σ; limitations under non-stationary behavior. *Evidence:* — *Assumptions:* Illustrative thresholds only. *Tested:* Formula recall plus limitation awareness. *Avoid:* Presenting it as universally sufficient.

**26. Why use MAD?** *Concise:* More outlier-robust than standard deviation (§8.25). *Detailed:* Median-based statistics resist distortion from a few extreme values. *Evidence:* — *Assumptions:* — *Tested:* Whether the specific robustness advantage is named. *Avoid:* "It's similar to Z-score" without saying why it's chosen instead.

**27. Why use EWMA?** *Concise:* Detects gradual drift a point-in-time method would miss (§8.25). *Detailed:* Exponential weighting favors recent data while smoothing noise. *Evidence:* — *Assumptions:* — *Tested:* Whether the sensitivity/noise trade-off is understood. *Avoid:* Ignoring the λ trade-off.

**28. Why use CUSUM?** *Concise:* Accumulates small persistent shifts too subtle for a simple threshold (§8.25). *Detailed:* The door-closing-time example. *Evidence:* — *Assumptions:* — *Tested:* Whether a concrete example is ready. *Avoid:* A definition with no example.

**29. Why use changepoint detection?** *Concise:* Pinpoints exactly when behavior genuinely shifted, abrupt or gradual (§8.26). *Detailed:* BOCPD's online, real-time framing. *Evidence:* — *Assumptions:* — *Tested:* Whether this is distinguished from simple threshold-crossing. *Avoid:* Conflating changepoint detection with basic anomaly flagging.

**30. Why use Isolation Forest?** *Concise:* Efficient multivariate point-anomaly detection without needing a labeled distance metric (§8.27). *Detailed:* Path-length-to-isolation as the anomaly score. *Evidence:* — *Assumptions:* Requires prior feature engineering. *Tested:* Whether the mechanism (not just the name) is understood. *Avoid:* Treating it as a black box.

**31. Why not use an LSTM?** *Concise:* Because it needs more data and compute than this project currently has, and is harder to validate/explain (§8.28, §8.41). *Detailed:* A legitimate, powerful method for the right data volume — just not the right first choice here. *Evidence:* — *Assumptions:* — *Tested:* Whether "advanced = better" is resisted. *Avoid:* Dismissing LSTMs as bad — they're situationally inappropriate here, not flawed in general.

**32. Why not use a Transformer?** *Concise:* Same reasoning as Q31, more acutely — Transformers are the most data-hungry, least interpretable option in this chapter's toolkit (§8.28, §8.40). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with Q31's answer. *Avoid:* A different justification than the one given for LSTMs, without explaining why.

**33. How much training data do you need?** *Concise:* Depends heavily on method — statistical baselines need very little; deep-learning methods need substantially more than this project currently has (§8.40–§8.42). *Detailed:* — *Evidence:* §8.40's table. *Assumptions:* — *Tested:* Whether a specific, defensible answer exists rather than a shrug. *Avoid:* A vague non-answer.

**34. How do you handle rare faults?** *Concise:* Favor methods that learn "normal" from abundant data rather than requiring labeled rare-fault examples (§8.29, §8.42). *Detailed:* Self-supervised/contrastive approaches specifically target this. *Evidence:* — *Assumptions:* — *Tested:* Whether class-imbalance is understood as a real constraint. *Avoid:* Assuming enough labeled fault examples exist.

**35. How do you handle missing sensor data?** *Concise:* Distinguish it explicitly from a true negative — never treat silence as "normal" (§8.5, Ch.7 §7.26). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with Ch.7's negative-evidence discipline. *Avoid:* Filling gaps with assumed values.

**36. How do you handle sensor failure?** *Concise:* Cross-check against independent/complementary signals wherever possible (§8.15's encoder-vs-leveling-sensor pattern). *Detailed:* — *Evidence:* Ch.7 §7.34. *Assumptions:* An independent check must actually exist — not guaranteed for every signal. *Tested:* Whether a concrete example is ready. *Avoid:* Assuming redundancy always exists.

**37. How do you validate an anomaly detector?** *Concise:* Against synthetic, physics-grounded scenarios at this project stage — explicitly not claimed as production validation (§8.42). *Detailed:* — *Evidence:* Understanding Report §K. *Assumptions:* — *Tested:* Whether this caveat is volunteered unprompted. *Avoid:* Presenting synthetic-scenario success as real-world proof.

**38. How do you avoid false alarms?** *Concise:* Careful threshold selection, acknowledging it as a real trade-off, not a solved problem (§8.34). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the trade-off (vs. false negatives) is named explicitly. *Avoid:* Claiming false alarms can be eliminated without cost.

**39. How do you avoid missing real faults?** *Concise:* Same trade-off, opposite direction (§8.34). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether Q38 and Q39 are recognized as two sides of one trade-off, not independent problems. *Avoid:* Answering as if sensitivity has no cost.

**40. How does anomaly detection feed RCA?** *Concise:* Via a structured evidence package, not raw telemetry (§8.47). *Detailed:* Every field in the package maps to something Chapter 7's reasoning loop needs. *Evidence:* §8.45's pipeline. *Assumptions:* — *Tested:* Whether the chapter-to-chapter handoff is concrete, not hand-wavy. *Avoid:* A vague "it provides evidence" without naming the structure.

**41. How do you distinguish sensor anomaly from equipment anomaly?** *Concise:* Cross-checking against independent signals and known sensor-failure signatures (stuck values, impossible readings — §8.5). *Detailed:* — *Evidence:* — *Assumptions:* Not always fully resolvable with available evidence. *Tested:* Whether this is acknowledged as genuinely hard, not solved. *Avoid:* Implying a guaranteed method exists.

**42. How do you use synthetic data responsibly?** *Concise:* As demonstration data for the reasoning process, never presented as production validation (§8.42). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this distinction is second nature by this point in the book. *Avoid:* Blurring demonstration and validation.

**43. How do you know an anomaly is meaningful?** *Concise:* You often don't, alone — meaningfulness is established by combining it with context, correlation, and eventually RCA reasoning (§8.30, §8.35). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether overconfidence in raw anomaly scores is avoided. *Avoid:* Implying an anomaly score alone answers this.

**44. How do you handle changing operating conditions?** *Concise:* State-aware baselines, not one global "normal" (§8.24, §8.31). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the operating-state framework is genuinely applied, not just mentioned. *Avoid:* A single global threshold as the implied answer.

**45. What happens when signals disagree?** *Concise:* This is itself diagnostic information, not a problem to average away (§8.15, Ch.7 §7.27, §7.34's independent-sensor-agreement check). *Detailed:* Disagreement between an encoder and an independent leveling sensor is precisely what distinguishes a feedback fault from a genuine motion problem. *Evidence:* Ch.7 §7.34's worked example. *Assumptions:* — *Tested:* Whether disagreement is understood as valuable evidence, not noise to be resolved by picking one signal. *Avoid:* Arbitrarily trusting one signal over another without justification.

---

# Master Comparison Table

| Technique | Purpose | Input | Output | Strength | Limitation | Elevator Application | RCA Contribution |
|---|---|---|---|---|---|---|---|
| Signal filtering | Remove noise | Raw signal | Cleaned signal | Preserves genuine pattern | Can hide transient fault signatures | Pre-processing every telemetry stream | Cleaner downstream features |
| Statistical features | Summarize signal behavior | Cleaned signal | RMS, variance, peak, etc. | Simple, interpretable | Doesn't capture frequency content | Current/vibration summarization | Core evidence inputs |
| FFT | Reveal frequency content | Time-domain signal | Frequency spectrum | Distinguishes signal character | Assumes some stationarity within the analysis window | MCSA, vibration analysis | Discriminates fault types sharing similar time-domain stats |
| Cross-correlation | Relate two signals over time | Two signals | Correlation + lag | Quantifies lead/lag relationships | Doesn't prove causation | Current-vs-vibration timing | Chronology evidence |
| Temporal correlation | Establish event ordering | Event timestamps | Ordering + windows | Simple, necessary first step | Insufficient alone | Alarm sequencing | Necessary input to alarm correlation |
| Alarm clustering | Group related alarms | Alarm stream | Incident windows | Reduces alarm-flood confusion | Risk of over-merging | Multi-alarm cascades | Forms fault episodes |
| Alarm correlation | Identify primary/consequential structure | Clustered alarms | Causal chain hypothesis | Turns floods into episodes | Requires physical-plausibility checking | The Ch.4 §4.5 cascade pattern | Directly structures the RCA hypothesis space |
| Z-score / MAD | Point-anomaly detection | Feature + baseline stats | Anomaly flag | Simple, interpretable | Assumes stable baseline | Sudden deviations | Evidence generation, baseline tier |
| EWMA / CUSUM | Drift/gradual-shift detection | Feature time series | Trend/drift flag | Detects subtle degradation early | Sensitivity/noise trade-off | Door-cycle drift, wear trends | Evidence generation, baseline tier |
| Control charts | Process-level monitoring | Aggregate metric | In/out-of-control flag | Borrowed, mature methodology | Originally manufacturing-focused | Fleet-level metric tracking | Contextual evidence |
| Changepoint detection | Locate behavior shifts | Feature time series | Changepoint estimate | Precise timing of change | Moderate complexity | Onset-timing evidence | Sharpens temporal evidence for RCA |
| Isolation Forest / One-Class SVM / PCA | Multivariate anomaly detection | Feature vectors | Anomaly score | Captures cross-signal patterns | Needs feature engineering; limited temporal awareness | Multi-sensor operating-point anomalies | Multivariate evidence generation |
| Autoencoder / LSTM-AE / Temporal CNN / Transformer / VAE | Learned, potentially temporal, anomaly detection | Raw or feature sequences | Reconstruction-based anomaly score | Captures complex, temporal patterns | Data-hungry, low interpretability | Sequence-aware degradation detection | Advanced-tier evidence generation, requires justification |
| Self-supervised / contrastive learning | Learn from unlabeled normal data | Unlabeled sequences | Representation-based anomaly score | Addresses label scarcity directly | Still needs abundant normal data | Distinguishing normal-variant patterns without labels | Addresses this project's specific data-scarcity constraint |

# What We Now Understand

Elevator telemetry is inherently time-dependent, and a single instantaneous reading rarely carries enough diagnostic meaning on its own. Signal quality problems — missing data, sensor dropout, misalignment — must be caught before anything downstream can be trusted, and timestamps must be genuinely synchronized before temporal reasoning about them means anything. Raw telemetry is not immediately diagnostic evidence; it has to pass through filtering, feature extraction, and context-aware comparison against an appropriately state-specific baseline first. Alarm correlation transforms alarm floods into coherent incident chains, and the primary-vs-consequential distinction from Phase 2 has a concrete, repeatable procedure behind it now, not just a principle. Anomaly detection spans a wide toolkit — from simple, interpretable statistical baselines through increasingly data-hungry deep-learning methods — and the roadmap's own recommendation to start simple is defensible on real engineering grounds: interpretability, data scarcity, and validation difficulty, not just convention. Critically, and repeatedly: an anomaly is not a fault, and anomaly detection is not root-cause analysis — this chapter generates the evidence Chapter 7's reasoning framework consumes; it does not replace that reasoning.

# The Central Principle

> **ANOMALY DETECTION FINDS UNUSUAL BEHAVIOR; RCA EXPLAINS WHY THAT BEHAVIOR OCCURRED.**

Every technique surveyed in this chapter — from a simple Z-score to a Transformer-based sequence model — does exactly one job: flag that something deviates from expectation, with as much precision, context, and honesty about uncertainty as the method allows. None of them, however sophisticated, answer *why*. That boundary is not a limitation to be engineered away in some future version of this chapter's methods — it's the correct, permanent division of labor between evidence generation (this chapter) and evidence-weighed reasoning (Chapter 7), and the entire architecture of this project depends on respecting it.

---

# Bridge to Phase 7 — Elevator-Specific AI, Generative AI, RAG, Multi-Agent Reasoning & Explainable AI

Phases 5 and 6 together have now established:

```
ENGINEERING KNOWLEDGE + RCA METHODS + FAULT TREES + CAUSAL REASONING
+ TIME-SERIES EVIDENCE + ANOMALY DETECTION + ALARM CORRELATION
```

Every conceptual piece this project's diagnostic reasoning needs now exists — as engineering knowledge and mathematical methodology, not yet as software. The question that remains is the one this whole research book has been building toward: **how can AI systems actually use all of this structured evidence and engineering knowledge to perform scalable, real-time diagnostic reasoning?**

```
ENGINEERING KNOWLEDGE + TELEMETRY + EVENTS + ALARMS + ANOMALIES + HISTORICAL DATA
        ↓
AI REASONING
        ↓
EVIDENCE-GROUNDED DIAGNOSIS
```

Phase 7 must therefore study elevator-specific AI research (vibration diagnosis, door classification, acoustic monitoring, IoT analytics, digital twins, physics-informed neural networks, graph neural networks, few-shot learning, transfer learning, remaining-useful-life prediction, sensor fusion), LLMs for industrial RCA specifically (structured outputs, tool calling, ReAct, planning, reflection, verification), retrieval-augmented generation (embeddings, vector databases, hybrid retrieval, reranking, maintenance-document retrieval), multi-agent architectures, and explainability/evidence provenance.

Phase 7 content is not generated here — this document ends at the close of Phase 6.
