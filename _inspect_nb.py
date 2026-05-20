import json, sys

nb_path = sys.argv[1]
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f'Total cells: {len(cells)}')
for i, c in enumerate(cells):
    src = c['source']
    first_line = src[0].strip()[:90] if src else '(empty)'
    print(f'  Cell {i:2d} [{c["cell_type"]:8s}]: {first_line}')
