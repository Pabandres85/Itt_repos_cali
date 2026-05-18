"""Agregar celdas de Heatmap y Barras trimestrales para Educacion en Barrio Obrero."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Celda Heatmap Educacion (insertar despues de Celda 11 Cohesion, idx 32)
heatmap_educ_md = {
    "cell_type": "markdown",
    "id": "md_heatmap_educ",
    "metadata": {},
    "source": ["## Celda 11B — Heatmap: Dimension Educacion y Desarrollo\n"]
}

heatmap_educ_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": "heatmap_educ",
    "metadata": {},
    "outputs": [],
    "source": [
        "# Heatmap Educacion - score por trimestre\n",
        "# 2023-2025: Proxy 54.9 | 2026 Q1: real 31.5 (Comuna 9)\n",
        "fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)\n",
        "fig.suptitle('Dimension Educacion y Desarrollo — Score Trimestral | Barrio Obrero',\n",
        "             fontsize=13, fontweight='bold', color='#1B2631')\n",
        "\n",
        "# Construir tabla de scores educacion por trimestre\n",
        "educ_data = []\n",
        "for _, row in corr_trim.iterrows():\n",
        "    año = int(row['año'])\n",
        "    trim = int(row['trimestre'])\n",
        "    if año == 2026:\n",
        "        score = REF_EDUC_DES_2026  # 31.5 real\n",
        "    else:\n",
        "        score = REF_EDUC_DES  # 54.9 proxy\n",
        "    educ_data.append({'año': año, 'trimestre': trim, 'score_educ': score})\n",
        "\n",
        "df_educ = pd.DataFrame(educ_data)\n",
        "pivot = df_educ.pivot(index='año', columns='trimestre', values='score_educ')\n",
        "pivot.columns = ['Q1','Q2','Q3','Q4']\n",
        "\n",
        "# Anotaciones con - para trimestres sin datos\n",
        "annot_arr = pivot.copy().astype(object)\n",
        "for c in annot_arr.columns:\n",
        "    for r in annot_arr.index:\n",
        "        val = pivot.loc[r, c]\n",
        "        if pd.isna(val) or (r == 2026 and c != 'Q1'):\n",
        "            annot_arr.loc[r, c] = '-'\n",
        "        elif r == 2026:\n",
        "            annot_arr.loc[r, c] = f'{val:.1f} (real)'\n",
        "        else:\n",
        "            annot_arr.loc[r, c] = f'{val:.1f} (proxy)'\n",
        "pivot_plot = pivot.fillna(0)\n",
        "\n",
        "sns.heatmap(pivot_plot, annot=annot_arr.values, fmt='', cmap='YlGn',\n",
        "    linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size':10},\n",
        "    cbar_kws={'label':'Score (0-100)','shrink':0.8}, vmin=0, vmax=100)\n",
        "ax.set_title('Score Educacion (Proxy 2023-2025 | Real 2026)', fontweight='bold', pad=8)\n",
        "ax.set_ylabel(''); ax.set_xlabel('')\n",
        "plt.tight_layout()\n",
        "plt.savefig(IMG_DIR + 'itt_obrero_heatmap_educ.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
        "plt.show()\n",
    ]
}

# Celda Barras Educacion (insertar despues de Celda 14 Cohesion)
barras_educ_md = {
    "cell_type": "markdown",
    "id": "md_barras_educ",
    "metadata": {},
    "source": ["## Celda 14B — Evolucion trimestral: Educacion y Desarrollo\n"]
}

barras_educ_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": "barras_educ",
    "metadata": {},
    "outputs": [],
    "source": [
        "# Barras trimestrales Educacion\n",
        "# Muestra el score de educacion por trimestre (Proxy vs Real)\n",
        "fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)\n",
        "fig.suptitle('Dimension Educacion y Desarrollo - Score Trimestral | Barrio Obrero',\n",
        "             fontsize=13, fontweight='bold', color='#1B2631')\n",
        "\n",
        "# Gama verde claro a oscuro\n",
        "COLORES_EDUC = ['#A5D6A7', '#43A047', '#1B5E20', '#003300']\n",
        "x = np.arange(4); n = len(ANIOS); w = 0.8/n\n",
        "\n",
        "for idx, año in enumerate(ANIOS):\n",
        "    if año == 2026:\n",
        "        vals = [REF_EDUC_DES_2026]  # Solo Q1 real\n",
        "    else:\n",
        "        vals = [REF_EDUC_DES] * 4  # Proxy constante\n",
        "    x_pos = x[:len(vals)]\n",
        "    b = ax.bar(x_pos + (idx-n/2+0.5)*w, vals, w, label=str(año), color=COLORES_EDUC[idx], alpha=0.85, edgecolor='white')\n",
        "    for bar in b:\n",
        "        h = bar.get_height()\n",
        "        lbl = f'{h:.1f}' if año == 2026 else f'{h:.1f}*'\n",
        "        ax.text(bar.get_x()+bar.get_width()/2, h+0.5, lbl, ha='center', va='bottom', fontsize=8, fontweight='bold')\n",
        "\n",
        "ax.set_xticks(x); ax.set_xticklabels(['Q1','Q2','Q3','Q4'])\n",
        "ax.set_ylabel('Score (0-100)'); ax.set_ylim(0, 100)\n",
        "ax.axhline(y=REF_EDUC_DES, color='gray', linestyle='--', alpha=0.5, label=f'Proxy={REF_EDUC_DES}')\n",
        "ax.axhline(y=REF_EDUC_DES_2026, color='red', linestyle='--', alpha=0.5, label=f'Real 2026={REF_EDUC_DES_2026}')\n",
        "ax.legend(fontsize=8)\n",
        "ax.set_title('* = Proxy (sin datos propios) | 2026 Q1 = dato real Comuna 9', fontsize=9, color='#666666')\n",
        "plt.tight_layout()\n",
        "plt.savefig(IMG_DIR + 'itt_obrero_educ_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
        "plt.show()\n",
    ]
}

# Insertar en el orden correcto
# Heatmap Educacion: despues de idx 32 (Heatmap Cohesion code)
# Primero encontrar la posicion correcta
insert_heatmap = None
insert_barras = None

for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if 'Celda 12' in source and 'Seguridad' in source:
            insert_heatmap = i  # Insertar ANTES de Celda 12
            break

for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if 'Celda 15' in source and 'ITT Global' in source:
            insert_barras = i  # Insertar ANTES de Celda 15
            break

if insert_barras:
    cells.insert(insert_barras, barras_educ_md)
    cells.insert(insert_barras + 1, barras_educ_code)
    print(f'  Barras Educacion insertadas en idx {insert_barras}')

if insert_heatmap:
    # Recalcular posicion despues de la insercion anterior
    # Insertar despues de Celda 11 (Cohesion heatmap) = antes de Celda 12
    cells.insert(insert_heatmap, heatmap_educ_md)
    cells.insert(insert_heatmap + 1, heatmap_educ_code)
    print(f'  Heatmap Educacion insertado en idx {insert_heatmap}')

nb['cells'] = cells

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('\nCeldas de Educacion agregadas:')
print('  - Heatmap Educacion (Celda 11B): score por trimestre con proxy vs real')
print('  - Barras Educacion (Celda 14B): evolucion trimestral con lineas de referencia')
print('  - Colores: verde gradiente [#A5D6A7, #43A047, #1B5E20, #003300]')
