import glob
import json
import re

# 1. Patch the actual Jupyter Notebooks safely
for nb_file in glob.glob("training/*.ipynb"):
    try:
        with open(nb_file, "r", encoding="utf-8") as f:
            nb = json.load(f)

        modified = False
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                new_source = []
                for line in cell["source"]:
                    if "if eeg_data.shape[1] < self.max_len:" in line:
                        if "len(eeg_data.shape) != 2" not in "".join(new_source):
                            new_source.append(
                                "        if len(eeg_data.shape) != 2 or eeg_data.shape[0] != 105:\n"
                            )
                            new_source.append(
                                "            eeg_data = np.zeros((105, self.max_len))\n"
                            )
                            modified = True
                    new_source.append(line)
                cell["source"] = new_source

        if modified:
            with open(nb_file, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=1)
            print(f"Patched notebook {nb_file}")
    except Exception as e:
        print(f"Failed to patch {nb_file}: {e}")

# 2. Patch the generator scripts so future generation is safe
for py_file in glob.glob("scripts/make_notebook*.py"):
    try:
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "len(eeg_data.shape) != 2" not in content:
            # Safely replace the line without relying on exact quote formatting
            new_content = re.sub(
                r'([ "\']*)if eeg_data\.shape\[1\] < self\.max_len:\\n(["\']*,)',
                r"\1if len(eeg_data.shape) != 2 or eeg_data.shape[0] != 105:\\n\2\n\1    eeg_data = np.zeros((105, self.max_len))\\n\2\n\1if eeg_data.shape[1] < self.max_len:\\n\2",
                content,
            )
            if new_content != content:
                with open(py_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Patched script {py_file}")
    except Exception as e:
        print(f"Failed to patch {py_file}: {e}")
