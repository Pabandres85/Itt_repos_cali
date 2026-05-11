# =============================================================================
# Celda 6 — Procesamiento de indicadores (con deduplicación)
# =============================================================================
# Copiar este contenido completo en la Celda 6 del notebook
# 04_itt_pulmon_oriente_2026_v2.ipynb en Colab
# =============================================================================

FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'fecha_hecho', 'fecha', 'FECHA_HECH']

def pick_col(df, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

def procesar(raw, nombre):
    """Procesa GeoJSON: extrae properties + coordenadas, elimina duplicados exactos."""
    registros = []
    for feat in raw['features']:
        row = dict(feat['properties'])
        # Extraer coordenadas para detectar duplicados espaciales
        if feat.get('geometry') and feat['geometry'].get('coordinates'):
            coords = feat['geometry']['coordinates']
            row['_lon'] = coords[0]
            row['_lat'] = coords[1]
        elif 'x' in row and 'y' in row:
            row['_lon'] = row['x']
            row['_lat'] = row['y']
        else:
            row['_lon'] = None
            row['_lat'] = None
        registros.append(row)
    
    df = pd.DataFrame(registros)
    n_total = len(df)
    
    # Eliminar duplicados: mismos atributos + misma coordenada
    cols_dedup = [c for c in df.columns if c not in ['_lon', '_lat']]
    cols_dedup_con_coords = cols_dedup + ['_lon', '_lat']
    df = df.drop_duplicates(subset=cols_dedup_con_coords, keep='first').reset_index(drop=True)
    n_unicos = len(df)
    n_dupes = n_total - n_unicos
    
    print(f'  {nombre:15s}: {n_total:>5} total -> {n_unicos:>5} unicos ({n_dupes} duplicados eliminados)')
    
    # Procesar fecha
    col_fecha = pick_col(df, FECHA_CANDIDATES)
    if col_fecha is None:
        raise ValueError(f'No se encontro columna de fecha en {nombre}')
    df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')
    df['año'] = df['_fecha'].dt.year
    df['trimestre'] = df['_fecha'].dt.quarter
    df = df.dropna(subset=['año'])
    df['año'] = df['año'].astype(int)
    return df[df['año'].isin(ANIOS)].copy()

def agg_anual(df):
    return df.groupby('año').size().reindex(ANIOS, fill_value=0)

# Trimestres con datos reales (2026 solo tiene T1)
def agg_trim(df):
    serie = df.groupby(['año','trimestre']).size()
    for anio in ANIOS:
        trims = [1,2,3,4] if anio < 2026 else [1]
        for trim in trims:
            if (anio, trim) not in serie.index:
                serie.loc[(anio, trim)] = 0
    return serie

print('Deduplicacion de registros:')
print('='*60)
df_hom = procesar(raw_hom, 'Homicidios')
df_hur = procesar(raw_hur, 'Hurtos')
df_vif = procesar(raw_vif, 'VIF')

# Rinas: filtrar de comparendos donde agrupado empieza con 'RI'
if raw_comp['features']:
    df_comp = procesar(raw_comp, 'Comparendos')
    df_rin = df_comp[df_comp['agrupado'].astype(str).str.upper().str.startswith('RI')].copy()
else:
    df_rin = pd.DataFrame(columns=['año', 'trimestre'])
print(f'  Rinas filtradas: {len(df_rin)} registros')
print('='*60)

# Tabla anual
base = pd.DataFrame({'año': ANIOS})
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:
    base[nombre] = agg_anual(df_src).values

# Tabla trimestral
idx_t = pd.MultiIndex.from_product([ANIOS,[1,2,3,4]], names=['año','trimestre'])
corr_trim = pd.DataFrame(index=idx_t).reset_index()
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:
    ser = agg_trim(df_src).reset_index()
    ser.columns = ['año','trimestre',nombre]
    corr_trim = corr_trim.merge(ser, on=['año','trimestre'], how='left')
corr_trim = corr_trim.fillna(0)

print()
print('Conteo anual (valores unicos):')
print(base.to_string(index=False))
print()
print('Conteo trimestral (valores unicos):')
print(corr_trim.to_string(index=False))
