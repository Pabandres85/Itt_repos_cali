import json

# Read Av Cali cells: 5-6 (clone/3A), 7-8 (celda 3), 25-26 (celda 11), 27-30 (celda 12, 12B), 31-32 (celda 13)
nb_path = r'notebooks/02_itt_avenida_ciudad_de_cali.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_read = [5, 6, 7, 8, 25, 26, 27, 28, 29, 30, 31, 32]
for i in cells_to_read:
    c = nb['cells'][i]
    src = ''.join(c['source'])
    print(f"\n{'='*80}")
    print(f"CELL {i} [{c['cell_type']}]:")
    print(f"{'='*80}")
    print(src[:3000])
    if len(src) > 3000:
        print("...(truncated)")
