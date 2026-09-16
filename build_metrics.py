import glob
import json

decoder_code = """
import difflib
from IPython.display import display
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

def greedy_decoder(logits, char_to_idx):
    idx_to_char = {v: k for k, v in char_to_idx.items()}
    # logits shape: [time, batch, classes]
    preds = torch.argmax(logits, dim=-1).transpose(0, 1) # [batch, time]
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
        # ratio() returns 1.0 for perfect match, approximate for CER/Recall
        scores.append(difflib.SequenceMatcher(None, p, t).ratio())
    return sum(scores) / max(1, len(scores))
"""


def generate_train_model(name_arch):
    # Depending on arch, data visualization changes
    if name_arch == "audio":
        data_plot = """
            sample = eeg[0].detach().cpu().numpy().T
            im = ax1.imshow(sample, aspect="auto", origin="lower", cmap="viridis")
            ax1.set_title(f"Live Spectrogram (Subj: {subj})")
            ax1.set_xlabel("Time step")
            ax1.set_ylabel("Channel/Freq bin")
"""
    elif name_arch == "nlp":
        data_plot = """
            sample = eeg[0].detach().cpu().numpy()[:50, :]
            ax1.plot(sample)
            ax1.legend(["Gamma", "Beta", "Alpha", "Theta", "Delta"], loc="upper right")
            ax1.set_title(f"Live NLP Bands (Subj: {subj})")
            ax1.set_xlabel("Window")
"""
    else:
        data_plot = """
            sample = eeg[0].detach().cpu().numpy()
            for ch in range(min(5, sample.shape[1])):
                ax1.plot(sample[:, ch] + ch * 2.0, label=f"Ch {ch}")
            ax1.legend(loc="upper right")
            ax1.set_title(f"Live Raw EEG (Subj: {subj})")
            ax1.set_xlabel("Time")
"""

    return f"""def train_model(model, name, dataloader, epochs=5, char_to_idx=None):
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    loss_history = []
    recall_history = []
    model.train()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    display_handle = display(fig, display_id=True)
    plt.close(fig) # Prevent duplicate static rendering

    for epoch in range(epochs):
        epoch_loss = 0
        epoch_recall = 0

        pbar = tqdm(dataloader, desc=f"[{{name}}] Epoch {{epoch + 1}}/{{epochs}}")
        for eeg, target, subject in pbar:
            batch_size = eeg.size(0)
            subj = subject[0] if len(subject) > 0 else "Unknown"

            # Forward pass
            optimizer.zero_grad()
            out = model(eeg)
            out = out.transpose(0, 1)  # [time, batch, classes]
            out_log_sm = nn.functional.log_softmax(out, dim=2)

            out_time = eeg.size(1) // 2 if "DeepSpeech" in type(model).__name__ else eeg.size(1)
            input_lengths = torch.full(size=(batch_size,), fill_value=out_time, dtype=torch.long)
            target_lengths = torch.tensor([len(t) if isinstance(t, list) else len(t[0]) for t in target])
            # Handle potential nested lists from dataloader for targets
            target_flat = []
            for t in target:
                if isinstance(t, list):
                    target_flat.extend(t)
                else:
                    target_flat.extend(t[0].tolist() if isinstance(t[0], torch.Tensor) else t[0])

            # Compute loss
            loss = criterion(out_log_sm, target, input_lengths, target_lengths)
            loss.backward()
            optimizer.step()

            batch_loss = loss.item()
            epoch_loss += batch_loss

            # Compute Metrics (Recall/Accuracy)
            batch_recall = 0
            if char_to_idx is not None:
                preds = greedy_decoder(out_log_sm, char_to_idx)
                # target back to text
                idx_to_char = {{v: k for k, v in char_to_idx.items()}}
                targets_text = []
                for t in target:
                    t_list = t if isinstance(t, list) else t[0].tolist()
                    targets_text.append("".join([idx_to_char.get(c, "") for c in t_list]))
                batch_recall = calculate_cer(preds, targets_text)
            epoch_recall += batch_recall

            # Update Live Visuals
            ax1.clear()
            ax2.clear()
            ax3.clear()

{data_plot}

            ax2.plot(loss_history + [batch_loss], color="r", label="CTC Loss")
            ax2.set_title("Real-Time CTC Loss")
            ax2.set_xlabel("Batches")
            ax2.legend(loc="upper right")

            ax3.plot(recall_history + [batch_recall], color="g", label="Recall (Accuracy)")
            ax3.set_title("Real-Time Character Recall")
            ax3.set_xlabel("Batches")
            ax3.legend(loc="upper right")

            display_handle.update(fig)
            pbar.set_postfix({{"Loss": f"{{batch_loss:.4f}}", "Recall": f"{{batch_recall:.4f}}"}})

        avg_loss = epoch_loss / max(1, len(dataloader))
        avg_recall = epoch_recall / max(1, len(dataloader))
        loss_history.append(avg_loss)
        recall_history.append(avg_recall)

    import os
    if not os.path.exists("models"):
        os.makedirs("models")
    torch.save(model.state_dict(), os.path.join("models", f"{{name}}_checkpoint.pth"))
    return loss_history, recall_history
"""


for nb_file in glob.glob("training/*.ipynb"):
    with open(nb_file, "r", encoding="utf-8") as f:
        nb = json.load(f)

    arch = "raw"
    if "audio" in nb_file:
        arch = "audio"
    elif "nlp" in nb_file:
        arch = "nlp"

    # 1. Patch Dataset class to return Subject
    for cell in nb["cells"]:
        if cell["cell_type"] == "code" and "class EEGDataset" in "".join(
            cell["source"]
        ):
            new_source = []
            for line in cell["source"]:
                if "return eeg_tensor, target_tensor" in line:
                    new_source.append(
                        '        subject = os.path.normpath(file_path).split(os.sep)[-3] if len(os.path.normpath(file_path).split(os.sep)) >= 3 else "Unknown"\n'
                    )
                    new_source.append(
                        "        return eeg_tensor, target_tensor, subject\n"
                    )
                else:
                    new_source.append(line)
            cell["source"] = new_source

    # 2. Patch Train Model Function
    for cell in nb["cells"]:
        if cell["cell_type"] == "code" and "def train_model(" in "".join(
            cell["source"]
        ):
            full_code = decoder_code + "\n" + generate_train_model(arch)
            cell["source"] = [line + "\n" for line in full_code.split("\n")]

    # 3. Patch Execution Block to pass char_to_idx
    for cell in nb["cells"]:
        if (
            cell["cell_type"] == "code"
            and "train_model(" in "".join(cell["source"])
            and "def train_model" not in "".join(cell["source"])
        ):
            new_source = []
            for line in cell["source"]:
                if "train_model(" in line and "char_to_idx" not in line:
                    line = line.replace(")", ", char_to_idx=dataset.char_to_idx)")
                new_source.append(line)
            cell["source"] = new_source

    with open(nb_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Patched {nb_file} completely!")
