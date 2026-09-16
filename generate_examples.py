import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Search in the person directory since data directory wasn't populated yet
DATA_DIR = os.path.join(PROJECT_ROOT, "dataset", "extracted", "person")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "aeg")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try to load channel mapping
mapping_path = os.path.join(PROJECT_ROOT, "scripts", "zuco_channel_mapping.json")
try:
    with open(mapping_path, "r") as f:
        mapping = json.load(f)
    CHANNEL_LABELS = ["" for _ in range(105)]
    for m in mapping:
        idx = m["matrix_index"]
        if 0 <= idx < 105:
            CHANNEL_LABELS[idx] = m["electrode_name"]
except Exception:
    CHANNEL_LABELS = [f"CH{i}" for i in range(105)]

# Find 3 files recursively
h5_files = glob.glob(os.path.join(DATA_DIR, "**", "*.h5"), recursive=True)
if not h5_files:
    print(f"No .h5 files found in {DATA_DIR}!")
    exit(1)

sample_files = h5_files[:3]

for i, h5_path in enumerate(sample_files):
    fname = os.path.basename(h5_path)
    print(f"Processing {fname}...")
    
    with h5py.File(h5_path, 'r') as f:
        eeg_data = f['eeg'][:]
        # In person-centric, the filename itself is the transcript
        transcript = os.path.splitext(fname)[0].replace('_', ' ')
    
    if eeg_data.shape[0] > eeg_data.shape[1]:
        eeg_data = eeg_data.T
    
    fig, ax = plt.subplots(figsize=(15, 20))
    im = ax.imshow(eeg_data, aspect="auto", cmap="viridis")
    plt.colorbar(im, ax=ax, label="Amplitude")
    
    ax.set_title(f"Extracted Cache (h5): {transcript[:80]}")
    ax.set_xlabel("Time points")
    ax.set_ylabel("EEG Channels")
    
    num_ch = eeg_data.shape[0]
    if num_ch == len(CHANNEL_LABELS):
        ax.set_yticks(np.arange(num_ch))
        ax.set_yticklabels(CHANNEL_LABELS, fontsize=8)
    else:
        ax.set_yticks(np.arange(0, num_ch, max(1, num_ch // 20)))
        
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, f"example_{i+1}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"  -> Saved {out_path}")

print("Done generating examples in 'aeg' folder.")
