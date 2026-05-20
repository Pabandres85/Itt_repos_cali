import json

# Read Pulmon Oriente cells 5,6 (clone), 15-16 (celda 6-7), 19-20 (celda 8-9), 22-24 (celda 10-11), 26-28 (celda 12), 30-32 (celda 13-14)
nb_path = r'notebooks/04_itt_pulmon_oriente_2026_v2.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_read = [5, 6, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
for i in cells_to_read:
    c = nb['cells'][i]
    src = ''.join(c['source'])
    print(f"\n{'='*80}")
    print(f"CELL {i} [{c['cell_type']}]:")
    print(f"{'='*80}")
    print(src[:2000])
    print("..." if len(src) > 2000 else "")
