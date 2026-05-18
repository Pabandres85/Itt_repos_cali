"""
Fix final para Barrio Obrero:
1. Celda 15 (ITT Global) y Celda 16 (Radar): usar ANIOS_COMPLETOS [2023,2024,2025]
2. Heatmaps: mostrar '-' en trimestres sin datos (Q2-Q4 2026) con color gris
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Buscar y corregir TODAS las celdas que usan ANIOS con base (ITT Global, Radar)
for i, cell in enumerate(cells):
    if cell.get('cell_type') != 'code':
        continue
    source = cell.get('source', [])
    joined = ''.join(source)
    
    # Celda ITT Global o Radar que usa base con ANIOS
    if ('ITT Global' in joined or 'ITT por Ano' in joined or 'Composicion ITT' in joined) and 'base[' in joined:
        new_source = []
        for line in source:
            # Reemplazar ANIOS por ANIOS_COMPLETOS donde se usa con base
            if 'ax1.bar(ANIOS' in line or 'ax1.set_xticks(ANIOS' in line:
                line = line.replace('ANIOS', 'ANIOS_COMPLETOS')
            if 'ax2.bar(ANIOS' in line or 'ax2.set_xticks(ANIOS' in line or 'ax2.plot(ANIOS' in line:
                line = line.replace('ANIOS', 'ANIOS_COMPLETOS')
            if 'bottom = np.zeros(len(ANIOS))' in line:
                line = line.replace('len(ANIOS)', 'len(ANIOS_COMPLETOS)')
            new_source.append(line)
        # Agregar definicion de ANIOS_COMPLETOS al inicio si no existe
        if 'ANIOS_COMPLETOS' not in joined:
            new_source = ["ANIOS_COMPLETOS = [2023, 2024, 2025]\n", "\n"] + new_source
        cells[i]['source'] = new_source
        cells[i]['outputs'] = []
        print(f'  Celda {i} (ITT Global/Composicion): corregida a ANIOS_COMPLETOS')
    
    # Radar
    if 'Radar ITT' in joined and 'polar' in joined and 'base[' in joined:
        new_source = []
        for line in source:
            if 'enumerate(ANIOS)' in line:
                line = line.replace('enumerate(ANIOS)', 'enumerate(ANIOS_COMPLETOS)')
            new_source.append(line)
        if 'ANIOS_COMPLETOS' not in ''.join(new_source):
            new_source = ["ANIOS_COMPLETOS = [2023, 2024, 2025]\n", "COLORES_R = ['#42A5F5', '#2E7D32', '#E53935']\n", "\n"] + new_source
        cells[i]['source'] = new_source
        cells[i]['outputs'] = []
        print(f'  Celda {i} (Radar): corregida a ANIOS_COMPLETOS')

# Corregir Heatmaps: mostrar '-' en trimestres sin datos
for i, cell in enumerate(cells):
    if cell.get('cell_type') != 'code':
        continue
    source = cell.get('source', [])
    joined = ''.join(source)
    
    if 'sns.heatmap' in joined and 'pivot' in joined and 'Heatmap' in joined:
        # Reemplazar la logica del heatmap para manejar NaN como '-'
        new_source = []
        for line in source:
            # Cambiar pivot para que incluya todos los trimestres (1-4) para todos los años
            # y reemplazar annot=True, fmt='.0f' por anotaciones custom
            if "sns.heatmap(pivot, annot=True, fmt='.0f'" in line:
                # Reemplazar con anotaciones custom que muestren '-' para NaN/0 en Q2-Q4 2026
                new_source.append("    # Anotaciones: '-' para trimestres sin datos\n")
                new_source.append("    annot_arr = pivot.copy().astype(object)\n")
                new_source.append("    for c in annot_arr.columns:\n")
                new_source.append("        for r in annot_arr.index:\n")
                new_source.append("            val = pivot.loc[r, c]\n")
                new_source.append("            if r == 2026 and c != 'Q1':\n")
                new_source.append("                annot_arr.loc[r, c] = '-'\n")
                new_source.append("            elif pd.isna(val) or val == 0:\n")
                new_source.append("                annot_arr.loc[r, c] = '-' if r == 2026 else '0'\n")
                new_source.append("            else:\n")
                new_source.append("                annot_arr.loc[r, c] = f'{val:.0f}'\n")
                # Reemplazar NaN en pivot con 0 para que el colormap funcione
                new_source.append("    pivot_plot = pivot.fillna(0)\n")
                # Escribir la linea de heatmap con annot custom
                line_new = line.replace("sns.heatmap(pivot, annot=True, fmt='.0f'", "sns.heatmap(pivot_plot, annot=annot_arr.values, fmt=''")
                new_source.append(line_new)
            else:
                new_source.append(line)
        
        cells[i]['source'] = new_source
        cells[i]['outputs'] = []
        print(f'  Celda {i} (Heatmap): anotaciones con - para trimestres sin datos')

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('\nListo:')
print('  - ITT Global y Radar usan solo 2023-2025')
print('  - Heatmaps muestran - en Q2-Q4 2026 (sin datos)')
