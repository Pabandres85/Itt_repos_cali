"""
Barrio Obrero: Educacion usa 54.9 (Proxy) para 2023-2025 y 31.5 (real) para Q1 2026.
Fuente dato real: geojson_educacion.zip -> Comuna 9 -> score_educacion = 31.5
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Celda 24 (normalizacion) - agregar logica diferenciada para score_educ_des
source = cells[24]['source']
new_source = []
for line in source:
    if "base['score_educ_des']  = REF_EDUC_DES" in line:
        new_source.append("# Educacion: 54.9 (Proxy) para 2023-2025\n")
        new_source.append("base['score_educ_des']  = REF_EDUC_DES  # 54.9 para años completos\n")
    else:
        new_source.append(line)

cells[24]['source'] = new_source
cells[24]['outputs'] = []

# Celda 22 (procesamiento) - agregar REF_EDUC_DES_2026 y aplicar en corr_trim
source22 = cells[22]['source']
# Agregar al final la logica de score_educ_des diferenciado en corr_trim
extra = [
    "\n",
    "# === Score Educacion diferenciado por periodo ===\n",
    "# 2023-2025: Proxy 54.9 (sin datos propios)\n",
    "# 2026 Q1: Dato real 31.5 (geojson_educacion.zip, Comuna 9, corte Marzo 2026)\n",
    "REF_EDUC_DES_2026 = 31.5  # Score real Educacion Comuna 9 (fuente: SIMAT 2026)\n",
    "print(f'Score Educacion: 2023-2025 = {REF_EDUC_DES} (Proxy) | 2026 Q1 = {REF_EDUC_DES_2026} (real Comuna 9)')\n",
]
cells[22]['source'] = source22 + extra
cells[22]['outputs'] = []

# Ahora buscar donde se calcula ITT en corr_trim (si existe) para aplicar el score diferenciado
# Buscar celda que calcule scores trimestrales
for i in range(23, len(cells)):
    cell = cells[i]
    source = ''.join(cell.get('source', []))
    if 'corr_trim' in source and 'score_educ_des' in source and 'REF_EDUC_DES' in source:
        # Reemplazar la linea que asigna REF_EDUC_DES a corr_trim
        new_lines = []
        for line in cell['source']:
            if "corr_trim['score_educ_des']" in line and 'REF_EDUC_DES' in line:
                new_lines.append("# Educacion diferenciada: Proxy para 2023-2025, real para 2026\n")
                new_lines.append("corr_trim['score_educ_des'] = REF_EDUC_DES  # default Proxy\n")
                new_lines.append("corr_trim.loc[corr_trim['año'] == 2026, 'score_educ_des'] = REF_EDUC_DES_2026  # dato real 2026\n")
            else:
                new_lines.append(line)
        cells[i]['source'] = new_lines
        cells[i]['outputs'] = []
        print(f'  Celda {i}: score_educ_des diferenciado en corr_trim')
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Barrio Obrero actualizado:')
print('  - 2023-2025: score_educ_des = 54.9 (Proxy)')
print('  - 2026 Q1: score_educ_des = 31.5 (real, Comuna 9, SIMAT 2026)')
