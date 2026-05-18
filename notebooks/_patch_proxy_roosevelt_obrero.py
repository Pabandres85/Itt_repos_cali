"""
Patch: Agrega logica Proxy 2026 a Roosevelt v2 y Barrio Obrero.
Como estos notebooks solo tienen datos 2023-2025, se generan valores Proxy
para TODO el año 2026 (Q1-Q4) usando promedios historicos trimestrales.

python notebooks/_patch_proxy_roosevelt_obrero.py
"""
import json
from pathlib import Path

NOTEBOOKS = [
    ('01_itt_roosevelt_v2.ipynb', 10, 16, 18),  # (nombre, celda_params, celda_proceso, celda_norm)
    ('03_itt_barrio_obrero.ipynb', 10, None, None),  # Barrio Obrero tiene estructura diferente
]


def patch_notebook(nb_path, idx_params, idx_proceso, idx_norm):
    print(f'\n{"="*60}')
    print(f'Parcheando: {nb_path.name}')
    print(f'{"="*60}')

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    # 1. Cambiar ANIOS para incluir 2026
    cell_params = cells[idx_params]
    new_source = []
    for line in cell_params['source']:
        if 'ANIOS' in line and '[2023, 2024, 2025]' in line:
            line = line.replace('[2023, 2024, 2025]', '[2023, 2024, 2025, 2026]')
            print(f'  ANIOS actualizado a incluir 2026')
        new_source.append(line)
    cell_params['source'] = new_source
    cell_params['outputs'] = []

    # 2. Encontrar la celda de procesamiento (donde se construye corr_trim y base)
    if idx_proceso is None:
        # Buscar automaticamente
        for i, cell in enumerate(cells):
            source = ''.join(cell.get('source', []))
            if 'corr_trim' in source and 'merge' in source and 'agg_trim' in source:
                idx_proceso = i
                break

    if idx_proceso is None:
        print('  ERROR: No se encontro celda de procesamiento')
        return

    print(f'  Celda procesamiento: {idx_proceso}')

    # 3. Inyectar logica Proxy al final de la celda de procesamiento
    cell_proc = cells[idx_proceso]
    joined = ''.join(cell_proc['source'])

    if 'PROXY' in joined or 'proxy_values' in joined:
        print('  Celda procesamiento ya tiene logica Proxy (no se modifica)')
    else:
        proxy_code = [
            "\n",
            "# ══════════════════════════════════════════════════════════\n",
            "# VALORES PROXY 2026 (Q1-Q4)\n",
            "# No hay datos reales de 2026 para esta zona.\n",
            "# Se estiman TODOS los trimestres con promedio historico 2023-2025.\n",
            "# ══════════════════════════════════════════════════════════\n",
            "indicadores_proxy = [c for c in base.columns if c != 'año']\n",
            "\n",
            "# Proxy anual: promedio de 2023-2025\n",
            "hist_anual = base[base['año'].isin([2023, 2024, 2025])]\n",
            "proxy_anual = hist_anual[indicadores_proxy].mean().round(1)\n",
            "row_2026 = {'año': 2026}\n",
            "row_2026.update(proxy_anual.to_dict())\n",
            "base = pd.concat([base, pd.DataFrame([row_2026])], ignore_index=True)\n",
            "\n",
            "# Proxy trimestral: promedio por trimestre de 2023-2025\n",
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
            "print('VALORES PROXY 2026 (promedio historico 2023-2025):')\n",
            "print('  Anual:', {k: f'{v:.1f}**' for k, v in proxy_anual.items()})\n",
            "print('  ** = Todos los valores de 2026 son estimados (Proxy)')\n",
            "print()\n",
            "print('Indicadores anuales (con Proxy 2026**):')\n",
            "print(base.to_string(index=False))\n",
        ]
        cell_proc['source'] = cell_proc['source'] + proxy_code
        cell_proc['outputs'] = []
        print('  Logica Proxy inyectada en celda procesamiento')

    # 4. Encontrar celda de normalizacion
    if idx_norm is None:
        for i in range(idx_proceso + 1, len(cells)):
            source = ''.join(cells[i].get('source', []))
            if 'def score_ref' in source and 'score_seguridad' in source:
                idx_norm = i
                break

    if idx_norm is None:
        print('  ERROR: No se encontro celda de normalizacion')
        return

    print(f'  Celda normalizacion: {idx_norm}')

    # 5. En la celda de normalizacion, agregar marcador ** para 2026 en la salida
    cell_norm = cells[idx_norm]
    joined_norm = ''.join(cell_norm['source'])
    if '2026' not in joined_norm and 'proxy' not in joined_norm.lower():
        # Agregar nota al final
        cell_norm['source'].append("\nprint()\nprint('NOTA: 2026** = valores Proxy (promedio historico 2023-2025). No hay datos reales de 2026 para esta zona.')\n")
        cell_norm['outputs'] = []
        print('  Nota Proxy agregada en celda normalizacion')

    # 6. Parchear graficos - buscar celdas con plt.savefig y agregar ** a 2026
    patched_graphs = 0
    for i in range(idx_norm + 1, len(cells)):
        cell = cells[i]
        if cell.get('cell_type') != 'code':
            continue
        source = cell.get('source', [])
        joined = ''.join(source)

        if 'plt.savefig' in joined or 'plt.show' in joined:
            modified = False
            new_source = []
            for line in source:
                # Cambiar label=str(año) para agregar **
                if "label=str(año)" in line:
                    line = line.replace("label=str(año)", "label=str(año) + ('**' if año==2026 else '')")
                    modified = True
                # Agregar nota al pie antes de plt.show()
                if 'plt.show()' in line and '** ' not in joined:
                    new_source.append("plt.figtext(0.5, -0.02, '** 2026 = valores Proxy (promedio historico 2023-2025, sin datos reales)', ha='center', fontsize=8, style='italic', color='#666666')\n")
                    modified = True
                new_source.append(line)

            if modified:
                cells[i]['source'] = new_source
                cells[i]['outputs'] = []
                patched_graphs += 1

    print(f'  {patched_graphs} celdas de graficos parcheadas con ** para 2026')

    # Guardar
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)
    print(f'  Guardado: {nb_path.name}')


def main():
    nb_dir = Path(__file__).parent

    # Roosevelt v2
    patch_notebook(nb_dir / '01_itt_roosevelt_v2.ipynb', 10, 16, 18)

    # Barrio Obrero
    patch_notebook(nb_dir / '03_itt_barrio_obrero.ipynb', 10, None, None)

    print('\n' + '='*60)
    print('LISTO. Ambos notebooks ahora incluyen:')
    print('  - ANIOS extendido a [2023, 2024, 2025, 2026]')
    print('  - Valores Proxy 2026 (promedio historico 2023-2025)')
    print('  - Marcadores ** en graficos para 2026')
    print('  - Nota metodologica en salidas')
    print('='*60)


if __name__ == '__main__':
    main()
