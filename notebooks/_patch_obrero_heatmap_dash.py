"""Fix Celda 9 (Heatmap Seguridad) en Barrio Obrero.
Mostrar '-' en trimestres sin datos (Q2-Q4 2026). Sin Proxy.
Tambien corregir Celdas 10 y 11 (Movilidad y Cohesion) con la misma logica.
"""
import json
from pathlib import Path
import re

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Heatmap Seguridad (celda 28)
heatmap_seg = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)\n",
    "fig.suptitle('Dimension Seguridad — Heatmap Trimestral | Barrio Obrero',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "for ax, col, titulo_h, cmap_h in [\n",
    "    (axes[0],'homicidios','Homicidios','Blues'),\n",
    "    (axes[1],'hurtos','Hurtos','Oranges')]:\n",
    "    # Pivot con todos los trimestres (NaN donde no hay datos)\n",
    "    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)\n",
    "    pivot.columns = ['Q1','Q2','Q3','Q4']\n",
    "    # Anotaciones: '-' para trimestres sin datos\n",
    "    annot_arr = pivot.copy().astype(object)\n",
    "    for c in annot_arr.columns:\n",
    "        for r in annot_arr.index:\n",
    "            val = pivot.loc[r, c]\n",
    "            if pd.isna(val) or (r == 2026 and c != 'Q1'):\n",
    "                annot_arr.loc[r, c] = '-'\n",
    "            else:\n",
    "                annot_arr.loc[r, c] = f'{val:.0f}'\n",
    "    pivot_plot = pivot.fillna(0)\n",
    "    sns.heatmap(pivot_plot, annot=annot_arr.values, fmt='', cmap=cmap_h,\n",
    "        linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':11},\n",
    "        cbar_kws={'label':'Casos','shrink':0.8})\n",
    "    ax.set_title(titulo_h, fontweight='bold', pad=8)\n",
    "    ax.set_ylabel(''); ax.set_xlabel('')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_obrero_heatmap_seg.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

cells[28]['source'] = heatmap_seg
cells[28]['outputs'] = []
print('Celda 28 (Heatmap Seguridad): corregida con - para trimestres sin datos')

# Buscar y corregir Heatmap Movilidad y Cohesion con la misma logica
for i in range(29, len(cells)):
    cell = cells[i]
    if cell.get('cell_type') != 'code':
        continue
    joined = ''.join(cell.get('source', []))
    
    if 'sns.heatmap' in joined and 'Movilidad' in joined and 'Heatmap' in joined:
        cells[i]['source'] = [
            "fig, axes = plt.subplots(1, 3, figsize=(20, 4), facecolor=BG)\n",
            "fig.suptitle('Dimension Movilidad — Heatmap Trimestral | Barrio Obrero',\n",
            "             fontsize=13, fontweight='bold', color='#1B2631')\n",
            "for ax, col, titulo_h, cmap_h in [\n",
            "    (axes[0],'siniestralidad','Siniestralidad Total','Oranges'),\n",
            "    (axes[1],'lesionados','Acc. con Lesionados','Oranges'),\n",
            "    (axes[2],'mortales','Acc. Mortales','Reds')]:\n",
            "    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)\n",
            "    pivot.columns = ['Q1','Q2','Q3','Q4']\n",
            "    annot_arr = pivot.copy().astype(object)\n",
            "    for c in annot_arr.columns:\n",
            "        for r in annot_arr.index:\n",
            "            val = pivot.loc[r, c]\n",
            "            if pd.isna(val) or (r == 2026 and c != 'Q1'):\n",
            "                annot_arr.loc[r, c] = '-'\n",
            "            else:\n",
            "                annot_arr.loc[r, c] = f'{val:.0f}'\n",
            "    pivot_plot = pivot.fillna(0)\n",
            "    sns.heatmap(pivot_plot, annot=annot_arr.values, fmt='', cmap=cmap_h,\n",
            "        linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':11},\n",
            "        cbar_kws={'label':'Casos','shrink':0.8})\n",
            "    ax.set_title(titulo_h, fontweight='bold', pad=8)\n",
            "    ax.set_ylabel(''); ax.set_xlabel('')\n",
            "plt.tight_layout()\n",
            "plt.savefig(IMG_DIR + 'itt_obrero_heatmap_mov.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
            "plt.show()\n",
        ]
        cells[i]['outputs'] = []
        print(f'Celda {i} (Heatmap Movilidad): corregida con - para trimestres sin datos')
        break

for i in range(29, len(cells)):
    cell = cells[i]
    if cell.get('cell_type') != 'code':
        continue
    joined = ''.join(cell.get('source', []))
    
    if 'sns.heatmap' in joined and 'Cohesion' in joined and 'Heatmap' in joined:
        cells[i]['source'] = [
            "fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)\n",
            "fig.suptitle('Dimension Cohesion Social — Heatmap Trimestral | Barrio Obrero',\n",
            "             fontsize=13, fontweight='bold', color='#1B2631')\n",
            "for ax, col, titulo_h in [\n",
            "    (axes[0],'vif','VIF — Violencia Intrafamiliar'),\n",
            "    (axes[1],'rinas','Rinas / Conflictividad')]:\n",
            "    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)\n",
            "    pivot.columns = ['Q1','Q2','Q3','Q4']\n",
            "    annot_arr = pivot.copy().astype(object)\n",
            "    for c in annot_arr.columns:\n",
            "        for r in annot_arr.index:\n",
            "            val = pivot.loc[r, c]\n",
            "            if pd.isna(val) or (r == 2026 and c != 'Q1'):\n",
            "                annot_arr.loc[r, c] = '-'\n",
            "            else:\n",
            "                annot_arr.loc[r, c] = f'{val:.0f}'\n",
            "    pivot_plot = pivot.fillna(0)\n",
            "    sns.heatmap(pivot_plot, annot=annot_arr.values, fmt='', cmap='RdPu',\n",
            "        linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':11},\n",
            "        cbar_kws={'label':'Casos','shrink':0.8})\n",
            "    ax.set_title(titulo_h, fontweight='bold', pad=8)\n",
            "    ax.set_ylabel(''); ax.set_xlabel('')\n",
            "plt.tight_layout()\n",
            "plt.savefig(IMG_DIR + 'itt_obrero_heatmap_coh.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
            "plt.show()\n",
        ]
        cells[i]['outputs'] = []
        print(f'Celda {i} (Heatmap Cohesion): corregida con - para trimestres sin datos')
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('\nTodos los heatmaps muestran - en Q2-Q4 2026 (sin datos)')
