"""Fix: Celda 13 (Movilidad) y Celda 14 (Cohesion) - 4 colores gradiente claro a oscuro + solo Q1 2026."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Celda 13 - Movilidad (indice 36)
cells[36]['source'] = [
    "fig, axes = plt.subplots(1, 3, figsize=(20, 5), facecolor=BG)\n",
    "titulo = 'Dimension Movilidad - Evolucion Trimestral | Barrio Obrero'\n",
    "fig.suptitle(titulo, fontsize=13, fontweight='bold', color='#1B2631')\n",
    "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
    "# Gama naranja claro a oscuro (4 tonos)\n",
    "CMOV = ['#FFCC80', '#FB8C00', '#E65100', '#4E2600']\n",
    "\n",
    "for ax, col, tp in [(axes[0],'siniestralidad','Siniestralidad'),(axes[1],'lesionados','Lesionados'),(axes[2],'mortales','Mortales')]:\n",
    "    for idx, año in enumerate(ANIOS):\n",
    "        vals = corr_trim[corr_trim['año']==año][col].values\n",
    "        offset = (idx-n/2+0.5)*w\n",
    "        x_pos = x[:len(vals)]\n",
    "        b = ax.bar(x_pos+offset, vals, w, label=str(año), color=CMOV[idx], alpha=0.85, edgecolor='white')\n",
    "        for bar in b:\n",
    "            h = bar.get_height()\n",
    "            if h > 0:\n",
    "                ax.text(bar.get_x()+bar.get_width()/2, h+0.05, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
    "    ax.set_title(tp, fontweight='bold', pad=8)\n",
    "    ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2','Q3','Q4'])\n",
    "    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_obrero_mov_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]
cells[36]['outputs'] = []
print('Celda 36 (Movilidad): 4 colores naranja gradiente + solo Q1 2026')

# Celda 14 - Cohesion (buscar)
for i in range(37, len(cells)):
    cell = cells[i]
    if cell.get('cell_type') != 'code':
        continue
    joined = ''.join(cell.get('source', []))
    if 'Cohesion' in joined and 'Evolucion' in joined and 'ax.bar' in joined:
        cells[i]['source'] = [
            "fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)\n",
            "titulo = 'Dimension Cohesion Social - Evolucion Trimestral | Barrio Obrero'\n",
            "fig.suptitle(titulo, fontsize=13, fontweight='bold', color='#1B2631')\n",
            "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
            "# Gama purpura claro a oscuro (4 tonos)\n",
            "CCOH = ['#CE93D8', '#8E24AA', '#4A148C', '#1A0033']\n",
            "\n",
            "for ax, col, tp in [(axes[0],'vif','VIF'),(axes[1],'rinas','Rinas')]:\n",
            "    for idx, año in enumerate(ANIOS):\n",
            "        vals = corr_trim[corr_trim['año']==año][col].values\n",
            "        offset = (idx-n/2+0.5)*w\n",
            "        x_pos = x[:len(vals)]\n",
            "        b = ax.bar(x_pos+offset, vals, w, label=str(año), color=CCOH[idx], alpha=0.85, edgecolor='white')\n",
            "        for bar in b:\n",
            "            h = bar.get_height()\n",
            "            if h > 0:\n",
            "                ax.text(bar.get_x()+bar.get_width()/2, h+0.05, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
            "    ax.set_title(tp, fontweight='bold', pad=8)\n",
            "    ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2','Q3','Q4'])\n",
            "    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()\n",
            "plt.tight_layout()\n",
            "plt.savefig(IMG_DIR + 'itt_obrero_coh_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
            "plt.show()\n",
        ]
        cells[i]['outputs'] = []
        print(f'Celda {i} (Cohesion): 4 colores purpura gradiente + solo Q1 2026')
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('\nColores finales:')
print('  Seguridad: #90CAF9 -> #42A5F5 -> #1565C0 -> #003366 (azul)')
print('  Movilidad: #FFCC80 -> #FB8C00 -> #E65100 -> #4E2600 (naranja)')
print('  Cohesion:  #CE93D8 -> #8E24AA -> #4A148C -> #1A0033 (purpura)')
