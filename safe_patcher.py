import glob
import json

decoder_code = """
import difflib
from IPython.display import display
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

def greedy_decoder(logits, char_to_idx):
    idx_to_char = {v: k for k, v in char_to_idx.items()}
    preds = torch.argmax(logits, dim=-1).transpose(0, 1)
    decoded = []
    for seq in preds:
        prev = -1
        text = ""
        for c in seq:
            c = c.item()
            if c != 0 and c != prev:
                text += idx_to_char.get(c, "")
            prev = c
        decoded.append(text)
    return decoded

def calculate_cer(pred_texts, target_texts):
    scores = []
    for p, t in zip(pred_texts, target_texts):
        scores.append(difflib.SequenceMatcher(None, p, t).ratio())
    return sum(scores) / max(1, len(scores))
"""

for nb_file in glob.glob("training/*.ipynb"):
    with open(nb_file, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # 1. Update Dataset
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])
            if "class EEGDataset" in src:
                src = src.replace(
                    "return eeg_tensor, target_tensor",
                    "subject = os.path.normpath(file_path).split(os.sep)[-3] if len(os.path.normpath(file_path).split(os.sep)) >= 3 else 'Unknown'\n        return eeg_tensor, target_tensor, subject",
                )
                cell["source"] = src.splitlines(True)

    # 2. Add Decoder Code Cell at top
    nb["cells"].insert(
        1,
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in decoder_code.strip().split("\n")],
        },
    )

    # 3. Patch the Training Loops
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])

            # Common replacements
            if "loss_history = []" in src:
                src = src.replace(
                    "loss_history = []",
                    "loss_history = []\n    recall_history = []\n    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))\n    display_handle = display(fig, display_id=True)\n    plt.close(fig)",
                )

            if "for epoch in range(epochs):" in src:
                src = src.replace(
                    "epoch_loss = 0", "epoch_loss = 0\n        epoch_recall = 0"
                )
                if (
                    "train_eeg.ipynb" in nb_file
                    and "audio" not in nb_file
                    and "nlp" not in nb_file
                ):
                    src = src.replace(
                        "for eeg, target in dataloader:",
                        "pbar = tqdm(dataloader, desc=f'Epoch {epoch + 1}/{epochs}')\n        for eeg, target, subject in pbar:",
                    )
                else:
                    src = src.replace(
                        "for feat, target in dataloader:",
                        "pbar = tqdm(dataloader, desc=f'Epoch {epoch + 1}/{epochs}')\n        for feat, target, subject in pbar:",
                    )

            if "epoch_loss += loss.item()" in src:
                # Build the visualization block
                vis_block = """epoch_loss += loss.item()

            batch_recall = 0
            if 'char_to_idx' in globals() or hasattr(dataset, 'char_to_idx'):
                char_to_idx = dataset.char_to_idx if hasattr(dataset, 'char_to_idx') else globals()['char_to_idx']
                preds = greedy_decoder(out, char_to_idx)
                idx_to_char = {v: k for k, v in char_to_idx.items()}
                targets_text = []
                for t in target:
                    t_list = t if isinstance(t, list) else t[0].tolist()
                    targets_text.append("".join([idx_to_char.get(c, "") for c in t_list]))
                batch_recall = calculate_cer(preds, targets_text)
            epoch_recall += batch_recall

            ax1.clear()
            ax2.clear()
            ax3.clear()
            subj = subject[0] if len(subject) > 0 else "Unknown"
"""
                if "audio" in nb_file:
                    vis_block += """
            sample = feat[0].detach().cpu().numpy().T
            ax1.imshow(sample, aspect="auto", origin="lower", cmap="viridis")
            ax1.set_title(f"Live Spectrogram (Subj: {subj})")
            ax1.set_xlabel("Time step")
"""
                elif "nlp" in nb_file:
                    vis_block += """
            sample = feat[0].detach().cpu().numpy()[:50, :]
            ax1.plot(sample)
            ax1.legend(["Gamma", "Beta", "Alpha", "Theta", "Delta"], loc="upper right")
            ax1.set_title(f"Live NLP Bands (Subj: {subj})")
            ax1.set_xlabel("Window")
"""
                else:
                    vis_block += """
            sample = eeg[0].detach().cpu().numpy()
            for ch in range(min(5, sample.shape[1])):
                ax1.plot(sample[:, ch] + ch * 2.0, label=f"Ch {ch}")
            ax1.legend(loc="upper right")
            ax1.set_title(f"Live Raw EEG (Subj: {subj})")
            ax1.set_xlabel("Time")
"""

                vis_block += """
            ax2.plot(loss_history + [loss.item()], color="r", label="CTC Loss")
            ax2.set_title("Real-Time CTC Loss")
            ax2.set_xlabel("Batches")
            ax2.legend(loc="upper right")

            ax3.plot(recall_history + [batch_recall], color="g", label="Recall (Accuracy)")
            ax3.set_title("Real-Time Character Recall")
            ax3.set_xlabel("Batches")
            ax3.legend(loc="upper right")

            display_handle.update(fig)
            pbar.set_postfix({"Loss": f"{loss.item():.4f}", "Recall": f"{batch_recall:.4f}"})
"""
                src = src.replace("epoch_loss += loss.item()", vis_block)

            if "avg_loss = epoch_loss / max(1, len(dataloader))" in src:
                src = src.replace(
                    "avg_loss = epoch_loss / max(1, len(dataloader))",
                    "avg_loss = epoch_loss / max(1, len(dataloader))\n        avg_recall = epoch_recall / max(1, len(dataloader))\n        recall_history.append(avg_recall)",
                )

            if "plt.plot(loss_history, marker=" in src:
                src = src.replace(
                    "plt.show()", ""
                )  # prevent duplicate show if it exists

            cell["source"] = src.splitlines(True)

    with open(nb_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Safely Patched {nb_file}!")
