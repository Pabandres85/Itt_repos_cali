"""Fix Cards en Roosevelt v2 y Barrio Obrero.
Comparacion solo entre años reales (2023-2025), no contra 2026 Proxy.
"""
import json
from pathlib import Path

def fix_cards(nb_path, cards_idx):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    source = cells[cards_idx]['source']

    new_source = []
    for line in source:
        # Reemplazar la linea que define año_ini, año_ant, año_ult
        if 'año_ini, año_ant, año_ult' in line and 'ANIOS' in line:
            new_source.append("# Comparacion entre años REALES (2023-2025). 2026 es Proxy, no se compara.\n")
            new_source.append("año_ini, año_ant, año_ult = 2023, 2024, 2025\n")
        else:
            new_source.append(line)

    cells[cards_idx]['source'] = new_source
    cells[cards_idx]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print(f'  {nb_path.name}: Cards (celda {cards_idx}) corregida -> compara 2023 vs 2024 vs 2025')


nb_dir = Path(__file__).parent

# Roosevelt v2
fix_cards(nb_dir / '01_itt_roosevelt_v2.ipynb', 20)

print('\nListo. Cards comparan solo datos reales (2023-2025).')
