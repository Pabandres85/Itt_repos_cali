"""
Barrio Obrero: Eliminar Proxy Q2-Q4 2026. Solo mostrar Q1 2026 real.
- corr_trim: solo trimestres con datos reales (2023 Q1-Q4, 2024 Q1-Q4, 2025 Q1-Q4, 2026 Q1)
- base: solo 2023-2025 (años completos)
- Heatmaps/Barras: 4 colores (naranja para 2026)
- ITT Global/Radar: solo 2023-2025
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Reescribir Celda 6 (procesamiento) - indice 22
new_celda6 = [
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
    "def agg_anual(df, anios):\n",
    "    return df.groupby('año').size().reindex(anios, fill_value=0)\n",
    "\n",
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
    "# === TABLA TRIMESTRAL (solo trimestres con datos reales) ===\n",
    "# 2023-2025: Q1-Q4 completos. 2026: solo Q1.\n",
    "idx_t = pd.MultiIndex.from_product([ANIOS,[1,2,3,4]], names=['año','trimestre'])\n",
    "corr_trim = pd.DataFrame(index=idx_t).reset_index()\n",
    "for nombre, df_src in [('homicidios',df_hom),('hurtos',df_hur),('siniestralidad',df_sin),\n",
    "                       ('lesionados',df_les),('mortales',df_mor),('vif',df_vif),('rinas',df_rin)]:\n",
    "    ser = agg_trim(df_src).reset_index()\n",
    "    ser.columns = ['año','trimestre',nombre]\n",
    "    corr_trim = corr_trim.merge(ser, on=['año','trimestre'], how='left').fillna({nombre:0})\n",
    "corr_trim['periodo'] = corr_trim['año'].astype(str) + '-Q' + corr_trim['trimestre'].astype(str)\n",
    "\n",
    "# Eliminar Q2-Q4 de 2026 (no hay datos reales, no usar Proxy)\n",
    "corr_trim = corr_trim[~((corr_trim['año']==2026) & (corr_trim['trimestre'].isin([2,3,4])))].copy()\n",
    "corr_trim = corr_trim.reset_index(drop=True)\n",
    "\n",
    "# === TABLA ANUAL (solo 2023-2025, años completos) ===\n",
    "ANIOS_COMPLETOS = [2023, 2024, 2025]\n",
    "base = pd.DataFrame({'año': ANIOS_COMPLETOS})\n",
    "for nombre, df_src in [('homicidios',df_hom),('hurtos',df_hur),('siniestralidad',df_sin),\n",
    "                       ('lesionados',df_les),('mortales',df_mor),('vif',df_vif),('rinas',df_rin)]:\n",
    "    base[nombre] = agg_anual(df_src, ANIOS_COMPLETOS).values\n",
    "\n",
    "print()\n",
    "print('Indicadores anuales (2023-2025, datos reales completos):')\n",
    "print(base.to_string(index=False))\n",
    "print()\n",
    "print('Indicadores trimestrales (solo datos reales, incluye Q1 2026):')\n",
    "print(corr_trim.to_string(index=False))\n",
]

cells[22]['source'] = new_celda6
cells[22]['outputs'] = []
print('Celda 6 (procesamiento) reescrita: solo Q1 2026 real, sin Proxy')

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Listo.')
print('  - base: 2023-2025 (Cards, ITT Global, Radar)')
print('  - corr_trim: 2023 Q1-Q4, 2024 Q1-Q4, 2025 Q1-Q4, 2026 Q1 (Heatmaps, Barras)')
print('  - Sin Proxy. Solo datos reales.')
print('  - Heatmaps/Barras necesitan 4to color naranja para 2026')
