import json

# Read the robust download script
with open("dataset_pipeline/download_zuco2.py", "r", encoding="utf-8") as f:
    download_code = f.read()

# Make it notebook compatible
download_code = download_code.replace(
    "PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
    "# Resolve dataset directory (../dataset/zuco2)\nPROJECT_ROOT = os.path.dirname(os.getcwd())",
)

# Remove the if __name__ == "__main__": block and just execute it directly in the notebook cell,
# but to be safe and clean, we'll keep the function definitions and just adjust the bottom execution block.
download_code = download_code.replace(
    'if __name__ == "__main__":', "# Execute Download"
)
# De-indent the bottom block
lines = download_code.split("\n")
new_lines = []
in_main = False
for line in lines:
    if line == "# Execute Download":
        in_main = True
        new_lines.append(line)
        continue
    if in_main:
        if line.startswith("    "):
            new_lines.append(line[4:])
        else:
            if line.strip() != "":
                in_main = False  # Left the block
            new_lines.append(line)
    else:
        new_lines.append(line)

new_download_code = "\n".join(new_lines)

# Read the notebook
with open("dataset_pipeline/visualize_zuco.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# The download cell is cell index 2
nb["cells"][2]["source"] = [line + "\n" for line in new_download_code.split("\n")]
nb["cells"][2]["source"][-1] = nb["cells"][2]["source"][-1].rstrip(
    "\n"
)  # Remove trailing newline from last line

# Write it back
with open("dataset_pipeline/visualize_zuco.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook cell 2 updated with the resumable download code.")
