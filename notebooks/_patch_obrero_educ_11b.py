"""Reemplazar Celda 11B con grafico de IE y sedes por comuna."""
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
            target_idx = i + 1  # La celda de codigo es la siguiente
            break

if target_idx is None:
    print('ERROR: No se encontro Celda 11B')
else:
    new_source = [
        "# Cargar info geografica de sedes educativas\n",
        "import zipfile\n",
        "from pathlib import Path as _Path\n",
        "\n",
        "# Ruta al archivo (Colab o local)\n",
        "_educ_path = None\n",
        "for p in [\n",
        "    _Path('/content/itt_repos_cali/data/referencia/data_Observatorio_de_Educación/Fuentes de datos/Información geográfica sedes.xlsx'),\n",
        "    _Path('/content/itt_repos_cali/data/referencia/data_Observatorio_de_Educacion/Fuentes de datos/Informacion geografica sedes.xlsx'),\n",
        "]:\n",
        "    if p.exists():\n",
        "        _educ_path = p\n",
        "        break\n",
        "\n",
        "if _educ_path is None:\n",
        "    # Intentar buscar recursivamente\n",
        "    import glob\n",
        "    matches = glob.glob('/content/itt_repos_cali/data/referencia/**/Informaci*n geogr*fica sedes.xlsx', recursive=True)\n",
        "    if matches:\n",
        "        _educ_path = _Path(matches[0])\n",
        "\n",
        "if _educ_path and _educ_path.exists():\n",
        "    df_sedes = pd.read_excel(_educ_path)\n",
        "    # Filtrar solo comunas urbanas (1-22)\n",
        "    df_sedes['num_comuna'] = pd.to_numeric(df_sedes['EEComCor'], errors='coerce')\n",
        "    df_urbano = df_sedes[df_sedes['num_comuna'].between(1, 22)].copy()\n",
        "\n",
        "    # Contar IE (instituciones unicas) y sedes por comuna\n",
        "    df_icet = df_urbano.groupby('num_comuna').agg(\n",
        "        instituciones=('EeCodDane', 'nunique'),\n",
        "        sedes_total=('EeConSede', 'count')\n",
        "    ).reset_index()\n",
        "\n",
        "    # Grafico: IE y sedes por comuna\n",
        "    fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
        "    comunas_label = [f'C{int(i)}' for i in df_icet.sort_values('num_comuna')['num_comuna']]\n",
        "    df_sorted = df_icet.sort_values('num_comuna')\n",
        "\n",
        "    # IE por comuna\n",
        "    bars = axes[0].bar(comunas_label, df_sorted['instituciones'], color='#66c2a5')\n",
        "    axes[0].set_title('Instituciones Educativas por comuna')\n",
        "    axes[0].set_xlabel('Comuna')\n",
        "    axes[0].set_ylabel('Cantidad de IE')\n",
        "    for bar in bars:\n",
        "        h = bar.get_height()\n",
        "        axes[0].text(bar.get_x()+bar.get_width()/2, h+0.2, f'{int(h)}', ha='center', fontsize=8)\n",
        "\n",
        "    # Sedes por comuna\n",
        "    bars = axes[1].bar(comunas_label, df_sorted['sedes_total'], color='#8da0cb')\n",
        "    axes[1].set_title('Sedes educativas por comuna')\n",
        "    axes[1].set_xlabel('Comuna')\n",
        "    axes[1].set_ylabel('Cantidad de sedes')\n",
        "    for bar in bars:\n",
        "        h = bar.get_height()\n",
        "        axes[1].text(bar.get_x()+bar.get_width()/2, h+0.2, f'{int(h)}', ha='center', fontsize=8)\n",
        "\n",
        "    plt.suptitle('Oferta educativa por comuna - Cali 2026', fontsize=13, y=1.02)\n",
        "    plt.tight_layout()\n",
        "    plt.savefig(IMG_DIR + 'itt_obrero_educ_oferta_comuna.png', dpi=150, bbox_inches='tight', facecolor=BG)\n",
        "    plt.show()\n",
        "    print(f'IE y sedes por comuna generado. Total: {len(df_icet)} comunas.')\n",
        "else:\n",
        "    print('Archivo de info geografica sedes no encontrado. Saltando grafico.')\n",
    ]

    cells[target_idx]['source'] = new_source
    cells[target_idx]['outputs'] = []

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('Celda 11B reemplazada con grafico IE y sedes por comuna')
