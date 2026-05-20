import json

nb = json.load(open(r'notebooks\02_itt_avenida_ciudad_de_cali.ipynb', 'r', encoding='utf-8'))

print("=== AVCALI Cell 26 (Barras Seg) FULL ===")
src26 = ''.join(nb['cells'][26]['source'])
print(src26)

print("\n\n=== AVCALI Cell 30 (Barras Cohesion) FULL ===")
src30 = ''.join(nb['cells'][30]['source'])
print(src30)

print("\n\n=== AVCALI Cell 32 (Heatmap Cohesion) FULL ===")
src32 = ''.join(nb['cells'][32]['source'])
print(src32)

print("\n\n=== AVCALI Cell 28 (Barras Movilidad) FULL ===")
src28 = ''.join(nb['cells'][28]['source'])
print(src28)
