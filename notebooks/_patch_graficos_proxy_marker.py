"""
Script para modificar las celdas de graficos del notebook 04_itt_pulmon_oriente_2026_v2.ipynb
Agrega marcadores ** en los VALORES mostrados en graficos para trimestres Proxy (Q2-Q4 2026).

Ejecutar desde la raiz del proyecto:
    python notebooks/_patch_graficos_proxy_marker.py
"""
import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent / '04_itt_pulmon_oriente_2026_v2.ipynb'

# =============================================================================
# NUEVO CODIGO PARA HEATMAP SEGURIDAD (Celda 22)
# =============================================================================
HEATMAP_SEG_SOURCE = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)\n",
    "fig.suptitle('Dimension Seguridad — Heatmap Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "for ax, col, titulo_h, cmap_h in [\n",
    "    (axes[0],'homicidios','Homicidios','Blues'),\n",
    "    (axes[1],'hurtos','Hurtos','Oranges')]:\n",
    "    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)\n",
    "    pivot.columns = ['Q1','Q2','Q3','Q4']\n",
    "    # Crear anotaciones con ** para Proxy (2026 Q2-Q4)\n",
    "    annot_arr = pivot.copy().astype(str)\n",
    "    for c in annot_arr.columns:\n",
    "        for r in annot_arr.index:\n",
    "            val = pivot.loc[r, c]\n",
    "            if r == 2026 and c in ['Q2','Q3','Q4']:\n",
    "                annot_arr.loc[r, c] = f'{val:.0f}**'\n",
    "            else:\n",
    "                annot_arr.loc[r, c] = f'{val:.0f}'\n",
    "    sns.heatmap(pivot, annot=annot_arr.values, fmt='', cmap=cmap_h,\n",
    "        linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':11},\n",
    "        cbar_kws={'label':'Casos','shrink':0.8})\n",
    "    ax.set_title(titulo_h, fontweight='bold', pad=8)\n",
    "    ax.set_ylabel(''); ax.set_xlabel('')\n",
    "plt.figtext(0.5, -0.02, '** Valores Q2-Q4 2026 estimados (Proxy: promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_heatmap_seg.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# =============================================================================
# NUEVO CODIGO PARA HEATMAP VIF (Celda 24)
# =============================================================================
HEATMAP_VIF_SOURCE = [
    "fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)\n",
    "fig.suptitle('Dimension Cohesion Social — VIF Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "pivot = corr_trim.pivot(index='año', columns='trimestre', values='vif')\n",
    "pivot.columns = ['Q1','Q2','Q3','Q4']\n",
    "# Crear anotaciones con ** para Proxy (2026 Q2-Q4)\n",
    "annot_arr = pivot.copy().astype(str)\n",
    "for c in annot_arr.columns:\n",
    "    for r in annot_arr.index:\n",
    "        val = pivot.loc[r, c]\n",
    "        if r == 2026 and c in ['Q2','Q3','Q4']:\n",
    "            annot_arr.loc[r, c] = f'{val:.0f}**'\n",
    "        else:\n",
    "            annot_arr.loc[r, c] = f'{val:.0f}'\n",
    "sns.heatmap(pivot, annot=annot_arr.values, fmt='', cmap='RdPu',\n",
    "    linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':11},\n",
    "    cbar_kws={'label':'Casos','shrink':0.8})\n",
    "ax.set_title('VIF — Violencia Intrafamiliar', fontweight='bold', pad=8)\n",
    "ax.set_ylabel(''); ax.set_xlabel('')\n",
    "plt.figtext(0.5, -0.02, '** Valores Q2-Q4 2026 estimados (Proxy: promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_heatmap_vif.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# =============================================================================
# NUEVO CODIGO PARA BARRAS SEGURIDAD (Celda 26)
# =============================================================================
BARRAS_SEG_SOURCE = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)\n",
    "fig.suptitle('Dimension Seguridad - Evolucion Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
    "COLORES = ['#42A5F5','#1B4F8A','#E53935','#FF6F00']\n",
    "for ax, col, tp in [(axes[0],'homicidios','Homicidios'),(axes[1],'hurtos','Hurtos')]:\n",
    "    for idx, año in enumerate(ANIOS):\n",
    "        vals = corr_trim[corr_trim['año']==año][col].values\n",
    "        offset = (idx-n/2+0.5)*w\n",
    "        lbl = str(año) + (' (Q2-Q4 Proxy**)' if año==2026 else '')\n",
    "        b = ax.bar(x+offset, vals, w, label=lbl, color=COLORES[idx%4], alpha=0.85, edgecolor='white')\n",
    "        for i_bar, bar in enumerate(b):\n",
    "            h = bar.get_height()\n",
    "            if h > 0:\n",
    "                txt = f'{int(h)}**' if (año==2026 and i_bar >= 1) else str(int(h))\n",
    "                ax.text(bar.get_x()+bar.get_width()/2, h+0.5, txt, ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
    "    ax.set_title(tp, fontweight='bold', pad=10)\n",
    "    ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2','Q3','Q4'])\n",
    "    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend(fontsize=8)\n",
    "plt.figtext(0.5, -0.02, '** Valores Q2-Q4 2026 estimados (Proxy: promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_seg_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# =============================================================================
# NUEVO CODIGO PARA BARRAS VIF/COHESION (Celda 28)
# =============================================================================
BARRAS_COH_SOURCE = [
    "fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)\n",
    "fig.suptitle('Dimension Cohesion Social - VIF Evolucion Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
    "CVIF = ['#CE93D8','#7B1FA2','#4A148C','#E91E63']\n",
    "for idx, año in enumerate(ANIOS):\n",
    "    vals = corr_trim[corr_trim['año']==año]['vif'].values\n",
    "    offset = (idx-n/2+0.5)*w\n",
    "    lbl = str(año) + (' (Q2-Q4 Proxy**)' if año==2026 else '')\n",
    "    b = ax.bar(x+offset, vals, w, label=lbl, color=CVIF[idx%4], alpha=0.85, edgecolor='white')\n",
    "    for i_bar, bar in enumerate(b):\n",
    "        h = bar.get_height()\n",
    "        if h > 0:\n",
    "            txt = f'{int(h)}**' if (año==2026 and i_bar >= 1) else str(int(h))\n",
    "            ax.text(bar.get_x()+bar.get_width()/2, h+0.5, txt, ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
    "ax.set_title('VIF', fontweight='bold', pad=8)\n",
    "ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2','Q3','Q4'])\n",
    "ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend(fontsize=8)\n",
    "plt.figtext(0.5, -0.02, '** Valores Q2-Q4 2026 estimados (Proxy: promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_coh_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]


def main():
    print(f'Leyendo notebook: {NOTEBOOK_PATH}')
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    # Mapeo de celdas a reemplazar por indice
    patches = {
        22: ('Heatmap Seguridad', HEATMAP_SEG_SOURCE),
        24: ('Heatmap VIF', HEATMAP_VIF_SOURCE),
        26: ('Barras Seguridad', BARRAS_SEG_SOURCE),
        28: ('Barras Cohesion/VIF', BARRAS_COH_SOURCE),
    }

    for idx, (nombre, new_source) in patches.items():
        if idx < len(cells):
            cells[idx]['source'] = new_source
            cells[idx]['outputs'] = []
            print(f'  Celda {idx} ({nombre}) reemplazada')
        else:
            print(f'  WARN: Celda {idx} no existe')

    # Tambien parchear ITT Global (Celda 30) y Radar (Celda 32) con nota al pie
    for idx in range(18, len(cells)):
        cell = cells[idx]
        if cell.get('cell_type') != 'code':
            continue
        source = cell.get('source', [])
        joined = ''.join(source)
        if 'ITT por Ano' in joined or 'Radar' in joined:
            # Agregar nota al pie si no la tiene
            if '** Valores Q2-Q4 2026' not in joined and 'plt.show()' in joined:
                new_source = []
                for line in source:
                    if 'plt.show()' in line and 'figtext' not in ''.join(source):
                        new_source.append("plt.figtext(0.5, -0.02, '** Valores Q2-Q4 2026 estimados (Proxy: promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n")
                    new_source.append(line)
                cells[idx]['source'] = new_source
                cells[idx]['outputs'] = []
                print(f'  Celda {idx} (ITT/Radar) — nota al pie agregada')

    # Guardar
    print(f'\nGuardando notebook modificado...')
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('LISTO. Los graficos ahora mostraran ** en los valores Proxy.')


if __name__ == '__main__':
    main()
