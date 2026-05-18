"""Fix: Celda 12 Seguridad - corregir idx%3 a idx para usar los 4 colores."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
source = cells[34]['source']
new_source = []
for line in source:
    line = line.replace('COLORES[idx%3]', 'COLORES[idx]')
    new_source.append(line)

cells[34]['source'] = new_source
cells[34]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 12: idx%3 -> idx (4 colores unicos para 4 años)')
