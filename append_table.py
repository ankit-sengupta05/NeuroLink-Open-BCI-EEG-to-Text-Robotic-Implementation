import os

docs = ['notes.md', 'PRD.md', 'README.md', 'resources.md']
with open('mapping_table.md', 'r') as f:
    table = f.read()

for doc in docs:
    with open(doc, 'a', encoding='utf-8') as f:
        f.write('\n\n### EEG Channel Mapping Reference (ZuCo 2.0)\n\n')
        f.write('This table documents the exact mapping of the 105 rows in our `.h5` EEG matrices to their original Geodesic 128-channel sensor names.\n\n')
        f.write(table)
    print(f'Appended to {doc}')

print('Done applying tables.')
