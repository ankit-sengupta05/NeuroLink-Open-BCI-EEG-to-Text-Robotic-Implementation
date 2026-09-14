"""Test the summary + unique-words cells from the rebuilt notebook."""

import glob
import os

import h5py
import pandas as pd

# Simulate notebook cwd = dataset_pipeline/
NB_CWD = os.path.join(
    r"C:\SDE Projects\Open-BCI-EEG-Waves-To-Text-Translation-And-further-Robotic-Implementaions",
    "dataset_pipeline",
)
PROJECT_ROOT = os.path.dirname(NB_CWD)
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset", "zuco2")

mat_files = glob.glob(os.path.join(DATASET_DIR, "**", "results*.mat"), recursive=True)
print(f"Found {len(mat_files)} .mat files.")


def get_string(f, ref):
    try:
        obj = f[ref]
        return "".join(chr(c[0]) for c in obj[:])
    except Exception:  # noqa: BLE001
        return ""


STRIP_CHARS = ".,;:!?\"'()[]"

all_rows = []
unique_words = set()
subjects = set()
tasks = set()

for mat_path in sorted(mat_files):
    fname = os.path.splitext(os.path.basename(mat_path))[0]
    parts = fname.replace("results", "").split("_")
    subject = parts[-1] if len(parts) >= 2 else fname
    task = "_".join(parts[:-1]) if len(parts) >= 2 else "unknown"
    subjects.add(subject)
    tasks.add(task)

    try:
        with h5py.File(mat_path, "r") as f:
            if "sentenceData" not in f:
                continue
            sd = f["sentenceData"]
            n_sentences = sd["content"].shape[0]
            for i in range(n_sentences):
                ref = sd["content"][i, 0]
                text = get_string(f, ref)
                if not text:
                    continue
                words = text.split()
                unique_words.update(w.strip(STRIP_CHARS) for w in words)
                all_rows.append(
                    {
                        "Subject": subject,
                        "Task": task,
                        "Sent #": i + 1,
                        "Sentence": text,
                        "# Words": len(words),
                    }
                )
    except Exception:  # noqa: BLE001
        pass

print()
print("=" * 60)
print(f"  Subjects (users): {len(subjects)}")
print(f"  Tasks found:      {sorted(tasks)[:5]} ...")
print(f"  Total sentences:  {len(all_rows)}")
print(f"  Unique words:     {len(unique_words)}")
print("=" * 60)

df = pd.DataFrame(all_rows)
print("\nFirst 5 rows:")
print(df.head(5).to_string(index=False))

print("\nFirst 20 unique words (sorted):")
sorted_words = sorted(w for w in unique_words if w)
print(sorted_words[:20])
