import json

# Pulmon notebook - read key cells
nb = json.load(open(r'notebooks\04_itt_pulmon_oriente_2026_v2.ipynb', 'r', encoding='utf-8'))

print("=== PULMON Cell 16 (Procesamiento) - first 5 lines ===")
src = ''.join(nb['cells'][16]['source'])
print(src[:300])
print("...")
print("=== PULMON Cell 16 - last 30 lines ===")
lines = src.split('\n')
print('\n'.join(lines[-30:]))

print("\n\n=== PULMON Cell 18 (Normalizacion) - first 20 lines ===")
src18 = ''.join(nb['cells'][18]['source'])
print(src18[:600])

print("\n\n=== PULMON Cell 20 (Cards) - first 10 lines ===")
src20 = ''.join(nb['cells'][20]['source'])
print(src20[:400])

print("\n\n=== PULMON Cell 22 (Heatmap Seg) - first 5 lines ===")
src22 = ''.join(nb['cells'][22]['source'])
print(src22[:300])

print("\n\n=== PULMON Cell 24 (Heatmap Cohesion) - first 5 lines ===")
src24 = ''.join(nb['cells'][24]['source'])
print(src24[:300])

print("\n\n=== PULMON Cell 26 (Barras Seg) - first 10 lines ===")
src26 = ''.join(nb['cells'][26]['source'])
print(src26[:500])

print("\n\n=== PULMON Cell 28 (Barras Cohesion) - first 10 lines ===")
src28 = ''.join(nb['cells'][28]['source'])
print(src28[:500])

print("\n\n=== PULMON Cell 30 (ITT Global) - first 10 lines ===")
src30 = ''.join(nb['cells'][30]['source'])
print(src30[:500])

print("\n\n=== PULMON Cell 32 (Radar) - first 10 lines ===")
src32 = ''.join(nb['cells'][32]['source'])
print(src32[:500])
