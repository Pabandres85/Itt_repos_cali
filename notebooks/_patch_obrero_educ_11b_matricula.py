"""Celda 11B: Matricula por comuna (Oficial vs No Oficial) con Comuna 9 resaltada."""
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
        "# Matricula por comuna - Oficial vs No Oficial (2026)\n",
        "import glob\n",
        "from pathlib import Path as _Path\n",
        "\n",
        "_mat_path = None\n",
        "for p in glob.glob('/content/itt_repos_cali/data/referencia/**/01_Matricula_2026.xlsx', recursive=True):\n",
        "    _mat_path = _Path(p)\n",
        "    break\n",
        "\n",
        "if _mat_path and _mat_path.exists():\n",
        "    df_mat = pd.read_excel(_mat_path, sheet_name='Por comuna')\n",
        "    # Filtrar solo comunas urbanas (1-22)\n",
        "    df_mat = df_mat[df_mat['comuna'].str.contains('Comuna', na=False)].copy()\n",
        "    df_mat['num_comuna'] = df_mat['comuna'].str.extract(r'(\\d+)').astype(int)\n",
        "    df_mat = df_mat[df_mat['num_comuna'].between(1, 22)].sort_values('num_comuna')\n",
        "\n",
        "    # Grafico barras agrupadas: Oficial vs No Oficial\n",
        "    fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)\n",
        "    x = np.arange(len(df_mat))\n",
        "    w = 0.35\n",
        "\n",
        "    bars1 = ax.bar(x - w/2, df_mat['Oficial'], w, label='Oficial', color='#1565C0', edgecolor='white', alpha=0.85)\n",
        "    bars2 = ax.bar(x + w/2, df_mat['No oficial'], w, label='No oficial', color='#FF8F00', edgecolor='white', alpha=0.85)\n",
        "\n",
        "    # Etiquetas de valores\n",
        "    for bar in bars1:\n",
        "        h = bar.get_height()\n",
        "        ax.text(bar.get_x()+bar.get_width()/2, h+100, f'{int(h):,}', ha='center', fontsize=6, fontweight='bold', color='#1565C0')\n",
        "    for bar in bars2:\n",
        "        h = bar.get_height()\n",
        "        ax.text(bar.get_x()+bar.get_width()/2, h+100, f'{int(h):,}', ha='center', fontsize=6, fontweight='bold', color='#FF8F00')\n",
        "\n",
        "    # Resaltar Comuna 9 (Barrio Obrero)\n",
        "    idx_c9 = list(df_mat['num_comuna']).index(9)\n",
        "    ax.axvspan(idx_c9-0.5, idx_c9+0.5, alpha=0.15, color='#E53935', label='Comuna 9 (Barrio Obrero)')\n",
        "\n",
        "    comunas_label = [f'C{int(i)}' for i in df_mat['num_comuna']]\n",
        "    ax.set_xticks(x)\n",
        "    ax.set_xticklabels(comunas_label, fontsize=9)\n",
        "    ax.set_xlabel('Comuna')\n",
        "    ax.set_ylabel('Estudiantes matriculados')\n",
        "    ax.set_title('Matricula por comuna — Oficial vs No Oficial | Cali 2026', fontsize=13, fontweight='bold')\n",
        "    ax.legend(fontsize=10)\n",
        "    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))\n",
        "\n",
        "    # Dato Comuna 9\n",
        "    c9 = df_mat[df_mat['num_comuna']==9].iloc[0]\n",
        "    ax.annotate(f'C9: {int(c9.Oficial):,} of. + {int(c9[\"No oficial\"]):,} no of.\\nTotal: {int(c9.Total):,}',\n",
        "               xy=(idx_c9, c9['Total']), xytext=(idx_c9+2, c9['Total']+3000),\n",
        "               fontsize=8, color='#E53935', fontweight='bold',\n",
        "               arrowprops=dict(arrowstyle='->', color='#E53935'))\n",
        "\n",
        "    plt.tight_layout()\n",
        "    plt.savefig(IMG_DIR + 'itt_obrero_educ_matricula_comuna.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
        "    plt.show()\n",
        "    print(f'Comuna 9: Oficial={int(c9.Oficial):,} | No oficial={int(c9[\"No oficial\"]):,} | Total={int(c9.Total):,}')\n",
        "else:\n",
        "    print('Archivo 01_Matricula_2026.xlsx no encontrado.')\n",
    ]

    cells[target_idx]['source'] = new_source
    cells[target_idx]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('Celda 11B: Matricula por comuna (Oficial vs No Oficial, Comuna 9 resaltada)')
