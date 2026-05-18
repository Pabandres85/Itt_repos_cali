"""Fix Celda 9 (Heatmap Seguridad) en Barrio Obrero."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

new_source = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)\n",
    "fig.suptitle('Dimension Seguridad — Heatmap Trimestral | Barrio Obrero',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "for ax, col, titulo_h, cmap_h in [\n",
    "    (axes[0],'homicidios','Homicidios','Blues'),\n",
    "    (axes[1],'hurtos','Hurtos','Oranges')]:\n",
    "    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)\n",
    "    pivot.columns = ['Q1','Q2','Q3','Q4']\n",
    "    # Anotaciones con ** para Proxy (2026)\n",
    "    annot_arr = pivot.copy().astype(object)\n",
    "    for c in annot_arr.columns:\n",
    "        for r in annot_arr.index:\n",
    "            val = pivot.loc[r, c]\n",
    "            if r == 2026:\n",
    "                annot_arr.loc[r, c] = f'{val:.0f}**'\n",
    "            else:\n",
    "                annot_arr.loc[r, c] = f'{val:.0f}'\n",
    "    sns.heatmap(pivot, annot=annot_arr.values, fmt='', cmap=cmap_h,\n",
    "        linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':11},\n",
    "        cbar_kws={'label':'Casos','shrink':0.8})\n",
    "    ax.set_title(titulo_h, fontweight='bold', pad=8)\n",
    "    ax.set_ylabel(''); ax.set_xlabel('')\n",
    "plt.figtext(0.5, -0.02, '** 2026 = valores Proxy (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_obrero_heatmap_seg.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

cells[28]['source'] = new_source
cells[28]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 9 (Heatmap Seguridad) corregida en Barrio Obrero:')
print('  - figtext ANTES de savefig')
print('  - Anotaciones con ** para 2026')
print('  - Color hurtos cambiado a Oranges')
