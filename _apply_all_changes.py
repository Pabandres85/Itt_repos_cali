"""
Script to re-apply all session changes after git checkout.
Modifies:
1. notebooks/04_itt_pulmon_oriente_2026_v2.ipynb
2. notebooks/02_itt_avenida_ciudad_de_cali.ipynb
3. notebooks_py/04_itt_pulmon_oriente_2025.py
4. outputs/CONSOLIDADO_ITT_ZONAS.txt
5. ITT_Seguimiento_Datasets.xlsx
6. Delete temporary files
"""
import json, os, sys
from pathlib import Path

ROOT = Path(r'c:\Users\Jorg3\Desktop\Itt_repos_cali-jorge_itt')

print("=" * 60)
print("STEP 1: Modify 04_itt_pulmon_oriente_2026_v2.ipynb")
print("=" * 60)

nb_path = ROOT / 'notebooks' / '04_itt_pulmon_oriente_2026_v2.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

def find_cell_after_markdown(cells, title_fragment):
    """Find the code cell that follows a markdown cell containing title_fragment."""
    for i, c in enumerate(cells):
        if c['cell_type'] == 'markdown':
            src = ''.join(c['source'])
            if title_fragment in src:
                # Next code cell
                for j in range(i+1, len(cells)):
                    if cells[j]['cell_type'] == 'code':
                        return j
    return None

# --- Celda 6 (Procesamiento): Remove Proxy generation for Q2-Q4 2026, mark as NaN ---
idx6 = find_cell_after_markdown(cells, 'Celda 6')
print(f"  Celda 6 (Procesamiento) at index {idx6}")
