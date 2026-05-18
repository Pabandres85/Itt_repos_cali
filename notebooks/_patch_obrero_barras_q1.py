"""Fix: Celda 12 Seguridad - 2026 solo muestra barra en Q1, no repite en Q2-Q4."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

new_source = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)\n",
    "titulo = 'Dimension Seguridad - Evolucion Trimestral | Barrio Obrero'\n",
    "fig.suptitle(titulo, fontsize=13, fontweight='bold', color='#1B2631')\n",
    "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
    "COLORES = ['#90CAF9', '#42A5F5', '#1565C0', '#003366']\n",
    "\n",
    "for ax, col, tp in [(axes[0],'homicidios','Homicidios'),(axes[1],'hurtos','Hurtos')]:\n",
    "    for idx, año in enumerate(ANIOS):\n",
    "        vals = corr_trim[corr_trim['año']==año][col].values\n",
    "        offset = (idx-n/2+0.5)*w\n",
    "        # Solo dibujar barras donde hay datos reales\n",
    "        x_pos = x[:len(vals)]\n",
    "        b = ax.bar(x_pos+offset, vals, w, label=str(año), color=COLORES[idx], alpha=0.85, edgecolor='white')\n",
    "        for bar in b:\n",
    "            h = bar.get_height()\n",
    "            if h > 0:\n",
    "                ax.text(bar.get_x()+bar.get_width()/2, h+0.05, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
    "    ax.set_title(tp, fontweight='bold', pad=10)\n",
    "    ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2','Q3','Q4'])\n",
    "    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_obrero_seg_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

cells[34]['source'] = new_source
cells[34]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 12: 2026 solo muestra barra en Q1 (x[:len(vals)])')
