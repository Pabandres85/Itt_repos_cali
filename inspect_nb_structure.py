import json

# Inspect Pulmon Oriente notebook
nb_path = r'notebooks/04_itt_pulmon_oriente_2026_v2.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
print("="*80)
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    first_line = src.split('\n')[0][:100] if src else "(empty)"
    print(f"Cell {i:2d} [{c['cell_type']:8s}]: {first_line}")
