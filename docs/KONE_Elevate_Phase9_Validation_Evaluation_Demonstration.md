# PHASE 9 — VALIDATION, EVALUATION, FAULT SCENARIOS, DEMONSTRATION & EVIDENCE OF VALUE

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

Labels: **[PROJECT SOURCE]**, **[ACADEMIC EVIDENCE]**, **[OFFICIAL STANDARD]**, **[INDUSTRY EVIDENCE]**, **[MODEL KNOWLEDGE]** (established evaluation, statistics, and ML-benchmarking methodology — the label for most of this chapter, none of it elevator- or KONE-specific), **[ENGINEERING INFERENCE]**, **[PROPOSED VALIDATION METHOD]** (this project's own design, not a claim about what's already been executed), **[NOT ESTABLISHED]**. This chapter's own central discipline, stated once and then simply practiced throughout: **no invented threshold, sample size, or percentage-improvement figure appears anywhere below without an explicit basis** — where this book cannot cite one, it says so.

**The central question of this chapter:** *how can we rigorously demonstrate that an evidence-driven elevator fault-isolation and root-cause-analysis system actually works, rather than merely producing convincing-looking AI responses?*

```
SCENARIO → GROUND TRUTH → OBSERVED DATA → SYSTEM ANALYSIS → FAULT ISOLATION
   → ROOT-CAUSE RANKING → EVIDENCE TRACE → CONFIDENCE → HUMAN REVIEW
   → REFERENCE OUTCOME → COMPARISON → METRICS → ERROR ANALYSIS → IMPROVEMENT
```

---

## From Phase 8 to Phase 9

A system can be architecturally elegant, secure, and safety-aware — everything Phase 8 established — and still fail to demonstrate actual diagnostic value. **Architecture ≠ validation. AI sophistication ≠ diagnostic correctness. A convincing explanation ≠ a correct root cause.** Every one of the preceding eight phases built the capability to reason well; this phase exists specifically to answer whether that reasoning is actually, measurably, defensibly correct — and where, honestly, it is not.

---

# Part I — Defining "Works"

## 11.1 What Does "Works" Mean?

Eleven genuinely distinct questions, none of which collapse into a single accuracy number:

- **Detection** — did the system notice something abnormal?
- **Fault classification** — did it identify the correct fault category?
- **Fault isolation** — did it identify the correct subsystem?
- **Root-cause identification** — did it identify the actual, or most plausible, underlying cause?
- **Evidence correctness** — did it use the correct evidence?
- **Temporal correctness** — did it interpret chronology correctly?
- **Retrieval correctness** — did it retrieve relevant documentation?
- **Explanation correctness** — did it accurately explain its own conclusion?
- **Confidence quality** — was its stated confidence appropriate to the actual evidence strength?
- **Abstention quality** — did it recognize when evidence was insufficient?
- **Technician usefulness** — did it actually help the human investigator?

> **KEY CONCEPT:** A system that gets the root cause right for the wrong reason, or with unsupported evidence, or with unjustified confidence, has not "worked" in the sense this project needs — every one of the eleven dimensions above can fail independently of the others, which is precisely why this chapter refuses to report one number.

## 11.2 The Validation Hierarchy

```
DATA VALIDATION
     ↓
SIGNAL VALIDATION
     ↓
EVENT / ALARM VALIDATION
     ↓
ANOMALY VALIDATION
     ↓
FAULT ISOLATION VALIDATION
     ↓
RCA VALIDATION
     ↓
EXPLANATION VALIDATION
     ↓
HUMAN-USABILITY VALIDATION
     ↓
SYSTEM-LEVEL VALIDATION
```

Each layer's failure invalidates confidence in every layer above it — a perfectly-scoring RCA layer built on corrupted data validation has validated nothing real. This is the same dependency-chain logic Chapter 9 §9.45's architecture diagram already established, now read as a validation order rather than a data-flow order.

## 11.3 Ground Truth

**What is ground truth, precisely:** the actual, correct answer a system's output is compared against. For this project, potential sources include a confirmed maintenance outcome (a technician's completed repair, verified to have resolved the issue), a technician's own diagnosis (whether or not independently confirmed), a controlled engineering test, a deliberately injected known fault, a verified historical incident, manufacturer documentation, or expert consensus among domain specialists.

**Three tiers, distinguished precisely, because they carry very different evidentiary weight:**

- **True ground truth** — the actual, physically-confirmed cause, established beyond reasonable doubt (e.g., a controlled fault-injection test where the injected fault is known by construction).
- **Expert-labeled reference** — a domain expert's best judgment given the available evidence, treated as a working reference but not infallible.
- **Inferred ground truth** — reconstructed after the fact from incomplete records (e.g., "the repair log says the brake was replaced, so the root cause was presumably brake-related") — the weakest tier, since the repair may have addressed a symptom rather than confirmed the true cause (Ch.5 §5.16's exact caution about repeat faults applies directly here).

**Why RCA validation is genuinely difficult:** in a great many real maintenance records, the *actual* root cause was never rigorously confirmed — a technician fixed the presenting problem and moved on, without a controlled test proving that specific component was the singular cause. This isn't a flaw unique to this project's validation plan; it's a structural feature of real-world maintenance data that any RCA system's evaluation has to reckon with honestly.

## 11.4 Ground-Truth Quality

| Ground-Truth Source | Reliability | Advantage | Limitation |
|---|---|---|---|
| Technician notes | Moderate | Real-world, practically grounded | Subjective, inconsistent detail, may reflect symptom-fixing rather than confirmed cause |
| Repair records | Moderate | Documents the action actually taken | Doesn't confirm the action was the *correct* one (Ch.5 §5.16) |
| Controlled test | High | Cause is known by design | Expensive, limited coverage, may not reflect field conditions |
| Fault injection (real or simulated) | High (for the injected condition specifically) | Exact, known ground truth | Injected faults may not perfectly represent naturally-occurring ones |
| Historical incident (fully reconstructed) | Variable | Real-world relevance | Depends entirely on how well the incident was documented at the time |
| Expert panel | Moderate–high | Draws on real diagnostic experience | Subject to inter-rater disagreement (§11.26); reflects judgment, not certainty |
| Synthetic scenario | High (for the designed condition) | Fully known, fully controllable | Not a claim about real-world representativeness (§11.25) |

**A benchmark is only as trustworthy as its labels.** No metric computed later in this chapter is more reliable than the ground-truth tier it was measured against — a headline "95% accuracy" figure against weak, inferred ground truth is a materially weaker claim than the same number against a controlled test, and this chapter insists on naming which tier backs every number reported.

---

# Part II — The Fault Scenario Library

## 11.5 Scenario Library Structure

Every scenario in this library, organized by subsystem, records: the fault, its failure mechanism, observable symptoms, expected alarms, telemetry changes, temporal behavior, possible secondary alarms, candidate root causes, discriminating evidence, negative evidence, the expected maintenance investigation, and a stated validation difficulty. **This formalizes and consolidates scenario content already built across Chapters 2, 4, and 7 of this book** — rather than re-deriving new scenarios from scratch, this section organizes the project's existing evidence base into the validation-ready format this chapter needs.

## 11.6 Motor, Drive, and Brake Scenarios

| Subsystem | Fault | Mechanism | Key Symptoms/Alarms | Discriminating Evidence | Negative Evidence | Validation Difficulty |
|---|---|---|---|---|---|---|
| Motor | Abnormal current (mechanical) | Obstruction/brake drag/load raises torque demand (Ch.1 §1.5, Ch.2 §2.5) | Overcurrent alarm, correlated vibration | Motion/brake-timing correlation; clean drive self-test | No drive-temperature anomaly | Moderate — 9 overlapping candidate causes (Ch.2 §2.5, Ch.7 §7.7.1) |
| Motor | Thermal degradation | Progressive winding insulation breakdown | Gradual temperature trend, eventual overcurrent | Temperature trend independent of duty cycle | Phase currents remain balanced until late-stage | **High** — gradual onset, easily confused with duty-cycle-driven heating |
| Motor | Electrical (winding) fault | Insulation breakdown, partial short | Phase-current imbalance | Imbalance present even at light/no load | — | Moderate |
| Drive | Overcurrent (drive-attributable) | IGBT/inverter fault | Drive fault code, drive-temperature spike | Failed drive self-test | Clean self-test if the cause is actually mechanical | Moderate — the drive-side/motor-side boundary is the classic confusion pair (§11.13) |
| Drive | Overtemperature | Cooling/ventilation issue, or genuine drive fault | Drive temperature alarm | Correlation with machine-room temperature (Ch.3 §3.5-E) | — | Moderate — environmental context required |
| Drive | Communication issue | Bus/wiring fault between drive and controller | Intermittent/erratic drive data | Comm-error counters | — | **High** — overlaps with genuine drive faults in symptom presentation |
| Brake | Brake drag | Incomplete release (wear, misadjustment, coil issue) | Overcurrent correlated with brake-release timing | Tight correlation across multiple trips | No correlation if cause is elsewhere | Moderate — the canonical mechanical-looks-electrical case (Ch.3 §3.2) |
| Brake | Timing anomaly | Release/engage delay | Leveling deviation, position drift while held | Brake-timing sensor deviation | — | Moderate |

## 11.7 Door, Encoder/Position, and Sensor-Failure Scenarios

| Subsystem | Fault | Mechanism | Key Symptoms/Alarms | Discriminating Evidence | Negative Evidence | Validation Difficulty |
|---|---|---|---|---|---|---|
| Door | Genuine obstruction | Physical blockage | Door-close timeout, single repeatable event | Consistent physical location | Clears when removed | Low |
| Door | Photo-eye degradation | Alignment/lens drift | Repeated reopening, no visible cause | Multi-cycle instability, no consistent location | — | **High** — the canonical ambiguity with genuine obstruction (Ch.4 §4.9), resolvable only across many cycles |
| Door | Mechanical resistance (roller/track) | Wear, debris | Slow/noisy movement, elevated current | Elevated current + longer cycle time | — | Low–moderate |
| Encoder/Position | Encoder signal degradation | Contamination, connector wear | Leveling deviation, rough motion | Disagreement with an *independent* leveling sensor | Independent sensor also drifts *together* with encoder → suggests real motion instead (Ch.7 §7.34) | **High** — requires an independent cross-check to resolve at all |
| Encoder/Position | Intermittent position loss | Marginal connector | Brief, self-resolving deviations | Historical/event-log pattern only (Ch.4 §4.13) | Absent during any single inspection | **Very high** — the canonical intermittent-fault case |
| Sensor | Stuck value | Sensor frozen | Identical repeated readings | Zero variance over a period where variance is physically expected | — | Moderate — easy to miss if only checking for out-of-range values |
| Sensor | Drift | Calibration degradation | Gradual disagreement with an independent reference | Divergence from a cross-check signal | — | High — resembles genuine gradual equipment degradation |
| Sensor | Noisy | Electrical interference | Erratic, high-variance readings | Statistical noise-floor check | — | Moderate |
| Sensor | Impossible value | Corruption/spoofing | Out-of-physical-range reading | Simple range check | — | Low, if range-checked at ingestion |

**Why sensor-failure scenarios are critical, restated one final time in this chapter's own words:** an observed anomaly is not automatically an equipment failure — it may be the sensor itself. **The RCA system must detect sensor-quality problems before attributing them to the equipment**, exactly the discipline Chapter 6 §8.5 and Chapter 7 §7.26 established and this validation library now tests directly.

## 11.8 Communication Scenarios

Intermittent communication, packet/data loss, controller communication issues, and gateway outages each produce a distinctive signature — sudden, often widespread data gaps rather than a plausible physical degradation pattern in any one signal — that the system should learn to distinguish from a genuine equipment fault (Ch.4 §4.7-F). **Validation difficulty: high** — a communication fault's symptom (missing/erratic data) can, in the worst case, resemble several different equipment-fault symptoms simultaneously, which is exactly why this category deserves its own dedicated test cases rather than being folded into "missing data" generically.

## 11.9 Multiple-Simultaneous-Fault and Cascade Scenarios

**Real systems may genuinely experience more than one fault at once** — door degradation *and* independent sensor degradation; a brake issue *and* an unrelated encoder anomaly. **Single-label classification fails here by construction**, since it forces the system to pick one answer when two independent, correct answers exist. Validated instead via multi-label diagnosis (does the system correctly retain and report more than one live hypothesis space, Ch.7 §7.28), hypothesis ranking (does each fault get appropriately ranked within its own evidence set, not blended with the other's), causal-graph reasoning (does the system correctly *not* connect two genuinely unrelated faults just because they're temporally close, Ch.6 §8.20), and evidence separation (is evidence correctly attributed to the fault it actually supports).

**Fault cascade scenarios**, formalizing Chapter 4 §4.6 and Chapter 6 §8.36's worked examples into test cases: `ROOT FAULT → PRIMARY SYMPTOM → CONTROLLER RESPONSE → SECONDARY EVENTS → ALARMS → DOWNSTREAM EFFECTS`. **Validation must distinguish root cause from consequential symptoms** — a system that correctly identifies "motor overcurrent" as the initiating event in a five-alarm cascade, but also correctly explains the other four as consequences rather than independent problems, should score fully; a system that treats all five as independent should not, even if its identification of the true root cause happens to be technically present somewhere in its output.

## 11.10 Primary vs. Consequential Alarm Validation

Using alarm-flood scenarios where one underlying fault produces several alarms (Ch.6 §8.16): **define a specific metric for this capability** — the fraction of cascade scenarios where the system correctly identifies the true primary event *and* correctly classifies every consequential alarm as such, distinct from a metric that only checks whether the root cause appears somewhere in the output. **A system can get the root cause "right" while still failing this specific capability**, if it fails to correctly explain which of the other alarms were consequences of it — which is exactly why this metric needs to exist as its own line item, not be assumed to follow automatically from RCA accuracy.

## 11.11 Intermittent Faults and Temporal Validation

**Intermittent faults are difficult** because of rare occurrence, partial evidence at any given moment, inconsistent signatures across occurrences, and the long time windows required to see the pattern at all (Ch.4 §4.13, Ch.6 §8.38's own worked example). Validation scenarios for this category should specifically test whether the system can reconstruct a pattern from historical, scattered evidence — not just from a single, present-moment snapshot.

**Temporal validation**, concretely: given a sequence like sensor anomaly at T0 → alarm at T1 → system trip at T2 → maintenance action at T3, **the system should never infer that T2 caused T0** — a validation test explicitly checks that the system's stated causal chain respects chronological ordering (Ch.4 §4.12, Ch.7 §7.13) and doesn't accidentally reverse it under complex, multi-event evidence.

---

# Part III — Metrics, Layer by Layer

## 11.12 Signal-Level and Anomaly Detection Metrics

*[MODEL KNOWLEDGE]* Validating Chapter 6's outputs specifically: anomaly detection precision, recall, false positive rate, false negative rate, detection latency, changepoint accuracy, and event-alignment accuracy.

A confusion matrix, for a binary "anomalous or not" decision:

| | Predicted Anomalous | Predicted Normal |
|---|---|---|
| **Actually Anomalous** | True Positive (TP) | False Negative (FN) |
| **Actually Normal** | False Positive (FP) | True Negative (TN) |

**Precision** = TP / (TP + FP) — of everything flagged, how much was genuinely anomalous. **Recall (Sensitivity)** = TP / (TP + FN) — of everything genuinely anomalous, how much was caught. **Specificity** = TN / (TN + FP) — of everything genuinely normal, how much was correctly left alone. **F1** = the harmonic mean of precision and recall, useful when both matter roughly equally. **False Positive Rate** = FP / (FP + TN); **False Negative Rate** = FN / (FN + TP).

**When each matters, per Chapter 6 §8.34's own trade-off:** high recall matters most when missing a real fault (a false negative) is the more costly error; high precision matters most when unnecessary technician dispatches (false positives) are the dominant cost. **Accuracy alone is not assumed sufficient** — on an imbalanced dataset (faults are, per Chapter 6 §8.42, rare), a model that simply predicts "normal" every time can score deceptively high accuracy while catching zero real faults, which is precisely why this chapter insists on the full confusion-matrix breakdown rather than one aggregate number.

## 11.13 Fault Classification and Fault Isolation Metrics

**Fault classification** (assigning the correct fault category, Ch.4 §4.7's taxonomy): accuracy, macro-F1 (averaging F1 across classes equally, regardless of how common each class is — important given real class imbalance), weighted-F1 (weighting by class frequency), precision/recall per class, and a full confusion matrix — **class imbalance matters directly here**, since rare fault types can be nearly invisible in an aggregate accuracy score while dominating a macro-F1 score, giving a materially different, more honest picture of performance on the cases that matter most.

**Fault isolation** (identifying the correct subsystem, Ch.4 §4.15's search-space-reducer framing, now made measurable): **Top-1 subsystem accuracy** (the system's single best guess is correct); **Top-3 subsystem accuracy** (the correct subsystem appears among the top three ranked candidates); **Top-k accuracy** generally. **Why top-k specifically matters for a diagnostic system, distinct from a typical classification benchmark:** this project's own design (Ch.7 §7.16) deliberately retains multiple live hypotheses rather than forcing a single answer — a system that ranks the true subsystem 2nd, with the true leader only narrowly ahead and both explicitly presented to the technician, has arguably still provided real diagnostic value, which Top-1 accuracy alone would fail to credit.

## 11.14 RCA Metrics

RCA is measurably harder than classification, and its metrics reflect that: **root-cause Top-1 and Top-k accuracy** (as above, applied to the specific cause, not just the subsystem); **causal-chain correctness** (did the system correctly identify the primary/consequential structure, §11.10, not just the ultimate cause); **hypothesis-ranking quality** (did the relative ordering of *all* candidate hypotheses make sense given the evidence, not just whether the top one was correct); and **alternative-cause-elimination accuracy** (did the system correctly rule out hypotheses that were genuinely inconsistent with the evidence, per Chapter 7 §7.25's procedure — a system that happens to rank the right cause first while failing to actually eliminate an inconsistent alternative has gotten the right answer for an incomplete reason, which this metric is specifically designed to catch).

## 11.15 Evidence and Retrieval Metrics

**Evidence metrics**, testing something classification/RCA-accuracy metrics alone cannot: **evidence relevance** (was the cited evidence actually pertinent), **evidence completeness** (was anything important left out), **evidence correctness** (was the cited evidence itself accurate — Ch.6 §8.5's quality checks, now applied to what the system *reported using*, not just what it had access to), **evidence attribution** (was each specific evidence claim correctly linked to its specific source), and **source provenance** (Ch.9 §9.18's claim→evidence→source→timestamp chain, tested directly). **A correct answer supported by incorrect or fabricated evidence is still a serious diagnostic failure** — this project's entire differentiation rests on auditability (Ch.6 §6.10), and an unauditable-but-correct answer doesn't deliver that differentiated value even when it happens to be right.

**Retrieval metrics** *[MODEL KNOWLEDGE — standard information-retrieval evaluation]*, for Chapter 9 §9.17's RAG pipeline specifically: **Precision@k** (of the top k retrieved documents, how many are genuinely relevant); **Recall@k** (of all genuinely relevant documents, how many appear in the top k); **MRR** (Mean Reciprocal Rank — how high, on average, the first genuinely relevant result ranks); **NDCG** (Normalized Discounted Cumulative Gain — rewards relevant results appearing earlier, weighted by graded relevance rather than a simple yes/no); and **context relevance** (of what actually reaches the LLM's context window, how much is useful). **Applied to maintenance RAG specifically:** a fault-code lookup query (better served by exact/keyword matching) and a conceptual query like "excessive motor torque" (better served by semantic retrieval) should be evaluated separately, since Chapter 9 §9.17's hybrid-retrieval design exists precisely because these two query types have different retrieval-quality profiles.

## 11.16 RAG Answer Faithfulness

Distinguishing retrieval quality (§11.15) from what the LLM actually *does* with what was retrieved: **citation correctness** (does a cited source actually say what the system claims it says), **groundedness** (is every substantive claim traceable to retrieved content, not the model's unaided memory — Ch.9 §9.11's central principle, tested directly), **unsupported claims** (content presented as fact with no corresponding retrieved evidence), and **hallucination rate** overall.

```
Claim → Retrieved evidence → Supported?
```

Every generated claim, checked against this three-step chain — a claim with no corresponding step-two evidence, or evidence that doesn't actually support the specific claim made, should be scored as unfaithful regardless of whether the claim happens to be true.

## 11.17 Explanation Metrics

Potential criteria for evaluating explanations directly: **factual correctness** (does the explanation's content match the actual evidence), **evidence consistency** (does the explanation's narrative match the structured evidence trace it's supposedly summarizing), **completeness** (does it cover the material evidence, not cherry-pick a subset), **source attribution** (§11.15), **causal consistency** (does the explained mechanism actually match Chapter 7 §7.13's causal-graph relationships, or does it assert an implausible mechanism), and **technician usefulness** (§11.20). **Human-readable is not assumed to mean technically correct** — a fluent, well-structured, entirely plausible-sounding explanation can still misrepresent the underlying evidence, and this project's own explainability design (Ch.9 §9.28) exists precisely to make that misrepresentation checkable rather than trusting fluency as a proxy for accuracy.

## 11.18 Confidence Calibration

*[MODEL KNOWLEDGE]* Continuing Chapter 9 §9.29: **if the system reports 90% confidence, approximately 90% of comparably-confident predictions should turn out correct**, under a properly designed calibration evaluation.

- **Reliability diagram** — plots predicted confidence against observed accuracy across confidence bins; a perfectly calibrated system falls exactly on the diagonal.
- **Brier score** — the mean squared difference between predicted probability and the actual outcome (0 or 1); lower is better calibrated.
- **Expected Calibration Error (ECE)** — a weighted average of the gap between confidence and observed accuracy across bins, condensing a reliability diagram into a single comparable number.

**Why confidence without calibration is dangerous:** an uncalibrated "90% confidence" that's actually correct only 60% of the time is worse than useless — it's actively misleading, encouraging exactly the human-overtrust risk (§11.38) this whole book has repeatedly flagged as its least architecturally-solvable risk (Ch.10 §10.31). Calibration testing is what turns "the system reports a number" into "the number means something."

## 11.19 Abstention Metrics

*[MODEL KNOWLEDGE — "selective prediction" is the standard ML term for this capability]* **Coverage** — the fraction of cases the system chooses to answer rather than abstain on. **Selective accuracy** — accuracy measured only on the covered (answered) cases. **Risk-coverage curve** — plots how error rate changes as the coverage threshold is relaxed (allowing the system to answer more cases, including lower-confidence ones). **Abstention rate** — the complement of coverage.

**The core expectation this project's own design (Ch.9 §9.31) should be tested against:** selective accuracy, on the cases the system chooses to answer, should be meaningfully *higher* than accuracy would be if the system were forced to answer every case — if abstention isn't actually improving accuracy on the covered subset, the abstention mechanism itself isn't working as designed, regardless of how principled it sounds in the architecture documentation.

## 11.20 Human-in-the-Loop Metrics

**Technician agreement** (does the technician's independent judgment match the system's leading hypothesis), **override rate** (how often a technician overrides the system's conclusion), **time to diagnosis**, **time to first useful hypothesis**, **number of diagnostic steps taken**, **unnecessary inspections avoided (or caused)**, **cognitive workload**, and **perceived usefulness** — **human performance is part of system validation**, not a separate concern, because this project's entire value proposition (Ch.9 §9.44's "human" column) is about augmenting a human process, not replacing it — a system that's technically accurate but makes the human's job harder or slower has not delivered on its actual design goal.

**Time-to-diagnosis, specifically:** compare T_baseline (unassisted) against T_AI-assisted. **Time saved does not automatically mean better diagnosis** — a faster wrong answer is worse than a slower right one — so this metric is only meaningful evaluated jointly with correctness (§11.13–§11.14), never reported alone.

**Technician effort**, additionally: number of data sources consulted, number of hypotheses manually evaluated, unnecessary site visits, and repeat visits. **No expected-improvement percentage is invented here** — real figures require real deployment data this project does not have.

## 11.21 Maintenance Value Metrics

Potential outcomes: faster diagnosis, fewer repeat visits, improved first-time-fix potential, better parts preparation, reduced diagnostic effort, and improved documentation quality. **Potential value is clearly distinguished from demonstrated value throughout this chapter** — every metric in this list remains a hypothesis to test (§11.43), not a claim already substantiated by this project's current, prototype-stage evidence.

---

# Part IV — Baselines and Ablation

## 11.22 Baseline Comparison

**Ablation and baseline comparisons are essential** because a headline accuracy number, alone, says nothing about whether this project's specific architectural choices (Ch.7–9) actually earned their complexity (Ch.9 §9.21's own caution, now given a concrete test methodology).

| Baseline | Description | What It Tests |
|---|---|---|
| **1 — Simple alarm lookup** | Fault code → predefined text, no reasoning | The floor: what a system with zero evidence-weighing achieves |
| **2 — Rule-based diagnostic logic** | Hand-written `IF alarm THEN candidate causes` rules | Whether structured reasoning beats simple rules at all |
| **3 — Classical ML classifier** | A trained model (Ch.6/Ch.9 Part II methods) with no RAG, no multi-agent structure | Whether the AI layer specifically adds value beyond conventional ML |
| **4 — LLM without RAG** | An LLM reasoning from its own training knowledge alone | Whether grounding in retrieved evidence (§11.16) actually matters |
| **5 — LLM + RAG (single agent)** | The retrieval-grounded version, without multi-agent structure | Whether multi-agent architecture (§11.23) earns its added complexity |
| **Proposed architecture** | The full evidence-driven, multi-agent RCA design | The complete system, measured against every baseline above |

## 11.23 Ablation Studies

**Component ablation** — removing one piece at a time from the full system and measuring the change: without alarm correlation, without maintenance history, without RAG, without the fault tree, without probabilistic (Bayesian) reasoning, without sensor fusion, without temporal reasoning. **What each experiment tells us:** a large performance drop when a component is removed is direct evidence that component earns its place in the architecture; a negligible drop suggests it may be adding complexity (and, per Chapter 9 §9.21, cost/latency/attack-surface) without commensurate value.

**LLM ablation, specifically:** No LLM → LLM only → LLM + RAG → LLM + tools → LLM + RAG + tools → LLM + the full structured RCA engine — **isolating which specific diagnostic tasks actually benefit from an LLM at all**, directly testing Chapter 9 §9.1's own task-by-task justification rather than assuming the LLM helps everywhere it's used.

**Multi-agent ablation:** single agent vs. multi-agent, measured on accuracy, latency, cost, error rate, inter-agent disagreement frequency, and debugging complexity — **multi-agent architecture must earn its complexity through this specific comparison**, not be assumed superior by default (Ch.9 §9.24's HALLUCINATION WARNING, now given a concrete test).

**Evidence ablation:** alarm-only → alarm + telemetry → alarm + telemetry + maintenance history → alarm + telemetry + engineering knowledge → the full evidence package — directly measuring the "stronger evidence set" claim Chapter 6 §8.30 and Chapter 7 throughout make conceptually, now as a testable, graduated experiment.

---

# Part V — Data for Validation

## 11.24 The Data-Scarcity Problem, Revisited

Because real, labeled elevator fault data is scarce (a finding independently confirmed across Chapter 9's real academic literature, not just this project's own assumption), **evaluating the system responsibly requires deliberately combining several imperfect sources — synthetic data, simulated faults, expert-authored scenarios, historical records, controlled experiments, and public research data — while never treating any of them as equivalent to each other.**

## 11.25 Synthetic Data: Construction and Limitations

**Constructing a conceptually realistic scenario** requires preserving physical plausibility (Ch.1's engineering constraints), temporal relationships (Ch.6's signal-timing behavior), sensor relationships (Ch.6 §8.30's correlated-evidence structure), alarm cascades (Ch.4 §4.6's patterns), and genuine fault mechanisms (Ch.7's fault trees) — **this book provides no instructions for physically inducing a real elevator fault**; every scenario in this chapter's library is a data/simulation construct, never a real-world test procedure.

**Limitations, stated as plainly as everywhere else in this book:** simulator bias (a simulation reflects its builder's assumptions), unrealistically clean noise characteristics, missing real-world correlations a physical system would actually exhibit, unrealistic fault signatures if the underlying physics model is subtly wrong, overly clean data generally, and the real risk of a model overfitting to the specific patterns of the simulation rather than learning genuinely generalizable diagnostic reasoning. **Synthetic validation ≠ production validation — restated, again, because it is the single most repeated caution in this entire research book, and this chapter is where that repetition matters most.**

## 11.26 Expert-Labeled Data and Inter-Rater Agreement

Domain experts can label scenarios with a primary fault, secondary consequences, affected subsystem, failure mode, root cause, supporting evidence, and their own confidence — but **when multiple experts label the same case, do they actually agree?** *[MODEL KNOWLEDGE]* **Cohen's kappa** (for two raters) and **Fleiss' kappa** (for more than two) measure agreement beyond what chance alone would produce. **Why disagreement is informative, not just noise:** genuine expert disagreement on a case can reveal real diagnostic ambiguity in that scenario itself — evidence the case is a hard one, worth flagging explicitly, rather than a labeling error to be resolved by picking whichever expert spoke first.

## 11.27 Benchmark Dataset Design

A conceptual KONE Elevate RCA benchmark case should contain: **Case ID**, asset configuration, operating state, time window, telemetry, events, alarms, maintenance history, relevant documentation, known/estimated fault, root cause, secondary consequences, evidence, and expected diagnostic-reasoning artifacts (the hypothesis space a well-reasoned investigation of this case should generate). **This is, in effect, Chapter 7 §7.38's investigation-state data model, populated with a known answer rather than an in-progress one** — the natural target format for every scenario built in Part II of this chapter.

## 11.28 Splitting and Generalization Testing

**Train/validation/test splitting**, done properly: random splitting, time-based splitting, asset-based splitting, and elevator-model-based splitting each test a different generalization claim. **Why random splitting can be misleadingly optimistic:** if cases from the same elevator, or the same incident, end up split across train and test, the system can appear to "generalize" while actually just recognizing a near-duplicate of something it already saw — a genuinely common and easy-to-miss evaluation error.

**Cross-asset generalization** — train on some elevators, evaluate on entirely different ones — tests whether the system's reasoning transfers beyond the specific units it was tuned on. **Cross-model generalization** — across different elevator configurations — tests robustness to the domain shift Chapter 9 §9.7/§9.32 already flagged as a real, open concern. **Temporal generalization** — train on an earlier period, test on a later one — can specifically reveal model drift (Ch.10 §10.21) that a same-period split would never surface.

**Rare-fault validation:** by definition, rare faults have few or no labeled examples — addressed through the same few-shot, transfer-learning, and physics-informed methods Chapter 9 Part II already surveyed with real academic precedent, combined with the fault-tree/probabilistic-reasoning structure that doesn't strictly require abundant labeled examples of every specific fault to function. **No overclaiming here** — rare-fault performance remains a genuinely open, actively-researched problem, not one this project claims to have solved.

---

# Part VI — Robustness and Security-Aware Testing

## 11.29 Robustness Testing

Testing the system under missing telemetry, noisy telemetry, delayed events, duplicate events, incorrect timestamps, irrelevant retrieved documents, incomplete maintenance history, and conflicting evidence — measuring **performance degradation**, not just pass/fail, since a well-designed system should degrade gracefully (Ch.10 §10.6) rather than fail catastrophically.

**Sensor-failure robustness, specifically:** does the system (1) notice the sensor problem at all, (2) reduce trust in that specific signal rather than the equipment it monitors, (3) avoid a false equipment diagnosis as a result, and (4) fall back on alternative, independent evidence where available (Ch.7 §7.34)? Each of these four is separately testable and separately meaningful — a system that notices the sensor problem but still lets it corrupt the final diagnosis has only partially succeeded.

**Missing-data robustness:** testing at multiple missing-data levels is worthwhile **only where scientifically justified by a specific research question** — this book does not assert a universal required set of test percentages (e.g., "10%/30%/50%") without a stated reason for choosing exactly those points; the right levels depend on what real-world missingness this project's actual data sources are expected to exhibit. Measured outcomes: diagnosis-quality degradation, confidence degradation, and abstention-behavior change as missingness increases.

**Conflicting-evidence testing:** constructing cases where telemetry suggests cause A, maintenance history suggests cause B, and the fault code suggests cause C — testing whether the system (a) detects the conflict explicitly, (b) does not silently pick one source over the others without justification, (c) requests additional evidence where possible, (d) reduces confidence appropriately, and (e) escalates rather than forcing a resolution (Ch.7 §7.27's exact principle, made testable).

## 11.30 Adversarial and Security-Aware Validation

Without providing any attack instructions, conceptually testing corrupted data, untrusted documents, malicious instructions embedded in retrieved text (Ch.9 §9.36), an unauthorized tool request, and inconsistent metadata — **measuring whether the security boundaries established in Chapter 10 actually prevent unsafe reasoning in practice**, not just whether they're documented as a design intent. This is the validation counterpart to Chapter 10's architecture — that chapter specified the boundary; this chapter is where the boundary gets tested against adversarial conditions rather than assumed to hold.

## 11.31 Hallucination, RAG, Tool-Calling, and Agent Validation

**Hallucination testing:** constructing test cases specifically designed to tempt the system into inventing fault codes, sensor values, documents, unsupported causes, or fabricated maintenance history — measuring hallucination rate and unsupported-claim rate directly (§11.16's framework applied as a stress test rather than passive observation).

**RAG testing:** across five conditions — the correct document is available; only a wrong document is available; multiple conflicting documents are available (Ch.10 §10.44's exact scenario); no relevant document exists at all; only an outdated document is available — measuring retrieval accuracy, source correctness, citation correctness, and, critically, **abstention behavior specifically under the "no relevant document" and "only outdated document" conditions**, where the correct system behavior is recognizing the gap, not confidently generating from unsupported memory.

**Tool-calling validation:** does the AI select the correct tool for a given evidence need, provide correct query parameters, correctly interpret the tool's returned output, handle a tool failure gracefully rather than fabricating a plausible-looking result, and avoid calling any tool outside its authorized scope (Ch.10 §10.22)?

**Agent validation:** orchestration correctness, role assignment correctness, evidence passing fidelity between agents (does information degrade across hand-offs, Ch.9 §9.23's concern, tested directly), state consistency, agent disagreement handling, and error-propagation containment (does one agent's mistake stay isolated, or cascade, Ch.9 §9.24).

## 11.32 Explainability Validation

Testing whether a generated explanation accurately reflects the observed evidence, the retrieved evidence, the actual hypothesis set considered, any genuine contradictions found, and the final ranking as computed — **a fluent explanation that misrepresents the underlying evidence must be scored as a failure**, exactly as strongly as a wrong conclusion, because this project's core value proposition (auditability, Ch.6 §6.10) depends on the explanation being a faithful representation of the reasoning, not merely a plausible-sounding narrative wrapped around it.

## 11.33 Reproducibility

**Can the same case be reconstructed?** Recording input data, timestamps, model version, prompt/configuration version, knowledge-base version, retrieved documents, tool outputs, and the final output (Ch.10 §10.37's versioning discipline, now applied specifically to re-running a past evaluation) — **reproducibility matters for validation specifically because an unreproducible result cannot be independently checked**, which undermines the entire evidentiary basis of any claim this chapter's methodology produces.

---

# Part VII — Statistical Rigor and Error Analysis

## 11.34 Statistical Validation and Sample Size

*[MODEL KNOWLEDGE]* Statistical tests are appropriate when comparing two systems' (or a system-vs-baseline's) performance and asking whether an observed difference is likely real or could plausibly be chance variation. Relevant tools, conceptually: **confidence intervals** (a range likely to contain the true performance value, not just a point estimate), **bootstrap resampling** (estimating uncertainty by resampling the available test cases), **paired comparisons** (comparing two systems on the *same* cases, which is more statistically powerful than comparing on different case sets), **significance testing**, and **effect size** (how large the difference actually is, distinct from whether it's statistically detectable at all). **This book does not blindly recommend p-values as the final word** — **practical significance matters too**: a statistically significant but practically tiny improvement may not justify the added complexity §11.23's ablation studies would reveal it costs.

**Why five impressive examples are not enough to establish general performance:** a handful of hand-picked, well-performing cases (exactly what a hackathon demo naturally selects for, §11.40) says nothing about the distribution of performance across the full range of scenarios a real system would encounter. Establishing general performance requires a real accounting of the number of scenarios tested, their diversity (across fault classes, not concentrated in one easy category), the number of independent assets represented (not all variations of one elevator), and, where feasible, repeated trials to characterize variance. **No universal required sample size is invented here** — the right number depends on the specific claim being made and the variance actually observed, not a fixed rule of thumb.

## 11.35 Error Analysis and the Error Taxonomy

**After every evaluation, accuracy alone is not the report.** The more important question is always: **what did the system get wrong, and why?**

A standardized error taxonomy, for classifying every failure encountered during evaluation:

- **E1 — Data Error** — the input data itself was wrong/corrupted before the system ever reasoned over it.
- **E2 — Signal Processing Error** — Chapter 6's feature-extraction or filtering stage introduced an error.
- **E3 — Event/Alarm Correlation Error** — alarms incorrectly merged or incorrectly kept separate.
- **E4 — Fault Detection Error** — a genuine anomaly missed, or a false one flagged.
- **E5 — Fault Isolation Error** — wrong subsystem identified.
- **E6 — Root-Cause Error** — correct subsystem, wrong specific cause.
- **E7 — Evidence Attribution Error** — evidence cited but misattributed or mischaracterized.
- **E8 — Retrieval Error** — wrong, missing, or irrelevant documentation retrieved.
- **E9 — Hallucination** — content generated with no corresponding grounded evidence.
- **E10 — Temporal Reasoning Error** — chronology misinterpreted, or causality inferred against the true event order.
- **E11 — Confidence Error** — miscalibrated confidence, in either direction.
- **E12 — Abstention Failure** — the system should have abstained and didn't, or abstained when it had sufficient evidence to conclude.
- **E13 — Human-Factor Failure** — the output was technically fine but poorly suited to actual technician use (§11.20, §11.38).
- **E14 — Security Boundary Failure** — any breach of Chapter 10's established controls, however contained.

**Why this taxonomy matters more than an aggregate score:** two systems with identical 80% accuracy can have completely different, and differently serious, error profiles — one dominated by E5/E6 (wrong diagnosis, a real diagnostic failure) and another dominated by E11/E12 (miscalibrated confidence on largely-correct diagnoses, a more fixable, less fundamentally worrying pattern). Reporting only the 80% erases this distinction entirely.

**Confusion matrices, applied to subsystem-level classification specifically, reveal *which* faults get confused with which** — motor issues vs. drive issues (the classic mechanical-looks-electrical boundary, Ch.1 §1.5); brake issues vs. general mechanical resistance; encoder issues vs. genuine leveling/traction issues. **These confusion patterns are not just error statistics — they reveal genuine engineering relationships** (Ch.3, Ch.7's fault trees), and a confusion pattern that maps cleanly onto a known, physically-justified ambiguity (e.g., brake drag vs. mechanical obstruction, both producing near-identical current signatures) is a fundamentally different, more forgivable finding than one with no such engineering explanation.

**RCA-specific error categories, kept distinct rather than collapsed into "wrong":** correct subsystem but wrong root cause; correct root cause but unsupported evidence; correct root cause but an incorrect explanation of the mechanism; correct diagnosis but unjustified (overstated) confidence. **These are different failure categories requiring different fixes** — a correct-conclusion/wrong-evidence case is an E7 problem even though it would pass a naive root-cause-accuracy check, which is exactly why the taxonomy above exists as a mandatory companion to every headline metric in this chapter.

## 11.36 Cost-Sensitive Validation

**False positives** carry real costs: unnecessary technician dispatch, unnecessary inspection, wasted time, unnecessary parts investigation, and — cumulatively — alert fatigue (a real, well-documented risk in any alarm-heavy system, Ch.6 §8.16–§8.17). **False negatives** can be more serious: missed degradation, delayed maintenance, and repeated failures — **though this book does not assign a specific safety-risk level to any false negative without supporting evidence**, since (per Chapter 10 Part I) this project's diagnostic failures have no direct path to a safety consequence; their cost is operational (missed/delayed maintenance), not safety-critical, by design.

| Prediction | Reality | Consequence |
|---|---|---|
| Fault flagged | No genuine fault (False Positive) | Unnecessary dispatch/inspection; time and trust cost |
| No fault flagged | Genuine fault present (False Negative) | Missed/delayed degradation; potential future failure |
| Fault flagged, wrong cause | Genuine fault, different cause | Wrong first repair attempt; wasted effort, possible repeat visit |
| Fault flagged, correct cause, low confidence | Genuine fault, correctly identified | Appropriately cautious — arguably a success, not a failure, if confidence is honestly calibrated |

**No arbitrary monetary values are invented for this matrix** — real cost figures require real operational data (labor rates, dispatch costs, downtime cost per hour) this project does not have and should not fabricate.

---

# Part VIII — The Human Element

## 11.37 Human vs. AI Comparison and Blind Evaluation

**A controlled conceptual comparison design:** technicians working without AI assistance versus technicians working with it, on the same (or matched) set of cases, measuring time, diagnostic correctness, stated confidence, evidence actually consulted, number of diagnostic steps taken, and reported workload. **Experimental design considerations:** matching case difficulty across the two groups (an easier case set for the AI-assisted group would bias the comparison), controlling for individual technician experience level, and — ideally — a within-subject or crossover design where the same technicians experience both conditions on different, matched cases.

**Blind evaluation:** where feasible, evaluators judging output quality should not know which system (baseline, ablated variant, or full proposed architecture) produced a given diagnosis — reducing the risk that the evaluator's own expectations bias the judgment, exactly the standard blind-review discipline used in rigorous comparative research generally.

## 11.38 Technician Usability and Automation Bias

Usability dimensions: cognitive load, output clarity, trust, explanation usefulness, actionability, and — a real, opposite-direction risk — **information overload** (an exhaustive evidence trace that's technically complete but practically overwhelming defeats its own purpose). **This book does not assume technicians will automatically trust AI output** — trust has to be earned through demonstrated reliability, not assumed from good design intent (Ch.9 §9.36's own caution, restated here).

**Automation bias**, made a major, explicit section because Chapter 10 §10.31 already named it the single least architecturally-solvable risk in this entire book: **the risk that a technician accepts an AI diagnosis simply because the AI produced it, without genuine independent review.** Mitigations: evidence visibility (showing the trace, not just the conclusion), displaying confidence honestly, surfacing alternative hypotheses explicitly rather than only the leader, showing contradicting evidence where it exists (not hiding it to present a cleaner-looking story), requiring an explicit human confirmation step (not a passive default), and communicating uncertainty plainly rather than false confidence. **None of these mitigations technically guarantee genuine review occurs** — this remains, honestly, a human-factors and process-design problem as much as an engineering one, and this chapter does not claim otherwise.

---

# Part IX — Demonstration

## 11.39 Demonstration vs. Validation

**A demo shows: "here is one case where it works." Validation asks: "how consistently does it work across representative cases?"** **A hackathon demo is not equivalent to production validation** — this distinction, already established throughout this book, is the organizing principle for everything that follows in this Part: a demonstration is legitimate and valuable for what it actually is (a concrete illustration of the reasoning working), and illegitimate the moment it's presented as if it were the validation this chapter has spent eight Parts defining properly.

## 11.40 Hackathon Demonstration Strategy and Case Selection

A technically credible live demonstration structure:

```
CASE → RAW TELEMETRY/EVENTS → ANOMALY → ALARM CORRELATION
   → EVIDENCE PACKAGE → RAG RETRIEVAL → HYPOTHESIS GENERATION
   → RCA → ALTERNATIVE CAUSES → CONFIDENCE → EXPLANATION
   → TECHNICIAN RECOMMENDATION
```

**What judges should actually see:** every stage of this pipeline made visible, not just the final answer — the whole point of demonstrating an *evidence-driven, auditable* system is showing the audit trail live, not asserting it exists.

**Case selection — 3 to 5 representative cases, chosen for capability coverage, not just polish:**

- **Case 1 — Motor overcurrent.** Demonstrates the flagship differential-diagnosis capability (Ch.2 §2.5, Ch.7 §7.15).
- **Case 2 — Door degradation.** Demonstrates gradual-drift detection and the photo-eye/obstruction ambiguity resolved via pattern (Ch.4 §4.9, Ch.6 §8.37).
- **Case 3 — Encoder/position anomaly.** Demonstrates the independent-sensor cross-check pattern (Ch.7 §7.34).
- **Case 4 — Alarm cascade.** Demonstrates primary/consequential reasoning (Ch.4 §4.5–§4.6, §11.10).
- **Case 5 — Insufficient/conflicting evidence.** **The most important case in the set.** Demonstrates that the system can, and does, abstain — direct, live proof of the single design principle this entire book returns to more than any other.

## 11.41 Demo Case Design

For each of the five cases: scenario description, input data, expected signals, expected alarms, the intended root cause, secondary effects, the specific evidence that should discriminate it, the expected AI output, expected confidence behavior, the expected explanation content, and the expected human-verification step. **Every value used is hypothetical/synthetic, clearly labeled as such** — consistent with every other worked example in this book, no case here is presented as real production KONE data.

**The failure case (Case 5), specifically:** the expected output is something like *"insufficient evidence to distinguish between [hypothesis A] and [hypothesis B] — recommend further inspection of [specific evidence gap]"* — **this demonstrates safety and epistemic humility live**, in front of the exact audience most likely to test whether this project's abstention claims are real or merely stated.

## 11.42 Demo Observability, Timeline, and Failure Recovery

**What the audience should be able to observe, explicitly avoiding any "AI thinks..." framing** (consistent with Chapter 9 §9.28's rejection of hidden-reasoning narration): show the actual evidence, its source, the hypothesis under consideration, the confidence score, the alternative hypotheses still live, and the final conclusion — the structured trace, presented directly, not narrated as an opaque internal process.

**A conceptual 5–10 minute timeline:** introduction and problem statement, the incident as it would arrive, the evidence-gathering stage, the AI investigation running live, the RCA output, the explanation, the technician's decision point, and the result — **kept simple enough to actually deliver in the time available**, not overcomplicated with every architectural detail this book has built.

**Demo failure recovery:** if RAG fails, telemetry is missing, the model fails, or an API is unavailable during the live demonstration, **the demo itself should exhibit the same graceful-degradation behavior Chapter 10 §10.6 specifies for the real system** — a live failure that visibly triggers appropriate abstention or a clear fallback message is, in an important sense, a *better* demonstration of this project's design philosophy than a demo that never encounters a hiccup at all.

---

# Part X — Value and Claims

## 11.43 Evidence of Value and Value Hypotheses

Measurable value dimensions, kept as **hypotheses to test**, not claims already substantiated: diagnostic speed, diagnostic accuracy, fault-isolation quality, first-time-fix potential, technician effort reduction, evidence traceability, repeat-visit reduction potential, and maintenance-planning quality.

- **H1** — Evidence correlation reduces diagnostic time.
- **H2** — Primary/consequential alarm separation improves fault-isolation accuracy.
- **H3** — Engineering-knowledge retrieval reduces unsupported conclusions.
- **H4** — Structured RCA improves explanation quality (relative to an unstructured LLM baseline, §11.22).
- **H5** — Confidence/abstention reduces overconfident incorrect diagnoses.

**Every one of these is stated as an H, deliberately** — a hypothesis this project's methodology (Parts III–VII of this chapter) is equipped to actually test, not a marketing claim awaiting confirmation after the fact.

**Baseline business metrics worth eventually measuring:** Mean Time to Diagnose, Mean Time to Repair, repeat-visit rate, first-time-fix rate, unnecessary dispatches, and diagnostic effort — **no KONE baseline values are fabricated here**; real baselines require real KONE operational data this project does not currently have.

## 11.44 Technical Success Criteria and Validation Gates

A success-criteria framework, organized by category (diagnostic correctness, evidence correctness, retrieval correctness, explanation correctness, confidence calibration, abstention behavior, latency, reliability) — **with no arbitrary threshold values invented for any of them.** Real thresholds should be established from the specific use case, an actual baseline, the real cost of different error types (§11.36), the specific dataset available, and expert expectations grounded in real maintenance practice — not asserted in a research book with no access to any of those inputs.

**Validation gates**, sequenced so that failure at an earlier gate should prevent overclaiming capability at a later one:

```
GATE 1   Data quality passes
GATE 2   Signal processing passes
GATE 3   Fault detection passes
GATE 4   Fault isolation passes
GATE 5   RCA passes
GATE 6   Evidence grounding passes
GATE 7   Confidence/abstention passes
GATE 8   Human usability passes
GATE 9   Security/safety validation passes
GATE 10  Pilot readiness
```

**Why this ordering matters:** a system that fails Gate 1 (data quality) has no business claiming strong Gate 5 (RCA) performance, even if its RCA logic tests well on clean synthetic inputs — every downstream gate's validity is conditional on every upstream gate having genuinely passed, mirroring §11.2's validation hierarchy exactly.

## 11.45 MVP Validation: What the Prototype Can and Cannot Claim

**What can realistically be validated in a hackathon prototype:** 3–5 carefully designed fault scenarios (§11.40's case set, or similar), structured synthetic/historical evidence, alarm correlation, RCA reasoning, RAG, explanation quality, confidence behavior, and abstention — **all achievable, all genuinely demonstrable, at this project's current scale.**

**A defensible claim the prototype can actually make:**

> *"The prototype demonstrates the feasibility of evidence-driven fault isolation and RCA on representative scenarios."*

**Why this is defensible:** every word is backed by something this chapter's methodology can actually show — "demonstrates feasibility" (not "proves production accuracy"), "on representative scenarios" (explicitly scoped, not claimed universal).

**What it cannot claim, restated as a firm list, consistent with — and extending — Chapter 10 §10.40:** production accuracy, universal elevator diagnosis, certified safety, fleet-wide performance, real-world improvement without actual measurement, guaranteed root-cause identification, real KONE deployment, or complete autonomous maintenance. **Every item on this list, claimed prematurely, would directly contradict this chapter's own validation-hierarchy logic** — none of Gates 6 through 10 have been cleared by a hackathon-stage prototype, and claiming their conclusions without clearing them is exactly the overclaiming this entire chapter exists to prevent.

## 11.46 The Validation Roadmap

```
PHASE A   Synthetic/offline validation           ← this project's current stage
     ↓
PHASE B   Historical-data validation
     ↓
PHASE C   Expert-reviewed benchmark
     ↓
PHASE D   Shadow mode (Ch.10 §10.36)
     ↓
PHASE E   Human-reviewed pilot
     ↓
PHASE F   Operational validation
```

Each stage requires the evidence gates of §11.44 relevant to it, cleared in order — Phase A requires Gates 1–6 (data through evidence grounding) on synthetic data; Phase B requires the same gates re-cleared on real historical data; Phase C adds genuine inter-rater-validated ground truth (§11.26); Phase D requires Gates 7–8; Phase E requires Gate 9; Phase F requires Gate 10 and sustained, monitored real-world performance.

## 11.47 The Research Reproducibility Package

What should accompany any real evaluation this project eventually performs: scenario definitions, the datasets used, data schemas, ground-truth labels (with their tier, per §11.3), model versions, prompts, RAG-corpus versions, evaluation scripts, the resulting metrics, the raw results, and the error analysis (§11.35) — **everything needed for an independent party to check this project's own claims**, the practical, concrete expression of the reproducibility principle Chapter 10 §10.37 already established at the architecture level.

---

# Master Validation Matrix

| Layer | Question | Metric | Ground Truth | Test Method | Failure Condition |
|---|---|---|---|---|---|
| Data | Is the input trustworthy? | Data-quality pass rate (Ch.6 §8.5) | Known-good/known-bad injected samples | Validation-rule testing | Corrupted data accepted as clean |
| Signals | Was the feature extraction correct? | Feature accuracy vs. known signal properties | Synthetic signals with known properties | Unit-level signal tests | Feature miscomputed |
| Anomalies | Was the deviation correctly flagged? | Precision/recall/F1 (§11.12) | Labeled anomalous/normal periods | Confusion-matrix evaluation | High FP or FN rate |
| Alarms | Were related alarms correctly grouped? | Cascade-grouping accuracy (§11.10) | Known cascade scenarios | Scenario-based testing | Unrelated alarms merged, or related ones split |
| Fault Isolation | Was the subsystem correct? | Top-1/Top-k accuracy (§11.13) | Expert-labeled/injected-fault scenarios | Benchmark evaluation | True subsystem absent from top-k |
| RCA | Was the root cause correct? | Root-cause Top-1/Top-k, causal-chain correctness (§11.14) | Confirmed outcomes / expert consensus | Benchmark evaluation, error taxonomy (§11.35) | Wrong cause ranked first with high confidence |
| Retrieval | Was relevant documentation found? | Precision@k/Recall@k/MRR/NDCG (§11.15) | Labeled relevant-document sets | IR-standard evaluation | Relevant document absent from results |
| Explanation | Is the explanation faithful? | Groundedness, citation correctness (§11.16–§11.17) | The system's own evidence trace | Claim-by-claim audit | Explanation contradicts the underlying trace |
| Confidence | Is confidence calibrated? | ECE, Brier score, reliability diagram (§11.18) | Outcome-labeled predictions | Calibration analysis | Systematic over/under-confidence |
| Human Usefulness | Did it help the technician? | Time, agreement, override rate (§11.20) | Controlled human-subject comparison | §11.37's design | No measurable improvement, or worse usability |
| System Reliability | Does it degrade safely? | Availability, graceful-degradation behavior (Ch.10 §10.6) | Fault-injection tests | Chaos/robustness testing (§11.29) | Hard failure instead of graceful degradation |

# Master Fault-Scenario Matrix

| Scenario | Primary Fault | Secondary Effects | Key Signals | Alarms | Discriminating Evidence | Expected RCA |
|---|---|---|---|---|---|---|
| Motor overcurrent (mechanical) | Obstruction/brake drag/load | Drive trip, position deviation | Current, vibration | Overcurrent, drive trip | Motion/brake correlation, clean self-test | Mechanical cause ranked leading |
| Motor overcurrent (electrical) | Winding fault | Overheating | Phase current imbalance, temperature | Overcurrent, motor-temp fault | Imbalance at light load | Winding fault ranked leading |
| Drive fault | IGBT/inverter | Drive trip | Current waveform, drive temp | Drive fault | Failed self-test | Drive/IGBT ranked leading |
| Brake fault | Coil/wear/timing | Overcurrent, leveling deviation | Brake timing, current | Overcurrent, brake fault | Brake-release correlation | Brake ranked leading |
| Door fault (obstruction) | Physical blockage | Timeout | Photo-eye, cycle time | Door obstruction/timeout | Consistent location | Obstruction ranked leading |
| Door fault (photo-eye) | Sensor degradation | Repeated reopening | Photo-eye instability | Door obstruction/timeout | Multi-cycle pattern, no location | Photo-eye ranked leading |
| Encoder fault | Signal degradation | Leveling deviation | Position-vs-commanded | Encoder fault, leveling deviation | Independent-sensor disagreement | Encoder ranked leading |
| Traction/rope fault | Wear/slip | Leveling deviation | Vibration, position | Position deviation | Agreement across independent sensors | Rope/sheave ranked leading |
| Controller/communication fault | Bus/wiring issue | Erratic data | Comm-error counters | Communication fault | Widespread, non-physical-pattern gaps | Communication fault ranked leading |
| Sensor fault | Stuck/drift/noise | Misleading equipment signal | The affected signal itself | Varies | Zero variance / independent-signal divergence | Sensor fault ranked leading, equipment ruled out |
| Thermal/environmental | Ambient/machine-room extremes | Context-dependent readings | Environmental sensors | Temperature-related | Correlation with environmental trend, not equipment | Environmental context, not equipment fault |
| Multiple simultaneous faults | Two independent causes | Two independent evidence sets | Both faults' respective signals | Both faults' respective alarms | Distinct, non-overlapping evidence clusters | Two separately-ranked hypothesis sets, not merged |

# Master AI Evaluation Matrix

| AI Capability | Baseline | Metric | Validation Method | Main Risk |
|---|---|---|---|---|
| Anomaly detection | Fixed threshold (Ch.6 §8.40) | Precision/recall/F1 | Confusion matrix on labeled periods | False positives/negatives |
| Classification | Rule-based lookup | Accuracy, macro-F1 | Benchmark evaluation | Class imbalance blind spots |
| Fault isolation | Classical ML | Top-1/Top-k accuracy | Benchmark evaluation | Wrong subsystem confidently claimed |
| RCA | LLM without RAG | Root-cause accuracy, causal-chain correctness | Benchmark + error taxonomy | Correct answer, wrong reasoning (E7) |
| RAG | LLM without retrieval | Precision@k/Recall@k/faithfulness | IR + faithfulness evaluation | Wrong or stale retrieval |
| LLM reasoning | Structured rules alone | Explanation quality, groundedness | Claim-by-claim audit | Fluent but unfaithful explanation |
| Multi-agent orchestration | Single agent | Accuracy, latency, cost, disagreement rate | Ablation (§11.23) | Complexity not earning its cost |
| Explanation | No explanation (bare label) | Faithfulness, completeness | Human + automated audit | Misrepresenting the evidence trace |
| Confidence | Uncalibrated raw score | ECE, Brier score | Calibration analysis | Overconfidence |
| Abstention | Always answer | Selective accuracy, coverage | Risk-coverage analysis | Abstention not actually improving accuracy |

# Master Demonstration Matrix

| Demo Case | Capability Demonstrated | Evidence | Expected Result | Judge Takeaway |
|---|---|---|---|---|
| 1 — Motor overcurrent | Multi-hypothesis differential diagnosis | Current, vibration, brake timing, drive self-test | Brake drag or mechanical cause ranked leading, alternatives shown | "This isn't a fault-code lookup" |
| 2 — Door degradation | Gradual-drift detection, pattern-based ambiguity resolution | Cycle-time trend, photo-eye instability pattern | Photo-eye degradation ranked leading | "It resolves the exact ambiguity from our own proposal" |
| 3 — Encoder/position anomaly | Independent-sensor cross-checking | Encoder vs. leveling-sensor agreement/disagreement | Correctly attributes cause based on sensor agreement pattern | "It knows when to trust a sensor" |
| 4 — Alarm cascade | Primary/consequential reasoning | A multi-alarm cascade sequence | One primary cause identified, others correctly explained as consequences | "One fault, not five" |
| 5 — Insufficient evidence | Abstention | A deliberately ambiguous evidence set | Explicit "insufficient evidence" output with named alternatives | "It can say it doesn't know" |

---

# Judge Questions

*Organized by the roadmap's own categories.*

### Validation

**1. How do you know your system works?** *Short:* Through the layered validation hierarchy (§11.2), not a single demo. *Detailed:* Data through system-level validation, each gated on the last (§11.44). *Evidence:* — *Assumptions:* — *Tested:* Whether "works" is defined precisely. *Avoid:* Pointing only at the demo.

**2. What is your ground truth?** *Short:* A mix of synthetic/injected (known), expert-labeled (working reference), and — where available — confirmed maintenance outcomes (§11.3). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the three-tier distinction is known. *Avoid:* Treating all ground truth as equally reliable.

**3. Where does your fault data come from?** *Short:* Physics-grounded synthetic scenarios (§11.25), consistent with this project's stated methodology throughout. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with every earlier chapter's answer. *Avoid:* Implying real KONE data was used.

**4. How do you validate synthetic data?** *Short:* You don't validate it *as* production-representative — you validate that the reasoning process behaves correctly against known-designed scenarios (§11.25). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this distinction is volunteered unprompted, as throughout the book. *Avoid:* Claiming synthetic success equals real-world validation.

**5. How many scenarios did you test?** *Short:* A small, curated set (the demo's 3–5, §11.40) at this project's current stage — explicitly insufficient for general-performance claims (§11.34). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Honesty about scale. *Avoid:* Implying a handful of demo cases constitutes a benchmark.

**6. Why is that enough?** *Short:* It's not, for a general-performance claim — it's enough only for the narrower claim of demonstrated feasibility (§11.45). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the team concedes this cleanly. *Avoid:* Defending the sample size as sufficient for anything beyond feasibility.

**7. What is your baseline?** *Short:* §11.22's five-tier comparison — alarm lookup, rules, classical ML, LLM-only, LLM+RAG. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a real comparison set, not just "better than nothing," is named. *Avoid:* No baseline at all.

**8. What metrics do you use?** *Short:* Layer-specific metrics (§11.12–§11.21), never one aggregate number. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specificity. *Avoid:* "Accuracy."

**9. Why isn't accuracy enough?** *Short:* It collapses eleven distinct "works" dimensions (§11.1) into one number, hiding exactly the failure patterns (§11.35) that matter most. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is the immediate, confident answer. *Avoid:* Hesitation.

**10. How do you evaluate RCA specifically?** *Short:* Root-cause Top-k accuracy, causal-chain correctness, hypothesis-ranking quality, alternative-cause-elimination accuracy — four distinct metrics, not one (§11.14). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether RCA's specific added complexity over classification is reflected in the metrics. *Avoid:* Reusing a plain classification metric for RCA.

### Data

**11. What if the historical diagnosis is wrong?** *Short:* This is exactly why "confirmed outcome" and "technician diagnosis" are separate, differently-weighted ground-truth tiers (§11.3–§11.4). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether ground-truth quality is treated as a real variable, not a given. *Avoid:* Treating all historical records as equally trustworthy.

**12. What if technician notes disagree with each other?** *Short:* Measured via inter-rater agreement (§11.26); genuine disagreement may reflect real diagnostic ambiguity, not just noise. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether disagreement is treated as informative, not discarded. *Avoid:* Picking one note arbitrarily.

**13. How do you handle class imbalance?** *Short:* Macro-F1 alongside accuracy, specifically because rare fault classes matter disproportionately (§11.13). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether macro-F1 is named specifically. *Avoid:* Citing accuracy alone.

**14. How do you handle rare faults?** *Short:* Few-shot/transfer/physics-informed methods with real academic precedent (Ch.9 Part II), combined with fault-tree structure that doesn't require abundant examples (§11.28). *Detailed:* — *Evidence:* [ACADEMIC EVIDENCE] *Assumptions:* — *Tested:* Whether a real precedent, not just an assertion, is cited. *Avoid:* Overclaiming rare-fault performance.

**15. How do you avoid data leakage?** *Short:* Asset-based and time-based splitting, not naive random splitting (§11.28). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the specific leakage mechanism (near-duplicate cases across train/test) is named. *Avoid:* Assuming random splitting is automatically safe.

**16. How do you test cross-elevator generalization?** *Short:* Cross-asset and cross-model splits specifically (§11.28). *Detailed:* — *Evidence:* — *Assumptions:* This book's scope is a modern gearless traction elevator. *Tested:* Whether the scope limitation is volunteered. *Avoid:* Claiming universal generalization.

**17. How do you handle missing data?** *Short:* Explicitly flagged, tested at multiple justified missingness levels, never silently imputed (§11.29, Ch.7 §7.26). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Cross-chapter consistency. *Avoid:* Silent imputation.

**18. How do you test sensor failure specifically?** *Short:* Dedicated scenarios checking whether the system notices, reduces trust, avoids false equipment diagnosis, and uses alternative evidence — four separate checks (§11.29). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether all four checks are named, not just "we test for it." *Avoid:* A vague answer.

### AI

**19. How do you evaluate hallucination?** *Short:* Claim-by-claim groundedness checking against the retrieved evidence, plus dedicated stress tests (§11.16, §11.31). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the claim→evidence→supported chain is named. *Avoid:* A vague "we check for it."

**20. How do you evaluate RAG?** *Short:* Precision@k/Recall@k/MRR/NDCG for retrieval, plus faithfulness metrics for what the LLM does with what's retrieved — two distinct evaluation layers (§11.15–§11.16). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether retrieval quality and generation faithfulness are kept separate. *Avoid:* Conflating the two.

**21. How do you evaluate explanations?** *Short:* Faithfulness to the underlying evidence trace, not just fluency or plausibility (§11.17, §11.32). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "human-readable ≠ correct" is stated. *Avoid:* Equating clarity with accuracy.

**22. How do you calibrate confidence?** *Short:* Via a dedicated calibration evaluation — reliability diagrams, Brier score, ECE — against real outcomes, not the LLM's self-report (§11.18). *Detailed:* — *Evidence:* — *Assumptions:* Full calibration requires outcome-labeled data this project doesn't yet have at scale. *Tested:* Whether "the LLM states its confidence" is avoided as the answer. *Avoid:* That exact wrong answer.

**23. When does the system abstain?** *Short:* When selective accuracy testing (§11.19) shows evidence is insufficient to support a confident conclusion. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Immediacy of the answer. *Avoid:* Hesitation.

**24. How do you test multi-agent reasoning?** *Short:* Orchestration correctness, role assignment, evidence-passing fidelity, and disagreement handling — tested directly, not assumed (§11.31). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specificity. *Avoid:* "We tested it and it works."

**25. Does adding agents improve accuracy?** *Short:* Not assumed — tested directly via ablation (§11.23), and Chapter 9 §9.24 explicitly warns it may not. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the team resists the "more agents = better" assumption reflexively. *Avoid:* Asserting it does without the ablation evidence.

**26. How do you prove that?** *Short:* Single-agent vs. multi-agent ablation, measured on accuracy, latency, cost, and error rate together, not accuracy alone (§11.23). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Follow-through on Q25's answer. *Avoid:* A vaguer answer than Q25's.

### RCA

**27. How do you know the AI found the root cause?** *Short:* Compared against tiered ground truth (§11.3), never assumed correct from a confident-sounding output alone. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether ground-truth tier is cited. *Avoid:* "It sounds right" as any part of the answer.

**28. What if it identifies the correct subsystem but wrong root cause?** *Short:* Scored as a distinct RCA error category (E6), not credited as a success (§11.35). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the error taxonomy's granularity is understood. *Avoid:* Crediting partial correctness as full success.

**29. What if there are multiple simultaneous faults?** *Short:* Tested via dedicated multi-fault scenarios (§11.9); the system should retain separate hypothesis spaces, not force one answer. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "one incident, one cause" is avoided as an assumption. *Avoid:* Assuming single-cause by default.

**30. What if the fault is intermittent?** *Short:* Validated via historical-reconstruction-specific scenarios (§11.11), the hardest category in this book's own library. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is named as genuinely hard, not solved. *Avoid:* Overclaiming intermittent-fault performance.

**31. How do you distinguish cause from consequence?** *Short:* Primary/consequential alarm validation, a dedicated metric distinct from plain root-cause accuracy (§11.10). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is named as its own tested capability. *Avoid:* Assuming it follows automatically from correct RCA.

**32. How do you validate causal reasoning specifically?** *Short:* Temporal-ordering checks (§11.11) plus causal-chain correctness within RCA metrics (§11.14). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether temporal and causal validation are named as distinct checks. *Avoid:* Conflating them with plain accuracy.

**33. How do you handle conflicting evidence?** *Short:* Dedicated conflicting-evidence test cases (§11.29) checking for detection, no blind resolution, confidence reduction, and escalation — four specific behaviors. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether all four are named. *Avoid:* A vague "it handles conflicts."

### Human

**34. How do you compare AI vs. technician performance?** *Short:* A controlled, matched-case, ideally within-subject comparison design (§11.37). *Detailed:* — *Evidence:* — *Assumptions:* Not yet executed at this project's current stage. *Tested:* Whether a real experimental design, not just "we'd ask technicians," is described. *Avoid:* An unstructured comparison plan.

**35. How do you prevent automation bias?** *Short:* Evidence visibility, honest confidence display, explicit alternatives, contradiction display, and a genuine (not rubber-stamp) confirmation step (§11.38). *Detailed:* — *Evidence:* — *Assumptions:* None of these technically guarantee genuine review. *Tested:* Whether this is honestly flagged as unsolved by architecture alone. *Avoid:* Claiming automation bias is prevented, full stop.

**36. How do technicians override the system?** *Short:* Explicitly, as a first-class action, per the human-in-the-loop design (Ch.9 §9.33, Ch.10 Part I). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether override is described as easy and expected, not a rare exception. *Avoid:* Implying override is discouraged.

**37. How do you measure technician usefulness?** *Short:* Time-to-diagnosis jointly with correctness, agreement rate, and perceived usefulness — never time savings alone (§11.20). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "time saved ≠ better diagnosis" is stated. *Avoid:* Citing speed alone as the value metric.

**38. What happens if the technician disagrees with the AI?** *Short:* The technician's judgment prevails — this is by design, not an edge case (Ch.9 §9.33). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Firmness. *Avoid:* Any hedge suggesting the AI's conclusion takes precedence.

### Demonstration

**39. Is your demo real data?** *Short:* No — synthetic/illustrative, explicitly labeled as such throughout (§11.41). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is volunteered immediately. *Avoid:* Any ambiguity.

**40. Is it synthetic?** *Short:* Yes. *Detailed:* Physics-grounded, per this project's stated methodology (§11.25). *Evidence:* — *Assumptions:* — *Tested:* Consistency with Q39. *Avoid:* A different answer than Q39's.

**41. What exactly does the demo prove?** *Short:* Feasibility of the reasoning process on representative cases (§11.45) — nothing about production accuracy. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Precision about the claim's actual scope. *Avoid:* Overstating what the demo shows.

**42. What does it not prove?** *Short:* Production accuracy, generalization, fleet-scale performance, or safety-certified reliability (§11.45). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this list is volunteered readily. *Avoid:* Hedging on any item.

**43. Why did you choose these scenarios?** *Short:* Deliberately for capability coverage — including one designed to show abstention, not just successes (§11.40). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether Case 5's deliberate inclusion is explained. *Avoid:* Implying the cases were chosen only to look impressive.

**44. What happens when your system fails during the demo?** *Short:* It should degrade gracefully and visibly, consistent with the architecture's own design (§11.42, Ch.10 §10.6) — itself a demonstration of the design philosophy, not an embarrassment. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether live failure is treated as an opportunity, not a disaster to avoid discussing. *Avoid:* Being unprepared for this question.

**45. Can the system abstain?** *Short:* Yes — demonstrated live, deliberately, as Case 5 (§11.40–§11.41). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is the single most confident answer in the entire Q&A. *Avoid:* Any hesitation whatsoever.

### Business

**46. How do you prove time savings?** *Short:* You don't yet — it's H1, a hypothesis this project's methodology is designed to test, not a demonstrated result (§11.43). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the hypothesis-vs-claim distinction holds under pressure. *Avoid:* Claiming proven time savings.

**47. How do you prove fewer repeat visits?** *Short:* Same answer pattern as Q46 — a value hypothesis, not yet validated (§11.43). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with Q46. *Avoid:* A different, stronger claim than Q46's.

**48. What is the baseline for these business metrics?** *Short:* Not established — real baselines require real KONE operational data this project does not have (§11.43). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a fabricated baseline is avoided. *Avoid:* Inventing a number.

**49. What is your expected ROI?** *Short:* Not calculated — this book explicitly avoids inventing business figures without a real baseline to compute them from. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Discipline under a tempting-to-fabricate question. *Avoid:* Making up a number.

**50. Which metrics would KONE care about?** *Short:* Mean Time to Diagnose/Repair, repeat-visit rate, first-time-fix rate, unnecessary dispatches (§11.21, §11.43) — named as relevant categories, not projected values. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether categories are named without inventing figures. *Avoid:* Attaching a specific improvement percentage to any of them.

### Safety

**51. Can a wrong diagnosis cause unsafe action?** *Short:* No — the safety architecture's independence (Ch.10 Part I) means a diagnostic error has no path to physical consequence. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Cross-chapter consistency with Chapter 10's answers. *Avoid:* Any drift from Chapter 10's established position.

**52. What prevents this?** *Short:* The architectural boundary itself (Ch.10 §10.38) — not a policy, a structural absence of any control path. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same. *Avoid:* Same.

**53. Is the system safety-certified?** *Short:* No, and never claimed to be (Ch.10 §10.40). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same. *Avoid:* Same.

**54. What happens when evidence is insufficient?** *Short:* Abstention (§11.19, §11.41's Case 5). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same reflexive confidence as Q23/Q45. *Avoid:* Hesitation.

**55. What happens if the AI fails entirely?** *Short:* Graceful degradation; the existing pre-AI maintenance process remains available (§11.42, Ch.10 §10.6). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Cross-chapter consistency. *Avoid:* Any drift.

### Deployment

**56. How would you validate before production?** *Short:* The full A–F validation roadmap (§11.46), each phase gated on the last. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a real staged plan, not "more testing," is described. *Avoid:* Vagueness.

**57. What is shadow mode?** *Short:* The AI runs alongside real operations without influencing them, compared against actual outcomes (Ch.10 §10.36, §11.46 Phase D). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Definitional accuracy. *Avoid:* Confusing it with a pilot (which does influence decisions).

**58. How would you run a pilot?** *Short:* Limited fleet, selected fault classes, mandatory human verification, full logging, baseline comparison, explicit safety boundaries, and rollback capability (Ch.10 §10.36, §11.46 Phase E). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Concreteness. *Avoid:* An unstructured "we'd try it out."

**59. How do you monitor drift?** *Short:* Model-governance drift monitoring (Ch.10 §10.21), plus temporal-generalization testing specifically (§11.28). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether both the architecture-level and validation-level answers are connected. *Avoid:* Citing only one.

**60. How do you reproduce an old diagnosis?** *Short:* Via the full versioned artifact set — input data, model/prompt/knowledge versions, retrieved sources, tool outputs (Ch.10 §10.37, §11.33). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Concreteness of the artifact list. *Avoid:* "We keep logs" without the specific list.

### Hard Questions

**61. What if your benchmark is biased?** *Short:* A real, named risk — mitigated by diverse scenario coverage (§11.34) and explicit sample-size/diversity reporting, never eliminated entirely. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether bias risk is acknowledged honestly, not denied. *Avoid:* Claiming the benchmark is bias-free.

**62. What if your labels are wrong?** *Short:* This is exactly why ground-truth tier (§11.3) and inter-rater agreement (§11.26) are tracked explicitly — label quality is a named, measured variable, not assumed perfect. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether label uncertainty is treated as real, not theoretical. *Avoid:* Assuming labels are ground truth by default.

**63. What if your synthetic data is unrealistic?** *Short:* A named, real limitation (§11.25) — mitigated by physics-grounding, never eliminated. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Honesty. *Avoid:* Defending synthetic data as fully realistic.

**64. What if the model memorizes the fault scenarios rather than learning to reason?** *Short:* Exactly the risk asset/time-based splitting and held-out generalization testing (§11.28) are designed to catch. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether memorization is named as a real, specific risk with a named countermeasure. *Avoid:* Dismissing the possibility.

**65. What if your RAG source is incorrect?** *Short:* Detected via source-validation and faithfulness checks (§11.16, §11.31) — a real, acknowledged residual risk, not eliminated. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Honesty about residual risk. *Avoid:* Overclaiming source reliability.

**66. What if the correct root cause is absent from your knowledge base entirely?** *Short:* The system should recognize the poor evidence fit and abstain, per OOD detection (Ch.9 §9.32) and rare-fault handling (§11.28) — not force a match to the nearest known cause. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether abstention is named as the correct behavior here specifically. *Avoid:* Implying the system always finds a match.

**67. What if no historical example exists for a given fault?** *Short:* Addressed via fault-tree/physics-based reasoning (Ch.7) rather than pure pattern-matching, plus few-shot methods (Ch.9 Part II) — genuinely harder, honestly flagged. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the difficulty is acknowledged, not minimized. *Avoid:* Claiming this case is fully solved.

**68. What if two causes are equally plausible?** *Short:* Both are retained and reported, with the ambiguity stated explicitly (Ch.7 §7.28, §11.19's expected behavior). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a tied output is treated as a legitimate, honest result. *Avoid:* Implying the system always breaks ties.

**69. What if the system is consistently overconfident?** *Short:* Exactly what calibration testing (§11.18) is designed to detect — a real evaluation finding to fix via recalibration, not a hypothetical. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether overconfidence is treated as detectable and correctable, not denied as a possibility. *Avoid:* Claiming the system is inherently well-calibrated without evidence.

**70. What is the single biggest limitation of your validation?** *Short:* The absence, at this project's current stage, of confirmed real-world ground truth — every validation claim rests on synthetic or expert-labeled data, never yet on genuinely confirmed field outcomes (§11.3, §11.25). *Detailed:* This is arguably the most important question in the entire chapter to answer honestly and immediately. *Evidence:* — *Assumptions:* — *Tested:* Whether the team volunteers their single most important limitation confidently, rather than being caught defending against it. *Avoid:* Naming a minor, secondary limitation instead of this central one.

---

# Final Validation Principles

1. A demo is not validation.
2. Accuracy is not enough.
3. Ground truth must be defined, and its tier stated explicitly.
4. Ground-truth quality matters as much as the metric computed against it.
5. RCA is harder than classification, and its metrics must reflect that.
6. Evidence correctness matters independently of conclusion correctness.
7. Temporal correctness matters, and must never be inferred backward.
8. Retrieval correctness and generation faithfulness are two distinct things to test.
9. Explanation correctness means faithfulness to the evidence trace, not fluency.
10. Confidence must be evaluated through calibration, never taken at face value.
11. Abstention is a measurable capability, not an excuse.
12. Rare faults require validation methods built for scarcity, not assumed away.
13. Synthetic data must be treated cautiously, and labeled as such, always.
14. Baselines are mandatory — a number with nothing to compare against proves nothing.
15. Ablation reveals which components actually earn their complexity.
16. Error analysis matters as much as aggregate metrics — arguably more.
17. Human usefulness must be measured directly, not assumed from technical accuracy.
18. Safety claims require appropriate evidence, and this project makes none it hasn't earned.
19. Prototype results must never be generalized beyond the tested scope.
20. Every major claim in this project should be traceable to a specific experiment or an authoritative source — never asserted on confidence alone.

---

# What We Now Understand

Validation is a layered discipline, not a single number: data through system-level validation, each layer gated on the one beneath it. Ground truth comes in tiers of trustworthiness, and every metric this chapter defines is only as reliable as the tier it was measured against. The fault-scenario library, built from this book's own prior chapters, gives validation a concrete, elevator-specific foundation rather than a generic AI-benchmarking exercise. RCA is measurably harder to evaluate than classification, requiring dedicated metrics for causal-chain correctness and alternative-cause elimination that plain accuracy cannot capture. RAG and explanation each need their own faithfulness checks, distinct from whether the final answer happened to be right. Confidence is only meaningful once calibrated, and abstention is only a real capability once measured to actually improve accuracy on the cases the system chooses to answer. Humans remain part of the validated system, not an afterthought to it, and automation bias remains the least architecturally-solvable risk this entire project carries. A hackathon demonstration and genuine validation are different activities, and this chapter has been careful, throughout, never to let the first one impersonate the second.

> **"The objective of validation is not to prove that the AI is always right. It is to determine where the system is reliable, where it is uncertain, where it fails, and whether it creates measurable diagnostic value within clearly defined boundaries."**

Technically: this reframes the entire chapter's purpose away from a pass/fail verdict and toward a *map* — which of the eleven "works" dimensions (§11.1) hold up, under which conditions, with what error patterns (§11.35), and at what confidence — because that map, not a single accuracy figure, is what a real engineering team, a real KONE SME reviewer, or a real judge actually needs to make an informed decision about this project's genuine, bounded, honestly-stated value.

---

# Bridge to Phase 10 — Scope, Prioritization, What Not to Build, MVP Architecture & Technical Decision Framework

Given everything established across nine phases, one question remains: **given everything we have learned, what should KONE Elevate actually build — and what should it deliberately not build?**

Phase 10 must synthesize the accumulated research into a clear decision framework — core problem definition, must-have versus nice-to-have capabilities, unnecessary complexity to avoid, the MVP-to-production roadmap, build-vs-buy decisions, rule-vs-ML-vs-LLM allocation, single-agent-vs-multi-agent justification, the real necessity (or non-necessity) of RAG, digital twins, GNNs, and PINNs for this project's actual scope, minimum data and minimum viable fault-scenario requirements, technical dependencies, team capability and implementation-effort realism, risk-vs-value-vs-feasibility weighing, and the hard constraints of a hackathon timeline — organized into a final: **"Build this." "Do not build this." "Build later." "Research only."**

Phase 10 content is not generated here — this document ends at the close of Phase 9.
