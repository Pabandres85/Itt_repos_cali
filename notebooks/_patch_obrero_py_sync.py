"""Sync 03_itt_barrio_obrero.py with Colab notebook logic."""
from pathlib import Path

p = Path(__file__).parent.parent / 'notebooks_py' / '03_itt_barrio_obrero.py'
content = p.read_text(encoding='utf-8')

# 1. Replace procesar() with auto-detect version
old = """def procesar(raw, col_fecha, filtro=None, filtro_col=None):
    df = pd.DataFrame([f['properties'] for f in raw['features']])
    if filtro and filtro_col:
        df = df[df[filtro_col] == filtro].copy()
    df['_fecha'] = pd.to_datetime(df[col_fecha])
    df['año'] = df['_fecha'].dt.year
    df['trimestre'] = df['_fecha'].dt.quarter
    return df[df['año'].isin(ANIOS)].copy()"""

new = """FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'FECHA_HECH', 'Fecha', 'fecha']

def pick_col(df, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns: return cand
        if cand.lower() in cols_lower: return cols_lower[cand.lower()]
    return None

def procesar(raw, nombre, filtro=None, filtro_col=None, startswith=False):
    df = pd.DataFrame([f['properties'] for f in raw['features']])
    if filtro and filtro_col:
        if startswith:
            df = df[df[filtro_col].astype(str).str.upper().str.startswith(filtro)].copy()
        else:
            df = df[df[filtro_col] == filtro].copy()
    col_fecha = pick_col(df, FECHA_CANDIDATES)
    if col_fecha is None:
        raise ValueError(f'No se encontro columna de fecha en {nombre}. Columnas: {list(df.columns)[:10]}')
    df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')
    df['año'] = df['_fecha'].dt.year
    df['trimestre'] = df['_fecha'].dt.quarter
    df = df.dropna(subset=['año'])
    df['año'] = df['año'].astype(int)
    return df[df['año'].isin(ANIOS)].copy()"""

content = content.replace(old, new)

# 2. Replace procesar() calls
content = content.replace("df_hom = procesar(raw_hom, 'FECHA_HECH')", "df_hom = procesar(raw_hom, 'Homicidios')")
content = content.replace("df_hur = procesar(raw_hur, 'FECHA_HECH')", "df_hur = procesar(raw_hur, 'Hurtos')")
content = content.replace("df_sin = procesar(raw_sin, 'Fecha')", "df_sin = procesar(raw_sin, 'Siniestros')")
content = content.replace("df_vif = procesar(raw_vif, 'FECHA_HECH')", "df_vif = procesar(raw_vif, 'VIF')")
content = content.replace("df_rin = procesar(raw_comp, 'fecha_hech', filtro='RIÑAS', filtro_col='agrupado')", "df_rin = procesar(raw_comp, 'Comparendos', filtro='RI', filtro_col='agrupado', startswith=True)")

# 3. Replace heatmaps with '-' annotation logic
old_heatmap = "    sns.heatmap(pivot, annot=True, fmt='.0f', cmap=cmap_h, linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})"
new_heatmap = """    annot_arr = pivot.copy().astype(object)
    for c in annot_arr.columns:
        for r in annot_arr.index:
            val = pivot.loc[r, c]
            if pd.isna(val) or (r == 2026 and c != 'Q1'):
                annot_arr.loc[r, c] = '-'
            else:
                annot_arr.loc[r, c] = f'{val:.0f}'
    pivot_plot = pivot.fillna(0)
    sns.heatmap(pivot_plot, annot=annot_arr.values, fmt='', cmap=cmap_h, linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})"""
content = content.replace(old_heatmap, new_heatmap)

# RdPu heatmap
old_rdpu = "    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdPu', linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})"
new_rdpu = """    annot_arr = pivot.copy().astype(object)
    for c in annot_arr.columns:
        for r in annot_arr.index:
            val = pivot.loc[r, c]
            if pd.isna(val) or (r == 2026 and c != 'Q1'):
                annot_arr.loc[r, c] = '-'
            else:
                annot_arr.loc[r, c] = f'{val:.0f}'
    pivot_plot = pivot.fillna(0)
    sns.heatmap(pivot_plot, annot=annot_arr.values, fmt='', cmap='RdPu', linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})"""
content = content.replace(old_rdpu, new_rdpu)

p.write_text(content, encoding='utf-8')
print('03_itt_barrio_obrero.py sincronizado con Colab:')
print('  - procesar() con pick_col() auto-deteccion')
print('  - Rinas con startswith(RI)')
print('  - Heatmaps con - para Q2-Q4 2026')
