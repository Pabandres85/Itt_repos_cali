"""Fix: La logica Proxy en Barrio Obrero crea una fila duplicada de 2026.
El problema es que ANIOS incluye 2026, entonces agg_anual crea una fila con 0,
y luego el Proxy agrega OTRA fila con los promedios. Resultado: 2 filas 2026.

Solucion: Primero construir base solo con 2023-2025, luego agregar 2026 Proxy.
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Reemplazar la logica Proxy en celda 22 (ultimas lineas)
source = cells[22]['source']

# Encontrar donde empieza la seccion Proxy
proxy_start = None
for i, line in enumerate(source):
    if 'VALORES PROXY 2026' in line:
        proxy_start = i - 1  # incluir el comentario anterior
        break

if proxy_start is None:
    print('ERROR: No se encontro seccion PROXY en celda 22')
else:
    # Reemplazar desde proxy_start hasta el final
    new_proxy = [
        "\n",
        "# ══════════════════════════════════════════════════════════\n",
        "# VALORES PROXY 2026 (Q1-Q4)\n",
        "# No hay datos reales de 2026 para Barrio Obrero.\n",
        "# Se estiman TODOS los trimestres con promedio historico 2023-2025.\n",
        "# ══════════════════════════════════════════════════════════\n",
        "\n",
        "# Eliminar fila 2026 con ceros (creada por agg_anual con ANIOS que incluye 2026)\n",
        "base = base[base['año'] != 2026].copy()\n",
        "\n",
        "indicadores_proxy = [c for c in base.columns if c != 'año']\n",
        "\n",
        "# Proxy anual: promedio de 2023-2025\n",
        "hist_anual = base[base['año'].isin([2023, 2024, 2025])]\n",
        "proxy_anual = hist_anual[indicadores_proxy].mean().round(1)\n",
        "row_2026 = {'año': 2026}\n",
        "row_2026.update(proxy_anual.to_dict())\n",
        "base = pd.concat([base, pd.DataFrame([row_2026])], ignore_index=True)\n",
        "\n",
        "# Proxy trimestral: eliminar filas 2026 con ceros y agregar promedios\n",
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

    cells[22]['source'] = source[:proxy_start] + new_proxy
    cells[22]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('Celda 22 corregida:')
    print('  - Elimina fila 2026 con ceros ANTES de agregar Proxy')
    print('  - Elimina filas trimestrales 2026 con ceros ANTES de agregar Proxy')
    print('  - base ahora tiene exactamente 1 fila por año (2023, 2024, 2025, 2026)')
