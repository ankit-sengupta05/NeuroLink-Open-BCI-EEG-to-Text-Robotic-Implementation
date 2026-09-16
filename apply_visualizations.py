import json
import glob

# 1. Update train_eeg.ipynb (Raw EEG)
def patch_raw_eeg(source):
    new_source = []
    for line in source:
        if 'for eeg, target in dataloader:' in line:
            new_source.append(line)
            new_source.append('            # Live plotting\n')
            new_source.append('            from IPython.display import clear_output\n')
            new_source.append('            clear_output(wait=True)\n')
            new_source.append('            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))\n')
            new_source.append('            sample = eeg[0].detach().cpu().numpy()\n')
            new_source.append('            for ch in range(min(5, sample.shape[1])):\n')
            new_source.append('                ax1.plot(sample[:, ch] + ch * 2.0)\n')
            new_source.append('            ax1.set_title(f"Live Raw EEG Processing (Model: {name})")\n')
            new_source.append('            ax1.set_xlabel("Time")\n')
            new_source.append('            ax2.plot(loss_history, color="r")\n')
            new_source.append('            ax2.set_title(f"CTC Loss (Epoch {epoch+1}/{epochs})")\n')
            new_source.append('            plt.show()\n')
            continue
        if 'if isinstance(model, DeepSpeechEEG)' in line:
            new_source.append(line.replace('DeepSpeechEEG', 'DeepSpeechEEG_placeholder')) # Just in case
            continue
        new_source.append(line)
    return new_source

# 2. Update train_eeg_nlp.ipynb (Frequency Bands)
def patch_nlp_eeg(source):
    new_source = []
    for line in source:
        if 'for eeg, target in dataloader:' in line:
            new_source.append(line)
            new_source.append('            from IPython.display import clear_output\n')
            new_source.append('            clear_output(wait=True)\n')
            new_source.append('            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))\n')
            new_source.append('            # eeg shape: [batch, time, bands]\n')
            new_source.append('            sample = eeg[0].detach().cpu().numpy()[:50, :]\n')
            new_source.append('            ax1.plot(sample)\n')
            new_source.append('            ax1.legend(["Gamma", "Beta", "Alpha", "Theta", "Delta"], loc="upper right")\n')
            new_source.append('            ax1.set_title(f"Live NLP Band Features (Model: {name})")\n')
            new_source.append('            ax1.set_xlabel("Window")\n')
            new_source.append('            ax2.plot(loss_history, color="g")\n')
            new_source.append('            ax2.set_title(f"CTC Loss (Epoch {epoch+1}/{epochs})")\n')
            new_source.append('            plt.show()\n')
            continue
        new_source.append(line)
    return new_source

# 3. Update train_eeg_audio.ipynb (Spectrograms)
def patch_audio_eeg(source):
    new_source = []
    for line in source:
        if 'for eeg, target in dataloader:' in line:
            new_source.append(line)
            new_source.append('            from IPython.display import clear_output\n')
            new_source.append('            clear_output(wait=True)\n')
            new_source.append('            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))\n')
            new_source.append('            # eeg shape: [batch, time, channels]\n')
            new_source.append('            sample = eeg[0].detach().cpu().numpy().T\n')
            new_source.append('            im = ax1.imshow(sample, aspect="auto", origin="lower", cmap="viridis")\n')
            new_source.append('            ax1.set_title(f"Live Spectrogram mimicry (Model: {name})")\n')
            new_source.append('            ax1.set_xlabel("Time step")\n')
            new_source.append('            ax1.set_ylabel("Channel/Freq bin")\n')
            new_source.append('            ax2.plot(loss_history, color="b")\n')
            new_source.append('            ax2.set_title(f"CTC Loss (Epoch {epoch+1}/{epochs})")\n')
            new_source.append('            plt.show()\n')
            continue
        new_source.append(line)
    return new_source


for nb_file in glob.glob("training/*.ipynb"):
    with open(nb_file, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    for cell in nb["cells"]:
        if cell["cell_type"] == "code" and "def train_model(" in "".join(cell["source"]):
            if "clear_output" in "".join(cell["source"]):
                continue # already patched
            if "train_eeg.ipynb" in nb_file and "audio" not in nb_file and "nlp" not in nb_file:
                cell["source"] = patch_raw_eeg(cell["source"])
            elif "train_eeg_nlp.ipynb" in nb_file:
                cell["source"] = patch_nlp_eeg(cell["source"])
            elif "train_eeg_audio.ipynb" in nb_file:
                cell["source"] = patch_audio_eeg(cell["source"])
    
    with open(nb_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Patched {nb_file}")
