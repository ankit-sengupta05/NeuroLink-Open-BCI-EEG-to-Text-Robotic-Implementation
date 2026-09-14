# Research Notes

> Transcribed from handwritten notes (5 pages, dated 2026-09-05).
> Original images are stored locally in `assets/Notes/` and are **not** pushed to git.

---

## Open-BCI-EEG-Waves-To-Text-Translation-And-further-Robotic-Implementaions

## Page 1 — Core Concepts

### EEG Waves

- **EEG waves = potential difference between two different electrodes.**
- Most instructions given by our brain originate from the **frontal lobe**.

### Two-Model Architecture

Two models are required for research and scalability for the future:

| Model                 | Role                                                                       |
| --------------------- | -------------------------------------------------------------------------- |
| **Model 1 (Initial)** | Gets labelled, formatted data for text translation from EEG waves          |
| **Model 2 (Second)**  | Decrypts the **intent** for each statement and understands the **emotion** |

### Reasoning — Language-Independent Thought

> _"We might think in different languages but we think with the same intent. What we say might vary, but what we think cannot — that is the thing that is fundamentally unique, whether you are deaf, dumb, etc."_

- We first get a **thought**, and then we make a **language medium** to communicate that thought.
- **Predictive Intent Understanding:** Because intent precedes language formulation, we can potentially predict the intended speech _before_ the user consciously puts it down into a sentence. By understanding the core patterns of intent, the model can predict the meaning directly from pre-linguistic EEG waves.
- The research question: **What if we could communicate without the need of any language?**
  - This is a concept of research, not yet proven, but something we can actually implement.

---

## Page 2 — Requirements and Expectations

### Expectations

- We are expecting this model to give **fast outputs in millisecond (ms) latency**.
- We need to **minimize latency** of each prediction.
- For such requirements, we need to **tweak both hardware and software** to get the best output.

**Best-case expectation:**

> The model could be trained on a base language first, then implemented with **Reinforcement Learning (RL)** and be able to **grow and learn new words** with time spent with the user (adaptive/personalised learning).

### Requirements

- **Hardware** must be optimised for:
  - Small form factor
  - Superfast compute power
  - Huge unified shared memory that is **fast-access** and can be directly accessed by CPU or processor used in system

- **Frontal lobe focus:** As most commands and thoughts are generated in the frontal lobe of the brain, our model will mostly focus on the **front to mid** region to decrypt instructions and thoughts.

---

## Page 3 — What Could the Prototype Look Like?

### Form Factor Options

For **commercial use**, the device can be morphed into everyday objects:

| Form Factor                 | Notes                                                |
| --------------------------- | ---------------------------------------------------- |
| **Cap**                     | General consumer form factor, handy for everyday use |
| **Headband**                | Focused on frontal lobe, tighter fit, precise output |
| **Headset (emotive-style)** | Easy to carry, mostly focuses on frontal lobe        |

- If all electrodes can be concentrated to the frontal lobe, a headband enables a **tighter fit and more precise output**.
- A headset form factor is easy to carry and similarly focuses on the frontal lobe.

### Possible Partnerships

| Partner                 | Area                                                                          |
| ----------------------- | ----------------------------------------------------------------------------- |
| **Emotiv**              | Hardware — existing EEG headset manufacturer                                  |
| **OpenBCI Dev Kit**     | Hardware — open-source BCI hardware platform                                  |
| **ElevenLabs (11labs)** | Voice — provides a vast variety of realistic human voices for voiceless users |

- For **voice output** (e.g., giving voice to the voiceless), we may partner with **ElevenLabs** which provides a vast variety of realistic human voices.

---

## Page 4 — How Could the Dataset Look Like?

### Ideal Dataset Structure — Chunked EEG + Transcripts

The **best and ideal** way to chunk data:

```
[ Multiple EEG waves with timestamps (0:00 to 1:00) ]
          +
[ Transcript: "I am a person" -> mapped to those timestamps ]
```

- This mirrors the same data structure used by **classical voice-to-text generation models**.
- Even classical voice-to-text generation models were trained in the same data structure.

### Multi-User Same-Transcript Approach

For the same transcript (e.g., "I am a boy ... end"), we collect EEG wave data from **multiple users**:

```
Long EEG passage (User 1) ->  [EEG waves]
Long EEG passage (User 2) ->  [EEG waves]
Long EEG passage (User 3) ->  [EEG waves]
```

- **Single Transcript x Multiple Waves** = generalisable pattern learning.

> **Note:** Long-passage single-transcript mapping is **mostly not recommended** because we also
> do not have any means to manually transcribe it to smaller chunks as we do not know
> what a specific wave form segment says within a long passage.

### Summary

| Approach                                   | Recommendation  |
| ------------------------------------------ | --------------- |
| Chunked EEG + timestamp-aligned transcript | Best and Ideal  |
| Long passage EEG + single bulk transcript  | Not recommended |

### Storage Format (Data Architecture)

**The Two-Stage Standard for EEG-ML Workflows (and ZuCo 2.0 specifics):**

1. **Stage 1 (Raw/Archival Storage):**
   - Generally, domain-standard formats like **EDF+**, **BDF** (24-bit), or **FIF** (MNE-Python native) are used for interoperability.
   - **For ZuCo 2.0:** The dataset is distributed as `.mat` v7.3 files. Because MATLAB switched to HDF5-based storage from v7.3 onward, these files are _already_ lossless HDF5 containers. (Note: ZuCo 1.0 used `.mat` v7, which is NOT HDF5).
   - **Best Practice:** Keep the original `.mat` (v7.3) files as the archival/ground-truth copy. _(Compatibility Warning: Some published benchmarks use Python 3.7.16 specifically to avoid `h5py` version conflicts when parsing these files)._
2. **Stage 2 (DL Training Efficiency):** Extract the required arrays (per-trial, per-word, or per-sentence epochs) and dump them into a flatter, training-optimized **HDF5** (`.h5`) file as `float32` with lossless compression. This avoids re-parsing the awkward nested MATLAB struct on every epoch.

### Dataset Extraction Scope (What are we curating?)

- **Data Type:** **Preprocessed Data.** The extraction script exclusively targets the `results*.mat` files. In ZuCo 2.0, these are the preprocessed arrays that have already been cleaned via ICA (Independent Component Analysis) to remove eye-tracking and muscle artifacts.
- **Tasks Included:** **Task 1 (NR - Normal Reading) & Task 2 (TSR - Task Specific Reading).** The pipeline recursively pulls all available `results*.mat` files, meaning it extracts and compiles the sentence data across both tasks into the final dataset cache.

- **Recommended DL Approach (Unified Matrix / HDF5):** `dataset/extracted/subject<n>/<transcript>.h5`
  - Store the entire chunked recording as a single multi-dimensional matrix in **HDF5 (`.h5`)** format.
  - **Zero Data Loss Standard:** Inherit the source `dtype` (usually `float64`) + lossless `gzip` compression. This achieves bit-for-bit identical preservation of the raw signal without quantization, while compression saves disk space by removing redundancy.
  - **Shape:** `[num_channels, time_steps]` (e.g., `[105, 500]`). This allows fast load times, chunked reads, and aligns perfectly with PyTorch/TF dataloaders.
  - _(Metadata Tip: We can store sample rate, channel names, and labels as HDF5 attributes alongside the array)._
- **Not Recommended (Split by Node):** `dataset/extracted/subject<n>/<transcript>/<node_name>.npy`
  - **Do NOT split data by channel (node).** Storing each channel as a separate file (e.g., `128 files` per chunk) introduces severe disk I/O bottlenecks and bloats the file system with millions of small files.

#### DL Storage Approach Comparison

| Metric                   | ✅ Unified Matrix Approach (HDF5)          | ❌ Split by Node Approach               |
| :----------------------- | :----------------------------------------- | :-------------------------------------- |
| **Path Example**         | `subject1/fetch_water.h5`                  | `subject1/fetch_water/Fp1.npy`          |
| **Data Shape**           | `[105 channels, 500 time_steps]`           | `[500 time_steps]` per file             |
| **Format & Quality**     | `float32` + `gzip` (lossless, bit-perfect) | Uncompressed `.npy` (wastes space)      |
| **Files per Transcript** | **1** file                                 | **105** separate files                  |
| **Disk I/O Speed**       | **Extremely Fast** (chunked, sequential)   | **Very Slow** (random seek bottlenecks) |
| **OS File Overhead**     | Minimal                                    | Massive (wasted block space)            |

### Channel Dimensions (ZuCo 2.0)

- The ZuCo dataset was originally recorded using a **128-channel** EEG cap.
- During preprocessing, 23 channels (mostly facial boundary and neck electrodes capturing muscle/EOG artifacts) were removed.
- **Final Channel Count:** The data extracted from ZuCo 2.0 `.mat` files consistently contains exactly **105 channels**.

---

## Page 5 — Training Process Idea

### Core Idea — Generalise the Wave Pattern

- We **sample out multiple EEG waves for a given transcript** to generalise the wave pattern.
- In human thoughts while reading, there are also **side thoughts** which might vary person to person.
- By sampling for many users, we will try to **reduce the noise** (where noise = side thoughts).

```
Raw Noisy Data -> [User 1 wave] [User 2 wave] [User 3 wave] [User 4 wave]
                           | aggregation
                  [ Generalised waveform ] <- Generalises all the noise
                           |
                  Transcript output
```

- Now, while in use: the wave form which is most similar to this generalised pattern will get the transcript of that wave.

### Scaled / Creative Use Case — Transformer Architecture

- We can also **train with a Transformer architecture model** and predict **n-byte chunks** of the wave.
- Using **LSTM or Transformer architecture** will also help to **sustain longer context** and carry more meaning for each wave chunk.

### Architecture Options

| Architecture              | Benefit                                                 |
| ------------------------- | ------------------------------------------------------- |
| Transformer (chunk-based) | Predicts n-byte wave chunks, scalable                   |
| LSTM                      | Sustains longer context, carries more meaning per chunk |

---

## Summary of Key Insights from Notes

| Topic                 | Key Insight                                                             |
| --------------------- | ----------------------------------------------------------------------- |
| EEG signal            | Potential difference between electrodes; frontal lobe is primary source |
| Two-model system      | Model 1 = EEG to text; Model 2 = intent + emotion decryption            |
| Language-independence | Thought intent is universal; language is just the output medium         |
| Latency requirement   | ms-level inference; hardware + software co-optimisation needed          |
| Adaptive learning     | RL-based personalisation, grows vocabulary with user over time          |
| Form factor           | Cap / headband / headset focused on frontal lobe                        |
| Partnerships          | Emotiv (HW), OpenBCI Dev Kit (HW), ElevenLabs (voice output)            |
| Dataset design        | Chunked EEG + timestamp-aligned transcripts, multi-user per transcript  |
| Training strategy     | Sample multiple waves per transcript to generalise and reduce noise     |
| Model architecture    | Transformer or LSTM for chunk-based wave prediction                     |

---

## ZuCo 2.0 Dataset Directory Structure

The official ZuCo 2.0 dataset (pulled from OSF node `2urht`) is structured as follows:

- **`answers/`**
  - Contains tiny metadata files (v7 `.mat` format, e.g., `results_NR_YAC_1.mat`). These hold the text responses/answers that the participants typed out for the reading comprehension questions.

- **`scripts/`**
  - Contains the official MATLAB helper scripts provided by the dataset authors for loading and preprocessing. _(We bypass this as we utilize a pure Python/PyTorch pipeline)._

- **`task1 - NR/` (Normal Reading) & `task2 - TSR/` (Task Specific Reading)**
  - These are the main data trees for the experiments. They both contain three sub-folders:
    1. **`Raw data/`**: Contains subfolders for each subject with the raw, untouched 128-channel EEG sensor dumps.
    2. **`Preprocessed/`**: Contains subfolders for each subject with granular, file-per-node or file-per-sentence cleaned data.
    3. **`Matlab files/`**: Contains the massive, consolidated `results<SUBJECT>_<TASK>.mat` files (e.g., `resultsYAC_NR.mat`). These are the finalized, preprocessed HDF5 (v7.3) data structures that perfectly align the 105-channel ICA-cleaned EEG arrays with the sentence text and eye-tracking data. **(This folder is the primary source of truth our extraction script targets).**

- **`task_materials/`**
  - Contains the stimuli files used in the experiment—specifically the raw text files of the sentences shown on the screen and the reading comprehension questions.
