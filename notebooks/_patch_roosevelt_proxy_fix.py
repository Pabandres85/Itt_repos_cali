"""Fix: La logica Proxy en Roosevelt v2 crea una fila duplicada de 2026.
Misma correccion que Barrio Obrero.
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '01_itt_roosevelt_v2.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Celda 16 es la de procesamiento en Roosevelt
source = cells[16]['source']

proxy_start = None
for i, line in enumerate(source):
    if 'VALORES PROXY 2026' in line or 'PROXY 2026' in line:
        proxy_start = i - 1
        break

if proxy_start is None:
    print('ERROR: No se encontro seccion PROXY en celda 16 de Roosevelt')
else:
    new_proxy = [
        "\n",
        "# ══════════════════════════════════════════════════════════\n",
        "# VALORES PROXY 2026 (Q1-Q4)\n",
        "# No hay datos reales de 2026 para Roosevelt.\n",
        "# Se estiman TODOS los trimestres con promedio historico 2023-2025.\n",
        "# ══════════════════════════════════════════════════════════\n",
        "\n",
        "# Eliminar fila 2026 con ceros (creada por agg_anual)\n",
        "base = base[base['año'] != 2026].copy()\n",
        "\n",
        "indicadores_proxy = [c for c in base.columns if c != 'año']\n",
        "hist_anual = base[base['año'].isin([2023, 2024, 2025])]\n",
        "proxy_anual = hist_anual[indicadores_proxy].mean().round(1)\n",
        "row_2026 = {'año': 2026}\n",
        "row_2026.update(proxy_anual.to_dict())\n",
        "base = pd.concat([base, pd.DataFrame([row_2026])], ignore_index=True)\n",
        "\n",
        "# Proxy trimestral\n",
        "corr_trim = corr_trim[corr_trim['año'] != 2026].copy()\n",
        "hist_trim = corr_trim[corr_trim['año'].isin([2023, 2024, 2025])]\n",
        "indicadores_trim = [c for c in corr_trim.columns if c not in ['año','trimestre','periodo']]\n",
        "for trim in [1, 2, 3, 4]:\n",
        "    trim_hist = hist_trim[hist_trim['trimestre'] == trim]\n",
        "    proxy_row = {'año': 2026, 'trimestre': trim}\n",
        "    for ind in indicadores_trim:\n",
        "        proxy_row[ind] = round(trim_hist[ind].mean(), 1)\n",
        "    proxy_row['periodo'] = f'2026-Q{trim}'\n",
        "    corr_trim = pd.concat([corr_trim, pd.DataFrame([proxy_row])], ignore_index=True)\n",
        "\n",
        "corr_trim['es_proxy'] = corr_trim['año'] == 2026\n",
        "\n",
        "print()\n",
        "print('VALORES PROXY 2026** (promedio historico 2023-2025, sin datos reales):')\n",
        "print('  ', {k: f'{v:.1f}**' for k, v in proxy_anual.items()})\n",
        "print()\n",
        "print('Indicadores anuales (con Proxy 2026**):')\n",
        "print(base.to_string(index=False))\n",
    ]

    cells[16]['source'] = source[:proxy_start] + new_proxy
    cells[16]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('Roosevelt celda 16 corregida: elimina fila 2026 con ceros antes de agregar Proxy')
