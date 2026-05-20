import json

# Inspect Pulmon notebook
nb = json.load(open(r'notebooks\04_itt_pulmon_oriente_2026_v2.ipynb', 'r', encoding='utf-8'))
print(f"=== PULMON NOTEBOOK: {len(nb['cells'])} cells ===")
for i, c in enumerate(nb['cells']):
    src = c['source']
    first_line = src[0][:90] if src else "(empty)"
    print(f"  {i:2d}: {c['cell_type']:8s} | {first_line.strip()}")

print("\n")

# Inspect AvCali notebook
nb2 = json.load(open(r'notebooks\02_itt_avenida_ciudad_de_cali.ipynb', 'r', encoding='utf-8'))
print(f"=== AV CALI NOTEBOOK: {len(nb2['cells'])} cells ===")
for i, c in enumerate(nb2['cells']):
    src = c['source']
    first_line = src[0][:90] if src else "(empty)"
    print(f"  {i:2d}: {c['cell_type']:8s} | {first_line.strip()}")
