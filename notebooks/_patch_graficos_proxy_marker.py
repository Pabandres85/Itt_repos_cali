"""
Script para modificar las celdas de graficos del notebook 04_itt_pulmon_oriente_2026_v2.ipynb
Agrega marcadores ** en las etiquetas de los trimestres Proxy (Q2-Q4 2026).

Estrategia:
- En heatmaps: cambiar columnas de Q2,Q3,Q4 a Q2**,Q3**,Q4** para la fila 2026
- En barras trimestrales: agregar ** a los valores anotados de 2026 Q2-Q4
- En la leyenda: cambiar "2026" por "2026 (Q2-Q4 Proxy**)"
- En el grafico ITT Global y Radar: agregar nota al pie

Ejecutar desde la raiz del proyecto:
    python notebooks/_patch_graficos_proxy_marker.py
"""
import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent / '04_itt_pulmon_oriente_2026_v2.ipynb'


def main():
    print(f'Leyendo notebook: {NOTEBOOK_PATH}')
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    # 1. Inyectar periodo_lbl en Celda 7 si no existe
    idx7 = None
    for i, cell in enumerate(cells):
        source = ''.join(cell.get('source', []))
        if 'def score_ref' in source and 'score_seguridad' in source:
            idx7 = i
            break

    if idx7 is None:
        print('ERROR: No se encontro la Celda 7')
        return

    # 2. Parchear heatmaps (indices 22, 24) - agregar ** a columnas Q2,Q3,Q4 de fila 2026
    patched = 0
    for i in range(idx7 + 1, len(cells)):
        cell = cells[i]
        if cell.get('cell_type') != 'code':
            continue
        source = cell.get('source', [])
        joined = ''.join(source)

        # --- HEATMAPS: pivot con Q1,Q2,Q3,Q4 ---
        if 'sns.heatmap' in joined and "pivot" in joined and "'Q1','Q2','Q3','Q4'" in joined:
            new_source = []
            for line in source:
                if "pivot.columns = ['Q1','Q2','Q3','Q4']" in line:
                    # Agregar logica para marcar la fila 2026 con **
                    new_source.append(line)
                    new_source.append("    # Marcar valores Proxy con ** en anotaciones de 2026\n")
                    new_source.append("    if 2026 in pivot.index:\n")
                    new_source.append("        pivot.columns = ['Q1','Q2**','Q3**','Q4**']\n")
                else:
                    new_source.append(line)
            cells[i]['source'] = new_source
            cells[i]['outputs'] = []
            patched += 1
            continue

        # --- BARRAS TRIMESTRALES: set_xticklabels(['Q1','Q2','Q3','Q4']) ---
        if 'ax.bar' in joined and "set_xticklabels(['Q1','Q2','Q3','Q4'])" in joined:
            new_source = []
            for line in source:
                # Cambiar etiquetas del eje X
                if "set_xticklabels(['Q1','Q2','Q3','Q4'])" in line:
                    line = line.replace(
                        "set_xticklabels(['Q1','Q2','Q3','Q4'])",
                        "set_xticklabels(['Q1','Q2**','Q3**','Q4**'])"
                    )
                # Cambiar leyenda de 2026 para indicar Proxy
                if "label=str(año)" in line:
                    line = line.replace(
                        "label=str(año)",
                        "label=str(año) + (' (Q2-Q4 Proxy**)' if año==2026 else '')"
                    )
                new_source.append(line)
            cells[i]['source'] = new_source
            cells[i]['outputs'] = []
            patched += 1
            continue

        # --- ITT GLOBAL / RADAR: agregar nota al pie ---
        if ('ITT' in joined or 'Radar' in joined) and 'savefig' in joined and 'plt.show' in joined:
            new_source = []
            for line in source:
                if 'plt.show()' in line:
                    # Agregar nota antes de plt.show()
                    new_source.append("plt.figtext(0.5, -0.02, '** Valores Q2-Q4 2026 estimados (Proxy: promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n")
                new_source.append(line)
            cells[i]['source'] = new_source
            cells[i]['outputs'] = []
            patched += 1
            continue

    print(f'  {patched} celdas de graficos parcheadas con marcadores **')

    # Guardar
    print(f'Guardando notebook modificado...')
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('LISTO.')
    print('Los graficos ahora mostraran:')
    print('  - Heatmaps: columnas Q2**, Q3**, Q4** para 2026')
    print('  - Barras: eje X con Q2**, Q3**, Q4** y leyenda "2026 (Q2-Q4 Proxy**)"')
    print('  - ITT Global/Radar: nota al pie indicando valores estimados')


if __name__ == '__main__':
    main()
