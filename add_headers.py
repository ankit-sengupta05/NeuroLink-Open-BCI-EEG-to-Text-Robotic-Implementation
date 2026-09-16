import os
import glob

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

HEADER = """# ==============================================================================
# Copyright (c) 2026 Ankit Sengupta. All rights reserved.
# 
# This source code is licensed under the Research & Non-Commercial Attribution 
# License (RNCA) found in the LICENSE file in the root directory of this project.
# 
# If you use, evaluate, or substantially derive from this code in an academic 
# publication, you MUST provide appropriate citation to the original author 
# and repository. See CITATION.cff for citation details.
# ==============================================================================
"""

py_files = glob.glob(os.path.join(PROJECT_ROOT, "scripts", "*.py")) + glob.glob(os.path.join(PROJECT_ROOT, "*.py"))

for py_file in py_files:
    if "append_table.py" in py_file or "generate_examples.py" in py_file or "generate_original.py" in py_file or "patch_nb.py" in py_file:
        continue # Skip temp scripts
        
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "Copyright (c) 2026 Ankit Sengupta" not in content:
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write(HEADER + "\n" + content)
        print(f"Added header to {os.path.basename(py_file)}")

print("Done appending headers.")
