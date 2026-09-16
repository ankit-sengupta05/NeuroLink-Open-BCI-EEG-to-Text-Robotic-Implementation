# NeuroLink

## EEG-to-Text and Brain-to-Robot Intelligence Platform

<p align="center">
  <img src="assets/neuroflow.svg" alt="NeuroLink pipeline" width="100%" />
</p>

**EEG → neural representations → language and intent → safe robot action**

NeuroLink is a research platform exploring how non-invasive EEG can be decoded into constrained language, semantic intent, and eventually closed-loop robotic behavior. It starts with measurable EEG classification and advances toward simulator-first brain-to-robot interaction.

## Why this project matters

<p align="center">
  <img src="assets/importance.svg" alt="Importance of the project" width="100%" />
</p>

| Domain                     | Why it matters                                                                    |
| -------------------------- | --------------------------------------------------------------------------------- |
| Healthcare                 | Enables more natural communication pathways for patients and accessibility tools. |
| Robotics                   | Lets a human communicate intent without heavy manual control interfaces.          |
| AI research                | Pushes representation learning, multimodal reasoning, and temporal decoding.      |
| Human-computer interaction | Explores how brains and machines can cooperate under uncertainty and feedback.    |

## Product direction

| Track               | Near-term outcome                                   | Difficulty |
| ------------------- | --------------------------------------------------- | ---------- |
| EEG classification  | LEFT, RIGHT, YES, NO baselines                      | Low        |
| EEG-to-language     | Research decoding of speech-related representations | High       |
| EEG-to-robot intent | Validated commands such as `FETCH(WATER)`           | High       |

The project prioritizes structured intent over unrestricted mind-reading claims. Confidence, abstention, human confirmation, and robot feedback are core product behaviors.

## Research pipeline

```text
EEG -> preprocessing -> representation learning -> transformer encoder
    -> text / intent -> task planner -> perception -> motion -> feedback
```

### Data Architecture

- **Storage:** Extracted data chunks must be saved as single `.npy` or `.npz` matrix files containing all channels `[channels, time_steps]`.
  - ✅ **Recommended:** `dataset/extracted/subject<n>/<transcript>.npy`
  - ❌ **Not Recommended:** `dataset/extracted/subject<n>/<transcript>/<node_name>.npy` (Splitting data by individual channels creates millions of small files, causing severe disk I/O bottlenecks during model training).
- **Dimensions:** The current pipeline utilizes **105 channels** (standardized from ZuCo 2.0, where 23 artifact-prone facial/neck channels are removed from the original 128-channel recordings).

## Main scientific scope

1. **EEG classification**: simple baselines like LEFT/RIGHT/YES/NO.
2. **EEG-to-language**: decoding meaningful language or semantic intent from neural patterns.
3. **EEG-to-robot intent**: more realistic robotics path where EEG becomes structured task instructions.

This staged approach matters because imagined speech from non-invasive EEG is scientifically difficult due to noise, variability, and low signal quality. Research progress is more realistic when we build constrained steps first.

## Two-Model Architecture

The platform is designed around two distinct models:

| Model                          | Role                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------ |
| **Model 1 — EEG-to-Text**      | Trained on labelled, formatted data to translate EEG wave patterns into raw text                 |
| **Model 2 — Intent & Emotion** | Decrypts the underlying intent for each decoded statement and understands the associated emotion |

The core hypothesis: humans think with the **same intent** regardless of language — what varies is the language medium used to express that thought. Because this intent is formed _before_ being put down into a sentence, EEG may let us access and **predict the intended speech early**, directly from these universal pre-linguistic intent patterns.

## Prototype Form Factor

For consumer/commercial use the device can take several everyday forms, all oriented around frontal lobe electrode placement:

| Form Factor                | Notes                                              |
| -------------------------- | -------------------------------------------------- |
| **Cap**                    | General consumer use, handy for everyday carry     |
| **Headband**               | Tight frontal-lobe focus, precise output           |
| **Headset (Emotiv-style)** | Easy to carry, predominantly frontal lobe coverage |

**Possible partnerships:**

- **Emotiv** — hardware (existing EEG headset platform)
- **OpenBCI Dev Kit** — open-source BCI hardware
- **ElevenLabs** — realistic synthetic voice output for voiceless users

## Electrode Placement

<p align="center">
  <img src="assets/electrode_placement.png" alt="Electrode Placement (10-20 System)" width="45%" />
  <img src="assets/electrode_pathway.png" alt="Electrode Pathway Reference" width="45%" />
</p>

These reference images show the standard 10-20 system external electrode placements, highlighting connections to the central Cz node for signal processing, as well as sequential pathways along the left hemisphere (e.g., Fp1->F7->T3->T5->O1 and Fp1->F3->C3->P3->O1).

## Documentation

- [PRD.md](PRD.md) — complete product requirements and research plan
- [notes.md](notes.md) — transcribed research notes (concepts, requirements, dataset design, training ideas)
- [resources.md](resources.md) — EEG datasets and external resources
- [setup-git2.cmd](setup-git2.cmd) — direct Windows setup launcher
- [setup-git2.sh](setup-git2.sh) — direct shell launcher

## Academic Use & Citation

If this repository, its source code, algorithms, implementation, experimental methodology, or substantial portions of its contents are used in academic research, publications, conference papers, these, dissertations, or other scholarly work, please cite this repository appropriately.

Citation information is provided in `CITATION.cff`.

Example:

> Sengupta, A. (2026). NeuroLink: Open-BCI EEG-to-Text & Robotic Implementation. GitHub.
> https://github.com/ankit-sengupta05/NeuroLink-Open-BCI-EEG-to-Text-Robotic-Implementation

**License Restrictions:** Use of the source code is subject to the **Research & Non-Commercial Attribution License (RNCA)**. This explicitly prohibits commercial use without permission, while actively encouraging academic research, education, and personal experimentation.

## Quality checks

```bash
python -m pre_commit run --all-files
python scripts/scan_secrets.py
```

**Status:** Student research prototype progressing toward an advanced research platform.

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
