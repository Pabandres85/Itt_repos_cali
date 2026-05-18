"""Celda 11B: Grafico combinado IE + Sedes por comuna (barras agrupadas)."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Buscar Celda 11B
target_idx = None
for i, cell in enumerate(cells):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if '11B' in source and 'Educacion' in source:
            target_idx = i + 1
            break

if target_idx is None:
    print('ERROR: No se encontro Celda 11B')
else:
    new_source = [
        "# Cargar info geografica de sedes educativas\n",
        "from pathlib import Path as _Path\n",
        "import glob\n",
        "\n",
        "_educ_path = None\n",
        "for p in glob.glob('/content/itt_repos_cali/data/referencia/**/Informaci*n geogr*fica sedes.xlsx', recursive=True):\n",
        "    _educ_path = _Path(p)\n",
        "    break\n",
        "\n",
        "if _educ_path and _educ_path.exists():\n",
        "    df_sedes = pd.read_excel(_educ_path)\n",
        "    df_sedes['num_comuna'] = pd.to_numeric(df_sedes['EEComCor'], errors='coerce')\n",
        "    df_urbano = df_sedes[df_sedes['num_comuna'].between(1, 22)].copy()\n",
        "\n",
        "    df_icet = df_urbano.groupby('num_comuna').agg(\n",
        "        instituciones=('EeCodDane', 'nunique'),\n",
        "        sedes_total=('EeConSede', 'count')\n",
        "    ).reset_index().sort_values('num_comuna')\n",
        "\n",
        "    # Grafico combinado: barras agrupadas IE + Sedes\n",
        "    fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)\n",
        "    x = np.arange(len(df_icet))\n",
        "    w = 0.35\n",
        "\n",
        "    bars1 = ax.bar(x - w/2, df_icet['instituciones'], w, label='Instituciones Educativas (IE)', color='#66c2a5', edgecolor='white')\n",
        "    bars2 = ax.bar(x + w/2, df_icet['sedes_total'], w, label='Sedes educativas', color='#8da0cb', edgecolor='white')\n",
        "\n",
        "    # Etiquetas de valores\n",
        "    for bar in bars1:\n",
        "        h = bar.get_height()\n",
        "        ax.text(bar.get_x()+bar.get_width()/2, h+0.3, str(int(h)), ha='center', fontsize=7, fontweight='bold', color='#2d6a4f')\n",
        "    for bar in bars2:\n",
        "        h = bar.get_height()\n",
        "        ax.text(bar.get_x()+bar.get_width()/2, h+0.3, str(int(h)), ha='center', fontsize=7, fontweight='bold', color='#3949ab')\n",
        "\n",
        "    # Resaltar Comuna 9 (Barrio Obrero)\n",
        "    idx_c9 = df_icet[df_icet['num_comuna']==9].index[0] - df_icet.index[0]\n",
        "    ax.axvspan(idx_c9-0.5, idx_c9+0.5, alpha=0.15, color='#FF6F00', label='Comuna 9 (Barrio Obrero)')\n",
        "\n",
        "    comunas_label = [f'C{int(i)}' for i in df_icet['num_comuna']]\n",
        "    ax.set_xticks(x)\n",
        "    ax.set_xticklabels(comunas_label, fontsize=9)\n",
        "    ax.set_xlabel('Comuna')\n",
        "    ax.set_ylabel('Cantidad')\n",
        "    ax.set_title('Oferta educativa por comuna — Cali 2026', fontsize=13, fontweight='bold')\n",
        "    ax.legend(fontsize=10)\n",
        "    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))\n",
        "    plt.tight_layout()\n",
        "    plt.savefig(IMG_DIR + 'itt_obrero_educ_oferta_comuna.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
        "    plt.show()\n",
        "\n",
        "    # Dato de Comuna 9\n",
        "    c9 = df_icet[df_icet['num_comuna']==9].iloc[0]\n",
        "    print(f'Comuna 9 (Barrio Obrero): {int(c9.instituciones)} IE, {int(c9.sedes_total)} sedes')\n",
        "else:\n",
        "    print('Archivo de info geografica sedes no encontrado.')\n",
    ]

    cells[target_idx]['source'] = new_source
    cells[target_idx]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('Celda 11B: grafico combinado IE + Sedes (barras agrupadas, Comuna 9 resaltada)')
