import json

# AvCali notebook - read key cells
nb = json.load(open(r'notebooks\02_itt_avenida_ciudad_de_cali.ipynb', 'r', encoding='utf-8'))

print("=== AVCALI Cell 6 (Celda 3A - Subida ZIPs) ===")
src6 = ''.join(nb['cells'][6]['source'])
print(src6[:500])

print("\n\n=== AVCALI Cell 8 (Celda 3 - Rutas) ===")
src8 = ''.join(nb['cells'][8]['source'])
print(src8[:600])

print("\n\n=== AVCALI Cell 26 (Celda 11 - Barras Seg) - first 20 lines ===")
src26 = ''.join(nb['cells'][26]['source'])
print(src26[:600])

print("\n\n=== AVCALI Cell 28 (Celda 12 - Barras Movilidad) - first 20 lines ===")
src28 = ''.join(nb['cells'][28]['source'])
print(src28[:600])

print("\n\n=== AVCALI Cell 30 (Celda 12B - Barras Cohesion) - first 20 lines ===")
src30 = ''.join(nb['cells'][30]['source'])
print(src30[:600])

print("\n\n=== AVCALI Cell 32 (Celda 13 - Heatmap Cohesion) - first 20 lines ===")
src32 = ''.join(nb['cells'][32]['source'])
print(src32[:600])

print("\n\n=== AVCALI Cell 44 (last code cell - export) ===")
src44 = ''.join(nb['cells'][44]['source'])
print(src44[:300])

# Check if clone cell exists before Celda 3A
print("\n\n=== Checking cells 4-6 for clone ===")
for i in range(4, 7):
    src = ''.join(nb['cells'][i]['source'])
    print(f"Cell {i}: {src[:100]}")
