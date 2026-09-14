import json

with open("dataset_pipeline/visualize_zuco.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# Keep only the first 6 cells (intro + download + setup + helper fns)
preserved = nb["cells"][:6]


def md_cell(source):
    return {"cell_type": "markdown", "id": "md_cell", "metadata": {}, "source": source}


def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "code_cell",
        "metadata": {},
        "outputs": [],
        "source": source,
    }


# ── Cell: Dataset Summary ─────────────────────────────────────────────────────
SUMMARY_MD = md_cell(
    "### Dataset Summary\n"
    "Scans all downloaded `.mat` files and produces:\n"
    "- **User count** and file overview\n"
    "- **Full sentence transcript** table\n"
    "- **Unique words** table across all sentences\n"
)

SUMMARY_CODE = code_cell(
    "import glob\n"
    "import os\n"
    "\n"
    "import h5py\n"
    "import numpy as np\n"
    "import pandas as pd\n"
    "from IPython.display import HTML, display\n"
    "\n"
    "# Paths — notebook cwd is dataset_pipeline/, so go up one level\n"
    "PROJECT_ROOT = os.path.dirname(os.getcwd())\n"
    'DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset", "zuco2")\n'
    "\n"
    'mat_files = glob.glob(os.path.join(DATASET_DIR, "**", "results*.mat"), recursive=True)\n'
    'print(f"Found {len(mat_files)} .mat files.")\n'
    "\n"
    "\n"
    "def get_string(f, ref):\n"
    '    """Extracts string from h5py object reference."""\n'
    "    try:\n"
    "        obj = f[ref]\n"
    '        return "".join(chr(c[0]) for c in obj[:])\n'
    "    except Exception:  # noqa: BLE001\n"
    '        return ""\n'
    "\n"
    "\n"
    "STRIP_CHARS = '.,;:!?\"\\'()[]'\n"
    "\n"
    "all_rows = []\n"
    "unique_words = set()\n"
    "subjects = set()\n"
    "tasks = set()\n"
    "\n"
    "for mat_path in sorted(mat_files):\n"
    "    fname = os.path.splitext(os.path.basename(mat_path))[0]\n"
    '    parts = fname.replace("results", "").split("_")\n'
    "    subject = parts[-1] if len(parts) >= 2 else fname\n"
    '    task = "_".join(parts[:-1]) if len(parts) >= 2 else "unknown"\n'
    "    subjects.add(subject)\n"
    "    tasks.add(task)\n"
    "\n"
    "    try:\n"
    "        with h5py.File(mat_path, 'r') as f:\n"
    '            if "sentenceData" not in f:\n'
    "                continue\n"
    '            sd = f["sentenceData"]\n'
    "            n_sentences = sd['content'].shape[0]\n"
    "\n"
    "            num_ch = 'Unknown'\n"
    "            for i in range(n_sentences):\n"
    "                for key in ['rawData', 'mean_t1', 'mean_t2']:\n"
    "                    if key in sd:\n"
    "                        eeg = f[sd[key][i, 0]][:]\n"
    "                        if np.array(eeg).dtype != object:\n"
    "                            num_ch = eeg.shape[0] if eeg.shape[0] < eeg.shape[1] else eeg.shape[1]\n"
    "                            break\n"
    "                if num_ch != 'Unknown':\n"
    "                    break\n"
    "\n"
    "            for i in range(n_sentences):\n"
    "                ref = sd['content'][i, 0]\n"
    "                text = get_string(f, ref)\n"
    "                if not text:\n"
    "                    continue\n"
    "                words = text.split()\n"
    "                unique_words.update(w.strip(STRIP_CHARS) for w in words)\n"
    "                all_rows.append({\n"
    '                    "Subject": subject,\n'
    '                    "Task": task,\n'
    '                    "Sent #": i + 1,\n'
    '                    "Sentence": text,\n'
    '                    "# Words": len(words),\n'
    '                    "# Channels": num_ch,\n'
    "                })\n"
    "    except Exception:  # noqa: BLE001\n"
    "        pass\n"
    "\n"
    "print()\n"
    "print('=' * 60)\n"
    'print(f"  Subjects (users): {len(subjects)}")\n'
    'print(f"  Tasks found:      {sorted(tasks)}")\n'
    'print(f"  Total sentences:  {len(all_rows)}")\n'
    'print(f"  Unique words:     {len(unique_words)}")\n'
    "print('=' * 60)\n"
    "\n"
    "df = pd.DataFrame(all_rows)\n"
)

# ── Cell: Subject/User Table ──────────────────────────────────────────────────
USERS_MD = md_cell(
    "### Users & Tasks Overview\n"
    "Summary table of each subject and how many sentences they contributed per task, along with the number of EEG channels.\n"
)

USERS_CODE = code_cell(
    "if not df.empty:\n"
    "    summary = df.groupby(['Subject', 'Task']).agg(\n"
    "        Sentences=('Sent #', 'count'),\n"
    '        Total_Words=("# Words", "sum"),\n'
    '        Channels=("# Channels", "first"),\n'
    "    ).reset_index()\n"
    "    print(f'Total subjects: {df[\"Subject\"].nunique()}')\n"
    "    display(HTML(summary.to_html(index=False, border=0)))\n"
)

# ── Cell: Full Transcript Table ───────────────────────────────────────────────
TRANSCRIPT_MD = md_cell(
    "### Full Sentence Transcript\n"
    "Every sentence extracted from all subjects and tasks.\n"
)

TRANSCRIPT_CODE = code_cell(
    "if not df.empty:\n"
    "    display(HTML(df.to_html(index=False, border=0)))\n"
    "else:\n"
    "    print('No data found — run the download cell first.')\n"
)

# ── Cell: Unique Words Table ──────────────────────────────────────────────────
WORDS_MD = md_cell(
    "### Unique Words in Dataset\n"
    "All unique tokens found across the entire corpus (punctuation stripped).\n"
)

WORDS_CODE = code_cell(
    "if unique_words:\n"
    "    sorted_words = sorted(w for w in unique_words if w)\n"
    "    cols = 6\n"
    "    rows_w = [sorted_words[i:i+cols] for i in range(0, len(sorted_words), cols)]\n"
    "    while len(rows_w[-1]) < cols:\n"
    '        rows_w[-1].append("")\n'
    "    df_words = pd.DataFrame(rows_w, columns=[f'Word {j+1}' for j in range(cols)])\n"
    "    print(f'Total unique words: {len(sorted_words)}')\n"
    "    display(HTML(df_words.to_html(index=False, border=0)))\n"
)

# ── Cell: EEG Preview ─────────────────────────────────────────────────────────
PREVIEW_MD = md_cell(
    "### EEG Waveform Preview\n"
    "Sample **sentence-level** and **word-level** EEG heatmaps from the first available `.mat` file,\n"
    "with all 105 electrode names labelled on the Y-axis.\n"
)

PREVIEW_CODE = code_cell(
    "import matplotlib.pyplot as plt\n"
    "\n"
    "CHANNEL_LABELS = [\n"
    '    "E2","E3","E4","E5","E6","E7","E9","E10","E11","E12","E13","E15","E16",\n'
    '    "E18","E19","E20","E22","E23","E24","E26","E27","E28","E29","E30","E31",\n'
    '    "E33","E34","E35","E36","E37","E38","E39","E40","E41","E42","E43","E44",\n'
    '    "E45","E46","E47","E50","E51","E52","E53","E54","E55","E57","E58","E59",\n'
    '    "E60","E61","E62","E64","E65","E66","E67","E69","E70","E71","E72","E74",\n'
    '    "E75","E76","E77","E78","E79","E80","E82","E83","E84","E85","E86","E87",\n'
    '    "E89","E90","E91","E92","E93","E95","E96","E97","E98","E100","E101","E102",\n'
    '    "E103","E104","E105","E106","E108","E109","E110","E111","E112","E114",\n'
    '    "E115","E116","E117","E118","E120","E121","E122","E123","E124","Cz",\n'
    "]\n"
    "\n"
    "\n"
    "def plot_eeg_ax(ax, eeg_data, title):\n"
    "    eeg_data = np.array(eeg_data, dtype=float)\n"
    "    if len(eeg_data.shape) < 2:\n"
    "        return\n"
    "    if eeg_data.shape[0] > eeg_data.shape[1]:\n"
    "        eeg_data = eeg_data.T\n"
    "    num_ch = eeg_data.shape[0]\n"
    '    im = ax.imshow(eeg_data, aspect="auto", cmap="viridis")\n'
    '    plt.colorbar(im, ax=ax, label="Amplitude", fraction=0.03)\n'
    "    ax.set_title(title, fontsize=9, pad=4)\n"
    '    ax.set_xlabel("Time points", fontsize=8)\n'
    '    ax.set_ylabel("EEG Channels", fontsize=8)\n'
    "    if num_ch == len(CHANNEL_LABELS):\n"
    "        ax.set_yticks(np.arange(num_ch))\n"
    "        ax.set_yticklabels(CHANNEL_LABELS, fontsize=5)\n"
    "    else:\n"
    "        ax.set_yticks(np.arange(0, num_ch, max(1, num_ch // 20)))\n"
    "\n"
    "\n"
    "# Pick the first valid HDF5 .mat file\n"
    "preview_mat = None\n"
    "for mat_path in sorted(mat_files):\n"
    "    try:\n"
    "        with h5py.File(mat_path, 'r') as f:\n"
    '            if "sentenceData" in f:\n'
    "                preview_mat = mat_path\n"
    "                break\n"
    "    except Exception:  # noqa: BLE001\n"
    "        pass\n"
    "\n"
    "if not preview_mat:\n"
    "    print('No valid .mat file found. Run the download cell first.')\n"
    "else:\n"
    "    print(f'Previewing: {os.path.basename(preview_mat)}')\n"
    "    N_PREVIEW = 3\n"
    "    with h5py.File(preview_mat, 'r') as f:\n"
    '        sd = f["sentenceData"]\n'
    "        n_sents = sd['content'].shape[0]\n"
    "\n"
    "        # Sentence previews\n"
    "        fig, axes = plt.subplots(1, N_PREVIEW, figsize=(18, 22))\n"
    '        fig.suptitle("Sentence-Level EEG Mappings", fontsize=14, fontweight="bold", y=1.01)\n'
    "        plotted = 0\n"
    "        for i in range(n_sents):\n"
    "            if plotted >= N_PREVIEW:\n"
    "                break\n"
    "            sent_text = get_string(f, sd['content'][i, 0])\n"
    "            eeg_sent = None\n"
    '            for key in ["rawData", "mean_t1"]:\n'
    "                if key in sd:\n"
    "                    eeg_sent = f[sd[key][i, 0]][:]\n"
    "                    break\n"
    "            if eeg_sent is None or np.array(eeg_sent).dtype == object:\n"
    "                continue\n"
    "            plot_eeg_ax(axes[plotted], eeg_sent, f'Sent {i+1}: {sent_text[:30]}...')\n"
    "            plotted += 1\n"
    "        plt.tight_layout()\n"
    "        plt.show()\n"
    "\n"
    "        # Word previews\n"
    "        fig, axes = plt.subplots(1, N_PREVIEW, figsize=(18, 22))\n"
    '        fig.suptitle("Word-Level EEG Mappings (1st Fixation)", fontsize=14, fontweight="bold", y=1.01)\n'
    "        plotted = 0\n"
    "        for i in range(n_sents):\n"
    "            if plotted >= N_PREVIEW:\n"
    "                break\n"
    '            if "word" not in sd:\n'
    "                break\n"
    "            words_grp = f[sd['word'][i, 0]]\n"
    "            for w in range(words_grp['content'].shape[0]):\n"
    "                if plotted >= N_PREVIEW:\n"
    "                    break\n"
    "                w_text = get_string(f, words_grp['content'][w, 0])\n"
    "                eeg_word = None\n"
    '                for key in ["rawEEG", "FFD_t1"]:\n'
    "                    if key in words_grp:\n"
    "                        raw = f[words_grp[key][w, 0]][:]\n"
    "                        if raw.dtype == object:\n"
    "                            raw = f[raw[0, 0]][:]\n"
    "                        if len(raw.shape) == 2:\n"
    "                            eeg_word = raw\n"
    "                        break\n"
    "                if eeg_word is None:\n"
    "                    continue\n"
    "                plot_eeg_ax(axes[plotted], eeg_word, f\"Word: '{w_text}'\")\n"
    "                plotted += 1\n"
    "        plt.tight_layout()\n"
    "        plt.show()\n"
)

# ── Cell: Save All Visualizations ────────────────────────────────────────────
SAVE_MD = md_cell(
    "### Save All EEG Visualizations to Disk\n"
    "Generates and saves labelled EEG heatmaps for all sentences and one word per sentence\n"
    "into `dataset/sentence eeg mapping/` and `dataset/word eeg mapping/`.\n"
)

SAVE_CODE = code_cell(
    'SENT_MAPPING_DIR = os.path.join(PROJECT_ROOT, "dataset", "sentence eeg mapping")\n'
    'WORD_MAPPING_DIR = os.path.join(PROJECT_ROOT, "dataset", "word eeg mapping")\n'
    "os.makedirs(SENT_MAPPING_DIR, exist_ok=True)\n"
    "os.makedirs(WORD_MAPPING_DIR, exist_ok=True)\n"
    "\n"
    "\n"
    "def save_eeg_plot(eeg_data, title, filepath):\n"
    "    eeg_data = np.array(eeg_data, dtype=float)\n"
    "    if len(eeg_data.shape) < 2:\n"
    "        return False\n"
    "    if eeg_data.shape[0] > eeg_data.shape[1]:\n"
    "        eeg_data = eeg_data.T\n"
    "    num_ch = eeg_data.shape[0]\n"
    "    fig, ax = plt.subplots(figsize=(15, 20))\n"
    '    im = ax.imshow(eeg_data, aspect="auto", cmap="viridis")\n'
    '    plt.colorbar(im, ax=ax, label="Amplitude")\n'
    "    ax.set_title(title)\n"
    '    ax.set_xlabel("Time points")\n'
    '    ax.set_ylabel("EEG Channels")\n'
    "    if num_ch == len(CHANNEL_LABELS):\n"
    "        ax.set_yticks(np.arange(num_ch))\n"
    "        ax.set_yticklabels(CHANNEL_LABELS, fontsize=8)\n"
    "    else:\n"
    "        ax.set_yticks(np.arange(0, num_ch, max(1, num_ch // 20)))\n"
    "    plt.tight_layout()\n"
    "    plt.savefig(filepath, dpi=150)\n"
    "    plt.close()\n"
    "    return True\n"
    "\n"
    "\n"
    "total_sent = 0\n"
    "total_word = 0\n"
    "\n"
    "for mat_path in sorted(mat_files):\n"
    "    fname = os.path.splitext(os.path.basename(mat_path))[0]\n"
    "    try:\n"
    "        with h5py.File(mat_path, 'r') as f:\n"
    '            if "sentenceData" not in f:\n'
    "                continue\n"
    '            sd = f["sentenceData"]\n'
    "            n_sents = sd['content'].shape[0]\n"
    "            for i in range(n_sents):\n"
    "                sent_text = get_string(f, sd['content'][i, 0])\n"
    "                safe = ''.join(c if c.isalnum() else '_' for c in sent_text)[:50]\n"
    "                # Sentence\n"
    '                for key in ["rawData", "mean_t1"]:\n'
    "                    if key in sd:\n"
    "                        eeg = f[sd[key][i, 0]][:]\n"
    "                        if np.array(eeg).dtype != object:\n"
    "                            out = os.path.join(SENT_MAPPING_DIR, f'{fname}_sent_{i}_{safe}.png')\n"
    "                            if save_eeg_plot(eeg, f'Sentence EEG: {sent_text[:60]}', out):\n"
    "                                total_sent += 1\n"
    "                        break\n"
    "                # Word (first valid per sentence)\n"
    '                if "word" not in sd:\n'
    "                    continue\n"
    "                words_grp = f[sd['word'][i, 0]]\n"
    "                for w in range(words_grp['content'].shape[0]):\n"
    "                    w_text = get_string(f, words_grp['content'][w, 0])\n"
    "                    safe_w = ''.join(c if c.isalnum() else '_' for c in w_text)\n"
    "                    eeg_word = None\n"
    '                    for key in ["rawEEG", "FFD_t1"]:\n'
    "                        if key in words_grp:\n"
    "                            raw = f[words_grp[key][w, 0]][:]\n"
    "                            if raw.dtype == object:\n"
    "                                raw = f[raw[0, 0]][:]\n"
    "                            if len(raw.shape) == 2:\n"
    "                                eeg_word = raw\n"
    "                            break\n"
    "                    if eeg_word is not None:\n"
    "                        out = os.path.join(WORD_MAPPING_DIR, f'{fname}_sent_{i}_word_{w}_{safe_w}.png')\n"
    "                        if save_eeg_plot(eeg_word, f'Word EEG: {w_text}', out):\n"
    "                            total_word += 1\n"
    "                        break\n"
    "    except Exception:  # noqa: BLE001\n"
    '        print(f"  Skipping {fname}")\n'
    "\n"
    "print(f'Done! Saved {total_sent} sentence EEG images and {total_word} word EEG images.')\n"
)

# ── Cell: Data Extraction (Unified Matrix) ──────────────────────────────────
DATA_EXTRACTION_PERSON_MD = md_cell(
    "### Save Data to HDF5 Files (Person-Centric Approach)\n"
    "Implements the data storage process organized by subject:\n"
    "- **Person-centric Cache:** `dataset/extracted/person/<subject>/<task>/<transcript>.h5` (Identical zero-data-loss arrays)\n"
    "- **Format & Quality:** Native `dtype` (typically `float64`) + lossless `gzip` compression.\n"
    "- **Expected Space:** ~1.5-2 GB total.\n"
    "- **Speed:** Extremely fast disk I/O, optimized for chunked DataLoader reads in PyTorch/TF."
)

DATA_EXTRACTION_DATA_MD = md_cell(
    "### Save Data to HDF5 Files (Data-Centric Approach with Metadata)\n"
    "Implements the data storage process with embedded ML metadata attributes:\n"
    "- **Data-centric Cache:** `dataset/extracted/data/<subject>_<transcript>.h5`\n"
    "- **Format & Quality:** Native `dtype` (typically `float64`) + lossless `gzip` compression.\n"
    "- **Expected Space:** ~1.5-2 GB total.\n"
    "- **Metadata included:** `subject`, `task`, `transcript`, `sampling_rate`, `channel_labels`."
)

DATA_EXTRACTION_PERSON_CODE = code_cell(
    "import os\n"
    "import numpy as np\n"
    "import h5py\n"
    "import glob\n"
    "\n"
    "PROJECT_ROOT = os.path.dirname(os.getcwd())\n"
    "DATASET_DIR = os.path.join(PROJECT_ROOT, 'dataset', 'zuco2')\n"
    "EXTRACTED_DIR = os.path.join(PROJECT_ROOT, 'dataset', 'extracted')\n"
    "PERSON_DIR = os.path.join(EXTRACTED_DIR, 'person')\n"
    "os.makedirs(PERSON_DIR, exist_ok=True)\n"
    "\n"
    "CHANNEL_LABELS = [\n"
    "    'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E9', 'E10', 'E11', 'E12', 'E13', 'E15', 'E16',\n"
    "    'E18', 'E19', 'E20', 'E22', 'E23', 'E24', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31',\n"
    "    'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44',\n"
    "    'E45', 'E46', 'E47', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 'E57', 'E58', 'E59',\n"
    "    'E60', 'E61', 'E62', 'E64', 'E65', 'E66', 'E67', 'E69', 'E70', 'E71', 'E72', 'E74',\n"
    "    'E75', 'E76', 'E77', 'E78', 'E79', 'E80', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87',\n"
    "    'E89', 'E90', 'E91', 'E92', 'E93', 'E95', 'E96', 'E97', 'E98', 'E100', 'E101', 'E102',\n"
    "    'E103', 'E104', 'E105', 'E106', 'E108', 'E109', 'E110', 'E111', 'E112', 'E114',\n"
    "    'E115', 'E116', 'E117', 'E118', 'E120', 'E121', 'E122', 'E123', 'E124', 'Cz'\n"
    "]\n"
    "\n"
    "def get_string(f, ref):\n"
    "    try:\n"
    "        obj = f[ref]\n"
    "        return ''.join(chr(c[0]) for c in obj[:])\n"
    "    except Exception:\n"
    "        return 'Unknown'\n"
    "\n"
    "mat_files = glob.glob(os.path.join(DATASET_DIR, '**', 'results*.mat'), recursive=True)\n"
    "valid_files = [f for f in mat_files if os.path.getsize(f) > 1000000] # Skip tiny v7 metadata files\n"
    "\n"
    "saved_unified = 0\n"
    "\n"
    "for mat_path in sorted(valid_files): # Process all valid files\n"
    "    fname = os.path.splitext(os.path.basename(mat_path))[0]\n"
    "    parts = fname.replace('results', '').split('_')\n"
    "    subject = parts[0] if len(parts) >= 2 else fname\n"
    "    task = parts[1] if len(parts) >= 2 else 'Unknown'\n"
    "    subject_dir = os.path.join(PERSON_DIR, subject, task)\n"
    "    os.makedirs(subject_dir, exist_ok=True)\n"
    "\n"
    "    try:\n"
    "        with h5py.File(mat_path, 'r') as f:\n"
    "            if 'sentenceData' not in f:\n"
    "                continue\n"
    "            sd = f['sentenceData']\n"
    "            n_sents = sd['content'].shape[0]\n"
    "            for i in range(n_sents):\n"
    "                sent_text = get_string(f, sd['content'][i, 0])\n"
    "                transcript_safe = ''.join(c if c.isalnum() else '_' for c in sent_text)[:50]\n"
    "                if not transcript_safe:\n"
    "                    transcript_safe = f'sent_{i}'\n"
    "                \n"
    "                eeg_sent = None\n"
    "                for key in ['rawData', 'mean_t1', 'mean_t2']:\n"
    "                    if key in sd:\n"
    "                        eeg_sent = f[sd[key][i, 0]][:]\n"
    "                        if np.array(eeg_sent).dtype != object:\n"
    "                            break\n"
    "                \n"
    "                if eeg_sent is None or np.array(eeg_sent).dtype == object:\n"
    "                    continue\n"
    "                \n"
    "                # Ensure shape is [channels, time_steps]\n"
    "                if eeg_sent.shape[0] > eeg_sent.shape[1]:\n"
    "                    eeg_sent = eeg_sent.T\n"
    "                \n"
    "                # Save to person-centric cache\n"
    "                unified_path = os.path.join(subject_dir, f'{transcript_safe}.h5')\n"
    "                with h5py.File(unified_path, 'w') as out_f:\n"
    "                    out_f.create_dataset(\n"
    "                        'eeg', \n"
    "                        data=eeg_sent,\n"
    "                        compression='gzip'\n"
    "                    )\n"
    "\n"
    "                saved_unified += 1\n"
    "                \n"
    "    except Exception as e:\n"
    "        print(f'Error processing {fname}: {e}')\n"
    "\n"
    "print(f'Unified Matrix Data extraction complete.')\n"
    "print(f'Saved {saved_unified} Unified Matrix files (.h5).')\n"
)

DATA_EXTRACTION_DATA_CODE = code_cell(
    "import os\n"
    "import sys\n"
    "import json\n"
    "import numpy as np\n"
    "import h5py\n"
    "import glob\n"
    "\n"
    "PROJECT_ROOT = os.path.dirname(os.getcwd())\n"
    "DATASET_DIR = os.path.join(PROJECT_ROOT, 'dataset', 'zuco2')\n"
    "EXTRACTED_DIR = os.path.join(PROJECT_ROOT, 'dataset', 'extracted')\n"
    "DATA_DIR = os.path.join(EXTRACTED_DIR, 'data')\n"
    "os.makedirs(DATA_DIR, exist_ok=True)\n"
    "\n"
    "CHANNEL_LABELS = [\n"
    "    'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E9', 'E10', 'E11', 'E12', 'E13', 'E15', 'E16',\n"
    "    'E18', 'E19', 'E20', 'E22', 'E23', 'E24', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31',\n"
    "    'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44',\n"
    "    'E45', 'E46', 'E47', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 'E57', 'E58', 'E59',\n"
    "    'E60', 'E61', 'E62', 'E64', 'E65', 'E66', 'E67', 'E69', 'E70', 'E71', 'E72', 'E74',\n"
    "    'E75', 'E76', 'E77', 'E78', 'E79', 'E80', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87',\n"
    "    'E89', 'E90', 'E91', 'E92', 'E93', 'E95', 'E96', 'E97', 'E98', 'E100', 'E101', 'E102',\n"
    "    'E103', 'E104', 'E105', 'E106', 'E108', 'E109', 'E110', 'E111', 'E112', 'E114',\n"
    "    'E115', 'E116', 'E117', 'E118', 'E120', 'E121', 'E122', 'E123', 'E124', 'Cz'\n"
    "]\n"
    "\n"
    "def get_string(f, ref):\n"
    "    try:\n"
    "        obj = f[ref]\n"
    "        return ''.join(chr(c[0]) for c in obj[:])\n"
    "    except Exception:\n"
    "        return 'Unknown'\n"
    "\n"
    "mat_files = glob.glob(os.path.join(DATASET_DIR, '**', 'results*.mat'), recursive=True)\n"
    "valid_files = [f for f in mat_files if os.path.getsize(f) > 1000000] # Skip tiny v7 metadata files\n"
    "\n"
    "saved_unified = 0\n"
    "\n"
    "for mat_path in sorted(valid_files): # Process all valid files\n"
    "    fname = os.path.splitext(os.path.basename(mat_path))[0]\n"
    "    parts = fname.replace('results', '').split('_')\n"
    "    subject = parts[0] if len(parts) >= 2 else fname\n"
    "    task = parts[1] if len(parts) >= 2 else 'Unknown'\n"
    "\n"
    "    try:\n"
    "        with h5py.File(mat_path, 'r') as f:\n"
    "            if 'sentenceData' not in f:\n"
    "                continue\n"
    "            sd = f['sentenceData']\n"
    "            n_sents = sd['content'].shape[0]\n"
    "            for i in range(n_sents):\n"
    "                sent_text = get_string(f, sd['content'][i, 0])\n"
    "                transcript_safe = ''.join(c if c.isalnum() else '_' for c in sent_text)[:50]\n"
    "                if not transcript_safe:\n"
    "                    transcript_safe = f'sent_{i}'\n"
    "                \n"
    "                eeg_sent = None\n"
    "                for key in ['rawData', 'mean_t1', 'mean_t2']:\n"
    "                    if key in sd:\n"
    "                        eeg_sent = f[sd[key][i, 0]][:]\n"
    "                        if np.array(eeg_sent).dtype != object:\n"
    "                            break\n"
    "                \n"
    "                if eeg_sent is None or np.array(eeg_sent).dtype == object:\n"
    "                    continue\n"
    "                \n"
    "                # Ensure shape is [channels, time_steps]\n"
    "                if eeg_sent.shape[0] > eeg_sent.shape[1]:\n"
    "                    eeg_sent = eeg_sent.T\n"
    "                \n"
    "                # Save to data-centric cache with metadata\n"
    "                data_path = os.path.join(DATA_DIR, f'{subject}_{transcript_safe}.h5')\n"
    "                with h5py.File(data_path, 'w') as out_f:\n"
    "                    dset = out_f.create_dataset(\n"
    "                        'eeg', \n"
    "                        data=eeg_sent,\n"
    "                        compression='gzip'\n"
    "                    )\n"
    "                    # Attach ML metadata\n"
    "                    out_f.attrs['subject'] = subject\n"
    "                    out_f.attrs['task'] = task\n"
    "                    out_f.attrs['transcript'] = sent_text\n"
    "                    out_f.attrs['sampling_rate'] = 500\n"
    "                    out_f.attrs['channel_labels'] = json.dumps(CHANNEL_LABELS) if 'json' in sys.modules else str(CHANNEL_LABELS)\n"
    "\n"
    "                saved_unified += 1\n"
    "                \n"
    "    except Exception as e:\n"
    "        print(f'Error processing {fname}: {e}')\n"
    "\n"
    "print(f'Unified Matrix Data extraction complete.')\n"
    "print(f'Saved {saved_unified} Unified Matrix files (.h5).')\n"
)

# ── Cell: Data Extraction (Split by Node) ───────────────────────────────────
DATA_EXTRACTION_SPLIT_MD = md_cell(
    "### Save Data to .npy Files (Split by Node Approach)\n"
    "Implements the **Not Recommended** data storage process (for comparison/legacy requirements):\n"
    "- Split by Node Approach: `dataset/extracted/person/<subject>/<task>/<transcript>/<node_name>.npy`\n"
    "- **Expected Space:** ~4-6 GB total. Causes massive OS block space waste due to millions of tiny files.\n"
    "- **Speed:** Very slow random seek bottlenecks."
)

DATA_EXTRACTION_SPLIT_CODE = code_cell(
    "import os\n"
    "import numpy as np\n"
    "import h5py\n"
    "import glob\n"
    "\n"
    "PROJECT_ROOT = os.path.dirname(os.getcwd())\n"
    "DATASET_DIR = os.path.join(PROJECT_ROOT, 'dataset', 'zuco2')\n"
    "EXTRACTED_DIR = os.path.join(PROJECT_ROOT, 'dataset', 'extracted')\n"
    "PERSON_DIR = os.path.join(EXTRACTED_DIR, 'person')\n"
    "os.makedirs(PERSON_DIR, exist_ok=True)\n"
    "\n"
    "def get_string(f, ref):\n"
    "    try:\n"
    "        obj = f[ref]\n"
    "        return ''.join(chr(c[0]) for c in obj[:])\n"
    "    except Exception:\n"
    "        return 'Unknown'\n"
    "\n"
    "CHANNEL_LABELS = [\n"
    "    'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E9', 'E10', 'E11', 'E12', 'E13', 'E15', 'E16',\n"
    "    'E18', 'E19', 'E20', 'E22', 'E23', 'E24', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31',\n"
    "    'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40', 'E41', 'E42', 'E43', 'E44',\n"
    "    'E45', 'E46', 'E47', 'E50', 'E51', 'E52', 'E53', 'E54', 'E55', 'E57', 'E58', 'E59',\n"
    "    'E60', 'E61', 'E62', 'E64', 'E65', 'E66', 'E67', 'E69', 'E70', 'E71', 'E72', 'E74',\n"
    "    'E75', 'E76', 'E77', 'E78', 'E79', 'E80', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87',\n"
    "    'E89', 'E90', 'E91', 'E92', 'E93', 'E95', 'E96', 'E97', 'E98', 'E100', 'E101', 'E102',\n"
    "    'E103', 'E104', 'E105', 'E106', 'E108', 'E109', 'E110', 'E111', 'E112', 'E114',\n"
    "    'E115', 'E116', 'E117', 'E118', 'E120', 'E121', 'E122', 'E123', 'E124', 'Cz'\n"
    "]\n"
    "\n"
    "mat_files = glob.glob(os.path.join(DATASET_DIR, '**', 'results*.mat'), recursive=True)\n"
    "valid_files = [f for f in mat_files if os.path.getsize(f) > 1000000] # Skip tiny v7 metadata files\n"
    "\n"
    "saved_split = 0\n"
    "\n"
    "for mat_path in sorted(valid_files): # Process all valid files\n"
    "    fname = os.path.splitext(os.path.basename(mat_path))[0]\n"
    "    parts = fname.replace('results', '').split('_')\n"
    "    subject = parts[0] if len(parts) >= 2 else fname\n"
    "    task = parts[1] if len(parts) >= 2 else 'Unknown'\n"
    "    subject_dir = os.path.join(PERSON_DIR, subject, task)\n"
    "    os.makedirs(subject_dir, exist_ok=True)\n"
    "\n"
    "    try:\n"
    "        with h5py.File(mat_path, 'r') as f:\n"
    "            if 'sentenceData' not in f:\n"
    "                continue\n"
    "            sd = f['sentenceData']\n"
    "            n_sents = sd['content'].shape[0]\n"
    "            for i in range(n_sents):\n"
    "                sent_text = get_string(f, sd['content'][i, 0])\n"
    "                transcript_safe = ''.join(c if c.isalnum() else '_' for c in sent_text)[:50]\n"
    "                if not transcript_safe:\n"
    "                    transcript_safe = f'sent_{i}'\n"
    "                \n"
    "                eeg_sent = None\n"
    "                for key in ['rawData', 'mean_t1', 'mean_t2']:\n"
    "                    if key in sd:\n"
    "                        eeg_sent = f[sd[key][i, 0]][:]\n"
    "                        if np.array(eeg_sent).dtype != object:\n"
    "                            break\n"
    "                \n"
    "                if eeg_sent is None or np.array(eeg_sent).dtype == object:\n"
    "                    continue\n"
    "                \n"
    "                # Ensure shape is [channels, time_steps]\n"
    "                if eeg_sent.shape[0] > eeg_sent.shape[1]:\n"
    "                    eeg_sent = eeg_sent.T\n"
    "                \n"
    "                num_ch = eeg_sent.shape[0]\n"
    "                \n"
    "                split_dir = os.path.join(subject_dir, transcript_safe)\n"
    "                os.makedirs(split_dir, exist_ok=True)\n"
    "                \n"
    "                # Use available channels up to length of labels\n"
    "                for ch_idx in range(num_ch):\n"
    "                    ch_name = CHANNEL_LABELS[ch_idx] if ch_idx < len(CHANNEL_LABELS) else f'CH{ch_idx}'\n"
    "                    node_path = os.path.join(split_dir, f'{ch_name}.npy')\n"
    "                    np.save(node_path, eeg_sent[ch_idx, :])\n"
    "                saved_split += 1\n"
    "                \n"
    "    except Exception as e:\n"
    "        print(f'Error processing {fname}: {e}')\n"
    "\n"
    "print(f'Split by Node Data extraction complete.')\n"
    "print(f'Saved {saved_split} Split by Node directories (each containing {len(CHANNEL_LABELS)} files).')\n"
)

# ── Assemble notebook ─────────────────────────────────────────────────────────
nb["cells"] = (
    preserved[:2]  # intro md + download md
    + [preserved[2]]  # download code
    + [preserved[3]]  # setup (imports + paths)
    + [preserved[4], preserved[5]]  # helper fns md + code
    + [SUMMARY_MD, SUMMARY_CODE]
    + [USERS_MD, USERS_CODE]
    + [TRANSCRIPT_MD, TRANSCRIPT_CODE]
    + [WORDS_MD, WORDS_CODE]
    + [PREVIEW_MD, PREVIEW_CODE]
    + [SAVE_MD, SAVE_CODE]
    + [DATA_EXTRACTION_PERSON_MD, DATA_EXTRACTION_PERSON_CODE]
    + [DATA_EXTRACTION_DATA_MD, DATA_EXTRACTION_DATA_CODE]
    + [DATA_EXTRACTION_SPLIT_MD, DATA_EXTRACTION_SPLIT_CODE]
)

with open("dataset_pipeline/visualize_zuco.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Notebook rebuilt with {len(nb['cells'])} cells.")
