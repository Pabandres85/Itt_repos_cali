"""
Patch completo: Agrega ** a TODOS los valores Proxy visibles en graficos.
Incluye: heatmaps, barras, cards, ITT Global, Radar.

python notebooks/_patch_graficos_proxy_marker.py
"""
import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent / '04_itt_pulmon_oriente_2026_v2.ipynb'

# ===================== CELDA 20: CARDS =====================
CARDS_SOURCE = [
    "def safe_pct(new, old):\n",
    "    if old == 0: return 0.0\n",
    "    return (new - old) / old * 100\n",
    "\n",
    "def arrow(pct, inv=True):\n",
    "    if abs(pct) < 1: return 'Sin cambio', 'gray'\n",
    "    if inv: return (f'V {abs(pct):.1f}%', '#2E7D32') if pct < 0 else (f'A {abs(pct):.1f}%', '#C62828')\n",
    "    else: return (f'A {abs(pct):.1f}%', '#2E7D32') if pct > 0 else (f'V {abs(pct):.1f}%', '#C62828')\n",
    "\n",
    "año_ini, año_ant, año_ult = ANIOS[0], ANIOS[-2], ANIOS[-1]\n",
    "d_ini = base[base['año']==año_ini].iloc[0]\n",
    "d_ant = base[base['año']==año_ant].iloc[0]\n",
    "d_ult = base[base['año']==año_ult].iloc[0]\n",
    "\n",
    "# Nota: 2026 incluye Proxy** en Q2-Q4\n",
    "proxy_mark = '**' if año_ult == 2026 else ''\n",
    "\n",
    "cards = [\n",
    "    ('Homicidios', int(d_ini['homicidios']), int(d_ant['homicidios']), int(d_ult['homicidios']), True),\n",
    "    ('Hurtos', int(d_ini['hurtos']), int(d_ant['hurtos']), int(d_ult['hurtos']), True),\n",
    "    ('VIF', int(d_ini['vif']), int(d_ant['vif']), int(d_ult['vif']), True),\n",
    "    ('Score Seguridad', d_ini['score_seguridad'], d_ant['score_seguridad'], d_ult['score_seguridad'], False),\n",
    "    ('Score Cohesion', d_ini['score_cohesion'], d_ant['score_cohesion'], d_ult['score_cohesion'], False),\n",
    "    ('ITT Global', d_ini['ITT'], d_ant['ITT'], d_ult['ITT'], False),\n",
    "]\n",
    "\n",
    "fig, axes = plt.subplots(2, 3, figsize=(16, 7), facecolor=BG)\n",
    "fig.suptitle(f'ITT Pulmon de Oriente — Metricas Clave | {año_ini}-{año_ult}',\n",
    "             fontsize=14, fontweight='bold', color='#1B2631', y=0.98)\n",
    "for i, (titulo, v_ini, v_ant, v_ult, inv) in enumerate(cards):\n",
    "    ax = axes[i//3][i%3]; ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')\n",
    "    rect = mpatches.FancyBboxPatch((0.02,0.02),0.96,0.96, boxstyle='round,pad=0.02',\n",
    "            linewidth=1.5, edgecolor='#DEE2E6', facecolor='white')\n",
    "    ax.add_patch(rect)\n",
    "    ax.text(0.5,0.85, titulo, ha='center', va='center', fontsize=9, color='#6C757D', fontweight='bold')\n",
    "    val_d = f'{v_ult:.1f}{proxy_mark}' if isinstance(v_ult,float) else f'{v_ult}{proxy_mark}'\n",
    "    ax.text(0.5,0.60, val_d, ha='center', va='center', fontsize=19, fontweight='bold', color='#1B2631')\n",
    "    pct1 = safe_pct(v_ult, v_ant)\n",
    "    ar1, col1 = arrow(pct1, inv)\n",
    "    ax.text(0.5,0.38, f'{año_ult}{proxy_mark} vs {año_ant}: {ar1}', ha='center', fontsize=8, color=col1, fontweight='bold')\n",
    "    pct2 = safe_pct(v_ult, v_ini)\n",
    "    ar2, col2 = arrow(pct2, inv)\n",
    "    ax.text(0.5,0.22, f'vs {año_ini}: {ar2}', ha='center', fontsize=7.5, color=col2)\n",
    "    ref = f'{v_ini:.1f}' if isinstance(v_ini,float) else str(v_ini)\n",
    "    ax.text(0.5,0.08, f'{año_ini}: {ref}', ha='center', fontsize=7, color='#ADB5BD')\n",
    "\n",
    "plt.figtext(0.5, 0.01, '** Valores 2026 incluyen Proxy Q2-Q4 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout(rect=[0,0.03,1,0.95])\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_cards.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# ===================== CELDA 22: HEATMAP SEGURIDAD =====================
HEATMAP_SEG_SOURCE = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)\n",
    "fig.suptitle('Dimension Seguridad — Heatmap Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "for ax, col, titulo_h, cmap_h in [\n",
    "    (axes[0],'homicidios','Homicidios','Blues'),\n",
    "    (axes[1],'hurtos','Hurtos','Oranges')]:\n",
    "    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)\n",
    "    pivot.columns = ['Q1','Q2','Q3','Q4']\n",
    "    annot_arr = pivot.copy().astype(object)\n",
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
    "plt.figtext(0.5, -0.02, '** Valores Proxy Q2-Q4 2026 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_heatmap_seg.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# ===================== CELDA 24: HEATMAP VIF =====================
HEATMAP_VIF_SOURCE = [
    "fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)\n",
    "fig.suptitle('Dimension Cohesion Social — VIF Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "pivot = corr_trim.pivot(index='año', columns='trimestre', values='vif')\n",
    "pivot.columns = ['Q1','Q2','Q3','Q4']\n",
    "annot_arr = pivot.copy().astype(object)\n",
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
    "plt.figtext(0.5, -0.02, '** Valores Proxy Q2-Q4 2026 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_heatmap_vif.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# ===================== CELDA 26: BARRAS SEGURIDAD =====================
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
    "        lbl = f'{año}**' if año==2026 else str(año)\n",
    "        b = ax.bar(x+offset, vals, w, label=lbl, color=COLORES[idx%4], alpha=0.85, edgecolor='white')\n",
    "        for i_bar, bar in enumerate(b):\n",
    "            h = bar.get_height()\n",
    "            if h > 0:\n",
    "                txt = f'{int(h)}**' if (año==2026 and i_bar >= 1) else str(int(h))\n",
    "                ax.text(bar.get_x()+bar.get_width()/2, h+0.5, txt, ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
    "    ax.set_title(tp, fontweight='bold', pad=10)\n",
    "    ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2**','Q3**','Q4**'])\n",
    "    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend(fontsize=8)\n",
    "plt.figtext(0.5, -0.02, '** Valores Proxy Q2-Q4 2026 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_seg_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# ===================== CELDA 28: BARRAS VIF =====================
BARRAS_COH_SOURCE = [
    "fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)\n",
    "fig.suptitle('Dimension Cohesion Social - VIF Evolucion Trimestral | Pulmon de Oriente',\n",
    "             fontsize=13, fontweight='bold', color='#1B2631')\n",
    "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
    "CVIF = ['#CE93D8','#7B1FA2','#4A148C','#E91E63']\n",
    "for idx, año in enumerate(ANIOS):\n",
    "    vals = corr_trim[corr_trim['año']==año]['vif'].values\n",
    "    offset = (idx-n/2+0.5)*w\n",
    "    lbl = f'{año}**' if año==2026 else str(año)\n",
    "    b = ax.bar(x+offset, vals, w, label=lbl, color=CVIF[idx%4], alpha=0.85, edgecolor='white')\n",
    "    for i_bar, bar in enumerate(b):\n",
    "        h = bar.get_height()\n",
    "        if h > 0:\n",
    "            txt = f'{int(h)}**' if (año==2026 and i_bar >= 1) else str(int(h))\n",
    "            ax.text(bar.get_x()+bar.get_width()/2, h+0.5, txt, ha='center', va='bottom', fontsize=7, fontweight='bold')\n",
    "ax.set_title('VIF', fontweight='bold', pad=8)\n",
    "ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2**','Q3**','Q4**'])\n",
    "ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend(fontsize=8)\n",
    "plt.figtext(0.5, -0.02, '** Valores Proxy Q2-Q4 2026 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_coh_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# ===================== CELDA 30: ITT GLOBAL =====================
ITT_GLOBAL_SOURCE = [
    "fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)\n",
    "fig.suptitle('ITT Global — Pulmon de Oriente', fontsize=13, fontweight='bold', color='#1B2631')\n",
    "COLORES_ITT = ['#42A5F5','#2E7D32','#E53935','#FF6F00']\n",
    "band_configs = [(0,40,'#FFCDD2','Emergencia'),(40,60,'#FFE0B2','Consolidacion'),\n",
    "                (60,80,'#C8E6C9','Avance'),(80,100,'#BBDEFB','Transformacion')]\n",
    "\n",
    "ax1 = axes[0]\n",
    "x_labels = [f'{a}**' if a==2026 else str(a) for a in ANIOS]\n",
    "bars = ax1.bar(range(len(ANIOS)), base['ITT'], color=COLORES_ITT, alpha=0.85, edgecolor='white', width=0.5)\n",
    "for bar, val, nivel, año in zip(bars, base['ITT'], base['nivel'], ANIOS):\n",
    "    marca = '**' if año==2026 else ''\n",
    "    ax1.text(bar.get_x()+bar.get_width()/2, val+1, f'{val:.1f}{marca}\\n{nivel}', ha='center', va='bottom',\n",
    "            fontsize=10, fontweight='bold', color=NIVEL_COLORS.get(nivel,'#1B2631'))\n",
    "for y0,y1,c,l in band_configs: ax1.axhspan(y0,y1, alpha=0.15, color=c)\n",
    "ax1.set_title('ITT por Año (promedio trimestral)', fontweight='bold', pad=10)\n",
    "ax1.set_ylim(0,115); ax1.set_ylabel('ITT (0-100)')\n",
    "ax1.set_xticks(range(len(ANIOS))); ax1.set_xticklabels(x_labels)\n",
    "\n",
    "ax2 = axes[1]\n",
    "dims = ['score_seguridad','score_movilidad','score_entorno_u','score_educ_des','score_cohesion']\n",
    "dim_lbl = ['Seguridad','Movilidad (ref)','EntornoU (ref)','EducDes (ref)','Cohesion']\n",
    "dim_p = [PESOS['Seguridad'],PESOS['Movilidad'],PESOS['EntornoU'],PESOS['EducDes'],PESOS['Cohesion']]\n",
    "dim_c = [C_SEG, C_MOV, '#43A047', '#FB8C00', C_COH]\n",
    "bottom = np.zeros(len(ANIOS))\n",
    "for dim, lbl, peso, col in zip(dims, dim_lbl, dim_p, dim_c):\n",
    "    vals = base[dim].values * peso\n",
    "    ax2.bar(range(len(ANIOS)), vals, bottom=bottom, label=f'{lbl} ({peso:.0%})', color=col, alpha=0.8, edgecolor='white', width=0.5)\n",
    "    bottom += vals\n",
    "ax2.plot(range(len(ANIOS)), base['ITT'], 'D-', color='black', linewidth=2, markersize=8, label='ITT Total', zorder=5)\n",
    "for y0,y1,c,l in band_configs: ax2.axhspan(y0,y1, alpha=0.1, color=c)\n",
    "ax2.set_title('Composicion ITT', fontweight='bold', pad=10)\n",
    "ax2.set_ylim(0,115); ax2.set_ylabel('Score ponderado')\n",
    "ax2.set_xticks(range(len(ANIOS))); ax2.set_xticklabels(x_labels)\n",
    "ax2.legend(loc='upper right', fontsize=7)\n",
    "plt.figtext(0.5, -0.02, '** 2026 incluye valores Proxy Q2-Q4 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_global.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]

# ===================== CELDA 32: RADAR =====================
RADAR_SOURCE = [
    "DIMS_LBL = ['Seguridad','Movilidad\\n(ref)','Cohesion\\nSocial','Entorno\\nUrbano (ref)','Educ y\\nDes (ref)']\n",
    "N_DIMS = 5\n",
    "angles = [i/N_DIMS*2*np.pi for i in range(N_DIMS)] + [0]\n",
    "COLORES_R = ['#42A5F5','#2E7D32','#E53935','#FF6F00']\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True), facecolor=BG)\n",
    "fig.suptitle('Radar ITT — Pulmon de Oriente | 5 Dimensiones', fontsize=13, fontweight='bold', color='#1B2631')\n",
    "ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)\n",
    "ax.set_xticks(angles[:-1]); ax.set_xticklabels(DIMS_LBL, fontsize=9)\n",
    "ax.set_ylim(0,100); ax.set_yticks([20,40,60,80,100])\n",
    "ax.set_yticklabels(['20','40','60','80','100'], fontsize=7, color='gray')\n",
    "ax.yaxis.grid(True, linestyle='--', alpha=0.4)\n",
    "\n",
    "for idx, año in enumerate(ANIOS):\n",
    "    row = base[base['año']==año].iloc[0]\n",
    "    vals = [row['score_seguridad'],row['score_movilidad'],row['score_cohesion'],row['score_entorno_u'],row['score_educ_des']]\n",
    "    vals_c = vals + [vals[0]]\n",
    "    lbl = f'{año}**' if año==2026 else str(año)\n",
    "    ax.plot(angles, vals_c, 'o-', color=COLORES_R[idx], linewidth=2, markersize=5, label=lbl)\n",
    "    ax.fill(angles, vals_c, alpha=0.08, color=COLORES_R[idx])\n",
    "ax.legend(loc='upper right', bbox_to_anchor=(1.3,1.1), fontsize=9)\n",
    "plt.figtext(0.5, -0.02, '** 2026 incluye valores Proxy Q2-Q4 (promedio historico 2023-2025)', ha='center', fontsize=8, style='italic', color='#666666')\n",
    "plt.tight_layout()\n",
    "plt.savefig(IMG_DIR + 'itt_pulmon_radar.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
    "plt.show()\n",
]


def main():
    print(f'Leyendo notebook: {NOTEBOOK_PATH}')
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    patches = {
        20: ('Cards metricas', CARDS_SOURCE),
        22: ('Heatmap Seguridad', HEATMAP_SEG_SOURCE),
        24: ('Heatmap VIF', HEATMAP_VIF_SOURCE),
        26: ('Barras Seguridad', BARRAS_SEG_SOURCE),
        28: ('Barras Cohesion/VIF', BARRAS_COH_SOURCE),
        30: ('ITT Global', ITT_GLOBAL_SOURCE),
        32: ('Radar', RADAR_SOURCE),
    }

    for idx, (nombre, new_source) in patches.items():
        if idx < len(cells):
            cells[idx]['source'] = new_source
            cells[idx]['outputs'] = []
            print(f'  Celda {idx} ({nombre}) — reemplazada con marcadores **')

    print(f'\nGuardando notebook...')
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('LISTO. Todos los graficos mostraran ** en valores Proxy 2026.')


if __name__ == '__main__':
    main()
