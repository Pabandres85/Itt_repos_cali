"""
Script para modificar directamente el notebook 04_itt_pulmon_oriente_2026_v2.ipynb
Reemplaza las Celdas 6 y 7 con la logica de Proxy y normalizacion completa.

Ejecutar desde la raiz del proyecto:
    python notebooks/_patch_pulmon_oriente_proxy.py
"""
import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).parent / '04_itt_pulmon_oriente_2026_v2.ipynb'

# =============================================================================
# NUEVO CONTENIDO CELDA 6
# =============================================================================
CELDA6_SOURCE = [
    "FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'fecha_hecho', 'fecha', 'FECHA_HECH']\n",
    "\n",
    "def pick_col(df, candidates):\n",
    "    cols_lower = {c.lower(): c for c in df.columns}\n",
    "    for cand in candidates:\n",
    "        if cand in df.columns:\n",
    "            return cand\n",
    "        if cand.lower() in cols_lower:\n",
    "            return cols_lower[cand.lower()]\n",
    "    return None\n",
    "\n",
    "def dedup_raw(raw, nombre):\n",
    "    \"\"\"Deduplica features de un GeoJSON por coordenada (datos estaticos).\"\"\"\n",
    "    registros = []\n",
    "    for feat in raw['features']:\n",
    "        row = dict(feat['properties'])\n",
    "        if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "            coords = feat['geometry']['coordinates']\n",
    "            row['_lon'] = coords[0]\n",
    "            row['_lat'] = coords[1]\n",
    "        elif 'x' in row and 'y' in row:\n",
    "            row['_lon'] = row['x']\n",
    "            row['_lat'] = row['y']\n",
    "        else:\n",
    "            row['_lon'] = None\n",
    "            row['_lat'] = None\n",
    "        registros.append(row)\n",
    "    df = pd.DataFrame(registros)\n",
    "    n_total = len(df)\n",
    "    df = df.drop_duplicates(keep='first').reset_index(drop=True)\n",
    "    n_unicos = len(df)\n",
    "    n_dupes = n_total - n_unicos\n",
    "    print(f'  {nombre:15s}: {n_total:>5} total -> {n_unicos:>5} unicos ({n_dupes} duplicados eliminados)')\n",
    "    return df, n_dupes\n",
    "\n",
    "def procesar(raw, nombre):\n",
    "    \"\"\"Procesa GeoJSON: deduplica por FECHA + COORDENADA, filtra periodo.\"\"\"\n",
    "    registros = []\n",
    "    for feat in raw['features']:\n",
    "        row = dict(feat['properties'])\n",
    "        if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "            coords = feat['geometry']['coordinates']\n",
    "            row['_lon'] = coords[0]\n",
    "            row['_lat'] = coords[1]\n",
    "        elif 'x' in row and 'y' in row:\n",
    "            row['_lon'] = row['x']\n",
    "            row['_lat'] = row['y']\n",
    "        else:\n",
    "            row['_lon'] = None\n",
    "            row['_lat'] = None\n",
    "        registros.append(row)\n",
    "    df = pd.DataFrame(registros)\n",
    "    n_total = len(df)\n",
    "    col_fecha = pick_col(df, FECHA_CANDIDATES)\n",
    "    if col_fecha is None:\n",
    "        raise ValueError(f'No se encontro columna de fecha en {nombre}')\n",
    "    df['_fecha_str'] = df[col_fecha].astype(str).str.strip()\n",
    "    df = df.drop_duplicates(subset=['_fecha_str', '_lon', '_lat'], keep='first').reset_index(drop=True)\n",
    "    n_unicos = len(df)\n",
    "    n_dupes = n_total - n_unicos\n",
    "    print(f'  {nombre:15s}: {n_total:>5} total -> {n_unicos:>5} unicos ({n_dupes} duplicados eliminados)')\n",
    "    df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')\n",
    "    df['año'] = df['_fecha'].dt.year\n",
    "    df['trimestre'] = df['_fecha'].dt.quarter\n",
    "    df = df.dropna(subset=['año'])\n",
    "    df['año'] = df['año'].astype(int)\n",
    "    return df[df['año'].isin(ANIOS)].copy()\n",
    "\n",
    "def agg_anual(df):\n",
    "    return df.groupby('año').size().reindex(ANIOS, fill_value=0)\n",
    "\n",
    "def agg_trim(df):\n",
    "    \"\"\"Agrega por trimestre. Rellena con 0 TODOS los trimestres.\"\"\"\n",
    "    serie = df.groupby(['año','trimestre']).size()\n",
    "    for anio in ANIOS:\n",
    "        for trim in [1, 2, 3, 4]:\n",
    "            if (anio, trim) not in serie.index:\n",
    "                serie.loc[(anio, trim)] = 0\n",
    "    return serie\n",
    "\n",
    "# --- Deduplicar ---\n",
    "print('Deduplicacion de registros (por fecha + coordenada):')\n",
    "print('='*60)\n",
    "df_hom = procesar(raw_hom, 'Homicidios')\n",
    "df_hur = procesar(raw_hur, 'Hurtos')\n",
    "df_vif = procesar(raw_vif, 'VIF')\n",
    "if raw_comp['features']:\n",
    "    df_comp = procesar(raw_comp, 'Comparendos')\n",
    "    df_rin = df_comp[df_comp['agrupado'].astype(str).str.upper().str.startswith('RI')].copy()\n",
    "else:\n",
    "    df_rin = pd.DataFrame(columns=['año', 'trimestre'])\n",
    "print(f'Rinas filtradas: {len(df_rin)} registros')\n",
    "\n",
    "# Datos estaticos\n",
    "print()\n",
    "df_arb, _ = dedup_raw(raw_arb, 'Arboles') if raw_arb['features'] else (pd.DataFrame(), 0)\n",
    "df_sed, _ = dedup_raw(raw_sed, 'Sedes Educ') if raw_sed['features'] else (pd.DataFrame(), 0)\n",
    "df_cai, _ = dedup_raw(raw_cai, 'CAI/MECAL') if raw_cai['features'] else (pd.DataFrame(), 0)\n",
    "print('='*60)\n",
    "\n",
    "# --- Tabla trimestral ---\n",
    "indicadores = ['homicidios', 'hurtos', 'vif', 'rinas']\n",
    "idx_t = pd.MultiIndex.from_product([ANIOS,[1,2,3,4]], names=['año','trimestre'])\n",
    "corr_trim = pd.DataFrame(index=idx_t).reset_index()\n",
    "for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:\n",
    "    ser = agg_trim(df_src).reset_index()\n",
    "    ser.columns = ['año','trimestre',nombre]\n",
    "    corr_trim = corr_trim.merge(ser, on=['año','trimestre'], how='left')\n",
    "corr_trim = corr_trim.fillna(0)\n",
    "\n",
    "# =============================================================\n",
    "# VALORES PROXY PARA Q2, Q3, Q4 DE 2026\n",
    "# Metodo: Promedio historico trimestral 2023-2025\n",
    "# =============================================================\n",
    "print()\n",
    "print('='*60)\n",
    "print('GENERACION DE VALORES PROXY — 2026 Q2, Q3, Q4')\n",
    "print('Metodo: Promedio historico trimestral 2023-2025')\n",
    "print('='*60)\n",
    "\n",
    "historico = corr_trim[corr_trim['año'].isin([2023, 2024, 2025])]\n",
    "proxy_values = {}\n",
    "for trim in [2, 3, 4]:\n",
    "    trim_hist = historico[historico['trimestre'] == trim]\n",
    "    proxy_values[trim] = {}\n",
    "    for ind in indicadores:\n",
    "        proxy_values[trim][ind] = round(trim_hist[ind].mean(), 1)\n",
    "\n",
    "# Aplicar Proxy\n",
    "for trim in [2, 3, 4]:\n",
    "    mask = (corr_trim['año'] == 2026) & (corr_trim['trimestre'] == trim)\n",
    "    for ind in indicadores:\n",
    "        corr_trim.loc[mask, ind] = proxy_values[trim][ind]\n",
    "\n",
    "corr_trim['es_proxy'] = False\n",
    "corr_trim.loc[(corr_trim['año'] == 2026) & (corr_trim['trimestre'].isin([2,3,4])), 'es_proxy'] = True\n",
    "corr_trim['periodo'] = corr_trim['año'].astype(str) + '-Q' + corr_trim['trimestre'].astype(str)\n",
    "\n",
    "# Recalcular anual con Proxy\n",
    "base = pd.DataFrame({'año': ANIOS})\n",
    "for ind in indicadores:\n",
    "    for anio in ANIOS:\n",
    "        base.loc[base['año'] == anio, ind] = corr_trim[corr_trim['año'] == anio][ind].sum()\n",
    "\n",
    "# Mostrar\n",
    "print()\n",
    "print('Valores Proxy generados:')\n",
    "for ind in indicadores:\n",
    "    q2, q3, q4 = proxy_values[2][ind], proxy_values[3][ind], proxy_values[4][ind]\n",
    "    print(f'  {ind:15s}  Q2={q2:.1f}**  Q3={q3:.1f}**  Q4={q4:.1f}**')\n",
    "\n",
    "print()\n",
    "print('Indicadores anuales (con Proxy 2026):')\n",
    "print(base.to_string(index=False))\n",
    "print()\n",
    "print('Indicadores trimestrales (** = Proxy):')\n",
    "print(corr_trim[['año','trimestre'] + indicadores + ['periodo','es_proxy']].to_string(index=False))\n",
    "print()\n",
    "print('NOTA: Q2, Q3, Q4 de 2026 son valores Proxy (promedio historico 2023-2025).')\n",
]

# =============================================================================
# NUEVO CONTENIDO CELDA 7
# =============================================================================
CELDA7_SOURCE = [
    "def score_ref(valor, ref_min, ref_max, inverso):\n",
    "    if ref_max == ref_min: return 100.0\n",
    "    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)\n",
    "    return 100 - raw if inverso else raw\n",
    "\n",
    "# Scores trimestrales por indicador\n",
    "for ind, (rmin, rmax, inv, desc) in REFS.items():\n",
    "    corr_trim[f'score_{ind}'] = corr_trim[ind].apply(lambda v, rm=rmin, rx=rmax, i=inv: score_ref(v, rm, rx, i))\n",
    "\n",
    "# Scores trimestrales por dimension\n",
    "corr_trim['score_seguridad'] = (corr_trim['score_homicidios'] + corr_trim['score_hurtos']) / 2\n",
    "corr_trim['score_cohesion']  = (corr_trim['score_vif'] + corr_trim['score_rinas'] + REF_VULNERABILIDAD) / 3\n",
    "corr_trim['score_movilidad'] = REF_MOVILIDAD\n",
    "corr_trim['score_entorno_u'] = REF_ENTORNO_U\n",
    "corr_trim['score_educ_des']  = REF_EDUC_DES\n",
    "\n",
    "corr_trim['ITT'] = (\n",
    "    PESOS['Seguridad'] * corr_trim['score_seguridad'] +\n",
    "    PESOS['Movilidad'] * corr_trim['score_movilidad'] +\n",
    "    PESOS['EntornoU']  * corr_trim['score_entorno_u'] +\n",
    "    PESOS['EducDes']   * corr_trim['score_educ_des'] +\n",
    "    PESOS['Cohesion']  * corr_trim['score_cohesion']\n",
    ")\n",
    "\n",
    "def clasificar(v):\n",
    "    if v < 40: return 'Emergencia'\n",
    "    elif v < 60: return 'Consolidacion'\n",
    "    elif v < 80: return 'Avance'\n",
    "    else: return 'Transformacion'\n",
    "\n",
    "corr_trim['nivel'] = corr_trim['ITT'].apply(clasificar)\n",
    "\n",
    "# ITT anual = promedio de los 4 trimestres (incluyendo Proxy para 2026)\n",
    "base = corr_trim.groupby('año').agg({\n",
    "    'homicidios': 'sum', 'hurtos': 'sum', 'vif': 'sum',\n",
    "    'score_seguridad': 'mean', 'score_cohesion': 'mean',\n",
    "    'score_movilidad': 'mean', 'score_entorno_u': 'mean', 'score_educ_des': 'mean',\n",
    "    'ITT': 'mean'\n",
    "}).reset_index()\n",
    "base['nivel'] = base['ITT'].apply(clasificar)\n",
    "\n",
    "print('ITT Pulmon de Oriente — Normalizacion con ref_min/ref_max fijos')\n",
    "print(f'\\nReferentes: Movilidad={REF_MOVILIDAD}, EntornoU={REF_ENTORNO_U}, EducDes={REF_EDUC_DES}')\n",
    "print('\\nScores por dimension e ITT (anual = promedio 4 trimestres):')\n",
    "print(base[['año','score_seguridad','score_movilidad','score_cohesion','score_entorno_u','score_educ_des','ITT','nivel']].round(1).to_string(index=False))\n",
    "print()\n",
    "print('NOTA: ITT 2026 incluye valores Proxy para Q2, Q3 y Q4.')\n",
    "print('Los Proxy se calcularon con promedio historico trimestral 2023-2025.')\n",
]


def find_cell_by_marker(cells, marker):
    """Encuentra el indice de una celda cuyo source contiene el marker."""
    for i, cell in enumerate(cells):
        source = ''.join(cell.get('source', []))
        if marker in source:
            return i
    return None


def main():
    print(f'Leyendo notebook: {NOTEBOOK_PATH}')
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    # Buscar Celda 6 por su contenido caracteristico
    idx6 = find_cell_by_marker(cells, 'FECHA_CANDIDATES')
    if idx6 is None:
        print('ERROR: No se encontro la Celda 6 (FECHA_CANDIDATES)')
        return

    # Buscar Celda 7 por su contenido caracteristico
    idx7 = find_cell_by_marker(cells, 'score_ref')
    if idx7 is None:
        print('ERROR: No se encontro la Celda 7 (score_ref)')
        return

    # Asegurar que idx7 > idx6
    if idx7 <= idx6:
        # Buscar la segunda ocurrencia de score_ref despues de idx6
        for i in range(idx6 + 1, len(cells)):
            source = ''.join(cells[i].get('source', []))
            if 'score_ref' in source and 'def score_ref' in source:
                idx7 = i
                break

    print(f'  Celda 6 encontrada en indice: {idx6}')
    print(f'  Celda 7 encontrada en indice: {idx7}')

    # Reemplazar source de Celda 6
    cells[idx6]['source'] = CELDA6_SOURCE
    cells[idx6]['outputs'] = []  # Limpiar outputs anteriores
    print('  Celda 6 reemplazada con logica Proxy')

    # Reemplazar source de Celda 7
    cells[idx7]['source'] = CELDA7_SOURCE
    cells[idx7]['outputs'] = []  # Limpiar outputs anteriores
    print('  Celda 7 reemplazada con normalizacion completa')

    # Guardar
    print(f'Guardando notebook modificado...')
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

    print('LISTO. El notebook ahora tiene:')
    print('  - Celda 6: Deduplicacion + Proxy Q2-Q4 2026')
    print('  - Celda 7: Normalizacion con 4 trimestres completos')
    print()
    print('Siguiente paso: ejecutar el notebook en Colab desde Celda 6 en adelante.')


if __name__ == '__main__':
    main()
