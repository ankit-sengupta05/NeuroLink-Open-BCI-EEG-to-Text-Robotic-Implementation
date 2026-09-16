import mne

# 105 Channels expected from mapping_table.md
VALID_ELECTRODES = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    9,
    10,
    11,
    12,
    13,
    15,
    16,
    17,
    18,
    19,
    20,
    22,
    23,
    24,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    44,
    45,
    46,
    47,
    50,
    51,
    52,
    53,
    54,
    55,
    57,
    58,
    59,
    60,
    61,
    62,
    64,
    65,
    66,
    67,
    69,
    70,
    71,
    72,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    82,
    83,
    84,
    85,
    86,
    87,
    89,
    90,
    91,
    92,
    93,
    95,
    96,
    97,
    98,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    108,
    109,
    110,
    111,
    112,
    114,
    115,
    116,
    117,
    118,
    121,
    122,
    123,
    124,
]


def generate_mapping():
    montage = mne.channels.make_standard_montage("GSN-HydroCel-128")
    positions = montage.get_positions()["ch_pos"]

    output_lines = [
        "# 105-Channel EGI HydroCel-128 Coordinate-Based Scalp and Functional Candidate Map",
        "",
        "> **Disclaimer**: Electrode labels represent nominal scalp-coordinate regions and task-related hypotheses. They do not establish direct correspondence between any electrode and a specific cortical area. Functional assignments must be validated using participant-specific electrode digitization, anatomical registration, source localization, and task-based statistical analysis.",
        "",
        "## Notes",
        "- **Cz stand-in**: The 128-net has no vertex electrode (Cz). E55 serves as the midline vertex stand-in.",
        "- **FpZ/Frontal-pole**: E17 serves as the frontal-pole electrode.",
        "- **Coordinates**: Expressed in cm, normalized from the MNE standard montage.",
        "",
        "## Functional Envelopes",
        "- **Left inferior-frontal language-related candidate (Broca's candidate)**: `x <= -4.0, y >= 1.0, z >= -1.0`",
        "- **Left lateral/superior-temporal language-related candidate (Wernicke's candidate)**: `x <= -4.0, y < 1.0, z < 5.0`",
        "- **Right inferior-frontal homolog candidate**: `x >= 4.0, y >= 1.0, z >= -1.0`",
        "- **Medial frontal speech-preparation candidate (pre-SMA/SMA candidate)**: `|x| <= 2.0, y >= 2.0, z >= 5.0`",
        "",
        "| Electrode | Original Num | x (cm) | y (cm) | z (cm) | Scalp Region | Functional Candidate Hypothesis | Confidence |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for e_num in VALID_ELECTRODES:
        name = f"E{e_num}"
        # Fetch pos in meters, convert to cm
        pos = positions.get(name)
        if pos is None:
            continue

        x, y, z = pos * 100

        # Hemisphere logic
        if abs(x) <= 1.0:
            hemi = "Midline"
        elif x < -1.0:
            hemi = "Left"
        else:
            hemi = "Right"

        # Region logic
        if y >= 3.0:
            region = "Frontal"
        elif -2.0 <= y < 3.0:
            region = "Central"
        elif -6.9 <= y < -2.0:
            region = "Parietal"
        else:
            region = "Occipital"

        # Lateral border override
        if abs(x) >= 6.0 and z <= 3.0:
            region = "Lateral-temporal border"

        scalp_region = f"{hemi} {region}"

        # Override for landmarks
        confidence = "Medium"
        if e_num == 11:
            name = "Fz (E11)"
            scalp_region = "Midline Frontal"
            confidence = "High (nominal 10-10 correspondence)"
        elif e_num == 36:
            name = "C3 (E36)"
            scalp_region = "Left Central"
            confidence = "High (nominal 10-10 correspondence)"
        elif e_num == 104:
            name = "C4 (E104)"
            scalp_region = "Right Central"
            confidence = "High (nominal 10-10 correspondence)"
        elif e_num == 62:
            name = "Pz (E62)"
            scalp_region = "Midline Parietal"
            confidence = "High (nominal 10-10 correspondence)"
        elif e_num == 75:
            name = "Oz (E75)"
            scalp_region = "Midline Occipital"
            confidence = "High (nominal 10-10 correspondence)"

        # Add special notes for E55, E17
        if e_num == 55:
            scalp_region += " (Cz stand-in)"
        elif e_num == 17:
            scalp_region += " (Frontal-pole)"

        # Functional Envelopes
        funcs = []
        if x <= -4.0 and y >= 1.0 and z >= -1.0:
            funcs.append("Left inferior-frontal language-related")
        if x <= -4.0 and y < 1.0 and z < 5.0:
            funcs.append("Left lateral/superior-temporal language-related")
        if x >= 4.0 and y >= 1.0 and z >= -1.0:
            funcs.append("Right inferior-frontal homolog")
        if abs(x) <= 2.0 and y >= 2.0 and z >= 5.0:
            funcs.append("Medial frontal speech-preparation")

        func_str = ", ".join(funcs) if funcs else "-"

        output_lines.append(
            f"| **{name}** | {e_num} | {x:.2f} | {y:.2f} | {z:.2f} | {scalp_region} | {func_str} | {confidence} |"
        )

    with open("channel_EEG_Mapping.md", "w") as f:
        f.write("\n".join(output_lines))


if __name__ == "__main__":
    generate_mapping()
    print("Generated channel_EEG_Mapping.md successfully.")
