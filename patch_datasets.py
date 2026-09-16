import glob
import os

target = '        if eeg_data.shape[1] < self.max_len:\\n",'
replacement = '''        if len(eeg_data.shape) != 2 or eeg_data.shape[0] != 105:\\n",
"            eeg_data = np.zeros((105, self.max_len))\\n",
"        if eeg_data.shape[1] < self.max_len:\\n",'''

for f in glob.glob('scripts/make_notebook*.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'eeg_data.shape[0] != 105' not in content:
        content = content.replace(target, replacement)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Patched {f}")
