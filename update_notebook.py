import json

CHANNEL_LABELS = [
    "E2",
    "E3",
    "E4",
    "E5",
    "E6",
    "E7",
    "E9",
    "E10",
    "E11",
    "E12",
    "E13",
    "E15",
    "E16",
    "E18",
    "E19",
    "E20",
    "E22",
    "E23",
    "E24",
    "E26",
    "E27",
    "E28",
    "E29",
    "E30",
    "E31",
    "E33",
    "E34",
    "E35",
    "E36",
    "E37",
    "E38",
    "E39",
    "E40",
    "E41",
    "E42",
    "E43",
    "E44",
    "E45",
    "E46",
    "E47",
    "E50",
    "E51",
    "E52",
    "E53",
    "E54",
    "E55",
    "E57",
    "E58",
    "E59",
    "E60",
    "E61",
    "E62",
    "E64",
    "E65",
    "E66",
    "E67",
    "E69",
    "E70",
    "E71",
    "E72",
    "E74",
    "E75",
    "E76",
    "E77",
    "E78",
    "E79",
    "E80",
    "E82",
    "E83",
    "E84",
    "E85",
    "E86",
    "E87",
    "E89",
    "E90",
    "E91",
    "E92",
    "E93",
    "E95",
    "E96",
    "E97",
    "E98",
    "E100",
    "E101",
    "E102",
    "E103",
    "E104",
    "E105",
    "E106",
    "E108",
    "E109",
    "E110",
    "E111",
    "E112",
    "E114",
    "E115",
    "E116",
    "E117",
    "E118",
    "E120",
    "E121",
    "E122",
    "E123",
    "E124",
    "Cz",
]

nb_path = "dataset_pipeline/visualize_zuco.ipynb"
with open(nb_path, "r") as f:
    nb = json.load(f)

new_plot_code = f'''def get_string(f, ref):
    """Extracts string from h5py object reference."""
    try:
        obj = f[ref]
        return "".join(chr(c[0]) for c in obj[:])
    except Exception:
        return "Unknown"

CHANNEL_LABELS = {CHANNEL_LABELS}

def plot_eeg(eeg_data, title, filename, channel_labels=CHANNEL_LABELS):
    """
    Plots all EEG channels on a single heatmap graph and saves the image.
    eeg_data shape is usually (channels, time) or (time, channels).
    """
    if eeg_data is None or eeg_data.size == 0:
        return

    eeg_data = np.array(eeg_data)
    # Ensure shape is (channels, time)
    if eeg_data.shape[0] > eeg_data.shape[1]:
        eeg_data = eeg_data.T

    num_channels, _time_points = eeg_data.shape

    fig, ax = plt.subplots(figsize=(15, 20))
    cax = ax.imshow(eeg_data, aspect='auto', cmap='viridis')
    fig.colorbar(cax, ax=ax, label='Amplitude')

    ax.set_title(title)
    ax.set_xlabel("Time points")
    ax.set_ylabel("EEG Channels")

    if channel_labels and num_channels == len(channel_labels):
        ax.set_yticks(np.arange(num_channels))
        ax.set_yticklabels(channel_labels, fontsize=8)
    else:
        ax.set_yticks(np.arange(0, num_channels, max(1, num_channels//20)))

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
'''

for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "def plot_eeg" in "".join(cell["source"]):
        cell["source"] = [line + "\n" for line in new_plot_code.split("\n")]
        cell["source"][-1] = cell["source"][-1].rstrip("\n")
        break

with open(nb_path, "w") as f:
    json.dump(nb, f, indent=1)

print("Updated visualization script.")
