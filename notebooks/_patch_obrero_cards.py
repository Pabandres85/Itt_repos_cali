"""Fix Celda 8 (Cards) en Barrio Obrero.
La comparacion debe ser entre años con datos reales (2023-2025).
2026** se muestra como referencia pero no como año de comparacion principal.
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
    "# Comparacion entre años REALES (2023-2025). 2026 es Proxy.\n",
    "año_ini = 2023\n",
    "año_ant = 2024\n",
    "año_ult = 2025\n",
    "d_ini = base[base['año']==año_ini].iloc[0]\n",
    "d_ant = base[base['año']==año_ant].iloc[0]\n",
    "d_ult = base[base['año']==año_ult].iloc[0]\n",
    "\n",
    "cards = [\n",
    "    ('Homicidios',int(d_ini['homicidios']),int(d_ant['homicidios']),int(d_ult['homicidios']),True),\n",
    "    ('Hurtos',int(d_ini['hurtos']),int(d_ant['hurtos']),int(d_ult['hurtos']),True),\n",
    "    ('Siniestros',int(d_ini['siniestralidad']),int(d_ant['siniestralidad']),int(d_ult['siniestralidad']),True),\n",
    "    ('VIF',int(d_ini['vif']),int(d_ant['vif']),int(d_ult['vif']),True),\n",
    "    ('Rinas',int(d_ini['rinas']),int(d_ant['rinas']),int(d_ult['rinas']),True),\n",
    "    ('Score Seguridad',d_ini['score_seguridad'],d_ant['score_seguridad'],d_ult['score_seguridad'],False),\n",
    "    ('Score Movilidad',d_ini['score_movilidad'],d_ant['score_movilidad'],d_ult['score_movilidad'],False),\n",
    "    ('ITT Global',d_ini['ITT'],d_ant['ITT'],d_ult['ITT'],False),\n",
    "]\n",
    "\n",
    "fig, axes = plt.subplots(2, 4, figsize=(18, 7), facecolor=BG)\n",
    "fig.suptitle(f'ITT Barrio Obrero — Metricas Clave | {año_ini}-{año_ult} (datos reales)',\n",
    "             fontsize=14, fontweight='bold', color='#1B2631', y=0.98)\n",
    "for i, (titulo, v_ini, v_ant, v_ult, inv) in enumerate(cards):\n",
    "    ax = axes[i//4][i%4]; ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')\n",
    "    rect = mpatches.FancyBboxPatch((0.02,0.02),0.96,0.96, boxstyle='round,pad=0.02',\n",
    "            linewidth=1.5, edgecolor='#DEE2E6', facecolor='white')\n",
    "    ax.add_patch(rect)\n",
    "    ax.text(0.5,0.85, titulo, ha='center', va='center', fontsize=9, color='#6C757D', fontweight='bold')\n",
    "    val_d = f'{v_ult:.1f}' if isinstance(v_ult,float) else str(v_ult)\n",
    "    ax.text(0.5,0.60, val_d, ha='center', va='center', fontsize=19, fontweight='bold', color='#1B2631')\n",
    "    pct1 = safe_pct(v_ult, v_ant)\n",
    "    ar1, col1 = arrow(pct1, inv)\n",
    "    ax.text(0.5,0.38, f'{año_ult} vs {año_ant}: {ar1}', ha='center', fontsize=8, color=col1, fontweight='bold')\n",
    "    pct2 = safe_pct(v_ult, v_ini)\n",
    "    ar2, col2 = arrow(pct2, inv)\n",
    "    ax.text(0.5,0.22, f'vs {año_ini}: {ar2}', ha='center', fontsize=7.5, color=col2)\n",
    "    ref = f'{v_ini:.1f}' if isinstance(v_ini,float) else str(v_ini)\n",
    "    ax.text(0.5,0.08, f'{año_ini}: {ref}', ha='center', fontsize=7, color='#ADB5BD')\n",
    "\n",
    "plt.figtext(0.5, 0.01, '2026** = valores Proxy (promedio historico 2023-2025). Cards muestran solo datos reales.', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout(rect=[0,0.03,1,0.95])\n",
    "plt.savefig(IMG_DIR + 'itt_obrero_cards.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

cells[26]['source'] = new_source
cells[26]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 8 (Cards) corregida en Barrio Obrero:')
print('  - Comparacion entre años reales: 2023 vs 2024 vs 2025')
print('  - 2026 Proxy no se usa como año de comparacion')
print('  - Nota al pie indicando que Cards muestran solo datos reales')
