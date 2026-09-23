# PHASE 7 — ELEVATOR-SPECIFIC AI, GENERATIVE AI, RAG, MULTI-AGENT REASONING & EXPLAINABLE AI

### *KONE Elevate — Autonomous Fault Isolation & Root Cause Analysis: Master Research Book*

## How to Read This Chapter

Labels: **[PROJECT SOURCE]**, **[ACADEMIC EVIDENCE]** (real, cited papers — listed in full in "Sources Consulted"), **[OFFICIAL TECHNOLOGY DOCUMENTATION]**, **[INDUSTRY EVIDENCE]**, **[MODEL KNOWLEDGE]** (established AI/ML/software-engineering methodology — the label for most of the general LLM, RAG, and agentic-systems material below, none of it elevator- or KONE-specific), **[ENGINEERING INFERENCE]**, **[PROPOSED DESIGN]** (this project's own architectural choices, not a claim about what exists elsewhere), **[NOT ESTABLISHED]**. Where this chapter cites elevator-specific academic research, it uses real, current papers found via live search — no performance numbers are invented, and where a paper is cited, its actual claimed contribution is represented, not embellished.

**This chapter does not reduce to "use an LLM + RAG + multiple agents."** Every section below exists to answer a narrower, harder question: *which* intelligence technique should perform *which specific task*, what should stay deterministic, what should stay probabilistic, what should be retrieved rather than generated, and — the question that matters most for a safety-adjacent system — **what should the AI never be allowed to decide on its own.**

**The central question of this chapter:** *how can AI use engineering knowledge, telemetry, events, alarms, historical maintenance information, and structured diagnostic evidence to perform reliable, evidence-grounded fault isolation and root-cause reasoning?*

---

## From Phase 6 to Phase 7

Phase 5 taught how to reason about causes. Phase 6 taught how to extract trustworthy evidence from raw signals. But a real investigation can involve dozens of signals, hundreds of events, several alarms, maintenance records, technical manuals, fault-code descriptions, prior repairs, and genuinely conflicting evidence — more than any fixed rule table can enumerate, and more than a human technician can hold in working memory all at once, however experienced.

**The research question this chapter exists to answer:** *how can AI assist with this reasoning without hallucinating, inventing evidence, or making unsafe decisions?*

```
RAW DATA → STRUCTURED EVIDENCE → ENGINEERING KNOWLEDGE → AI REASONING → EXPLAINABLE DIAGNOSIS
```

---

# Part I — Why AI, and Which Kind

## 9.1 Why AI Is Needed

Not assumed — established. Conventional deterministic approaches genuinely struggle with several specific properties of this problem: **heterogeneous data** (numeric telemetry, discrete events, free-text technician notes, and PDF manuals don't share one native representation); **high-dimensional telemetry** (dozens of correlated signals, more than a hand-written rule table can practically enumerate); **long event sequences** (Chapter 4's cascades can span several alarms over several seconds, with the relevant history sometimes stretching back days, per Chapter 6's intermittent-fault reconstruction problem); **unstructured maintenance notes and technical documentation** (free text, not structured fields); **multiple competing hypotheses that must be weighed simultaneously**, not resolved by one lookup; **changing operating conditions** (Chapter 6 §8.24's context-dependence problem); **incomplete information** (Chapter 7 §7.26/§7.27's negative- and conflicting-evidence problem); **rare faults** (Chapter 6 §8.42's class-imbalance problem); and **cross-domain reasoning** (connecting a mechanical fact to an electrical signature to a maintenance-history pattern, three different kinds of knowledge, in one conclusion).

| Problem | Rule-Based Approach | ML Approach | LLM Approach | Best Candidate |
|---|---|---|---|---|
| Threshold-crossing detection | Simple, exact, fully auditable | Overkill | Overkill | **Rule-based** |
| Gradual drift detection | Brittle without careful tuning | Well-suited (EWMA/CUSUM, Ch.6 §8.25) | Overkill | **Statistical ML** |
| Multivariate anomaly scoring | Impractical to hand-enumerate every combination | Well-suited (Ch.6 §8.27–§8.28) | Poor fit — not a numerical-modeling tool | **ML** |
| Fault-tree traversal | Well-suited — the logic is genuinely enumerable | Unnecessary | Unnecessary | **Rule-based / deterministic** |
| Bayesian probability updates | Exact, well-defined math | N/A | **Should not be delegated to an LLM (§9.29 onward)** | **Deterministic probabilistic calculation** |
| Interpreting free-text maintenance notes | Impractical — language is not enumerable by rule | Possible but brittle without large labeled data | **Well-suited** | **LLM** |
| Retrieving relevant documentation | Impractical by keyword rules alone at scale | Possible (classic IR) | **Well-suited, especially combined with retrieval** | **LLM + RAG** |
| Explaining a conclusion in plain language | Rigid, templated | Not naturally suited | **Well-suited** | **LLM** |
| Planning which evidence to check next | Enumerable for known cases, brittle for novel ones | Not naturally suited | **Well-suited (§9.15)** | **LLM, tool-augmented** |

**AI is not the right tool for every stage of this problem** — the point of this table, and of this entire chapter, is to resist the temptation to force AI into rows where a deterministic or classical-statistical method is already the better answer.

## 9.2 A Taxonomy of AI Techniques in This System

These are not interchangeable, and treating them as such is a common source of muddled architecture:

```
DATA ANALYTICS           (Ch.6's statistical methods — thresholds, EWMA, CUSUM)
        ↓
MACHINE LEARNING          (Ch.6's classical ML — Isolation Forest, PCA, One-Class SVM)
        ↓
DEEP LEARNING              (Ch.6's autoencoders, LSTM-AE, Temporal CNN, Transformer)
        ↓
GENERATIVE AI                (models that produce new content — text, structured output)
        ↓
LLM                            (a specific, language-focused generative-AI technology)
        ↓
AGENTIC SYSTEM                   (an LLM given tools, planning, and multi-step autonomy)
```

Each layer builds on, rather than replaces, the one below it — an agentic system still needs the data analytics and ML layers underneath it to produce the evidence it reasons over (this is precisely Chapter 6's entire contribution to this project). Classical machine learning and deep learning remain the right tools for numerical pattern recognition (§9.3 onward); knowledge graphs and graph neural networks are the right tools for representing structured relationships (§9.10); LLMs are the right tool for language understanding, planning, and explanation (§9.11 onward) — and none of these five layers substitutes for any other.

---

# Part II — Elevator-Specific AI: The Academic Landscape

*[ACADEMIC EVIDENCE throughout this Part, unless otherwise labeled]* This section surveys real, current published research specifically on elevator AI applications — not general machine-learning theory. A clear pattern recurs across nearly every paper found: **elevator fault data scarcity is the field's defining constraint**, and most of the genuinely current research is explicitly organized around working around it.

## 9.3 Vibration AI

Elevator vibration diagnosis has an active, current research literature. A 2024 study published in *Scientific Reports* (Nature) combines a **Physics-Informed Neural Network (PINN)**, used as a generator to predict expected vibration behavior from physical first principles, with an **e-RGCN** (a relational graph convolutional network) acting as a discriminator that classifies the actual fault type by comparing the PINN's physics-based prediction against real measured vibration data — explicitly motivated by the "limited availability of fault data for elevators," the exact constraint this whole book has repeatedly named. A 2023 *ScienceDirect* study addresses a more foundational problem — elevator vibration signals are inherently noisy — proposing an autoencoder-based denoising method (built on a deep residual U-Net architecture) specifically to clean vibration signals before any downstream fault classification is attempted, building on earlier work combining time/frequency-domain features with neural-network classifiers and deep-autoencoder-based feature extraction. A 2025 trade-publication piece (*Elevator World*) describes a pipeline combining FFT-based feature extraction, a deep autoencoder, and a random forest classifier, and makes a specific, concrete engineering point worth carrying forward: analyzing the **vertical acceleration component separately for upward and downward travel**, since a traction elevator's vibration character genuinely differs by direction — a nice, independently-confirmed instance of Chapter 3 §3.3's counterweight-asymmetry reasoning. A 2025 *ScienceDirect* paper addresses the same scarcity problem from a different angle, using continuous wavelet transforms to convert vibration signals into time-frequency images, then classifying them with a capsule network (chosen specifically because it preserves geometric/spatial structure better than a standard CNN) combined with data augmentation, again explicitly motivated by "relatively limited unbalanced training samples... especially fault samples."

**Pipeline, synthesized from this literature:**

```
Vibration → Preprocessing/denoising → Features (time/frequency-domain, Ch.6 §8.7–§8.9)
   → Model (CNN / 1D-CNN / autoencoder / capsule network / PINN+GNN)
   → Classification or anomaly score → Diagnostic evidence
```

**Vibration anomaly detection vs. vibration-based root-cause diagnosis**, restated at the AI-model layer: every model surveyed above answers *"is this vibration pattern unusual, or which category does it best match"* — none of them, on their own, answers *"why did this vibration pattern occur,"* which remains Chapter 7's job regardless of how sophisticated the vibration model is (Ch.6 §8.35's anomaly-vs-RCA distinction, holding at every layer of this architecture).

## 9.4 Door AI

Two directly relevant, current papers. A study published in *PMC* proposes a **GNN-LSTM-BDANN** model for elevator door systems: acoustic (sound-based) monitoring, combined with **transfer learning** — using historical sound data from *other* elevators to help predict the remaining useful life of a target elevator's door system — motivated by the observation that wear-induced door faults (roller, guide-rail, and track wear) each produce distinctive sound signatures (rolling-friction noise, collision sounds, vibration-induced sounds). A 2026 *MDPI Applied Sciences* paper, "Cross-Scale Time-Frequency Fusion Network for Non-Stationary Vibration Fault Diagnosis of Elevator Door Systems," addresses door-specific vibration analysis directly, building on a documented line of prior elevator-vibration work (Jia et al. 2021's vibration-based elevator fault monitoring; Niu & Wang 2022's elevator-car vibration denoising).

Potential AI tasks for door systems, consistent with both papers and with Chapter 4 §4.9/Chapter 6 §8.14's engineering analysis: normal/abnormal cycle classification, obstruction detection, mechanical-degradation trend detection, door-motor behavior classification, photo-eye behavior-pattern classification, and cycle-time anomaly detection.

**Why door systems are a genuinely good AI candidate:** they produce frequent, repeated cycles — far more training examples per unit time than the main drive system generates, a real practical advantage for any data-hungry method. **Limitations, honestly stated:** different elevator models and door configurations, changing loads, and environmental variation (ambient noise for acoustic methods specifically) all threaten a model's ability to generalize beyond the specific installation(s) it was trained on — precisely the domain-shift concern §9.12's transfer-learning discussion addresses directly.

## 9.5 Acoustic AI

Building on §9.4's acoustic-monitoring paper: acoustic methods generally rely on microphone data, spectral features (closely related to Chapter 6 §8.9's frequency-domain methods, applied to sound rather than vibration or current), abnormal-sound classification, and — because real deployment environments are rarely quiet — an explicit need for noise robustness. **Limitations, honestly stated:** ambient building noise, the specific building's acoustic environment, microphone placement sensitivity, and — the recurring theme of this entire Part — data scarcity for genuinely labeled abnormal-sound examples. **This book does not claim acoustic diagnosis is sufficient for RCA on its own** — like every other single-signal method surveyed in this chapter, it's one evidence source among several (Chapter 6 §8.30's multi-signal principle, restated here for acoustic evidence specifically).

## 9.6 Remaining Useful Life (RUL)

**RUL asks:** *"what is the expected remaining operating life of a component?"* — a fundamentally different question from fault detection ("is something abnormal now"), fault isolation ("which subsystem"), or RCA ("why did an already-occurred fault happen"). §9.4's GNN-LSTM-BDANN paper is itself an RUL-prediction study specifically for elevator door systems; the general RUL literature (drawn from broader industrial contexts — bearing prognostics, turbofan-engine degradation, hydraulic-valve health monitoring) consistently emphasizes multi-sensor fusion as improving RUL prediction reliability over any single signal, directly reinforcing Chapter 6 §8.30's multi-signal principle from an independent research direction. **RUL is useful, but is not equivalent to RCA:** predicting that a door mechanism has roughly 30 days of useful life remaining tells you nothing about why a *specific, already-occurred* overcurrent event happened yesterday — these are complementary, not substitutable, capabilities (directly paralleling Chapter 3 §5.14's predictive-vs-diagnostic distinction, now grounded in the RUL literature specifically).

## 9.7 Few-Shot and Transfer Learning

**Why elevator fault data is difficult to obtain, restated with real evidence behind it:** rare faults, expensive/impractical labeling, proprietary OEM data (Ch.4 §4.23), and severe class imbalance are not this book's own speculation — they are the *explicitly stated motivation* in nearly every elevator-AI paper found in this research pass.

A 2025 *Sensors* (MDPI) paper, "MetaRes-DMT-AS," from a research group at Zhejiang University of Science and Technology, addresses this directly with a **meta-learning** approach — specifically Prototypical Networks combined with a Gram Angle Field signal-transformation technique — designed explicitly for **few-shot fault diagnosis**: learning to classify fault types from only a handful of labeled examples per class, rather than the large labeled datasets conventional deep learning assumes. The paper's own stated motivation is nearly verbatim the constraint this whole book has been working around: "conventional approaches typically require substantial labeled datasets that are often impractical to obtain."

**Transfer learning** — training on one domain, adapting to another — is the mechanism §9.4's door-RUL paper uses across different elevators specifically. **Challenges, honestly stated:** different elevator models, different sensor configurations, and different operating conditions all introduce genuine **domain shift**, and a model transferred without careful validation risks confidently misapplying patterns learned on one installation to a meaningfully different one. Transfer learning is a useful, real, actively-researched technique for this exact data-scarcity problem — **it must be validated on the target domain, not assumed to transfer cleanly.**

## 9.8 Sensor Fusion

Already introduced conceptually in Chapter 6 §8.30; here, formalized as an AI-architecture concern specifically. Combining current, vibration, temperature, position, speed, door data, alarms, and maintenance history can happen at three distinct levels:

- **Early fusion** — combine raw signals or low-level features *before* modeling, letting a single model learn cross-signal patterns directly.
- **Late fusion** — run separate models per signal type, then combine their individual outputs (e.g., each signal's own anomaly score, combined into one overall assessment).
- **Decision-level fusion** — combine final decisions/conclusions from otherwise-independent analyses, the loosest coupling of the three.

**Benefits and limitations:** early fusion can capture richer cross-signal interactions but requires more careful handling of Chapter 7 §7.16's correlated-evidence problem, since it directly mixes signals that may not be independent; late and decision-level fusion are more modular and easier to validate/debug per-signal, but can miss cross-signal patterns that only emerge when signals are considered jointly. **This connects directly to Phase 5:** multiple evidence sources produce a stronger hypothesis evaluation than any single source — the RUL literature surveyed in §9.6 reaches this same conclusion independently, from a different research direction entirely.

## 9.9 Digital Twins, PINNs, and Digital Twin + AI Combinations

**A digital twin, from first principles:** a physical elevator on one side, a **digital representation** on the other, kept in sync — ideally in something close to real time — such that the digital representation can be queried, simulated, and tested without touching the physical equipment. Core capabilities: real-time state synchronization, structured state representation, simulation of hypothetical scenarios, **fault injection** (deliberately simulating a failure to see its predicted effects), predictive simulation, scenario testing, and maintenance planning support.

**Digital twin vs. simulation vs. digital model, distinguished precisely:** a **digital model** is a static representation with no live connection to the physical asset. A **simulation** can run hypothetical scenarios but doesn't necessarily stay synchronized with a specific, individual, real asset's current actual state. A **digital twin** specifically maintains that live, individual-asset synchronization — the defining feature that distinguishes it from the other two.

**Digital twin + AI combinations, evaluated honestly rather than assumed:**

- **Digital twin + ML** — using the twin's simulated data to augment scarce real training data.
- **Digital twin + GNN** — §9.3's PINN+e-RGCN paper is precisely this combination in practice, a real, current example, not a hypothetical.
- **Digital twin + PINN** — using physical laws (Chapter 1's motor/traction physics, formalized) to constrain what a model is allowed to predict, directly addressing data scarcity by injecting known physics rather than requiring the model to learn it purely from limited examples.
- **Digital twin + LLM/agent** — an LLM could query a digital twin as one of its available tools (§9.14), asking "what would this fault look like under these conditions" as part of an investigation.

**When a digital twin is useful, and when it's unnecessary complexity:** genuinely valuable when (a) real fault-labeled data is scarce (exactly this project's situation, per §9.7) and physics-grounded simulation can credibly fill the gap, or (b) scenario testing ahead of a real intervention has real value. Unnecessary complexity when the diagnostic question at hand doesn't actually require simulating hypothetical states — much of Chapter 7's fault-tree and Bayesian reasoning, for instance, operates entirely on *already-observed* evidence and doesn't inherently need a live simulated twin to function. **This book does not claim the proposed RCA system requires a digital twin** — it's a legitimate, evidenced, but optional architectural component, evaluated on its own merits rather than assumed necessary because it's fashionable.

**PINNs specifically** — Physics-Informed Neural Networks — combine data with explicit physical-law constraints (§9.3's paper uses one as a generator predicting expected vibration from physics). The core idea, plainly: instead of asking a model to learn Chapter 1's torque/current/vibration relationships purely from limited examples, encode those known relationships directly into the model's training objective, so the model is constrained to produce physically plausible outputs even where labeled data is thin. **Limitations:** requires an accurate physics formulation in the first place (itself real engineering work), added computational cost, and risk of model mismatch if the encoded physics doesn't fully capture the real system's behavior.

## 9.10 Graph Neural Networks and Knowledge Graphs

**Why elevator systems naturally form graphs:** the mechanical energy path (Ch.1 §1.4: Motor → Drive → Traction → Rope → Car) and the electrical/diagnostic path (Ch.2: Motor → Current → Controller → Alarm) are both, structurally, chains of connected entities with directional relationships — exactly what a graph represents naturally and a flat feature vector does not.

**Graph Neural Networks (GNNs)**, conceptually: **nodes** represent entities (components, signals, subsystems); **edges** represent relationships between them; **features** attach to nodes and/or edges (a node's current sensor reading, an edge's known causal-mechanism strength); **message passing** is the mechanism by which a GNN propagates information between connected nodes across the graph, letting a node's learned representation reflect not just its own features but its neighbors' — directly analogous to how Chapter 7 §7.13's causal graphs represent how one node's state influences another's, but learned from data rather than hand-specified. §9.3's e-RGCN (a **relational** GCN, meaning it accounts for different *types* of edges/relationships, not just their presence) is a concrete, current, working example of exactly this applied to elevator vibration diagnosis.

**Knowledge graphs**, distinguished from GNNs: a knowledge graph is the explicit, human-readable *representation* of relationships — for example:

```
Motor        —connected_to→        Drive
Motor        —has_failure_mode→    Overcurrent
Brake        —can_cause→           Mechanical_resistance
Mechanical_resistance —can_increase→ Motor_current
```

— essentially, Chapter 7's fault trees and FMEA relationships, formalized in a graph-structured, queryable form. A **GNN** is a learned model that operates *over* graph-structured data (which could be a knowledge graph, or any other graph representation); a **knowledge graph** is one specific way of structuring and storing relational knowledge, queryable directly without necessarily requiring any learned model at all. **This book's fault trees (Chapter 7 §7.7) and FMEA table (§7.8) are, structurally, exactly the kind of content a knowledge graph would formalize** — the relationship, not a new one, between two things this book has already built.

> **Why This Matters to KONE Elevate RCA:** A GNN could, in principle, *learn* subsystem relationships from data (as §9.3's paper demonstrates for vibration specifically); a knowledge graph *encodes* the relationships this book already established through engineering reasoning (Chapters 1–3, 7) directly and queryably, without needing a trained model at all. For a hackathon-stage project with synthetic, physics-grounded data rather than abundant real training examples, the knowledge-graph route — encoding known engineering relationships explicitly — is the more defensible near-term choice; a learned GNN remains a credible, evidenced future direction (§9.3's paper proves the general approach works), not a required starting point.

---

# Part III — LLMs: What They Are and Are Not For

## 9.11 Introducing LLMs Into the Architecture

*[MODEL KNOWLEDGE]* Large Language Models bring genuine, distinct capabilities to this architecture: language understanding, multi-step reasoning over presented information, producing structured outputs on demand, using external tools, summarization, interpreting unstructured documentation, and generating candidate hypotheses in natural language.

**The single most important principle in this entire chapter, stated once and never relaxed:** **an LLM does not inherently know the actual state of any specific elevator.** It has no direct sensory access to a real, physical machine. Everything it "knows" about a specific fault episode has to arrive as explicitly provided evidence — retrieved, queried, or supplied as input — never assumed, inferred from general training knowledge, or invented to fill a gap. Every subsequent section in this chapter exists, in one way or another, to enforce this one boundary.

## 9.12 What the LLM Should and Should Not Do

| Task | LLM Appropriate? | Why |
|---|---|---|
| Summarize an investigation | **Yes** | Language synthesis over already-established facts |
| Interpret retrieved documentation | **Yes** | Genuine language-understanding task |
| Generate candidate hypotheses | **Yes**, from a defined fault-tree/knowledge-graph space (§9.10) | Structured hypothesis generation, not free invention |
| Compare evidence against hypotheses | **Yes**, when the evidence itself is supplied, not recalled from memory | Reasoning over provided facts |
| Explain a conclusion in plain language | **Yes** | The core language-generation strength |
| Structure technician-facing output | **Yes** | Formatting/communication task |
| Formulate the next investigation step | **Yes**, within a tool-calling framework (§9.14) | Planning over known available tools |
| **Raw numerical signal processing** | **No** | This is Chapter 6's job — deterministic/statistical computation, not language reasoning |
| **Exact probability calculation** | **No** (§9.29 develops this in depth) | Bayesian arithmetic belongs to a deterministic probabilistic model, not free-form generation |
| **Safety decisions** | **Never** | Outside this project's entire scope (Understanding Report §J) |
| **Autonomous equipment control** | **Never** | Same |
| **Inventing missing evidence** | **Never** | The single most dangerous failure mode in this whole architecture (§9.35) |
| **Unrestricted maintenance instructions** | **No** — must be grounded in retrieved, verified procedures (Ch.4 §4.15's "never let the LLM freely invent a maintenance action" principle) | Same reasoning as probability calculation — precision matters, and free generation risks fabricating a procedure that sounds plausible but isn't real |

> **KEY CONCEPT:** Every row in the top half of this table is a **language and reasoning-over-given-facts** task. Every row in the bottom half is either a **precise computation** task (better done deterministically) or a **consequential real-world action** (which this project's entire safety boundary keeps outside AI authority). The dividing line is not "hard vs. easy" — it's "does correctness here depend on exact, verifiable computation or irreversible real-world consequence."

## 9.13 Structured Outputs

**Why free-form LLM responses are insufficient for industrial RCA:** prose is hard to validate, hard to audit, and easy to subtly misparse downstream. The system needs a structured investigation object instead — conceptually:

```json
{
  "observation": "...",
  "time_window": "...",
  "evidence": [...],
  "hypotheses": [...],
  "supporting_evidence": {...},
  "contradicting_evidence": {...},
  "root_cause_ranking": [...],
  "confidence": ...,
  "unresolved_questions": [...],
  "verification_required": true
}
```

**This exact schema is not claimed as a required implementation** — it's illustrative of the *principle*: **LLM reasoning → structured state → deterministic validation → human-readable output.** A structured object can be checked programmatically (does every hypothesis have at least one evidence citation? does the confidence field fall in a valid range?) in a way free text cannot — turning "the LLM said something plausible" into "the LLM's output passed defined structural checks," a meaningfully stronger guarantee.

## 9.14 Tool Calling

*[MODEL KNOWLEDGE]* Rather than reasoning from memory, an LLM in this architecture calls external tools for anything requiring precise, verifiable data: a telemetry query, an alarm-history query, a maintenance-history query, documentation retrieval, a fault-tree lookup, an FMEA lookup, a statistical/signal-processing calculation (Chapter 6's methods, invoked as a tool rather than reimplemented in the LLM's own reasoning), or a knowledge-graph query.

```
LLM decides what evidence is needed
        ↓
Calls the appropriate tool
        ↓
Receives a structured result
        ↓
Reasons again, now with real data
```

**Tools should perform precise operations instead of asking the LLM to hallucinate calculations** — restating §9.1's table's core lesson at the implementation level: if a task belongs in the "deterministic" column, it should be *implemented* as a deterministic tool the LLM calls, not something the LLM is asked to compute itself, however capable it might seem at arithmetic in a given instance.

## 9.15 Agentic Reasoning Patterns: ReAct, Planning, Reflection, and Self-Consistency

Four related, well-established patterns for structuring how an LLM-driven investigation actually unfolds.

**ReAct (Reason → Act → Observe → Reason again).** *[MODEL KNOWLEDGE]* This book describes only the **observable workflow**, consistent with the project's stated principle (Understanding Report §H) that the system should not depend on exposing hidden internal model reasoning: a hypothesis is formed, a tool/action is taken (§9.14), the resulting evidence is observed, and the hypothesis is updated — repeated until the investigation reaches a confident conclusion or, per §9.31, honestly abstains.

**Planning.** Given initial evidence — say, a motor-overcurrent alarm — a planned investigation looks like: (1) check event chronology, (2) retrieve relevant fault-tree/FMEA knowledge, (3) analyze motor current, (4) check vibration, (5) check brake-related evidence, (6) check drive diagnostics, (7) check maintenance history, (8) rank hypotheses. **Why planning beats randomly querying data:** a planned sequence reflects the fault tree's actual structure (Chapter 7 §7.7.1) — checking brake timing specifically because brake drag is a live hypothesis, not querying arbitrary signals hoping something useful turns up.

**Reflection and verification, distinguished:** **reflection** is the model reviewing its own emerging conclusion for internal consistency; **verification** is checking that conclusion against independent evidence or rules. **Reflection alone does not guarantee correctness** — a model reflecting on a wrong conclusion can produce a more confident-sounding wrong conclusion just as easily as a corrected one. **Independent verification — against actual retrieved evidence, structural checks, or eventually human review — remains required regardless of how much internal reflection occurred.**

**Self-consistency.** Generate multiple independent reasoning paths (e.g., running the investigation process more than once, or exploring the hypothesis space along different orderings) and compare the resulting conclusions — general agreement across paths is weak evidence of robustness; disagreement is a useful signal to flag for closer review or lower confidence. **Real trade-offs:** meaningfully higher computational cost (running the process multiple times), and — the more important caveat — **self-consistency is not a substitute for genuine engineering evidence.** Multiple LLM reasoning paths converging on the same answer is not the same kind of evidence as an independent sensor confirming a hypothesis (Chapter 7 §7.34's exact distinguishing check); it primarily tells you the model's reasoning is *stable*, not that it's *correct*.

---

# Part IV — Retrieval-Augmented Generation

## 9.16 Why Retrieval, Not Memory

The diagnostic system needs access to technical manuals, fault-code descriptions, maintenance procedures, engineering documentation, historical maintenance records, previous incidents, and component information. **Retrieval is preferable to relying on an LLM's internal (training-time) knowledge** for exactly the reason established in §9.11: the LLM's training data cannot contain KONE's actual, current, potentially-proprietary documentation, and even where general knowledge overlaps, relying on it invites the LLM to answer from a plausible-sounding memory rather than a verifiable, currently-correct source. **RAG (Retrieval-Augmented Generation)** is the standard architecture for this: **LLM + retrieved external knowledge**, with the retrieved content — not the model's unaided memory — serving as the grounding for any documentation-dependent claim.

## 9.17 The RAG Pipeline

```
DOCUMENTS
   ↓
INGESTION         — parsing PDFs/manuals/service documents/notes/fault-code tables;
                      OCR where needed; preserving metadata (component, fault code,
                      procedure, revision, model, source identity) — provenance
                      matters as much as content, since a stale or wrong-model
                      manual retrieved confidently is arguably worse than no
                      retrieval at all
   ↓
CHUNKING          — dividing documents into retrievable units. Fixed-size chunks
                      are simple but can split a coherent procedure mid-thought;
                      semantic or section-based chunking preserves meaning better
                      at the cost of more complex preprocessing; overlapping
                      chunks reduce the risk of splitting critical context across
                      a chunk boundary. For maintenance documents specifically,
                      preserving component/fault-code/procedure/revision/model
                      metadata *per chunk* — not just per document — matters,
                      since a technician needs to know a retrieved procedure
                      actually applies to the equipment in front of them
   ↓
EMBEDDINGS        — converting text into a vector representation capturing
                      semantic similarity, so that a query like "motor current
                      high during acceleration" can retrieve a document chunk
                      about "overcurrent during motor startup" even though the
                      wording differs
   ↓
VECTOR DATABASE / INDEX  — stores embeddings for similarity search, typically
                      alongside metadata filtering (e.g., restrict retrieval to
                      documents for the correct elevator model)
   ↓
HYBRID RETRIEVAL  — semantic retrieval alone can miss an exact fault-code
                      lookup (a query for "E1234" is better served by keyword/
                      BM25 search than semantic similarity); semantic retrieval
                      alone is better for a conceptual query like "excessive
                      motor torque" with no exact matching string. Combining
                      both — hybrid retrieval — covers a broader, more precise
                      range of queries than either alone
   ↓
RERANKING         — an initial retrieval pass returns candidate documents; a
                      reranking step re-scores them for relevance before
                      anything reaches the LLM. Retrieval quality strongly
                      determines output quality — a well-reasoned LLM given
                      poor context still produces a poorly-grounded answer
   ↓
CONTEXT → LLM → GROUNDED RESPONSE
```

## 9.18 Source Grounding

**Every important diagnostic claim should be traceable to its source** — telemetry, an event, an alarm, a document, a maintenance record, an engineering rule, or a specific model output:

```
CLAIM → EVIDENCE → SOURCE → TIMESTAMP / VERSION
```

This is the RAG-pipeline-level implementation of the ExplainabilityTrace principle already established throughout this book (Chapter 4 §4.21, Chapter 7 §7.38) — a claim without a traceable source is, by this project's own design standard, not yet a usable claim.

## 9.19 RAG Failure Modes

Wrong retrieval (the retrieved documents aren't actually relevant), incomplete retrieval (relevant documents exist but weren't found), stale documentation (retrieved content is outdated), conflicting documents (two retrieved sources disagree), irrelevant chunks (poor chunking boundaries pull in noise), hallucination (the LLM asserts something beyond what was actually retrieved), prompt injection (§9.36), and a poisoned knowledge base (deliberately or accidentally corrupted source documents). **Each of these can directly corrupt a diagnosis** — RAG makes evidence *available*, but availability alone doesn't guarantee correctness, currency, or consistency, which is precisely why source grounding (§9.18) and downstream verification (§9.25 onward) remain necessary even with a well-built retrieval pipeline.

---

# Part V — Multi-Agent Architecture

## 9.20 Agent Roles

Consistent with this project's own architecture (Understanding Report §H), organized around specialized reasoning roles, each answering one specific question:

| Role | Guiding Question |
|---|---|
| **Signal Triage Agent** | Is anything abnormal? |
| **Orchestrator** | What should be investigated, and in what order? |
| **Retrieval Agent** | What evidence and documentation is needed? |
| **Fault Isolation Agent** | Which subsystem is involved? |
| **RCA Agent** | Why did it happen? |
| **Synthesis Agent** | What should be communicated, and to whom? |
| **Explainability Engine** | Why is this conclusion supported? |
| **Human Reviewer** | Should the conclusion or action proceed? |

**Not every role necessarily needs a separately-implemented agent.** §9.21 addresses this directly — this table describes a set of **responsibilities**, which could be distributed across genuinely separate agent processes or handled as distinct reasoning stages within a smaller number of implementations. The distinction that actually matters architecturally isn't "how many agent processes exist" — it's whether each responsibility above is being discharged cleanly, with its own clear inputs, outputs, and validation.

## 9.21 Single Agent vs. Multi-Agent

**Single agent:** one reasoning process, equipped with multiple tools (§9.14) — the LLM itself decides, within one continuous context, which tool to call next. **Multi-agent:** genuinely separate reasoning processes, each specialized to one role from §9.20's table, communicating through defined interfaces (most naturally, the structured investigation state from §9.23).

| Characteristic | Single Agent | Multi-Agent |
|---|---|---|
| Complexity | Lower | Higher |
| Latency | Generally lower (fewer hand-offs) | Generally higher (coordination overhead) |
| Debugging | Harder to isolate which reasoning step went wrong | Easier — each agent's contribution is separately inspectable |
| Observability | One large reasoning trace | Multiple smaller, role-specific traces |
| Specialization | Limited — one context handles everything | Strong — each agent can be tuned to its specific task |
| Failure propagation | A single error can corrupt the whole reasoning chain | An error can be isolated to one agent's output, though it can still propagate if unchecked (§9.24) |
| Cost | Generally lower | Generally higher (more model calls) |

**When multi-agent architecture is justified:** when the specialization benefit (each role genuinely benefits from a distinct prompt, distinct tool access, or distinct validation logic) and the debuggability/observability benefit outweigh the added latency, cost, and coordination-failure surface area (§9.24). For a problem with this many genuinely distinct reasoning stages — triage, evidence retrieval, subsystem isolation, causal reasoning, synthesis, explanation, and human hand-off, each requiring different tools and producing different kinds of output — the specialization case is real, not decorative; but that doesn't make every one of §9.20's eight roles automatically deserving of a fully separate implementation, which is exactly why §9.20 frames them as responsibilities first.

## 9.22 Diagnostic Orchestration

The orchestrator's conceptual responsibility: determine **what evidence already exists**, **what evidence is still missing**, **which hypothesis currently has the strongest support**, **what investigation step should happen next**, **when enough evidence exists to stop investigating**, **when to abstain instead of concluding** (§9.31), and **when to escalate to human review** (§9.33). **The orchestrator must never be permitted to directly override any safety system** — a hard boundary, not a tunable parameter, consistent with the safety architecture established from the Understanding Report onward.

## 9.23 Investigation State and the Evidence Trace

**Why the diagnostic process needs persistent, structured state rather than repeatedly passing unstructured text between agents:** free text degrades with each hand-off (subtle rephrasing, dropped nuance, the classic "lost in translation" problem across multiple language-model calls); structured state does not.

```
CASE
├── asset
├── incident
├── time_window
├── observations
├── alarms
├── telemetry
├── anomalies
├── hypotheses
├── evidence
├── contradictions
├── retrieved_sources
├── confidence
├── unresolved_questions
└── verification
```

For every conclusion, an **evidence trace** — the ExplainabilityTrace concept, now given its full form — records: **Observation → Evidence → Hypothesis → Supporting evidence → Contradicting evidence → Alternative hypotheses → Confidence → Decision → Verification.** This is a core artifact of the whole system, not an optional logging feature — every downstream explanation (Part VI) and every human review (§9.33) reads directly from this trace.

## 9.24 Multi-Agent Failure Modes

Agent disagreement (two agents reach different conclusions from the same evidence — itself useful signal if surfaced, dangerous if silently resolved); cascading errors (an early agent's mistake propagates uncorrected through every later stage); confirmation bias between agents (a later agent uncritically accepting an earlier agent's framing rather than independently evaluating evidence); duplicated reasoning (wasted effort, and a subtle risk that duplicated-but-not-identical reasoning gets treated as independent confirmation — Chapter 7 §7.16's double-counting problem, now at the agent level); incorrect orchestration (evidence gathered in the wrong order, or a stopping decision made too early or too late); retrieval contamination (Chapter 4 §4's/§9.19's RAG failure modes propagating into agent reasoning); circular reasoning (agent A's conclusion feeding agent B, whose conclusion feeds back into agent A's next reasoning step without genuinely new evidence); and false consensus (multiple agents agreeing, mistaken for corroborating evidence, when the agreement actually reflects a shared blind spot or shared flawed input, not independent confirmation).

> **HALLUCINATION WARNING:** **Adding more agents does not automatically increase accuracy.** Every failure mode above scales with the number of agents and hand-offs, not just the potential benefits — a poorly-orchestrated eight-agent system can be less reliable than a well-designed single agent with good tools, which is the direct architectural justification for §9.21's honest single-vs-multi-agent comparison rather than an automatic assumption that more specialization is always better.

---

# Part VI — Explainability

## 9.25 What Explainability Actually Means

Four genuinely distinct concepts, often blurred together under one word:

- **Model interpretability** — understanding *how a model's internals* produce a given output (e.g., which weights, which architecture).
- **Explanation** — communicating *why a conclusion was reached*, in terms a human can act on, independent of exposing model internals.
- **Evidence provenance** — showing *where the evidence itself came from* (§9.18).
- **Causal explanation** — explaining the actual *physical mechanism* connecting cause to effect (Chapter 7 §7.13).

This project's design (Understanding Report §H) deliberately prioritizes **explanation + evidence provenance + causal explanation** over deep **model interpretability** — a technician needs to know *why the system believes what it believes and on what evidence*, not the internal weight structure of whatever model produced the belief.

## 9.26 SHAP and LIME

*[MODEL KNOWLEDGE]* Two established feature-attribution techniques: **SHAP** (Shapley Additive exPlanations) and **LIME** (Local Interpretable Model-agnostic Explanations) both estimate how much each input feature contributed to a specific model output — SHAP via a game-theoretic attribution method, LIME by approximating the model's local behavior around one specific prediction with a simpler, interpretable model. Both support **local explanation** (why this specific prediction) and, with aggregation, some **global interpretation** (which features matter most overall).

**The most important limitation, stated as its own principle: feature importance ≠ causal explanation.** *"Motor current was highly important to this prediction"* does not mean *"motor current caused the failure."* SHAP and LIME describe what the *model* weighted heavily in reaching its output — a statistical/model-internal fact — not a claim about physical causation in the real world (Chapter 7 §7.13's correlation-vs-causation distinction, now at the model-explainability layer specifically). A model could weight motor current heavily because it's genuinely causal, or because it's merely strongly correlated with the true cause (Chapter 1 §1.5's whole "mechanical looks electrical" principle) — SHAP/LIME alone cannot tell these apart.

## 9.27 Counterfactual Explanations

**The question a counterfactual explanation answers:** *"what would need to be different for the conclusion to change?"* Example: *"if brake timing were normal, the probability of brake drag would decrease"* — directly actionable for a technician, since it names a specific, checkable condition. **Why this helps a technician understand diagnostic alternatives:** it reframes an abstract confidence number into a concrete "here's what to check that would change my mind," which is often more useful, practically, than the confidence score itself.

## 9.28 The Structured Explanation Object, and Why Not Chain-of-Thought

Rather than depending on exposing hidden model reasoning (an LLM's raw internal chain-of-thought), this project defines an explicit, **observable** explanation structure: **Observation** (what happened), **Evidence** (what was observed), **Hypothesis** (what cause is being considered), **Supporting evidence**, **Contradicting evidence**, **Alternatives** (what other causes remain live), **Confidence**, **Verification** (what should be checked), and **Source** (where the evidence came from).

**Why hidden chain-of-thought is not the explanation:** an industrial diagnostic system should not depend on a human trusting or parsing a model's private, unstructured internal reasoning trace — that reasoning may be an unreliable narration of the actual computation, is not naturally auditable, and is not a stable interface to build a safety-adjacent system on top of. Instead: **structured evidence + explicit intermediate artifacts + source provenance + validated outputs.** The goal is **auditability**, not access to private internal reasoning — a distinction repeated from the Understanding Report onward and now given its full architectural justification.

---

# Part VII — Confidence, Uncertainty, and the Human Boundary

## 9.29 Confidence

**High confidence does not automatically mean correct.** A confidence score's trustworthiness depends on evidence quantity, evidence quality, consistency across independent sources (Ch.7 §7.16's independence caveat still applies), the reliability of whatever model produced the score, and the reliability of the underlying data sources themselves. This chapter does not go deeply into formal calibration methodology here (reliability diagrams, Brier scores, conformal prediction) — consistent with Chapter 7 §7.30's own deferral, that remains a later phase's dedicated subject.

## 9.30 Diagnosis Confidence vs. Action Confidence

A major, deliberately-maintained distinction. Example: **diagnosis** — "likely brake drag," confidence 0.86. **Action** — "inspect the brake system," confidence 0.94, a *higher* number despite depending on the diagnosis. **Why these are not the same, and should not be forced to match:** "inspect the brake" is a low-risk, broadly-useful action even if the diagnosis turns out wrong (inspection rarely causes harm and often surfaces the true cause anyway) — so *action* confidence can reasonably be higher than *diagnosis* confidence for a conservative, low-risk recommended step. The reverse can also hold: a system might be quite confident in a diagnosis while still recommending low-confidence caution around a specific corrective action, if that action carries real consequences if the diagnosis is wrong. **A system can be relatively confident about a diagnosis while still requiring human verification before any action** — this separation is precisely why Chapter 4 §4.23's "never let the LLM freely invent a maintenance action" principle and this project's human-approval gate (Understanding Report §J) both exist independently of how confident the diagnosis itself is.

## 9.31 Abstention

**"Insufficient evidence" is a legitimate system output, not a failure.** When evidence is genuinely insufficient, the system should request more information or route to human review rather than force a conclusion. **Why forcing a diagnosis can be more dangerous than abstaining:** a confident-sounding wrong conclusion can send a technician toward the wrong repair, wasting time and potentially leaving the true cause unaddressed; an honest "insufficient evidence, recommend further investigation" costs less and misleads no one. This principle, established from the project's own idea proposal onward, is given its full technical justification across this entire research book (Ch.4 §4.16, Ch.7 §7.27/§7.30) and restated here as a first-class AI-architecture requirement, not an afterthought.

## 9.32 Out-of-Distribution Detection

**Known operating conditions vs. unfamiliar ones.** A model trained on data from one elevator family or configuration, encountering a significantly different architecture (a different machine type, a different sensor configuration, an installation the training data never resembled), is operating **out-of-distribution** — a condition where its outputs, including its own confidence scores, become considerably less trustworthy. Relevant concerns: **domain shift** (§9.7's transfer-learning caveat, restated as a runtime detection problem rather than a training-time one), **genuinely novel fault types** not represented in any fault tree this book has built, **new or unfamiliar sensor behavior**, and **a new elevator configuration** the system has no prior experience with. **Why this matters specifically for this project:** a system that cannot recognize when it's operating outside its known scope cannot reliably abstain (§9.31) when it should — OOD detection is, in a real sense, the technical prerequisite that makes principled abstention possible at all, rather than abstention being triggered only by explicit low-confidence signals within a familiar domain.

## 9.33 Human-in-the-Loop

```
AI → Recommendation → Human review → Confirmation/override → Action → Outcome
```

Discussed dimensions: **approval** (the human confirms the AI's conclusion before action), **override** (the human disagrees and substitutes their own judgment), **escalation** (a case is routed to more senior/specialized review), **low-confidence cases** (routed for review by design, per §9.31), **safety-sensitive cases** (routed regardless of confidence, per the safety boundary established throughout this book), and **learning from verified outcomes** (a genuinely valuable future direction — whether and how confirmed/overridden outcomes should feed back into improving future performance — deliberately not designed in depth here, consistent with this chapter's scope boundary against prematurely specifying implementation).

## 9.34 AI Decision Boundaries

| Decision | AI Can Assist | AI Can Recommend | Human Required | Never Autonomous |
|---|---|---|---|---|
| Anomaly detection | ✓ | | | |
| Fault ranking | ✓ | ✓ | | |
| Evidence retrieval | ✓ | | | |
| Diagnostic explanation | ✓ | ✓ | | |
| Inspection recommendation | | ✓ | ✓ (before acting) | |
| Repair recommendation | | ✓ | ✓ (before acting) | |
| Safety-system override | | | | **✓ — never** |
| Passenger rescue decisions | | | | **✓ — never** |
| Brake release | | | | **✓ — never** |
| Safety-chain bypass/reset | | | | **✓ — never** |

**This book provides no operational instructions for defeating, bypassing, or overriding any safety system, and would not do so regardless of how the request were framed** — those four bottom rows are not a design choice this project is weighing; they are a firm, non-negotiable boundary, consistent with every earlier chapter's safety discussion. **The governing architectural principle, restated once more because it governs every diagram in this chapter:**

> **OBSERVE → DIAGNOSE → EXPLAIN → RECOMMEND → HUMAN CONFIRMS.**

---

# Part VIII — Safety and Robustness of the AI Layer Itself

## 9.35 AI Hallucination and Its Mitigations

**Why hallucination is especially dangerous here, specifically:** an industrial diagnostic system's entire value proposition is trustworthy evidence-grounded reasoning; a hallucinated fault code, an invented sensor value, fabricated maintenance history, an invented manual procedure, a fabricated causal relationship, or unsupported confidence doesn't just produce a wrong answer — it produces a *confident-sounding, plausible-looking* wrong answer, which is a materially worse failure mode than an obviously broken one, because it's harder for a technician to catch.

**Mitigations, all already established piecemeal across this chapter and now listed together:** tool-based data access (§9.14 — the LLM retrieves real data rather than recalling from memory), RAG (§9.16 — grounding documentation claims in retrieved sources), structured outputs (§9.13 — enabling programmatic validation), source citations (§9.18), deterministic calculations for anything numerically precise (§9.1's table), contradiction checks (Chapter 7 §7.24's expected-vs-observed evidence testing), and — the last line of defense, always available — abstention (§9.31) and human review (§9.33).

## 9.36 Prompt Injection and RAG Security

**The concept, explained carefully:** a malicious or accidentally-corrupted document, retrieved as part of the RAG pipeline (§9.17), could contain text specifically crafted to manipulate an LLM's behavior when that text is included in the model's context — attempting to make the model ignore its actual task, follow embedded instructions instead of the user's, or leak information it shouldn't. This is called **prompt injection**; when the malicious content arrives via retrieved documents rather than the direct user input, it's specifically termed **indirect prompt injection**. A **poisoned knowledge base** is the broader version of this risk — a document corpus deliberately or accidentally seeded with content designed to manipulate future retrieval and reasoning.

**The core defense, stated as a principle:** **retrieved documents must always be treated as data, never as unquestioned instructions.** A maintenance manual, a fault-code description, or a technician note retrieved by the RAG pipeline should inform the model's *reasoning about the diagnostic problem* — it should never be interpreted as a new instruction overriding the model's actual task, its safety constraints, or its structured-output requirements. **This book provides no offensive exploitation detail** — the discussion here is strictly the defensive architectural principle a real system needs, not a guide to constructing an injection attack.

## 9.37 What Not to Build

Restating and consolidating this book's safety boundary at the AI-architecture layer specifically, one final time: this project does **not** design autonomous elevator control, autonomous safety override, autonomous brake control, safety-chain bypass, passenger-rescue automation, or unrestricted autonomous repair authorization. **Why these sit outside the diagnostic-intelligence scope, not merely deferred to a later phase:** every one of them requires the AI layer to take real-world, physically consequential action without a human confirming it first — directly violating the OBSERVE → DIAGNOSE → EXPLAIN → RECOMMEND → HUMAN CONFIRMS boundary that governs this entire book, not a capability this project intends to add once the technology matures.

---

# Part IX — Putting It Together: Architecture

## 9.38 Tool-Based Architecture

```
                 ┌── Telemetry Tool               (Ch.6)
                 │
                 ├── Alarm/Event Tool              (Ch.4)
                 │
                 ├── Maintenance History Tool        (Ch.5 §5.16)
                 │
  Orchestrator ──┼── Documentation/RAG Tool            (§9.16–§9.19)
                 │
                 ├── Fault Tree / FMEA Tool               (Ch.7 §7.7–§7.8)
                 │
                 ├── Signal Analysis Tool                   (Ch.6)
                 │
                 └── Knowledge Graph Tool                    (§9.10)
```

```
Evidence → Diagnostic reasoning → Structured conclusion → Explainability → Human review
```

No specific production APIs are defined here — this is a conceptual tool inventory, mapping each tool back to the chapter of this book that established the underlying method it wraps, deliberately left at that level of abstraction.

## 9.39 The Multi-Agent Diagnostic Workflow

| Stage | Input | Process | Output | Failure Mode | Validation Requirement |
|---|---|---|---|---|---|
| Incident | Raw alarm/anomaly | — | A triggered investigation | Missed trigger | Threshold review (Ch.6) |
| Signal Triage | Telemetry, alarms | Anomaly detection (Ch.6) | Confirmed abnormal condition | False positive/negative (Ch.6 §8.34) | Cross-check against independent signals |
| Orchestrator | Triaged signal | Plan the investigation (§9.15) | An ordered evidence-gathering plan | Poor sequencing | Compare against the relevant fault tree |
| Retrieval | The plan | Query tools/RAG (§9.14, §9.17) | Retrieved evidence + documentation | Wrong/stale retrieval (§9.19) | Source-grounding check (§9.18) |
| Fault Isolation | Retrieved evidence | Subsystem-level narrowing (Ch.4 §4.7) | A narrowed subsystem scope | Premature narrowing | Cross-check against the full fault tree, not just the leading branch |
| RCA | Isolated scope + evidence | Hypothesis testing, Bayesian updating (Ch.7) | A ranked, evidence-linked hypothesis set | Overconfidence, double-counting (Ch.7 §7.16) | Independent-evidence check |
| Evidence Verification | The ranking | Contradiction search (Ch.7 §7.25) | Confirmed or flagged ranking | Missed contradiction | Explicit "what would disconfirm this" check |
| Synthesis | Verified ranking | Convert to dual-audience output (Understanding Report §C) | Technician + manager views | Inconsistent framing between views | Both views traced to the same evidence object |
| Explanation | The synthesis | Build the structured trace (§9.23, §9.28) | An auditable ExplainabilityTrace | Incomplete trace | Every claim has a cited source |
| Human Review | The trace | Technician confirms/overrides | An approved (or rejected) conclusion | Rubber-stamping without genuine review | The trace must be genuinely inspectable, not just present |

## 9.40 Worked Example 1: Motor Overcurrent, End to End

**Input:** a motor overcurrent alarm. The system receives: the alarm itself, event chronology, motor current, vibration, speed, temperature, drive diagnostics, and maintenance history. **All data below is hypothetical/illustrative — no real production KONE result is claimed.**

- **Signal Triage:** confirms the current reading is genuinely abnormal (Ch.6 §8.25's methods), not a sensor artifact.
- **Orchestrator:** identifies the required evidence set, per §9.15's planning pattern — chronology, vibration, brake state, drive self-test, load, maintenance history.
- **Retrieval:** pulls the relevant fault-tree branch (Ch.7 §7.7.1), FMEA entries, and any documentation on this specific fault-code family.
- **Fault Isolation:** compares candidate subsystems — motor, brake, drive, cable, load, configuration — narrowing based on the retrieved evidence's early pattern (e.g., vibration present, drive self-test clean, narrowing away from the drive/IGBT branch specifically).
- **RCA:** evaluates mechanical obstruction, brake drag, motor winding fault, drive/IGBT fault, cable issue, and excessive load against the full evidence set, using Chapter 7 §7.15's Bayesian framework.
- **Evidence Verification:** actively checks for contradicting evidence against the leading hypothesis, not just supporting evidence (Ch.7 §7.25).
- **Synthesis:** ranks the causes and drafts both the technician-facing and manager-facing views from the same underlying evidence.
- **Explainability:** presents the full evidence trace — what was observed, what was checked, why the leading hypothesis is favored, what alternatives remain live.
- **Human:** the technician reviews the trace, physically verifies (Ch.7 §7.31's final loop stage), and either confirms or overrides before any repair proceeds.

## 9.41 Worked Example 2: Door Failure, End to End

**Input:** a door failure alarm, with door-cycle telemetry, door-motor current, position, photo-eye events, lock state, cycle time, and historical failure records. **Again, hypothetical/illustrative data only.**

```
Anomaly (repeated reopening pattern, Ch.6 §8.14)
   → Evidence (photo-eye state instability across many cycles, not one)
   → Retrieval (Ch.4 §4.9's differential fault tree, Ch.7 §7.7.2)
   → Hypotheses (photo-eye degradation, genuine obstruction, roller/belt/motor,
      encoder, lock/interlock, controller/electrical)
   → Ranking (photo-eye degradation favored, per the multi-event pattern —
      Ch.7 §7.33's own worked example reaches the same structural conclusion)
   → Explanation (the specific instability pattern shown as the deciding evidence)
   → Human verification (physical photo-eye alignment/cleaning check)
```

This example deliberately reuses Chapter 7 §7.33's underlying reasoning, now shown running through this chapter's full AI-architecture pipeline rather than as a standalone RCA walkthrough — the same conclusion, reached the same way, now demonstrably produced by the actual multi-agent workflow this chapter specifies rather than narrated directly.

## 9.42 Multi-Signal Reasoning, Revisited at the AI Layer

Current↑ alone is weak evidence — consistent with too many of Chapter 7 §7.7.1's nine candidate causes to be useful on its own. Current↑ + vibration↑ + abnormal acceleration + normal drive diagnostics + abnormal brake timing is materially stronger evidence for a mechanical/brake hypothesis specifically — not because there are simply "more signals," but because this particular combination is inconsistent with several competing hypotheses (Ch.7 §7.25's alternative-elimination logic) while remaining consistent with few. **The AI layer should reason over multiple independent, or appropriately-modeled-as-dependent, evidence sources** — restating Chapter 7 §7.16's correlation-aware caution one final time: the system must not blindly assume every additional signal is an independent confirmation just because it's an additional data point.

## 9.43 How AI Complements — Not Replaces — Bayesian Reasoning, Fault Trees, and Knowledge Graphs

**AI + Bayesian reasoning:** a dedicated probabilistic model calculates and updates hypothesis probabilities (Ch.7 §7.14–§7.16); the LLM interprets documentation, plans the investigation (§9.15), summarizes evidence, and explains results in plain language. **An LLM is not a Bayesian calculator** — asking a language model to freely generate a posterior probability, rather than computing it via a defined probabilistic model, reintroduces exactly the fabrication risk §9.1's table and §9.35 exist to prevent.

**AI + fault tree:** the fault tree (Ch.7 §7.7) defines the possible causal paths structurally; the AI's job is to select the relevant branches given the observed alarm, retrieve evidence for each, evaluate the hypotheses the tree already enumerates, and explain the resulting conclusion — not to invent a hypothesis space from scratch each time.

```
Top event (fault tree) → Candidate branches → Evidence requirements
   → Retrieved evidence → Branch elimination/ranking (AI-assisted, tree-structured)
```

**AI + knowledge graph:** the knowledge graph represents engineering relationships explicitly (§9.10); the AI queries and interprets those relationships rather than reconstructing them from memory each time — e.g., traversing Motor → Drive → Traction → Rope → Car to understand which components sit "upstream" of a given symptom, a structural fact the graph encodes once and the AI reuses repeatedly, rather than re-deriving.

**AI + RAG + telemetry, the complete evidence architecture:**

```
Real-time data + Historical data + Engineering knowledge + Documentation + Maintenance history
        ↓
Retrieval / Analytics (Chapters 6, this chapter's §9.16–§9.19)
        ↓
Structured evidence (Chapter 6 §8.47, this chapter's §9.13/§9.23)
        ↓
AI reasoning (this chapter, Parts III–VII)
        ↓
Explainable RCA (Chapter 7's reasoning, given a full evidence-and-explanation architecture)
```

## 9.44 What Should Be Deterministic, Probabilistic, and Human

**Deterministic:** unit conversion, signal calculations (Ch.6), timestamps, threshold checks, statistical calculations, fault-tree logic traversal, database queries, source citation, and — absolutely — safety constraints. **These should never be delegated to an LLM unnecessarily** — not because an LLM cannot approximate them, but because a deterministic implementation is exact, fast, and trivially auditable, while an LLM approximation of the same task introduces avoidable uncertainty for no corresponding benefit.

**Probabilistic:** hypothesis ranking, handling of genuinely uncertain evidence, anomaly scores, diagnosis confidence, and the comparison of competing causes. **Uncertainty here is part of the problem itself**, not a limitation to be engineered away — Chapter 7's entire Bayesian apparatus exists because the true state of the elevator genuinely cannot be known with certainty from available evidence alone, in general.

**Human:** safety-sensitive decisions, genuinely ambiguous diagnoses, physical inspection, final repair authorization, unusual/novel faults (§9.32's OOD case), and any low-confidence case (§9.31). **Human expertise remains essential** not as a stopgap for an immature system, but as a structural, permanent feature of a responsibly-scoped one — this project's stated safety boundary, restated one final time at the close of the architecture discussion.

## 9.45 The Complete Architectural Principle

```
PHYSICAL ELEVATOR
        ↓
Sensors → Controller → Connectivity → Data Platform
        ↓
Signal Processing (Ch.6)
        ↓
Anomaly Detection (Ch.6)
        ↓
Event / Alarm Correlation (Ch.4, Ch.6)
        ↓
Structured Evidence (Ch.6 §8.47)
        ↓
Engineering Knowledge Layer — FMEA / Fault Trees / Knowledge Graphs (Ch.7, §9.10)
        ↓
RCA / Probabilistic Reasoning (Ch.7)
        ↓
AI Orchestration (this chapter, Parts III–V)
        ↓
RAG / Tools (§9.14, §9.16–§9.19)
        ↓
Hypothesis Evaluation (Ch.7 + this chapter, together)
        ↓
Explainable Diagnosis (Part VI)
        ↓
Human Review (Part VII)
        ↓
Maintenance Action
        ↓
Verified Outcome
        ↓
Historical Knowledge  (feeds back into future evidence, Ch.5 §5.16)
```

**Why none of the individual technologies discussed in this chapter, alone, constitutes the complete solution:** every layer above depends on the layer beneath it having done its job correctly — a brilliant LLM reasoning over corrupted telemetry produces a confidently wrong answer; a perfect signal-processing pipeline feeding no reasoning framework produces clean data with no conclusion; a rigorous Bayesian model with no retrieval layer has no documentation to ground its reasoning in; explainability with no underlying evidence trace has nothing genuine to explain. **This is a pipeline of dependencies, not a menu of independently-sufficient options.**

---

# Part X — Honesty and Validation

## 9.46 Novelty Analysis

Is this proposed architecture merely another dashboard, another predictive model, another chatbot, another RAG system, or another multi-agent system? Chapter 6's competitive-landscape research already answered this precisely (Ch.6 §6.10, §6.18): every individual technology category named in that question is confirmed to exist at one or more of the four major OEMs researched. **The specific diagnostic contribution this chapter's architecture aims at is narrower and more checkable**: evidence-linked RCA (§9.18, Ch.7), structured causal reasoning (Ch.7, §9.43), primary/consequential alarm reasoning (Ch.4, Ch.6 §8.22), explicit alternative-cause elimination (Ch.7 §7.25, §9.42), explicit contradiction handling (§9.39's Evidence Verification stage), diagnostic provenance (§9.18, §9.23), calibrated confidence with diagnosis/action separation (§9.30), abstention (§9.31), and structured human verification (§9.33). **None of these are automatically claimed as unique** — each is, more precisely, **potential differentiation requiring validation**, per Chapter 6's own explicit research methodology, against real KONE SME review and, eventually, real data.

## 9.47 AI System Failure Modes

| Failure Mode | Example | Consequence | Mitigation |
|---|---|---|---|
| Hallucination | Invented fault-code meaning | Wrong diagnosis, technician misdirected | Tool-based access, RAG, structured outputs (§9.35) |
| Wrong retrieval | Irrelevant document surfaced | Diluted or misleading context | Hybrid retrieval + reranking (§9.17) |
| Missing evidence | A key signal wasn't queried | Incomplete hypothesis testing | Orchestrator planning discipline (§9.15, §9.22) |
| Bad telemetry | Sensor dropout treated as "normal" | False confidence in a wrong hypothesis | Ch.6 §8.5's signal-quality checks, upstream of this chapter entirely |
| Incorrect hypothesis | A plausible but wrong leading cause | Wrong repair attempted | Alternative-cause elimination (§9.42), human verification (§9.33) |
| False confidence | An overconfident score on thin evidence | Technician trusts an unverified conclusion | Calibration discipline (§9.29), correlated-evidence awareness (§9.42) |
| Confirmation bias (agent-level) | A later agent accepts an earlier agent's framing uncritically | Errors compound rather than get caught | Independent evidence-verification stage (§9.39) |
| Agent disagreement | Two agents reach different conclusions | Ambiguous system output | Surfaced explicitly, not silently resolved (§9.24) |
| Stale documentation | An outdated manual retrieved and trusted | Wrong or outdated procedure recommended | Source-grounding with version/timestamp (§9.18) |
| Sensor anomaly mistaken for equipment fault | A degrading sensor read as a real fault | Unnecessary component replacement | Independent-signal cross-checking (Ch.6 §8.15, Ch.7 §7.34) |
| Model/distribution drift | Performance degrades as real conditions diverge from training data | Silently declining reliability | OOD detection (§9.32) |
| Prompt injection | A malicious document manipulates model behavior | Compromised or misdirected reasoning | Treat retrieved content as data, never instructions (§9.36) |
| RAG poisoning | A corrupted knowledge base systematically biases retrieval | Persistent, hard-to-detect diagnostic errors | Source vetting, provenance tracking (§9.18) |
| Unsupported maintenance recommendation | A freely-generated repair instruction that isn't a real, verified procedure | Potential safety or equipment risk | Never let the LLM freely invent an action (Ch.4 §4.23) — ground every recommendation in retrieved, verified procedures |

## 9.48 Validation Requirements

**An AI diagnostic system cannot be validated merely by "the LLM gave a convincing answer."** Future validation dimensions, named but not yet developed into a full evaluation framework here (consistent with this chapter's scope): evidence correctness, retrieval correctness, fault-isolation accuracy, root-cause accuracy, top-k accuracy, explanation correctness, citation correctness, hallucination rate, confidence calibration, abstention behavior, and technician usefulness. Several of these already have named precedent in this book's earlier metrics discussion (Understanding Report §K) — this section restates them specifically as AI-architecture validation requirements, distinct from the general project-level metrics already established.

## 9.49 Research Gaps

Lack of public elevator datasets and limited labeled fault data (§9.7, confirmed repeatedly by the real academic literature surveyed in Part II); proprietary OEM information (Ch.4 §4.23); uncertain real-world causal probabilities (Ch.7 §7.40); limited benchmark datasets for this specific problem; genuine difficulty validating rare faults without real field data; limited public evidence of any OEM performing fully autonomous, structured elevator RCA (Ch.6 §6.11's own finding, restated here); open challenges in multi-agent reliability generally (§9.24); hallucination risk (§9.35); uncertainty calibration (§9.29, deferred formally to a later phase); and domain transfer (§9.7, §9.32). **Known:** the methods and their trade-offs, taught throughout this chapter, each grounded in either established AI/ML practice or real, cited academic literature. **Unknown:** their real-world calibrated performance on actual KONE equipment. **Assumed:** a modern gearless traction elevator's general characteristics, consistent throughout this book. **Proposed:** the specific architecture this chapter lays out — a design under evaluation, not a confirmed result.

---

# Judge Questions

**1. Why do you need AI?** *Short:* Heterogeneous, high-dimensional, unstructured evidence exceeds what deterministic rules can practically enumerate (§9.1). *Detailed:* §9.1's table shows exactly which problem rows justify it. *Evidence:* — *Assumptions:* — *Tested:* Whether AI is justified per-task, not assumed globally. *Avoid:* "AI is powerful" without the specific task-fit argument.

**2. Why can't rules solve this?** *Short:* Rules work for fault-tree traversal and threshold checks; they don't scale to free-text interpretation or the full multivariate hypothesis space (§9.1). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether rules are dismissed wholesale (wrong) or scoped precisely (right). *Avoid:* Claiming rules have no place — they remain core to §9.44's deterministic layer.

**3. Why do you need an LLM specifically?** *Short:* For language tasks — document interpretation, explanation, planning — not numerical computation (§9.11–§9.12). *Detailed:* §9.12's table. *Evidence:* — *Assumptions:* — *Tested:* Precise task-scoping. *Avoid:* "LLMs are smart" as the whole answer.

**4. What exactly does the LLM do?** *Short:* Summarizes, interprets documentation, generates hypotheses from a defined space, explains conclusions, plans investigation steps (§9.12). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Specificity. *Avoid:* Vagueness.

**5. What does the LLM NOT do?** *Short:* Raw signal math, exact probabilities, safety decisions, autonomous control, inventing evidence (§9.12). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the boundary is as clear as the capability list. *Avoid:* Hedging on any of the five.

**6. Why use RAG?** *Short:* An LLM's training memory can't contain KONE's actual current documentation; retrieval grounds claims in real, verifiable sources (§9.16). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "grounding" is understood, not just "RAG is standard practice." *Avoid:* Citing RAG as a buzzword.

**7. Why not fine-tune the model instead?** *Short:* Fine-tuning bakes in a fixed snapshot of knowledge; RAG allows documentation to update without retraining, and grounds specific claims traceably (§9.16–§9.18). *Detailed:* — *Evidence:* — *Assumptions:* Fine-tuning and RAG are not mutually exclusive in general — this is about which handles document-grounding better. *Tested:* Whether the trade-off is understood, not just "RAG is what we chose." *Avoid:* Implying fine-tuning is never useful.

**8. Why use tools?** *Short:* So precise operations are computed exactly, not approximated by generation (§9.14). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "hallucinated calculation" risk is named specifically. *Avoid:* A generic "tools help."

**9. Why use multiple agents?** *Short:* Specialization and debuggability for a problem with genuinely distinct reasoning stages (§9.21). *Detailed:* — *Evidence:* — *Assumptions:* Justified by task structure, not assumed superior by default. *Tested:* Whether the honest trade-off table is cited, not just the benefit. *Avoid:* "More agents = better."

**10. Why not one agent?** *Short:* A single agent is viable and lower-cost/lower-latency; multi-agent is chosen specifically where specialization outweighs coordination overhead (§9.21). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether single-agent is dismissed unfairly. *Avoid:* Treating single-agent as automatically inferior.

**11. Does more agents mean better accuracy?** *Short:* No (§9.24's HALLUCINATION WARNING). *Detailed:* Every failure mode in §9.24 scales with agent count. *Evidence:* — *Assumptions:* — *Tested:* Direct contradiction of a common assumption. *Avoid:* Any hedge toward "generally, yes."

**12. How do agents communicate?** *Short:* Through structured investigation state (§9.23), not free-form text hand-offs. *Detailed:* The CASE object's fields. *Evidence:* — *Assumptions:* — *Tested:* Whether "structured, not prose" is understood as a deliberate choice. *Avoid:* Implying agents just chat with each other.

**13. How do you prevent hallucination?** *Short:* Tool-based access, RAG, structured outputs, citations, deterministic math, contradiction checks, abstention (§9.35). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether multiple layered mitigations are named, not one silver bullet. *Avoid:* "We use RAG so hallucination is solved."

**14. How do you validate retrieved documents?** *Short:* Source grounding with version/timestamp metadata; reranking for relevance (§9.17–§9.18). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether provenance tracking is concrete. *Avoid:* Assuming retrieval is always correct.

**15. What if the documentation itself is wrong?** *Short:* The system can be no better than its sources — this is a real, named limitation (§9.19), not solved by architecture alone. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Honesty about this residual risk. *Avoid:* Claiming the system can detect all document errors.

**16. What if telemetry is missing?** *Short:* Distinguished from a true negative, never silently filled in (Ch.6 §8.5, Ch.7 §7.26). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Cross-chapter consistency. *Avoid:* Fabricating missing values.

**17. What if the sensor itself is faulty?** *Short:* Cross-checked against independent signals where possible (Ch.6 §8.15, Ch.7 §7.34). *Detailed:* — *Evidence:* — *Assumptions:* Not always resolvable. *Tested:* Whether this is acknowledged as genuinely hard. *Avoid:* Implying a guaranteed detection method.

**18. What if evidence conflicts?** *Short:* Surfaced explicitly; "insufficient evidence" is a valid outcome, not forced resolution (§9.27, Ch.7 §7.27). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether abstention is the reflexive answer. *Avoid:* Implying conflicts are always resolved somehow.

**19. What if two faults occur simultaneously?** *Short:* Multiple, separately-tracked hypothesis spaces can be retained (Ch.7 §7.28). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "one incident, one cause" is avoided as an assumption. *Avoid:* Assuming single-cause by default.

**20. What if the model encounters an unknown fault?** *Short:* OOD detection should flag this and trigger abstention/escalation (§9.32). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether novel-fault handling is a designed case, not an unhandled edge. *Avoid:* Implying the fault-tree coverage is exhaustive.

**21. Can the system abstain?** *Short:* Yes, explicitly and by design (§9.31). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Confidence in defending this as a strength. *Avoid:* Apologizing for it.

**22. How is confidence calculated?** *Short:* From evidence quantity/quality/consistency, via a defined probabilistic model, not LLM free generation (§9.29, §9.43). *Detailed:* — *Evidence:* — *Assumptions:* Full calibration methodology deferred to a later phase. *Tested:* Whether "the LLM says how confident it is" is avoided as the answer. *Avoid:* That exact wrong answer.

**23. Can an LLM calculate Bayesian probabilities reliably?** *Short:* Not relied upon to — a dedicated probabilistic model does the calculation (§9.43). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "LLM ≠ Bayesian calculator" is stated plainly. *Avoid:* Any answer suggesting the LLM does this math itself.

**24. Why not use a dedicated probabilistic model instead of an LLM for this?** *Short:* Both are used, for different jobs — probabilistic model for the math, LLM for language and planning (§9.43). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is framed as "both," not "either/or." *Avoid:* Presenting it as a single-technology choice.

**25. Why use fault trees?** *Short:* They define the hypothesis space the AI reasons within, rather than letting the AI invent one each time (§9.43, Ch.7 §7.7). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether fault trees are understood as a constraint on AI, not decoration. *Avoid:* Treating fault trees as optional.

**26. Why use knowledge graphs?** *Short:* Explicit, queryable representation of engineering relationships the AI reuses rather than re-derives (§9.10). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the graph-vs-GNN distinction (§9.10) is retained. *Avoid:* Conflating knowledge graphs with GNNs.

**27. Why use GNNs?** *Short:* Elevator systems are structurally graphs; a real 2024 paper (§9.3) demonstrates a GNN-based approach for exactly this problem. *Detailed:* The e-RGCN/PINN combination specifically. *Evidence:* [ACADEMIC EVIDENCE] — §9.3. *Assumptions:* — *Tested:* Whether a real citation, not a hypothetical, backs the claim. *Avoid:* Presenting GNNs as untested speculation when real evidence exists.

**28. Why use digital twins?** *Short:* Potentially valuable for scenario simulation and synthetic-data generation given real data scarcity — not claimed as required (§9.9). *Detailed:* When useful vs. unnecessary complexity, stated explicitly. *Evidence:* — *Assumptions:* — *Tested:* Whether digital twins are defended as optional, evidenced, not assumed mandatory. *Avoid:* Claiming the system requires one.

**29. Why use PINNs?** *Short:* To inject known physics (Ch.1) into a model, addressing data scarcity directly — a real, cited elevator application exists (§9.3, §9.9). *Detailed:* — *Evidence:* [ACADEMIC EVIDENCE] *Assumptions:* — *Tested:* Whether the physics-injection mechanism, not just the acronym, is understood. *Avoid:* Naming PINNs without explaining what "physics-informed" actually means.

**30. Why use sensor fusion?** *Short:* Multivariate evidence discriminates between hypotheses in ways single signals structurally cannot (§9.8, §9.42). *Detailed:* Independently confirmed by the general RUL literature surveyed in §9.6. *Evidence:* [ACADEMIC EVIDENCE] *Assumptions:* — *Tested:* Whether this connects back to Ch.7's Bayesian framework. *Avoid:* "More data is always better" as the whole justification.

**31. Why use time-series models specifically?** *Short:* Because elevator diagnostic evidence is inherently sequential — trajectory, not just snapshot value, carries information (Ch.6 §8.1, §9.28's LSTM-AE discussion). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the gradual-vs-sudden distinction is cited as the concrete payoff. *Avoid:* A generic answer without that example.

**32. How do you distinguish anomaly from fault?** *Short:* Anomaly detection flags deviation; fault detection requires matching a recognized failure pattern (Ch.6 §8.35). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this survives repetition across chapters. *Avoid:* Treating them as synonyms.

**33. How do you distinguish fault from root cause?** *Short:* A fault is a detected category; a root cause is the specific, evidence-weighed explanation of why it occurred (Ch.4 §4.1, Ch.7 §7.1). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same discipline, one level deeper. *Avoid:* Conflating detection with explanation.

**34. How do you prevent correlation from becoming false causation?** *Short:* Every causal claim is checked against a known physical mechanism (a causal graph), not accepted on temporal proximity alone (Ch.7 §7.13, §9.26's SHAP caveat). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is defended even at the model-explainability layer, not just the alarm-correlation layer. *Avoid:* A single-layer answer that misses the SHAP/LIME angle.

**35. How do you verify the AI's diagnosis?** *Short:* Structured evidence verification (§9.39) plus mandatory human physical confirmation (§9.33) before any action. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "verification" names a real stage, not a formality. *Avoid:* Implying the AI's own conclusion is self-validating.

**36. How does a technician trust the result?** *Short:* Through the full evidence trace (§9.23, §9.28), reviewable before acting, not a bare assertion. *Detailed:* — *Evidence:* — *Assumptions:* Trust must still be earned through real-world validation, not assumed from design intent alone. *Tested:* Whether "designed to be trustworthy" and "proven trustworthy" are kept distinct. *Avoid:* Assuming trust is automatic.

**37. What happens at low confidence?** *Short:* Abstention, request for more evidence, or human escalation (§9.31, §9.33). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is the immediate, confident answer. *Avoid:* Hesitation.

**38. What happens when the AI is wrong?** *Short:* Human review and physical verification are designed to catch it before action (§9.33); this remains a real, residual risk this book does not claim is eliminated. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Honesty about residual risk. *Avoid:* Claiming the architecture makes error impossible.

**39. Can the AI make repair decisions?** *Short:* No — it recommends; a human authorizes (§9.34). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Firmness on this boundary. *Avoid:* Any hedge.

**40. Can it override safety systems?** *Short:* Never (§9.34, §9.37). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Same firmness, higher stakes. *Avoid:* Any hedge whatsoever.

**41. What happens if a retrieved document contains malicious instructions?** *Short:* Retrieved content is always treated as data, never as instructions to follow (§9.36). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the data-vs-instruction distinction is stated precisely. *Avoid:* Vague reassurance without the specific principle.

**42. How do you prevent prompt injection?** *Short:* Same answer as Q41 — architectural separation of retrieved content from instruction-following (§9.36). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency with Q41. *Avoid:* A different, less precise answer than Q41's.

**43. How do you prevent RAG poisoning?** *Short:* Source vetting and provenance tracking (§9.18, §9.36) — a defense, not a guarantee. *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this is honestly framed as risk-reduction, not elimination. *Avoid:* Overclaiming a solved problem.

**44. How do you prevent agent confirmation bias?** *Short:* An explicit, independent Evidence Verification stage, not a later agent simply trusting an earlier one (§9.24, §9.39). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a specific architectural mitigation is named. *Avoid:* "We tell the agents to be careful."

**45. How do you audit the diagnosis?** *Short:* Via the structured evidence trace — every claim traceable to a source (§9.18, §9.23, §9.28). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether "auditability" is a concrete mechanism, not an aspiration. *Avoid:* Vague appeals to "transparency."

**46. How do you trace evidence to the conclusion?** *Short:* CLAIM → EVIDENCE → SOURCE → TIMESTAMP/VERSION, for every claim (§9.18). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the specific chain is named. *Avoid:* A generic "we keep records."

**47. What makes the system different from a chatbot?** *Short:* Structured, tool-grounded, multi-stage reasoning over verified evidence, not free-form conversation (§9.13, §9.28). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether the architectural distinction, not just tone, is named. *Avoid:* "It's more sophisticated" without specifics.

**48. What makes it different from predictive maintenance?** *Short:* Predictive maintenance forecasts future risk; this explains an already-occurred fault's cause (Ch.3 §5.14, §9.6). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Consistency across the whole book on this exact distinction. *Avoid:* Any drift from the established answer.

**49. What makes it different from existing OEM AI systems?** *Short:* Per Ch.6's research, the specific reasoning-structure capabilities (§9.46's list) are not publicly demonstrated anywhere researched, including at KONE, Otis, Schindler, or TK Elevator. *Detailed:* — *Evidence:* Ch.6's entire competitive-landscape chapter. *Assumptions:* — *Tested:* Whether Ch.6's research is genuinely internalized here, not re-derived weakly. *Avoid:* A weaker answer than Ch.6 §6.19 already gives.

**50. What is the genuinely difficult technical problem you are solving?** *Short:* Calibrating honest confidence and correctly deciding when to abstain, without labeled production data (Ch.7 §7.39, §9.29). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether a real, unsolved problem is named, not a solved one dressed up as hard. *Avoid:* Naming something trivial.

**51. What happens when there is insufficient data?** *Short:* Favor methods addressing scarcity directly — few-shot/meta-learning, transfer learning, physics-informed methods, synthetic data (§9.7, §9.9). *Detailed:* Real, cited papers (§9.3–§9.7) exist specifically because this is a field-wide constraint, not unique to this project. *Evidence:* [ACADEMIC EVIDENCE] *Assumptions:* — *Tested:* Whether this is framed as a known, actively-researched field problem, not a project-specific excuse. *Avoid:* Presenting data scarcity as solved.

**52. How do you test without production KONE data?** *Short:* Physics-grounded synthetic scenarios (Understanding Report §K); a 2024 paper (§9.9) demonstrates exactly this approach — multibody-dynamics simulation plus real healthy-state data — for elevator damage detection specifically. *Detailed:* — *Evidence:* [ACADEMIC EVIDENCE] *Assumptions:* — *Tested:* Whether a real precedent, not just an assertion, backs the approach. *Avoid:* Presenting synthetic testing as self-evidently sufficient without the precedent.

**53. How do you validate synthetic data?** *Short:* By checking the reasoning process behaves correctly given known-designed scenarios — never presented as production accuracy validation (Ch.6 §8.42). *Detailed:* — *Evidence:* — *Assumptions:* — *Tested:* Whether this caveat is volunteered unprompted, as it has been at every prior chapter. *Avoid:* Blurring demonstration and validation, the single most repeated caution in this book.

**54. How do you handle different elevator models?** *Short:* Domain-shift and OOD detection are explicitly named concerns (§9.7, §9.32), not assumed away. *Detailed:* — *Evidence:* — *Assumptions:* This book's scope is explicitly a modern gearless traction elevator (Ch.1's stated decision). *Tested:* Whether the scope limitation is acknowledged unprompted. *Avoid:* Claiming universal applicability across all elevator types.

**55. How does the system know when it does not know?** *Short:* OOD detection plus calibrated, evidence-based confidence plus abstention, working together (§9.29, §9.31, §9.32). *Detailed:* This is arguably the single most important question in the entire research book, and the answer should be immediate. *Evidence:* — *Assumptions:* — *Tested:* The final, cumulative check on whether the abstention principle — introduced in the project's own idea proposal and defended in every chapter since — is genuinely load-bearing. *Avoid:* Any hesitation at all.

---

# Master AI Capability Matrix

| Capability | Best Technology | Input | Output | Why Used | Limitation | Validation Requirement |
|---|---|---|---|---|---|---|
| Signal processing | Deterministic + statistical (Ch.6) | Raw telemetry | Cleaned features | Exact, fast, auditable | Doesn't reason about cause | Standard signal-processing validation |
| Anomaly detection | Statistical baseline first; ML/DL if justified (Ch.6) | Features | Anomaly score | Flags deviation without needing labels | Anomaly ≠ fault | Precision/recall against known scenarios |
| ML classification | Vibration/door-specific models (§9.3–§9.4) | Engineered features | Fault-category label | Real academic precedent | Data-hungry, needs careful validation | Held-out test accuracy |
| Probabilistic reasoning | Bayesian model (Ch.7) | Multi-source evidence | Ranked hypotheses + confidence | Principled uncertainty handling | Requires correlation-aware modeling | Calibration testing (deferred) |
| Fault trees / FMEA | Deterministic knowledge base (Ch.7) | Engineering knowledge | Structured hypothesis space | Exact, auditable, reusable | Static — doesn't adapt to novel faults alone | SME review |
| Knowledge graph | Structured relational store (§9.10) | Engineering relationships | Queryable graph | Explicit, no training needed | Manual construction effort | Consistency checking |
| GNN | Learned graph model (§9.3, §9.10) | Graph-structured data | Learned relational patterns | Real cited elevator precedent | Needs training data | Held-out validation |
| Digital twin | Simulated synchronized model (§9.9) | Physical + simulated state | Scenario predictions | Addresses data scarcity | Optional, not required | Simulation-vs-reality comparison |
| PINN | Physics-constrained model (§9.9) | Data + physical laws | Physically-plausible predictions | Real cited elevator precedent | Requires accurate physics formulation | Physics-consistency checking |
| LLM | Language model (§9.11) | Structured evidence, documentation | Explanation, hypotheses, plans | Language understanding, flexibility | No inherent knowledge of real elevator state | Structured-output validation |
| RAG | Retrieval + LLM (§9.16–§9.19) | Documents + query | Grounded response | Avoids reliance on model memory | Only as good as retrieval quality | Source-grounding audit |
| Tool calling | LLM + external tools (§9.14) | A defined need for precise data | Structured tool result | Precision without hallucination | Requires well-defined tools | Tool-output correctness |
| Agent orchestration | Planning LLM (§9.15, §9.22) | Case state | Investigation plan | Structures evidence-gathering | Coordination overhead | Plan-vs-fault-tree consistency |
| Multi-agent reasoning | Specialized agent roles (§9.20) | Case state | Distributed reasoning | Specialization, debuggability | Failure modes scale with agent count (§9.24) | Per-agent + end-to-end validation |
| Explainability | Structured trace, not hidden CoT (§9.28) | Full case state | ExplainabilityTrace | Auditability | Requires disciplined implementation throughout | Completeness/citation audit |
| Human review | Qualified technician (§9.33) | The full trace | Confirm/override | Irreplaceable judgment + accountability | Requires a genuinely inspectable trace | N/A — this is the validation step |

# Master Responsibility Matrix

| Task | Deterministic Logic | Statistical Model | ML/DL | Probabilistic Model | LLM | Human |
|---|---|---|---|---|---|---|
| Signal calculations (RMS, FFT, etc.) | ✓ | | | | | |
| Anomaly detection | | ✓ (baseline) | ✓ (if justified) | | | |
| Fault-tree traversal | ✓ | | | | | |
| Knowledge-graph query | ✓ | | | | | |
| Hypothesis generation (from defined space) | | | | | ✓ | |
| Evidence retrieval | ✓ (tool) | | | | ✓ (decides what to retrieve) | |
| Probability update | | | | ✓ | | |
| Contradiction checking | ✓ (structural) | | | ✓ (evidence weighing) | | |
| Document interpretation | | | | | ✓ | |
| Explanation generation | | | | | ✓ | |
| Confidence scoring | | | | ✓ | | |
| Abstention decision | ✓ (threshold logic) | | | ✓ (input) | | |
| Final diagnosis verification | | | | | | ✓ |
| Repair authorization | | | | | | ✓ |
| Safety-system interaction | | | | | | **N/A — never automated** |

**"AI" is not one monolithic component** — this table is the whole chapter's argument made concrete in a single glance: eleven distinct task rows, five genuinely different technology columns, and not one column checked across every row.

---

# What We Now Understand

AI is justified here task-by-task, not assumed wholesale — classical ML and deep learning contribute real, evidenced, elevator-specific fault-classification and RUL capability (Part II's academic literature, not speculation); probabilistic reasoning contributes principled uncertainty handling Chapter 7 already built; knowledge graphs and GNNs contribute explicit and learned relational structure respectively; digital twins and PINNs contribute simulation and physics-grounding, evidenced but optional; LLMs contribute language understanding, planning, and explanation — never raw computation or unilateral action; RAG contributes grounding in real, current, sourced documentation rather than model memory; tools contribute precise, hallucination-resistant data access; agents contribute specialization and auditability, purchased at a real coordination cost that must be justified, not assumed free; explainability contributes a structured, auditable trace rather than access to private model reasoning; confidence contributes honest uncertainty communication, deliberately separated between diagnosis and action; abstention contributes the ability to say "not enough evidence" as a designed strength; and humans contribute the judgment, accountability, and physical verification no part of this architecture is designed to replace.

# The Central Principle

> **THE LLM SHOULD NOT BE THE SOURCE OF TRUTH. IT SHOULD REASON OVER VERIFIED ENGINEERING KNOWLEDGE AND STRUCTURED EVIDENCE OBTAINED FROM TRUSTED SOURCES AND TOOLS.**

Every architectural choice in this chapter — tool calling over free recall, RAG over model memory, structured outputs over free text, a dedicated probabilistic model over LLM-generated probabilities, an explicit evidence trace over hidden chain-of-thought, and mandatory human review before any action — is a specific, separately-justified instance of this one governing rule. The LLM is the architecture's *reasoning and communication layer*, deliberately and permanently kept downstream of *verified fact*, never upstream of it.

# The Final Architectural Chain

```
ENGINEERING KNOWLEDGE + OBSERVED DATA + SIGNAL INTELLIGENCE + CAUSAL REASONING
+ PROBABILISTIC REASONING + RETRIEVED KNOWLEDGE + AI ORCHESTRATION
+ EXPLAINABILITY + HUMAN VERIFICATION
        ↓
TRUSTWORTHY DIAGNOSTIC INTELLIGENCE
```

No single technology surveyed across this chapter's ten Parts constitutes the complete solution on its own — trustworthiness here is an emergent property of the whole dependency chain being sound, link by link, not a property any one sufficiently advanced component could deliver alone.

---

# Bridge to Phase 8 — Safety Engineering, Cybersecurity, Data Architecture & Industrial Deployment

```
What the elevator is → What fails → What signals reveal → How KONE handles the
data → What competitors do → How RCA works → How signals become evidence →
How AI can reason over evidence
```

Now the critical question becomes: **how can such an AI diagnostic system be deployed safely, securely, and reliably around a safety-critical industrial system?** Everything built across Phases 1–7 has assumed, correctly for a research book building its reasoning layer by layer, that the system's outputs reach a human reviewer through some trustworthy channel, and that the AI layer genuinely has no path to safety-critical hardware. Phase 8 must now establish exactly *why* that assumption is sound — deeply researching the relevant safety standards (EN 81-20/50, ASME A17.1/CSA B44, ASME A17.2, ASME A17.4, IEC 61508, IEC 62061, PESSRAL, ISO 8100, ISO 8102-20) and their fail-safe, redundancy, and safety-chain requirements; the relevant cybersecurity standards and practices (IEC 62443, ISO 27001, ISO 8102-20, secure boot, device identity, encryption, TLS, authentication/authorization, OTA security, gateway/cloud security, segmentation, zero trust, and — specifically for this project's AI layer — model security, prompt injection, and RAG poisoning, already introduced conceptually in §9.36 and due for full standards-grounded treatment); and the infrastructure connecting the elevator through its controller, edge gateway, network, cloud, data platform, and AI layer via APIs and event-driven architecture.

Phase 8 content is not generated here — this document ends at the close of Phase 7.

---

## Sources Consulted (Academic Literature)

- *Scientific Reports* (Nature), "Elevator fault diagnosis based on digital twin and PINNs-e-RGCN," December 2024
- *ScienceDirect*, elevator vibration signal denoising via deep residual U-Net (AEDM), December 2023, referencing Zheng & Zhao (time/frequency-domain feature classification) and Mishra et al. (deep-autoencoder feature extraction)
- *Sensors* (MDPI), "MetaRes-DMT-AS: A Meta-Learning Approach for Few-Shot Fault Diagnosis in Elevator Systems," July 2025, DOI 10.3390/s25154611 (Zhejiang University of Science and Technology)
- *PMC*, "Research on Fault Prediction Method of Elevator Door System Based on Transfer Learning" (GNN-LSTM-BDANN, acoustic/RUL)
- *Elevator World*, "Condition Monitoring of Elevators Using Deep Learning and Frequency Analysis Approach," December 2025, extending Mishra et al., 2019
- *ScienceDirect*, multi-scale convolution capsule network with CWT, data augmentation, and attention for elevator fault diagnosis, October 2025
- *MDPI Sensors*, "Damage Detection and Identification on Elevator Systems Using Deep Learning Algorithms and Multibody Dynamics Models," December 2024, DOI 10.3390/s25010101
- *MDPI Applied Sciences*, "Cross-Scale Time-Frequency Fusion Network for Non-Stationary Vibration Fault Diagnosis of Elevator Door Systems," August 2026, citing Jia, Gao, Li & Pang (2021, *Shock and Vibration*) and Niu & Wang (2022, *Sensors*)
- General (non-elevator-specific) multi-sensor RUL/fusion literature consulted for background context: *ScienceDirect* (multi-sensor RUL fusion model, 2020); *Sensors*/PMC (IABC-BPNN tool-wear RUL, 2020; hydraulic-valve RUL, 2025); PMC (deep adversarial multi-sensor RUL prognostics); *Sensors* (multimodal sensor-fusion pitfalls and reporting standards, 2026)

No performance numbers from any of the above are restated as claims about this project's own system — they describe what the cited papers report about their own methods and datasets only.
