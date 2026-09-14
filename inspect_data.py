import json

with open("dataset_pipeline/visualize_zuco.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"][:4]):
    print(f"=== Cell {i} ({cell['cell_type']}) ===")
    print("".join(cell["source"])[:200])
    print()
