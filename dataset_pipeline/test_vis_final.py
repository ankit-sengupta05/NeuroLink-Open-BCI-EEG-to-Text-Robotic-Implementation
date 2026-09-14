import glob
import os

import h5py
import matplotlib.pyplot as plt
import numpy as np

# Setup paths
PROJECT_ROOT = os.path.dirname(os.getcwd())
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset", "zuco2")

# Output directories for visualizations
WORD_MAPPING_DIR = os.path.join(PROJECT_ROOT, "dataset", "word eeg mapping")
SENTENCE_MAPPING_DIR = os.path.join(PROJECT_ROOT, "dataset", "sentence eeg mapping")

os.makedirs(WORD_MAPPING_DIR, exist_ok=True)
os.makedirs(SENTENCE_MAPPING_DIR, exist_ok=True)

print(f"Data directory: {DATASET_DIR}")
print(f"Word mapping output: {WORD_MAPPING_DIR}")
print(f"Sentence mapping output: {SENTENCE_MAPPING_DIR}")


def get_string(f, ref):
    """Extracts string from h5py object reference."""
    try:
        obj = f[ref]
        return "".join(chr(c[0]) for c in obj[:])
    except Exception:
        return "Unknown"


def plot_eeg(eeg_data, title, filename):
    """
    Plots all EEG channels on a single graph and saves the image.
    eeg_data shape is usually (channels, time) or (time, channels).
    We assume the longer dimension is time.
    """
    if eeg_data is None or eeg_data.size == 0:
        return

    eeg_data = np.array(eeg_data)
    # Ensure shape is (channels, time)
    if eeg_data.shape[0] > eeg_data.shape[1]:
        eeg_data = eeg_data.T

    num_channels, _time_points = eeg_data.shape

    plt.figure(figsize=(15, 8))
    for i in range(num_channels):
        # Offset each channel to visualize them stacked
        offset = i * (np.max(eeg_data) - np.min(eeg_data)) * 0.5
        plt.plot(eeg_data[i, :] + offset, linewidth=0.5, alpha=0.8)

    plt.title(title)
    plt.xlabel("Time points")
    plt.ylabel("EEG Channels (Offset)")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()
    plt.close()


# Find all .mat files in the dataset directory
mat_files = glob.glob(os.path.join(DATASET_DIR, "**", "results*.mat"), recursive=True)
print(f"Found {len(mat_files)} .mat files.")

if not mat_files:
    print("No .mat files found. Make sure the download script has finished running.")

# Loop through files
for mat_file in mat_files:  # Let's test just the first 3 files
    subject_name = os.path.basename(mat_file).replace(".mat", "")
    print(f"Processing {subject_name}...")

    try:
        with h5py.File(mat_file, "r") as f:
            if "sentenceData" not in f:
                continue

            sd = f["sentenceData"]
            num_sentences = sd["content"].shape[0]

            # Limit to first 2 sentences for testing
            for i in range(num_sentences):
                # 1. Extract Sentence
                content_ref = sd["content"][i, 0]
                sent_text = get_string(f, content_ref)
                safe_sent_name = "".join(
                    [c if c.isalnum() else "_" for c in sent_text]
                )[:50]

                # 2. Sentence EEG Mapping
                eeg_sent = None
                for key in ["rawData", "mean_t1", "mean_t2"]:
                    if key in sd:
                        ref = sd[key][i, 0]
                        if ref:
                            eeg_sent = f[ref][:]
                        break

                if eeg_sent is not None:
                    out_name = os.path.join(
                        SENTENCE_MAPPING_DIR,
                        f"{subject_name}_sent_{i}_{safe_sent_name}.png",
                    )
                    plot_eeg(eeg_sent, f"Sentence EEG: {sent_text}", out_name)

                # 3. Word EEG Mapping
                if "word" in sd:
                    word_refs = sd["word"][i, 0]
                    if word_refs:
                        words = f[word_refs]
                        num_words = words["content"].shape[0]

                        # Limit to first 3 words for testing
                        for w in range(num_words):
                            w_ref = words["content"][w, 0]
                            w_text = get_string(f, w_ref)
                            safe_word_name = "".join(
                                [c if c.isalnum() else "_" for c in w_text]
                            )

                            eeg_word = None
                            for key in ["rawEEG", "FFD_t1", "TRT_t1"]:
                                if key in words:
                                    e_ref = words[key][w, 0]
                                    if e_ref:
                                        eeg_word = f[e_ref][:]
                                    break

                            if eeg_word is not None:
                                out_name = os.path.join(
                                    WORD_MAPPING_DIR,
                                    f"{subject_name}_sent_{i}_word_{w}_{safe_word_name}.png",
                                )
                                plot_eeg(eeg_word, f"Word EEG: {w_text}", out_name)

        print(f"Finished processing {subject_name}.")
    except (OSError, KeyError, ValueError) as e:
        print(f"Skipping {mat_file}: not a valid v7.3 HDF5 or no sentenceData ({e})")

print("Visualization pipeline completed. Check the 'dataset' subfolders for images.")
