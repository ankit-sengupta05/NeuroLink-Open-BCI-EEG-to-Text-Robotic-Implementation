# NeuroLink

## EEG-to-Text and Brain-to-Robot Intelligence Platform

<p align="center">
  <svg width="760" height="190" viewBox="0 0 760 190" role="img" aria-label="NeuroLink pipeline from EEG to robot action">
    <defs>
      <linearGradient id="flow" x1="0" x2="1">
        <stop offset="0" stop-color="#16B8A6"/>
        <stop offset="1" stop-color="#FFB547"/>
      </linearGradient>
      <filter id="shadow"><feDropShadow dx="0" dy="5" stdDeviation="6" flood-opacity=".18"/></filter>
    </defs>
    <rect width="760" height="190" rx="24" fill="#102A43"/>
    <path d="M110 95h540" stroke="url(#flow)" stroke-width="8" stroke-linecap="round"/>
    <g filter="url(#shadow)" font-family="Segoe UI,Arial,sans-serif" text-anchor="middle">
      <g><circle cx="90" cy="95" r="40" fill="#16B8A6"/><text x="90" y="91" fill="white" font-size="15" font-weight="700">EEG</text><text x="90" y="109" fill="white" font-size="11">signal</text></g>
      <g><circle cx="250" cy="95" r="40" fill="#2D9CDB"/><text x="250" y="91" fill="white" font-size="13" font-weight="700">DECODE</text><text x="250" y="109" fill="white" font-size="11">representation</text></g>
      <g><circle cx="410" cy="95" r="40" fill="#8C6FF0"/><text x="410" y="91" fill="white" font-size="13" font-weight="700">INTENT</text><text x="410" y="109" fill="white" font-size="11">text or task</text></g>
      <g><circle cx="570" cy="95" r="40" fill="#FFB547"/><text x="570" y="91" fill="#102A43" font-size="13" font-weight="700">PLAN</text><text x="570" y="109" fill="#102A43" font-size="11">robot action</text></g>
      <g><circle cx="690" cy="95" r="28" fill="#F26B5E"/><text x="690" y="99" fill="white" font-size="12" font-weight="700">ACT</text></g>
    </g>
  </svg>
</p>

> **Research prototype to closed-loop brain-computer interface.** NeuroLink investigates how non-invasive EEG can become reliable language, semantic intent, and safe robot action.

[![Stage](https://img.shields.io/badge/stage-student%20prototype%20%7C%20research%20platform-16B8A6)](#roadmap) [![Domain](https://img.shields.io/badge/domains-EEG%20%C2%B7%20AI%20%C2%B7%20robotics-2D9CDB)](#scope) [![Specification](https://img.shields.io/badge/specification-PRD-FFB547)](#)

## 1. Product North Star

NeuroLink will progressively translate brain activity into useful communication and executable robotic intent:

```text
EEG -> signal processing -> neural representation -> language / intent
    -> text or robot task -> planning -> perception -> motion -> feedback
```

The product is an experimental platform for measurable research, not a claim of unrestricted mind reading. Every stage must expose uncertainty, support human confirmation, and remain reversible.

## 2. Scope

| Track                   | Example output       | Difficulty | Initial role                   |
| ----------------------- | -------------------- | :--------: | ------------------------------ |
| **EEG classification**  | LEFT, RIGHT, YES, NO |    Low     | Baseline and calibration       |
| **EEG-to-language**     | “I want water”       |    High    | Research milestone             |
| **EEG-to-robot intent** | `FETCH(WATER)`       |    High    | Primary long-term product path |

Imagined speech is scientifically challenging because non-invasive EEG has low signal-to-noise ratio, strong subject variability, and context-dependent neural patterns. The platform therefore prioritizes constrained tasks and semantic commands before open-ended text generation.

### The language-independent thought hypothesis

Humans may think with the **same underlying intent** regardless of the language they use. What varies between individuals is the language medium chosen to express that thought. What cannot vary is the thought itself — which is fundamentally unique irrespective of whether a person is hearing, deaf, or mute.

Because intent precedes language formulation in the brain, understanding these core intent patterns allows for **predictive speech decoding**. The system could prospectively predict what the user wants to say _before_ they even formulate the full sentence mentally. If this hypothesis holds, decoding intent from EEG at the pre-linguistic level becomes not only a more tractable goal than decoding surface language, but also a significantly faster and more universal communication method.

## 3. System Model

```mermaid
flowchart LR
  H[Human] --> B[Brain activity]
  B --> E[EEG acquisition]
  E --> P[Preprocessing\nfiltering and artifact handling]
  P --> R[Neural representation\nencoder]
  R --> T[Transformer encoder]
  T --> L[Language decoder\ntext]
  T --> I[Intent decoder\nstructured task]
  L --> F[Human confirmation]
  I --> F
  F --> N[Task planner]
  N --> V[Robot perception]
  V --> M[Motion and navigation]
  M --> X[Robot execution]
  X --> Q[Environment feedback]
  Q --> H
```

### Command contract

| Layer         | Example                         | Required properties             |
| ------------- | ------------------------------- | ------------------------------- |
| Neural output | confidence distribution         | calibrated, timestamped         |
| Intent        | `FETCH`                         | closed vocabulary, confidence   |
| Parameters    | `object: WATER`                 | validated against scene/context |
| Plan          | navigate, locate, grasp, return | inspectable and interruptible   |
| Execution     | robot trajectory                | bounded, monitored, cancellable |

## 4. Product Principles

- **Constrained before open-ended:** earn complexity through validated baselines.
- **Intent before prose:** structured robot tasks are more realistic than unrestricted EEG-to-sentence decoding.
- **Human in the loop:** uncertain commands require confirmation rather than silent execution.
- **Closed-loop by design:** perception and environment feedback are part of the intelligence system.
- **Reproducible science:** version datasets, subjects, preprocessing, models, metrics, and experiments.
- **Safety first:** no physical action without authorization, confidence gates, and an emergency stop path.
- **Millisecond latency target:** the system must deliver predictions at ms-level latency; both hardware and software must be co-optimised to meet this target.
- **Frontal lobe primacy:** as most instructions and thoughts originate from the frontal lobe, the model and electrode placement will primarily focus on the front-to-mid brain region.
- **Adaptive personalisation:** after initial training on a base vocabulary, the model should use Reinforcement Learning (RL) to grow and learn new words over time with the individual user.

## 5. Research Workstreams

| Workstream              | Questions                                                               | Prototype deliverable                        |
| ----------------------- | ----------------------------------------------------------------------- | -------------------------------------------- |
| Acquisition             | Can recordings be synchronized and quality-scored?                      | EEG ingestion and session metadata           |
| Signal processing       | Which filters and artifact controls generalize?                         | Reproducible preprocessing pipeline          |
| Representation learning | Can subject-aware embeddings separate task signals?                     | Encoder baseline and embedding reports       |
| Decoding                | Which model and windowing strategy works best?                          | Classifier, language decoder, intent decoder |
| Intent & emotion        | Can the model extract intent and emotional context beyond literal text? | Intent decoder and emotion classifier        |
| Robotics                | Can commands be grounded safely in a scene?                             | Simulator-first planner and robot adapter    |
| Evaluation              | Does performance survive new sessions and users?                        | Benchmark harness and experiment registry    |

## 6. Milestones and Exit Criteria

| Phase | Focus           | Exit criteria                                                               |
| :---: | --------------- | --------------------------------------------------------------------------- |
| **0** | Instrumentation | Timestamped EEG sessions, data dictionary, quality checks                   |
| **1** | Classification  | Held-out-session baseline for LEFT/RIGHT/YES/NO; confusion matrix published |
| **2** | Robust decoding | Subject-independent evaluation, calibration, and ablation report            |
| **3** | Semantic intent | Closed-vocabulary commands with parameter validation and confirmation UI    |
| **4** | Simulated robot | Planner executes approved tasks in a deterministic simulator                |
| **5** | Physical pilot  | Low-risk, supervised tasks with emergency stop and event logs               |

## 7. Evaluation Framework

| Dimension      | Representative measures                                        |
| -------------- | -------------------------------------------------------------- |
| Signal quality | channel dropout rate, artifact ratio, usable-window percentage |
| Classification | accuracy, macro-F1, balanced accuracy, confusion matrix        |
| Generalization | cross-session and leave-one-subject-out performance            |
| Calibration    | expected calibration error, abstention quality                 |
| Language       | word error rate, semantic similarity, intent accuracy          |
| Robotics       | task completion, intervention rate, collision-free execution   |
| Human factors  | confirmation time, cognitive load, false activation rate       |

Every result should report subject count, session split, preprocessing, confidence intervals where possible, and a comparison with a non-EEG baseline.

## 8. Safety and Ethics

NeuroLink must remain a research system with explicit consent, privacy controls, and supervised operation. EEG data is sensitive biometric information: access must be controlled, identifiers minimized, and retention documented. The system must be able to abstain, explain its confidence, request confirmation, and stop robot motion immediately. No medical diagnosis, coercive use, or unsupervised high-risk actuation is in scope.

## 9. Prototype Architecture

```mermaid
graph TD
  A[EEG device adapter] --> B[Session recorder]
  B --> C[Preprocessing service]
  C --> D[Feature and representation store]
  D --> E[Model training and evaluation]
  E --> F[Inference gateway]
  F --> G[Text UI]
  F --> H[Intent validator]
  H --> I[Planner]
  I --> J[Simulator / robot adapter]
  J --> K[Telemetry and feedback]
  K --> B
```

| Component | Prototype choice                            | Boundary                            |
| --------- | ------------------------------------------- | ----------------------------------- |
| Data      | versioned local sessions plus metadata      | raw EEG never silently overwritten  |
| Models    | Python research modules, Transformer-ready  | training separated from execution   |
| Interface | text and structured intent views            | confidence and confirmation visible |
| Robotics  | simulator first, adapter second             | hardware actions gated and logged   |
| Quality   | pre-commit, secret scan, experiment reports | reproducible before scale           |

### Dataset design principles (from research notes)

The ideal dataset format mirrors classical voice-to-text data structure:

```
[ Multiple EEG waves with timestamps (e.g., 0:00 -> 1:00) ]
          +
[ Transcript: "I am a person" -> mapped to those timestamps ]
```

- **Multi-user same-transcript:** for each transcript, collect EEG from multiple users to generalise the wave pattern and reduce inter-subject noise (noise = individual side thoughts).
- **Avoid bulk single-transcript mapping:** long passages mapped to a single bulk transcript cannot be reliably chunked and are not recommended.

### Dataset Storage and Dimensions (Architecture)

- **Storage Format:** Extracted chunks must be saved as single `.npy` or `.npz` files representing a 2D matrix of shape `[channels, time_steps]`.
  - **Recommended structure:** `dataset/extracted/subject<n>/<transcript>.npy`
  - **Prohibited structure:** `dataset/extracted/subject<n>/<transcript>/<node_name>.npy`

#### Storage Approach Comparison

| Metric                   | ✅ Unified Matrix Approach           | ❌ Split by Node Approach               |
| :----------------------- | :----------------------------------- | :-------------------------------------- |
| **Path Example**         | `subject1/fetch_water.npy`           | `subject1/fetch_water/Fp1.npy`          |
| **Data Shape**           | `[105 channels, 500 time_steps]`     | `[500 time_steps]` per file             |
| **Files per Transcript** | **1** file                           | **105** separate files                  |
| **Disk I/O Speed**       | **Extremely Fast** (sequential read) | **Very Slow** (random seek bottlenecks) |
| **OS File Overhead**     | Minimal                              | Massive (wasted block space)            |

> **Note:** Splitting data across multiple files per channel is strictly prohibited due to severe file-system block-size overhead and I/O bottlenecks during model training.

- **Channel Dimensions (ZuCo 2.0):** The system expects **105 channels**. Although recorded with a 128-channel high-density cap, 23 artifact-heavy channels (face/neck) are discarded during standard preprocessing.

### Training process (from research notes)

```
Raw Noisy Data -> [User 1] [User 2] [User 3] [User 4]
                         | aggregation
               [ Generalised waveform ] <- reduces noise (side thoughts)
                         |
               Transcript output
```

- At inference time the input waveform is matched against the generalised pattern; the most similar pattern retrieves its associated transcript.
- **Architecture options:** Transformer (chunk-based n-byte prediction) or LSTM (longer context, richer per-chunk meaning).

### Hardware requirements (from research notes)

- Small form factor device.
- Superfast compute power.
- Large unified shared memory with fast access directly addressable by the CPU or processor.
- Optimised for millisecond-latency inference.

## 10. Open Research Questions

1. Which EEG montage, sampling rate, and task protocol give the strongest signal?
2. How much personalization is needed before transfer learning becomes useful?
3. Can uncertainty calibration reliably trigger abstention?
4. Which semantic command vocabulary is expressive enough for useful robot tasks while remaining learnable?
5. How should environmental feedback update decoding without creating unsafe feedback loops?
6. Can the model decode **intent** at a pre-linguistic level, independent of the spoken or thought language?
7. What is the minimum number of multi-user samples needed per transcript to reliably generalise the wave pattern?
8. How quickly can an RL-based personalisation loop learn new vocabulary words from a single user over repeated sessions?
9. Can Transformer or LSTM chunk-based architectures sustain sufficient context across long EEG passages?

## 11. Definition of Done

A milestone is complete only when the implementation, dataset version, configuration, evaluation report, failure cases, and safety behavior are documented and reproducible by another researcher.

---

**Status:** Research specification
**Product name:** NeuroLink
**Next practical step:** establish the EEG classification baseline and its reproducible session protocol.

### EEG Channel Mapping Reference (ZuCo 2.0)

This table documents the exact mapping of the 105 rows in our `.h5` EEG matrices to their original Geodesic 128-channel sensor names.

<details>
<summary><b>Click to expand full 105-Channel Mapping</b></summary>

| Matrix Index (Row) | Electrode Name | Original EGI 128 Number |
| :----------------- | :------------- | :---------------------- |
| `0`                | **E1**         | 1                       |
| `1`                | **E2**         | 2                       |
| `2`                | **E3**         | 3                       |
| `3`                | **E4**         | 4                       |
| `4`                | **E5**         | 5                       |
| `5`                | **E6**         | 6                       |
| `6`                | **E7**         | 7                       |
| `7`                | **E9**         | 9                       |
| `8`                | **E10**        | 10                      |
| `9`                | **Fz (E11)**   | 11                      |
| `10`               | **E12**        | 12                      |
| `11`               | **E13**        | 13                      |
| `12`               | **E15**        | 15                      |
| `13`               | **E16**        | 16                      |
| `14`               | **E17**        | 17                      |
| `15`               | **E18**        | 18                      |
| `16`               | **E19**        | 19                      |
| `17`               | **E20**        | 20                      |
| `18`               | **E22**        | 22                      |
| `19`               | **E23**        | 23                      |
| `20`               | **E24**        | 24                      |
| `21`               | **E26**        | 26                      |
| `22`               | **E27**        | 27                      |
| `23`               | **E28**        | 28                      |
| `24`               | **E29**        | 29                      |
| `25`               | **E30**        | 30                      |
| `26`               | **E31**        | 31                      |
| `27`               | **E32**        | 32                      |
| `28`               | **E33**        | 33                      |
| `29`               | **E34**        | 34                      |
| `30`               | **E35**        | 35                      |
| `31`               | **C3 (E36)**   | 36                      |
| `32`               | **E37**        | 37                      |
| `33`               | **E38**        | 38                      |
| `34`               | **E39**        | 39                      |
| `35`               | **E40**        | 40                      |
| `36`               | **E41**        | 41                      |
| `37`               | **E42**        | 42                      |
| `38`               | **E44**        | 44                      |
| `39`               | **E45**        | 45                      |
| `40`               | **E46**        | 46                      |
| `41`               | **E47**        | 47                      |
| `42`               | **E50**        | 50                      |
| `43`               | **E51**        | 51                      |
| `44`               | **E52**        | 52                      |
| `45`               | **E53**        | 53                      |
| `46`               | **E54**        | 54                      |
| `47`               | **E55**        | 55                      |
| `48`               | **E57**        | 57                      |
| `49`               | **E58**        | 58                      |
| `50`               | **E59**        | 59                      |
| `51`               | **E60**        | 60                      |
| `52`               | **E61**        | 61                      |
| `53`               | **Pz (E62)**   | 62                      |
| `54`               | **E64**        | 64                      |
| `55`               | **E65**        | 65                      |
| `56`               | **E66**        | 66                      |
| `57`               | **E67**        | 67                      |
| `58`               | **E69**        | 69                      |
| `59`               | **E70**        | 70                      |
| `60`               | **E71**        | 71                      |
| `61`               | **E72**        | 72                      |
| `62`               | **E74**        | 74                      |
| `63`               | **Oz (E75)**   | 75                      |
| `64`               | **E76**        | 76                      |
| `65`               | **E77**        | 77                      |
| `66`               | **E78**        | 78                      |
| `67`               | **E79**        | 79                      |
| `68`               | **E80**        | 80                      |
| `69`               | **E82**        | 82                      |
| `70`               | **E83**        | 83                      |
| `71`               | **E84**        | 84                      |
| `72`               | **E85**        | 85                      |
| `73`               | **E86**        | 86                      |
| `74`               | **E87**        | 87                      |
| `75`               | **E89**        | 89                      |
| `76`               | **E90**        | 90                      |
| `77`               | **E91**        | 91                      |
| `78`               | **E92**        | 92                      |
| `79`               | **E93**        | 93                      |
| `80`               | **E95**        | 95                      |
| `81`               | **E96**        | 96                      |
| `82`               | **E97**        | 97                      |
| `83`               | **E98**        | 98                      |
| `84`               | **E100**       | 100                     |
| `85`               | **E101**       | 101                     |
| `86`               | **E102**       | 102                     |
| `87`               | **E103**       | 103                     |
| `88`               | **C4 (E104)**  | 104                     |
| `89`               | **E105**       | 105                     |
| `90`               | **E106**       | 106                     |
| `91`               | **E108**       | 108                     |
| `92`               | **E109**       | 109                     |
| `93`               | **E110**       | 110                     |
| `94`               | **E111**       | 111                     |
| `95`               | **E112**       | 112                     |
| `96`               | **E114**       | 114                     |
| `97`               | **E115**       | 115                     |
| `98`               | **E116**       | 116                     |
| `99`               | **E117**       | 117                     |
| `100`              | **E118**       | 118                     |
| `101`              | **E121**       | 121                     |
| `102`              | **E122**       | 122                     |
| `103`              | **E123**       | 123                     |
| `104`              | **E124**       | 124                     |

</details>
