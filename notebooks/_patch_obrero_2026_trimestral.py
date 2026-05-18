"""
Barrio Obrero: ANIOS incluye 2026 para datos trimestrales.
- Q1 2026 = dato real
- Q2-Q4 2026 = Proxy** (promedio historico 2023-2025)
- Cards, ITT Global, Radar = solo 2023-2025 (años completos)
- Heatmaps, Barras trimestrales = incluyen 2026 con Proxy**
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# 1. Cambiar ANIOS a incluir 2026 (celda 10)
source = cells[10]['source']
new_source = []
for line in source:
    if '[2023, 2024, 2025]' in line and 'ANIOS' in line:
        line = line.replace('[2023, 2024, 2025]', '[2023, 2024, 2025, 2026]')
        print('  ANIOS actualizado a [2023, 2024, 2025, 2026]')
    new_source.append(line)
cells[10]['source'] = new_source
cells[10]['outputs'] = []

# 2. Inyectar logica Proxy en celda de procesamiento (celda 22)
# Buscar donde termina el procesamiento actual
source22 = cells[22]['source']
joined22 = ''.join(source22)

# Si ya tiene Proxy, no agregar de nuevo
if 'PROXY' not in joined22 and 'proxy' not in joined22:
    proxy_code = [
        "\n",
        "# ══════════════════════════════════════════════════════════\n",
        "# VALORES PROXY Q2-Q4 2026\n",
        "# Q1 2026 tiene datos reales. Q2-Q4 se estiman con promedio historico.\n",
        "# ══════════════════════════════════════════════════════════\n",
        "indicadores_trim = [c for c in corr_trim.columns if c not in ['año','trimestre','periodo']]\n",
        "hist_trim = corr_trim[corr_trim['año'].isin([2023, 2024, 2025])]\n",
        "\n",
        "for trim in [2, 3, 4]:\n",
        "    mask = (corr_trim['año'] == 2026) & (corr_trim['trimestre'] == trim)\n",
        "    if corr_trim.loc[mask, indicadores_trim].sum().sum() == 0:  # Si Q2-Q4 estan en 0\n",
        "        trim_hist = hist_trim[hist_trim['trimestre'] == trim]\n",
        "        for ind in indicadores_trim:\n",
        "            corr_trim.loc[mask, ind] = round(trim_hist[ind].mean(), 1)\n",
        "\n",
        "corr_trim['es_proxy'] = (corr_trim['año'] == 2026) & (corr_trim['trimestre'].isin([2,3,4]))\n",
        "\n",
        "print()\n",
        "print('Proxy Q2-Q4 2026 aplicado (promedio historico 2023-2025):')\n",
        "print(corr_trim[corr_trim['año']==2026][['año','trimestre'] + indicadores_trim].to_string(index=False))\n",
    ]
    cells[22]['source'] = source22 + proxy_code
    cells[22]['outputs'] = []
    print('  Logica Proxy Q2-Q4 inyectada en celda 22')
else:
    print('  Celda 22 ya tiene logica Proxy')

# 3. Celda 15 (ITT Global) y Celda 16 (Radar) - filtrar a 2023-2025
# Buscar estas celdas y agregar filtro
for i in range(len(cells)):
    cell = cells[i]
    if cell.get('cell_type') != 'code':
        continue
    source = ''.join(cell.get('source', []))
    
    # ITT Global (tiene 'ITT por Ano' o 'Composicion ITT')
    if 'ITT por Ano' in source or 'ITT Global' in source and 'suptitle' in source:
        lines = cell['source']
        # Agregar filtro al inicio si no existe
        if 'base_anual' not in source:
            cell['source'] = [
                "# Solo años con datos completos para ITT Global\n",
                "base_anual = base[base['año'].isin([2023, 2024, 2025])].copy()\n",
                "ANIOS_COMPLETOS = [2023, 2024, 2025]\n",
                "\n",
            ] + [line.replace('base[', 'base_anual[').replace("base['", "base_anual['").replace('ANIOS', 'ANIOS_COMPLETOS') if 'base' in line or 'ANIOS' in line else line for line in lines]
            cell['outputs'] = []
            print(f'  Celda {i} (ITT Global): filtrada a 2023-2025')
        break

for i in range(len(cells)):
    cell = cells[i]
    if cell.get('cell_type') != 'code':
        continue
    source = ''.join(cell.get('source', []))
    
    # Radar (tiene 'Radar ITT')
    if 'Radar ITT' in source and 'polar' in source:
        lines = cell['source']
        if 'base_anual' not in source:
            cell['source'] = [
                "# Solo años con datos completos para Radar\n",
                "base_anual = base[base['año'].isin([2023, 2024, 2025])].copy()\n",
                "ANIOS_COMPLETOS = [2023, 2024, 2025]\n",
                "\n",
            ] + [line.replace('base[', 'base_anual[').replace("base['", "base_anual['").replace('ANIOS', 'ANIOS_COMPLETOS') if ('base' in line or 'ANIOS' in line) and 'base_anual' not in line and 'ANIOS_COMPLETOS' not in line else line for line in lines]
            cell['outputs'] = []
            print(f'  Celda {i} (Radar): filtrada a 2023-2025')
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('\nListo. Barrio Obrero ahora:')
print('  - ANIOS = [2023, 2024, 2025, 2026]')
print('  - Heatmaps/Barras: Q1 2026 real + Q2-Q4 Proxy**')
print('  - Cards: 2025 vs 2024 (sin 2026)')
print('  - ITT Global: solo 2023-2025')
print('  - Radar: solo 2023-2025')
