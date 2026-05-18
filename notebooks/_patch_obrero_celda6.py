"""
Reescribir Celda 6 de Barrio Obrero para:
1. Detectar columna de fecha automaticamente (compatible con archivos DATIC nuevos)
2. Filtrar rinas con startswith('RI') en vez de == 'RIÑAS' (mas robusto)
3. Generar base (anual, solo 2023-2025) y corr_trim (trimestral, 2023-2026 con Proxy**)
4. Separar claramente datos reales vs Proxy
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

new_source = [
    "FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'fecha_hecho', 'fecha', 'FECHA_HECH', 'Fecha']\n",
    "\n",
    "def pick_col(df, candidates):\n",
    "    cols_lower = {c.lower(): c for c in df.columns}\n",
    "    for cand in candidates:\n",
    "        if cand in df.columns: return cand\n",
    "        if cand.lower() in cols_lower: return cols_lower[cand.lower()]\n",
    "    return None\n",
    "\n",
    "def procesar(raw, nombre, filtro=None, filtro_col=None, startswith=False):\n",
    "    df = pd.DataFrame([f['properties'] for f in raw['features']])\n",
    "    if filtro and filtro_col:\n",
    "        if startswith:\n",
    "            df = df[df[filtro_col].astype(str).str.upper().str.startswith(filtro)].copy()\n",
    "        else:\n",
    "            df = df[df[filtro_col]==filtro].copy()\n",
    "    col_fecha = pick_col(df, FECHA_CANDIDATES)\n",
    "    if col_fecha is None:\n",
    "        raise ValueError(f'No se encontro columna de fecha en {nombre}. Columnas: {list(df.columns)[:10]}')\n",
    "    df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')\n",
    "    df['año'] = df['_fecha'].dt.year\n",
    "    df['trimestre'] = df['_fecha'].dt.quarter\n",
    "    df = df.dropna(subset=['año'])\n",
    "    df['año'] = df['año'].astype(int)\n",
    "    return df[df['año'].isin(ANIOS)].copy()\n",
    "\n",
    "def agg_anual(df): return df.groupby('año').size().reindex(ANIOS, fill_value=0)\n",
    "def agg_trim(df):\n",
    "    idx = pd.MultiIndex.from_product([ANIOS,[1,2,3,4]], names=['año','trimestre'])\n",
    "    return df.groupby(['año','trimestre']).size().reindex(idx, fill_value=0)\n",
    "\n",
    "df_hom = procesar(raw_hom, 'Homicidios')\n",
    "df_hur = procesar(raw_hur, 'Hurtos')\n",
    "df_sin = procesar(raw_sin, 'Siniestros')\n",
    "df_les = df_sin[df_sin['Tipo_Confi']=='Lesiones'].copy() if 'Tipo_Confi' in df_sin.columns else pd.DataFrame(columns=['año','trimestre'])\n",
    "df_mor = df_sin[df_sin['Tipo_Confi']=='Mortal'].copy() if 'Tipo_Confi' in df_sin.columns else pd.DataFrame(columns=['año','trimestre'])\n",
    "df_vif = procesar(raw_vif, 'VIF')\n",
    "df_rin = procesar(raw_comp, 'Comparendos', filtro='RI', filtro_col='agrupado', startswith=True)\n",
    "\n",
    "print(f'Registros procesados:')\n",
    "for n, d in [('Homicidios',df_hom),('Hurtos',df_hur),('Siniestros',df_sin),('VIF',df_vif),('Rinas',df_rin)]:\n",
    "    print(f'  {n:12s}: {len(d):>4} registros')\n",
    "\n",
    "# === TABLA TRIMESTRAL (2023-2026, incluye Q1 2026 real) ===\n",
    "idx_t = pd.MultiIndex.from_product([ANIOS,[1,2,3,4]], names=['año','trimestre'])\n",
    "corr_trim = pd.DataFrame(index=idx_t).reset_index()\n",
    "for nombre, df_src in [('homicidios',df_hom),('hurtos',df_hur),('siniestralidad',df_sin),\n",
    "                       ('lesionados',df_les),('mortales',df_mor),('vif',df_vif),('rinas',df_rin)]:\n",
    "    ser = agg_trim(df_src).reset_index()\n",
    "    ser.columns = ['año','trimestre',nombre]\n",
    "    corr_trim = corr_trim.merge(ser, on=['año','trimestre'], how='left').fillna({nombre:0})\n",
    "corr_trim['periodo'] = corr_trim['año'].astype(str) + '-Q' + corr_trim['trimestre'].astype(str)\n",
    "\n",
    "# === PROXY Q2-Q4 2026 (promedio historico 2023-2025) ===\n",
    "indicadores_trim = [c for c in corr_trim.columns if c not in ['año','trimestre','periodo']]\n",
    "hist_trim = corr_trim[corr_trim['año'].isin([2023, 2024, 2025])]\n",
    "for trim in [2, 3, 4]:\n",
    "    mask = (corr_trim['año'] == 2026) & (corr_trim['trimestre'] == trim)\n",
    "    if corr_trim.loc[mask, indicadores_trim].sum().sum() == 0:\n",
    "        trim_hist = hist_trim[hist_trim['trimestre'] == trim]\n",
    "        for ind in indicadores_trim:\n",
    "            corr_trim.loc[mask, ind] = round(trim_hist[ind].mean(), 1)\n",
    "corr_trim['es_proxy'] = (corr_trim['año'] == 2026) & (corr_trim['trimestre'].isin([2,3,4]))\n",
    "\n",
    "# === TABLA ANUAL (solo 2023-2025, años completos con datos reales) ===\n",
    "ANIOS_COMPLETOS = [2023, 2024, 2025]\n",
    "base = pd.DataFrame({'año': ANIOS_COMPLETOS})\n",
    "for nombre, df_src in [('homicidios',df_hom),('hurtos',df_hur),('siniestralidad',df_sin),\n",
    "                       ('lesionados',df_les),('mortales',df_mor),('vif',df_vif),('rinas',df_rin)]:\n",
    "    base[nombre] = df_src[df_src['año'].isin(ANIOS_COMPLETOS)].groupby('año').size().reindex(ANIOS_COMPLETOS, fill_value=0).values\n",
    "\n",
    "print()\n",
    "print('Indicadores anuales (2023-2025, datos reales):')\n",
    "print(base.to_string(index=False))\n",
    "print()\n",
    "print('Indicadores trimestrales (2023-2026, Q2-Q4 2026 = Proxy**):')\n",
    "print(corr_trim[['año','trimestre'] + indicadores_trim + ['es_proxy']].to_string(index=False))\n",
]

# Celda 22 es la de procesamiento
cells[22]['source'] = new_source
cells[22]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 6 (procesamiento) reescrita:')
print('  - pick_col() detecta columna de fecha automaticamente')
print('  - Filtro rinas con startswith(RI) (robusto)')
print('  - base = solo 2023-2025 (años completos, para Cards/ITT Global/Radar)')
print('  - corr_trim = 2023-2026 con Proxy Q2-Q4 (para heatmaps/barras)')
