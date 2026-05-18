"""
Quitar 2026 de ANIOS en Barrio Obrero y Roosevelt.
Estos notebooks no tienen datos reales de 2026.
El Proxy 2026 solo aplica a Pulmon de Oriente (que tiene Q1 real).

Tambien elimina la logica Proxy inyectada anteriormente.
"""
import json
from pathlib import Path

def fix_notebook(nb_path, params_idx):
    print(f'\nParcheando: {nb_path.name}')
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    # 1. Revertir ANIOS a [2023, 2024, 2025]
    source = cells[params_idx]['source']
    new_source = []
    for line in source:
        if '[2023, 2024, 2025, 2026]' in line:
            line = line.replace('[2023, 2024, 2025, 2026]', '[2023, 2024, 2025]')
            print(f'  ANIOS revertido a [2023, 2024, 2025]')
        new_source.append(line)
    cells[params_idx]['source'] = new_source
    cells[params_idx]['outputs'] = []

    # 2. Eliminar la logica Proxy de la celda de procesamiento
    for i in range(params_idx + 1, len(cells)):
        cell = cells[i]
        if cell.get('cell_type') != 'code':
            continue
        source_joined = ''.join(cell.get('source', []))
        if 'VALORES PROXY 2026' in source_joined or 'proxy_anual' in source_joined:
            # Cortar la seccion Proxy
            lines = cell['source']
            cut_idx = None
            for j, line in enumerate(lines):
                if 'VALORES PROXY 2026' in line or 'Eliminar fila 2026' in line:
                    cut_idx = j - 1
                    break
            if cut_idx and cut_idx > 0:
                cell['source'] = lines[:cut_idx]
                cell['outputs'] = []
                print(f'  Logica Proxy eliminada de celda {i}')
            break

    # 3. Eliminar figtext de ** 2026 en graficos (ya no aplica)
    for i in range(len(cells)):
        cell = cells[i]
        if cell.get('cell_type') != 'code':
            continue
        source = cell.get('source', [])
        new_lines = []
        modified = False
        for line in source:
            if '** 2026' in line and 'figtext' in line:
                modified = True
                continue  # skip this line
            if "label=str(año) + ('**' if año==2026 else '')" in line:
                line = line.replace("label=str(año) + ('**' if año==2026 else '')", "label=str(año)")
                modified = True
            new_lines.append(line)
        if modified:
            cell['source'] = new_lines
            cell['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print(f'  Guardado: {nb_path.name}')
    print(f'  Ahora solo trabaja con 2023-2025 (datos reales)')


nb_dir = Path(__file__).parent
fix_notebook(nb_dir / '03_itt_barrio_obrero.ipynb', 10)
fix_notebook(nb_dir / '01_itt_roosevelt_v2.ipynb', 10)

print('\n' + '='*60)
print('LISTO. Barrio Obrero y Roosevelt vuelven a 2023-2025.')
print('Solo Pulmon de Oriente mantiene 2026 con Proxy.')
print('='*60)
