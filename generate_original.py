import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MAT_FILE = os.path.join(PROJECT_ROOT, "dataset", "zuco2", "task1-SR", "Matlab_files", "resultsYAC_NR.mat")
# Wait, let's find the actual path for resultsYAC_NR.mat
import glob
mat_files = glob.glob(os.path.join(PROJECT_ROOT, "dataset", "zuco2", "**", "resultsYAC_NR.mat"), recursive=True)
if not mat_files:
    print("Could not find resultsYAC_NR.mat")
    exit(1)
MAT_FILE = mat_files[0]

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "original")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_string(f, ref):
    try:
        obj = f[ref]
        return ''.join(chr(c[0]) for c in obj[:])
    except Exception:
        return 'Unknown'

# Load channel mapping
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

TARGETS = [
    "According_to_Errol_Flynn_s_memoirs__film_director_",
    "After_a_career_ending_injury__Howard_joined_the_st",
    "After_a_two_day_trial_she_was_banished_as_a_hereti"
]

found = 0

print(f"Opening {MAT_FILE}")
with h5py.File(MAT_FILE, 'r') as f:
    sd = f['sentenceData']
    n_sents = sd['content'].shape[0]
    
    for i in range(n_sents):
        sent_text = get_string(f, sd['content'][i, 0])
        safe_transcript = ''.join(c if c.isalnum() else '_' for c in sent_text)[:50]
        
        if safe_transcript in TARGETS:
            print(f"Processing target: {safe_transcript}")
            
            # Extract exactly as the pipeline did
            eeg_sent = None
            for key in ['rawData', 'mean_t1', 'mean_t2']:
                if key in sd:
                    eeg_sent = f[sd[key][i, 0]][:]
                    if np.array(eeg_sent).dtype != object:
                        break
            
            if eeg_sent is None or np.array(eeg_sent).dtype == object:
                print(f"Failed to find raw data for {safe_transcript}")
                continue
                
            if eeg_sent.shape[0] > eeg_sent.shape[1]:
                eeg_sent = eeg_sent.T
                
            fig, ax = plt.subplots(figsize=(15, 20))
            im = ax.imshow(eeg_sent, aspect="auto", cmap="viridis")
            plt.colorbar(im, ax=ax, label="Amplitude")
            
            ax.set_title(f"Original Cache (.mat): {sent_text[:80]}")
            ax.set_xlabel("Time points")
            ax.set_ylabel("EEG Channels")
            
            num_ch = eeg_sent.shape[0]
            if num_ch == len(CHANNEL_LABELS):
                ax.set_yticks(np.arange(num_ch))
                ax.set_yticklabels(CHANNEL_LABELS, fontsize=8)
            else:
                ax.set_yticks(np.arange(0, num_ch, max(1, num_ch // 20)))
                
            plt.tight_layout()
            
            target_idx = TARGETS.index(safe_transcript)
            out_path = os.path.join(OUTPUT_DIR, f"original_{target_idx + 1}.png")
            plt.savefig(out_path, dpi=150)
            plt.close()
            print(f"  -> Saved {out_path}")
            found += 1
            
            if found == 3:
                break

print(f"Done generating {found} examples in 'original' folder.")
