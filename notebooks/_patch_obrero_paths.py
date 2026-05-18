"""Actualizar PATHS en Barrio Obrero con los nuevos nombres de archivos GeoJSON (2026T1)."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Mapeo de nombres viejos a nuevos
replacements = {
    "HOMICIDIOS_2023_2025_Obrero.geojson": "DATIC_homicidios_2023_2026T1_Barrio_O.geojson",
    "HURTOS_2023_2025_OBRERO.geojson": "DATIC_hurtos_2023_2026T1_Barrio_O.geojson",
    "VIOLENCIA_INTRAFAMILIAR_2023_2025_OBRERO.geojson": "DATIC_violencia_intrafamiliar_2023_2026T1_Barrio_O.geojson",
    "COMPARENDOS_2023_2025_OBRERO.geojson": "DATIC_comparendos_2023_2026T1_Barrio_O.geojson",
}

# Buscar y reemplazar en todas las celdas
total_replaced = 0
for i, cell in enumerate(cells):
    if cell.get('cell_type') != 'code':
        continue
    source = cell.get('source', [])
    new_source = []
    cell_modified = False
    for line in source:
        original = line
        for old_name, new_name in replacements.items():
            if old_name in line:
                line = line.replace(old_name, new_name)
        if line != original:
            cell_modified = True
        new_source.append(line)
    if cell_modified:
        cells[i]['source'] = new_source
        cells[i]['outputs'] = []
        total_replaced += 1

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print(f'Rutas actualizadas en {total_replaced} celdas:')
for old, new in replacements.items():
    print(f'  {old}')
    print(f'    -> {new}')
