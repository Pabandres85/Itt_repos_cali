"""Fix Celda 11B: Anotacion de Comuna 9 mas arriba y solo con total."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Buscar Celda 11B code
target_idx = None
for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if '11B' in source and 'Educacion' in source:
            target_idx = i + 1
            break

if target_idx:
    source = cells[target_idx]['source']
    new_source = []
    for line in source:
        # Reemplazar la anotacion
        if 'ax.annotate' in line:
            new_source.append("    ax.annotate(f'C9 Total: {int(c9.Total):,}',\n")
        elif "xy=(idx_c9, c9['Total'])" in line:
            new_source.append("               xy=(idx_c9, max(c9['Oficial'], c9['No oficial'])),\n")
        elif "xytext=(idx_c9+2, c9['Total']+3000)" in line:
            new_source.append("               xytext=(idx_c9+3, 22000),\n")
        elif "fontsize=8, color='#E53935'" in line:
            new_source.append("               fontsize=9, color='#E53935', fontweight='bold',\n")
        else:
            new_source.append(line)
    
    cells[target_idx]['source'] = new_source
    cells[target_idx]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)
    print('Celda 11B: anotacion ajustada - solo total, flecha mas arriba')
