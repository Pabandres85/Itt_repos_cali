# =============================================================================
# Celda 6 — Procesamiento de indicadores (con deduplicación y Proxy 2026)
# =============================================================================
# Copiar este contenido completo en la Celda 6 del notebook
# 04_itt_pulmon_oriente_2026_v2.ipynb en Colab
#
# ESTRATEGIA DE DEDUPLICACION:
# Un registro se considera duplicado si tiene la MISMA FECHA y la MISMA
# COORDENADA (lon, lat) que otro registro.
#
# VALORES PROXY 2026:
# Para Q2, Q3 y Q4 de 2026 se generan valores estimados a partir del
# promedio historico trimestral de 2023-2025. Estos valores se marcan
# con doble asterisco (**) en las salidas.
# =============================================================================

FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'fecha_hecho', 'fecha', 'FECHA_HECH']

def pick_col(df, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

def dedup_raw(raw, nombre):
    """Deduplica features de un GeoJSON por coordenada (para datos estaticos sin fecha)."""
    registros = []
    for feat in raw['features']:
        row = dict(feat['properties'])
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
    cols_dedup = [c for c in df.columns]
    df = df.drop_duplicates(subset=cols_dedup, keep='first').reset_index(drop=True)
    n_unicos = len(df)
    n_dupes = n_total - n_unicos
    print(f'  {nombre:15s}: {n_total:>5} total -> {n_unicos:>5} unicos ({n_dupes} duplicados eliminados)')
    return df, n_dupes

def procesar(raw, nombre):
    """Procesa GeoJSON: extrae properties + coordenadas, deduplica por FECHA + COORDENADA."""
    registros = []
    for feat in raw['features']:
        row = dict(feat['properties'])
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

    col_fecha = pick_col(df, FECHA_CANDIDATES)
    if col_fecha is None:
        raise ValueError(f'No se encontro columna de fecha en {nombre}')

    # Deduplicar por FECHA + COORDENADA
    df['_fecha_str'] = df[col_fecha].astype(str).str.strip()
    cols_dedup = ['_fecha_str', '_lon', '_lat']
    df = df.drop_duplicates(subset=cols_dedup, keep='first').reset_index(drop=True)
    n_unicos = len(df)
    n_dupes = n_total - n_unicos
    print(f'  {nombre:15s}: {n_total:>5} total -> {n_unicos:>5} unicos ({n_dupes} duplicados eliminados)')

    df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')
    df['año'] = df['_fecha'].dt.year
    df['trimestre'] = df['_fecha'].dt.quarter
    df = df.dropna(subset=['año'])
    df['año'] = df['año'].astype(int)
    return df[df['año'].isin(ANIOS)].copy()

def agg_anual(df):
    return df.groupby('año').size().reindex(ANIOS, fill_value=0)

def agg_trim(df):
    serie = df.groupby(['año','trimestre']).size()
    for anio in ANIOS:
        trims = [1,2,3,4] if anio < 2026 else [1]
        for trim in trims:
            if (anio, trim) not in serie.index:
                serie.loc[(anio, trim)] = 0
    return serie

# --- Deduplicar datos de indicadores ---
print('Deduplicacion de registros (por fecha + coordenada):')
print('='*60)
df_hom = procesar(raw_hom, 'Homicidios')
df_hur = procesar(raw_hur, 'Hurtos')
df_vif = procesar(raw_vif, 'VIF')

if raw_comp['features']:
    df_comp = procesar(raw_comp, 'Comparendos')
    df_rin = df_comp[df_comp['agrupado'].astype(str).str.upper().str.startswith('RI')].copy()
else:
    df_rin = pd.DataFrame(columns=['año', 'trimestre'])
print(f'  Rinas filtradas: {len(df_rin)} registros')

# --- Deduplicar datos estaticos ---
print()
print('Datos estaticos (deduplicados):')
df_arb, _ = dedup_raw(raw_arb, 'Arboles') if raw_arb['features'] else (pd.DataFrame(), 0)
df_sed, _ = dedup_raw(raw_sed, 'Sedes Educ') if raw_sed['features'] else (pd.DataFrame(), 0)
df_cai, _ = dedup_raw(raw_cai, 'CAI/MECAL') if raw_cai['features'] else (pd.DataFrame(), 0)
print('='*60)

# --- Tabla anual ---
base = pd.DataFrame({'año': ANIOS})
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:
    base[nombre] = agg_anual(df_src).values

# --- Tabla trimestral ---
idx_t = pd.MultiIndex.from_product([ANIOS,[1,2,3,4]], names=['año','trimestre'])
corr_trim = pd.DataFrame(index=idx_t).reset_index()
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:
    ser = agg_trim(df_src).reset_index()
    ser.columns = ['año','trimestre',nombre]
    corr_trim = corr_trim.merge(ser, on=['año','trimestre'], how='left')
corr_trim = corr_trim.fillna(0)

# =============================================================================
# VALORES PROXY PARA Q2, Q3, Q4 DE 2026
# Metodologia: Promedio historico trimestral de 2023-2025
# Nota: Los valores Proxy se marcan con ** en las salidas
# =============================================================================
print()
print('='*60)
print('GENERACION DE VALORES PROXY — 2026 Q2, Q3, Q4')
print('Metodo: Promedio historico trimestral 2023-2025')
print('='*60)

# Calcular promedios historicos por trimestre (solo años 2023-2025)
historico = corr_trim[corr_trim['año'].isin([2023, 2024, 2025])]
indicadores = ['homicidios', 'hurtos', 'vif', 'rinas']

proxy_values = {}
for trim in [2, 3, 4]:
    trim_hist = historico[historico['trimestre'] == trim]
    proxy_values[trim] = {}
    for ind in indicadores:
        promedio = trim_hist[ind].mean()
        proxy_values[trim][ind] = round(promedio, 1)

# Aplicar Proxy a la tabla trimestral
for trim in [2, 3, 4]:
    mask = (corr_trim['año'] == 2026) & (corr_trim['trimestre'] == trim)
    for ind in indicadores:
        corr_trim.loc[mask, ind] = proxy_values[trim][ind]

# Marcar cuales son proxy
corr_trim['es_proxy'] = False
corr_trim.loc[(corr_trim['año'] == 2026) & (corr_trim['trimestre'].isin([2,3,4])), 'es_proxy'] = True

# Recalcular anual 2026 incluyendo Proxy
for ind in indicadores:
    total_2026 = corr_trim[corr_trim['año'] == 2026][ind].sum()
    base.loc[base['año'] == 2026, ind] = total_2026

# Mostrar Proxy generados
print()
print('Valores Proxy generados:')
print(f'  {"Indicador":15s} {"Q2 2026**":>12s} {"Q3 2026**":>12s} {"Q4 2026**":>12s}')
print(f'  {"-"*15} {"-"*12} {"-"*12} {"-"*12}')
for ind in indicadores:
    q2 = proxy_values[2][ind]
    q3 = proxy_values[3][ind]
    q4 = proxy_values[4][ind]
    print(f'  {ind:15s} {q2:>10.1f}** {q3:>10.1f}** {q4:>10.1f}**')

print()
print('='*60)
print('Conteo anual (con Proxy 2026):')
print(base.to_string(index=False))
print()
print('Conteo trimestral (con Proxy 2026 Q2-Q4 marcados **):')
# Mostrar con marcador **
for _, row in corr_trim.iterrows():
    marca = '**' if row['es_proxy'] else '  '
    print(f"  {int(row['año'])}  Q{int(row['trimestre'])}  "
          f"hom={row['homicidios']:>6.1f}{marca}  "
          f"hur={row['hurtos']:>7.1f}{marca}  "
          f"vif={row['vif']:>6.1f}{marca}  "
          f"rin={row['rinas']:>6.1f}{marca}")

print()
print('NOTA METODOLOGICA:')
print('Los valores correspondientes a los trimestres Q2, Q3 y Q4 del año 2026')
print('fueron estimados mediante valores Proxy calculados a partir de la linea')
print('base historica de los años 2023-2025, con el fin de normalizar la')
print('informacion y garantizar comparabilidad estadistica y visual en el analisis.')
print('Los valores Proxy se identifican con doble asterisco (**).')
