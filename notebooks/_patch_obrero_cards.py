"""Fix Celda 8 (Cards) en Barrio Obrero.
Compara los 2 ultimos años con datos reales disponibles.
Si no hay 2026, compara 2025 vs 2024.
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

new_source = [
    "def safe_pct(new, old):\n",
    "    if old == 0: return 0.0\n",
    "    return (new - old) / old * 100\n",
    "\n",
    "def arrow(pct, inv=True):\n",
    "    if abs(pct) < 1: return 'Sin cambio', 'gray'\n",
    "    if inv: return (f'V {abs(pct):.1f}%','#2E7D32') if pct<0 else (f'A {abs(pct):.1f}%','#C62828')\n",
    "    else:  return (f'A {abs(pct):.1f}%','#2E7D32') if pct>0 else (f'V {abs(pct):.1f}%','#C62828')\n",
    "\n",
    "# Tomar los 2 ultimos años con datos reales\n",
    "años_disponibles = sorted(base['año'].unique())\n",
    "año_actual = años_disponibles[-1]\n",
    "año_anterior = años_disponibles[-2]\n",
    "\n",
    "d_act = base[base['año']==año_actual].iloc[0]\n",
    "d_ant = base[base['año']==año_anterior].iloc[0]\n",
    "\n",
    "cards = [\n",
    "    ('Homicidios', int(d_ant['homicidios']), int(d_act['homicidios']), True),\n",
    "    ('Hurtos', int(d_ant['hurtos']), int(d_act['hurtos']), True),\n",
    "    ('Siniestros', int(d_ant['siniestralidad']), int(d_act['siniestralidad']), True),\n",
    "    ('VIF', int(d_ant['vif']), int(d_act['vif']), True),\n",
    "    ('Rinas', int(d_ant['rinas']), int(d_act['rinas']), True),\n",
    "    ('Score Seguridad', d_ant['score_seguridad'], d_act['score_seguridad'], False),\n",
    "    ('Score Movilidad', d_ant['score_movilidad'], d_act['score_movilidad'], False),\n",
    "    ('ITT Global', d_ant['ITT'], d_act['ITT'], False),\n",
    "]\n",
    "\n",
    "fig, axes = plt.subplots(2, 4, figsize=(18, 6), facecolor=BG)\n",
    "fig.suptitle(f'ITT Barrio Obrero — Metricas Clave | {año_actual} vs {año_anterior}',\n",
    "             fontsize=14, fontweight='bold', color='#1B2631', y=0.98)\n",
    "for i, (titulo, v_ant, v_act, inv) in enumerate(cards):\n",
    "    ax = axes[i//4][i%4]; ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')\n",
    "    rect = mpatches.FancyBboxPatch((0.02,0.02),0.96,0.96, boxstyle='round,pad=0.02',\n",
    "            linewidth=1.5, edgecolor='#DEE2E6', facecolor='white')\n",
    "    ax.add_patch(rect)\n",
    "    ax.text(0.5,0.88, titulo, ha='center', va='center', fontsize=9, color='#6C757D', fontweight='bold')\n",
    "    # Valor actual\n",
    "    val_d = f'{v_act:.1f}' if isinstance(v_act, float) else str(v_act)\n",
    "    ax.text(0.5,0.62, val_d, ha='center', va='center', fontsize=22, fontweight='bold', color='#1B2631')\n",
    "    ax.text(0.5,0.46, str(año_actual), ha='center', fontsize=8, color='#ADB5BD')\n",
    "    # Variacion\n",
    "    pct = safe_pct(v_act, v_ant)\n",
    "    ar, col = arrow(pct, inv)\n",
    "    ax.text(0.5,0.28, f'vs {año_anterior}: {ar}', ha='center', fontsize=9, color=col, fontweight='bold')\n",
    "    # Valor anterior\n",
    "    val_ant = f'{v_ant:.1f}' if isinstance(v_ant, float) else str(v_ant)\n",
    "    ax.text(0.5,0.12, f'{año_anterior}: {val_ant}', ha='center', fontsize=8, color='#ADB5BD')\n",
    "\n",
    "plt.tight_layout(rect=[0,0,1,0.95])\n",
    "plt.savefig(IMG_DIR + 'itt_obrero_cards.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

cells[26]['source'] = new_source
cells[26]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 8 (Cards) corregida: compara ultimos 2 años disponibles (2025 vs 2024)')
