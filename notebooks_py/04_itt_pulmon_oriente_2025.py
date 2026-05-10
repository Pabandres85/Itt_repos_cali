"""
ITT Pulmon de Oriente — Cali
Indice de Transformacion Territorial · 5 Dimensiones · 2023-2026

Zona: Pulmon de Oriente (zona agregada, multiples comunas)
Normalizacion: ref_min / ref_max fijos por indicador (trimestral)
Dimensiones: Seguridad (30%) · Movilidad (25% ref) · Entorno Urbano (20% ref) · Educ y Des (13% ref) · Cohesion Social (12%)
Periodo: 2023 - 2026 (2026 solo T1 disponible)

Datos reales: Homicidios, Hurtos, VIF, Comparendos/Rinas (ZIP consolidado 2026)
Referentes provisionales: Movilidad=35.0, Entorno Urbano=39.2, Educacion=54.9, Vulnerabilidad=54.1

Ejecutar con:
    uv run notebooks_py/04_itt_pulmon_oriente_2025.py
"""
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas>=2.0",
#     "numpy>=1.23",
#     "geopandas>=0.12",
#     "matplotlib>=3.6",
#     "seaborn>=0.12",
#     "openpyxl>=3.0",
#     "pyproj>=3.4",
#     "shapely>=2.0",
# ]
# ///

import json, os, re, warnings, zipfile
from pathlib import Path

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════
# Configuracion visual
# ══════════════════════════════════════════════════════════
C_SEG = '#1B4F8A'; C_MOV = '#E8852A'; C_COH = '#7B1FA2'; C_ITT = '#2E7D32'; BG = '#F4F6F9'
NIVEL_COLORS = {'Emergencia': '#E53935', 'Consolidacion': '#FB8C00', 'Avance': '#43A047', 'Transformacion': '#1E88E5'}
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': 'white', 'font.family': 'DejaVu Sans',
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.alpha': 0.3
})

# ══════════════════════════════════════════════════════════
# Rutas
# ══════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DATA_DIR = PROJECT_ROOT / 'data' / 'itt_pulmon_oriente'
ZIP_2025 = DATA_DIR / 'Pulmon_De_Oriente_2025.zip'
ZIP_2026 = DATA_DIR / 'Pulmon_De_Oriente_2026.zip'
EXTRACT_2025 = DATA_DIR / 'Pulmon_De_Oriente_2025'
EXTRACT_2026 = DATA_DIR / 'Pulmon_De_Oriente_2026'

IMG_DIR = str(PROJECT_ROOT / 'outputs' / 'IMAGENES_POR_ITT' / 'itt_pulmon_oriente') + os.sep
os.makedirs(IMG_DIR, exist_ok=True)
print(f'Imagenes se guardaran en: {IMG_DIR}')

# ══════════════════════════════════════════════════════════
# Descompresion automatica
# ══════════════════════════════════════════════════════════
for zip_path, extract_dir in [(ZIP_2025, EXTRACT_2025), (ZIP_2026, EXTRACT_2026)]:
    if not extract_dir.exists() and zip_path.exists():
        print(f'Descomprimiendo {zip_path.name}...')
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(DATA_DIR)
        print('Listo.')

# ══════════════════════════════════════════════════════════
# Busqueda de archivos
# ══════════════════════════════════════════════════════════
def find_file(base_dir: Path, pattern: str) -> Path | None:
    regex = re.compile(pattern, re.IGNORECASE)
    for root, _dirs, files in os.walk(base_dir):
        for f in files:
            if regex.search(f) and f.lower().endswith('.geojson'):
                return Path(root) / f
    return None

# ZIP 2026 (consolidado): homicidios, hurtos, VIF, comparendos
path_homicidios = find_file(DATA_DIR, r'DATIC_homicidios.*Pulmon_O')
path_hurtos = find_file(DATA_DIR, r'DATIC_hurtos.*Pulmon_O')
path_vif = find_file(DATA_DIR, r'VIOLENCIA_INTRAFAMILIAR|DATIC_violencia_intrafamiliar')
path_comparendos = find_file(DATA_DIR, r'DATIC_comparendos.*Pulmon_O')

# Datos estaticos (poligono, arboles, sedes, CAI)
path_poligono = find_file(DATA_DIR, r'poligonos\.geojson')
path_arboles = find_file(DATA_DIR, r'ARBOLES')
path_sedes = find_file(DATA_DIR, r'Sedes_educativas')
path_cai = find_file(DATA_DIR, r'CAI_MECAL')

print('\nArchivos encontrados:')
for nombre, path in [('Homicidios', path_homicidios), ('Hurtos', path_hurtos),
                     ('VIF', path_vif), ('Comparendos', path_comparendos),
                     ('Poligono', path_poligono), ('Arboles', path_arboles),
                     ('Sedes', path_sedes), ('CAI', path_cai)]:
    print(f'  {nombre:12s}: {"OK" if path else "NO ENCONTRADO"} — {path}')

# Validar minimos
for nombre, path in [('Homicidios', path_homicidios), ('Hurtos', path_hurtos), ('VIF', path_vif)]:
    if path is None:
        raise FileNotFoundError(f'No se encontro archivo para {nombre}')

# ══════════════════════════════════════════════════════════
# Parametros
# ══════════════════════════════════════════════════════════
ANIOS = [2023, 2024, 2025, 2026]
ZONA_NOMBRE = 'Pulmon de Oriente — Cali'

PESOS = {
    'Seguridad': 0.30, 'Movilidad': 0.25,
    'EntornoU': 0.20, 'EducDes': 0.13, 'Cohesion': 0.12,
}

# REFS trimestrales para zona grande (>100K hab) — de la guia metodologica seccion 4.1
REFS = {
    'homicidios':     (5,   50,  True, 'Homicidios trimestrales'),
    'hurtos':         (200, 450, True, 'Hurtos trimestrales'),
    'vif':            (60,  200, True, 'VIF trimestral'),
    'rinas':          (20,  160, True, 'Rinas trimestral'),
}

# Trimestres con datos reales (2026 solo tiene T1)
TRIM_CON_DATOS = {2023: [1,2,3,4], 2024: [1,2,3,4], 2025: [1,2,3,4], 2026: [1]}

# Referentes provisionales (dimensiones sin datos propios completos)
REF_MOVILIDAD = 35.0       # Score Movilidad Pulmon de Oriente T4-2025
REF_ENTORNO_U = 39.2       # Score Entorno Urbano
REF_EDUC_DES = 54.9        # Score Educacion y Desarrollo
REF_VULNERABILIDAD = 54.1  # Concentracion vulnerabilidad (indicador Cohesion)

print(f'\nPeriodo: {ANIOS[0]}-{ANIOS[-1]}')
print('Pesos:', ' | '.join(f'{k}={v:.0%}' for k, v in PESOS.items()))
print(f'Referentes: Movilidad={REF_MOVILIDAD}, EntornoU={REF_ENTORNO_U}, EducDes={REF_EDUC_DES}')

# ══════════════════════════════════════════════════════════
# Carga de datos
# ══════════════════════════════════════════════════════════
def load_gj(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

raw_hom = load_gj(path_homicidios)
raw_hur = load_gj(path_hurtos)
raw_vif = load_gj(path_vif)
raw_comp = load_gj(path_comparendos) if path_comparendos else {'features': []}

if path_poligono:
    gdf_zona = gpd.read_file(path_poligono)
    gdf_zona_wgs = gdf_zona.to_crs('EPSG:4326')

print('\nRegistros cargados:')
for n, r in [('Homicidios', raw_hom), ('Hurtos', raw_hur), ('VIF', raw_vif)]:
    print(f'  {n:12s}: {len(r["features"]):>6} registros')

# ══════════════════════════════════════════════════════════
# Procesamiento de indicadores
# ══════════════════════════════════════════════════════════
FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'fecha_hecho', 'fecha', 'FECHA_HECH']

def pick_col(df, candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

def procesar(raw, nombre):
    df = pd.DataFrame([f['properties'] for f in raw['features']])
    # Eliminar duplicados exactos
    n_antes = len(df)
    df = df.drop_duplicates()
    n_dupes = n_antes - len(df)
    if n_dupes > 0:
        print(f'  {nombre}: {n_dupes} duplicados eliminados')
    col_fecha = pick_col(df, FECHA_CANDIDATES)
    if col_fecha is None:
        raise ValueError(f'No se encontro columna de fecha en {nombre}. Columnas: {list(df.columns)[:15]}')
    df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')
    df['año'] = df['_fecha'].dt.year
    df['trimestre'] = df['_fecha'].dt.quarter
    df = df.dropna(subset=['año'])
    df['año'] = df['año'].astype(int)
    return df[df['año'].isin(ANIOS)].copy()

def agg_anual(df):
    return df.groupby('año').size().reindex(ANIOS, fill_value=0)

def agg_trim(df):
    idx = pd.MultiIndex.from_product([ANIOS, [1, 2, 3, 4]], names=['año', 'trimestre'])
    serie = df.groupby(['año', 'trimestre']).size().reindex(idx)
    # Solo rellenar con 0 los trimestres que SI tienen datos
    for anio in ANIOS:
        for trim in TRIM_CON_DATOS.get(anio, []):
            if pd.isna(serie.loc[(anio, trim)]):
                serie.loc[(anio, trim)] = 0
    return serie

df_hom = procesar(raw_hom, 'Homicidios')
df_hur = procesar(raw_hur, 'Hurtos')
df_vif = procesar(raw_vif, 'VIF')

# Rinas: filtrar de comparendos donde agrupado empieza con 'RI'
if raw_comp['features']:
    df_comp = procesar(raw_comp, 'Comparendos')
    df_rin = df_comp[df_comp['agrupado'].astype(str).str.upper().str.startswith('RI')].copy()
else:
    df_rin = pd.DataFrame(columns=['año', 'trimestre'])
print(f'Rinas filtradas: {len(df_rin)} registros')

# Tabla trimestral
idx_t = pd.MultiIndex.from_product([ANIOS, [1, 2, 3, 4]], names=['año', 'trimestre'])
corr_trim = pd.DataFrame(index=idx_t).reset_index()
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:
    ser = agg_trim(df_src).reset_index()
    ser.columns = ['año', 'trimestre', nombre]
    corr_trim = corr_trim.merge(ser, on=['año', 'trimestre'], how='left').fillna({nombre: 0})
corr_trim['periodo'] = corr_trim['año'].astype(str) + '-Q' + corr_trim['trimestre'].astype(str)

# Tabla anual
base = pd.DataFrame({'año': ANIOS})
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('vif', df_vif), ('rinas', df_rin)]:
    base[nombre] = agg_anual(df_src).values

print('\nIndicadores anuales:')
print(base.to_string(index=False))
print('\nIndicadores trimestrales:')
print(corr_trim.to_string(index=False))

# ══════════════════════════════════════════════════════════
# Normalizacion trimestral con ref_min / ref_max
# ══════════════════════════════════════════════════════════
def score_ref(valor, ref_min, ref_max, inverso):
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw

# Scores trimestrales
for ind, (rmin, rmax, inv, desc) in REFS.items():
    corr_trim[f'score_{ind}'] = corr_trim[ind].apply(lambda v, rm=rmin, rx=rmax, i=inv: score_ref(v, rm, rx, i))

corr_trim['score_seguridad'] = (corr_trim['score_homicidios'] + corr_trim['score_hurtos']) / 2
corr_trim['score_cohesion'] = (corr_trim['score_vif'] + corr_trim['score_rinas'] + REF_VULNERABILIDAD) / 3
corr_trim['score_movilidad'] = REF_MOVILIDAD
corr_trim['score_entorno_u'] = REF_ENTORNO_U
corr_trim['score_educ_des'] = REF_EDUC_DES

corr_trim['ITT'] = (
    PESOS['Seguridad'] * corr_trim['score_seguridad'] +
    PESOS['Movilidad'] * corr_trim['score_movilidad'] +
    PESOS['EntornoU'] * corr_trim['score_entorno_u'] +
    PESOS['EducDes'] * corr_trim['score_educ_des'] +
    PESOS['Cohesion'] * corr_trim['score_cohesion']
)

def clasificar(v):
    if v < 40: return 'Emergencia'
    elif v < 60: return 'Consolidacion'
    elif v < 80: return 'Avance'
    else: return 'Transformacion'

corr_trim['nivel'] = corr_trim['ITT'].apply(clasificar)

# Scores anuales (promedio de trimestres)
base_scores = corr_trim.groupby('año')[['score_seguridad', 'score_cohesion', 'score_movilidad',
                                         'score_entorno_u', 'score_educ_des', 'ITT']].mean().reset_index()
base_scores['nivel'] = base_scores['ITT'].apply(clasificar)

print('\nScores trimestrales (muestra ultimos 4):')
print(corr_trim[['periodo', 'score_seguridad', 'score_cohesion', 'ITT', 'nivel']].tail(4).round(1).to_string(index=False))
print('\nScores anuales (promedio trimestral):')
print(base_scores.round(1).to_string(index=False))

# ══════════════════════════════════════════════════════════
# Cards de metricas clave
# ══════════════════════════════════════════════════════════
def safe_pct(new, old):
    if old == 0: return 0.0
    return (new - old) / old * 100

def arrow(pct, inv=True):
    if abs(pct) < 1: return 'Sin cambio', 'gray'
    if inv: return (f'V {abs(pct):.1f}%', '#2E7D32') if pct < 0 else (f'A {abs(pct):.1f}%', '#C62828')
    else: return (f'A {abs(pct):.1f}%', '#2E7D32') if pct > 0 else (f'V {abs(pct):.1f}%', '#C62828')

año_ini, año_ant, año_ult = ANIOS[0], ANIOS[-2], ANIOS[-1]
d_ini = base_scores[base_scores['año'] == año_ini].iloc[0]
d_ant = base_scores[base_scores['año'] == año_ant].iloc[0]
d_ult = base_scores[base_scores['año'] == año_ult].iloc[0]

cards = [
    ('Homicidios (anual)', int(base.loc[base['año'] == año_ini, 'homicidios'].iloc[0]), int(base.loc[base['año'] == año_ant, 'homicidios'].iloc[0]), int(base.loc[base['año'] == año_ult, 'homicidios'].iloc[0]), True),
    ('Hurtos (anual)', int(base.loc[base['año'] == año_ini, 'hurtos'].iloc[0]), int(base.loc[base['año'] == año_ant, 'hurtos'].iloc[0]), int(base.loc[base['año'] == año_ult, 'hurtos'].iloc[0]), True),
    ('VIF (anual)', int(base.loc[base['año'] == año_ini, 'vif'].iloc[0]), int(base.loc[base['año'] == año_ant, 'vif'].iloc[0]), int(base.loc[base['año'] == año_ult, 'vif'].iloc[0]), True),
    ('Score Seguridad', d_ini['score_seguridad'], d_ant['score_seguridad'], d_ult['score_seguridad'], False),
    ('Score Cohesion', d_ini['score_cohesion'], d_ant['score_cohesion'], d_ult['score_cohesion'], False),
    ('ITT Global', d_ini['ITT'], d_ant['ITT'], d_ult['ITT'], False),
]

fig, axes = plt.subplots(2, 3, figsize=(16, 7), facecolor=BG)
fig.suptitle(f'ITT Pulmon de Oriente — Metricas Clave | {año_ini}-{año_ult}', fontsize=14, fontweight='bold', color='#1B2631', y=0.98)
for i, (titulo, v_ini, v_ant, v_ult, inv) in enumerate(cards):
    ax = axes[i // 3][i % 3]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    rect = mpatches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle='round,pad=0.02', linewidth=1.5, edgecolor='#DEE2E6', facecolor='white')
    ax.add_patch(rect)
    ax.text(0.5, 0.85, titulo, ha='center', va='center', fontsize=9, color='#6C757D', fontweight='bold')
    val_d = f'{v_ult:.1f}' if isinstance(v_ult, float) else str(v_ult)
    ax.text(0.5, 0.60, val_d, ha='center', va='center', fontsize=19, fontweight='bold', color='#1B2631')
    pct1 = safe_pct(v_ult, v_ant)
    ar1, col1 = arrow(pct1, inv)
    ax.text(0.5, 0.38, f'{año_ult} vs {año_ant}: {ar1}', ha='center', fontsize=8, color=col1, fontweight='bold')
    pct2 = safe_pct(v_ult, v_ini)
    ar2, col2 = arrow(pct2, inv)
    ax.text(0.5, 0.22, f'vs {año_ini}: {ar2}', ha='center', fontsize=7.5, color=col2)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(IMG_DIR + 'itt_pulmon_cards.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Heatmap Seguridad trimestral
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)
fig.suptitle('Dimension Seguridad — Heatmap Trimestral | Pulmon de Oriente', fontsize=13, fontweight='bold', color='#1B2631')
for ax, col, titulo_h, cmap_h in [(axes[0], 'homicidios', 'Homicidios', 'Blues'), (axes[1], 'hurtos', 'Hurtos', 'Oranges')]:
    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)
    pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap=cmap_h, linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})
    ax.set_title(titulo_h, fontweight='bold', pad=8); ax.set_ylabel(''); ax.set_xlabel('')
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_pulmon_heatmap_seg.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Heatmap Cohesion (VIF) trimestral
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
fig.suptitle('Dimension Cohesion Social — VIF Trimestral | Pulmon de Oriente', fontsize=13, fontweight='bold', color='#1B2631')
pivot = corr_trim.pivot(index='año', columns='trimestre', values='vif')
pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdPu', linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})
ax.set_title('VIF — Violencia Intrafamiliar', fontweight='bold', pad=8); ax.set_ylabel(''); ax.set_xlabel('')
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_pulmon_heatmap_vif.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Evolucion trimestral Seguridad (barras)
# ══════════════════════════════════════════════════════════
x = np.arange(4); n = len(ANIOS); w = 0.8 / n
COLORES = ['#42A5F5', '#1B4F8A', '#E53935', '#FF6F00']

fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)
fig.suptitle('Dimension Seguridad - Evolucion Trimestral | Pulmon de Oriente', fontsize=13, fontweight='bold', color='#1B2631')
for ax, col, tp in [(axes[0], 'homicidios', 'Homicidios'), (axes[1], 'hurtos', 'Hurtos')]:
    for idx, año in enumerate(ANIOS):
        vals = corr_trim[corr_trim['año'] == año][col].values
        offset = (idx - n / 2 + 0.5) * w
        b = ax.bar(x + offset, vals, w, label=str(año), color=COLORES[idx % 3], alpha=0.85, edgecolor='white')
        for bar in b:
            h = bar.get_height()
            if h > 0: ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')
    ax.set_title(tp, fontweight='bold', pad=10); ax.set_xticks(x); ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_pulmon_seg_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# ITT Global y composicion
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)
fig.suptitle('ITT Global — Pulmon de Oriente', fontsize=13, fontweight='bold', color='#1B2631')
COLORES_ITT = ['#42A5F5', '#2E7D32', '#E53935', '#FF6F00']
band_configs = [(0, 40, '#FFCDD2', 'Emergencia'), (40, 60, '#FFE0B2', 'Consolidacion'), (60, 80, '#C8E6C9', 'Avance'), (80, 100, '#BBDEFB', 'Transformacion')]

ax1 = axes[0]
bars = ax1.bar(ANIOS, base_scores['ITT'], color=COLORES_ITT, alpha=0.85, edgecolor='white', width=0.5)
for bar, val, nivel in zip(bars, base_scores['ITT'], base_scores['nivel']):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 1, f'{val:.1f}\n{nivel}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=NIVEL_COLORS.get(nivel, '#1B2631'))
for y0, y1, c, l in band_configs: ax1.axhspan(y0, y1, alpha=0.15, color=c)
ax1.set_title('ITT por Ano (promedio trimestral)', fontweight='bold', pad=10); ax1.set_ylim(0, 115); ax1.set_ylabel('ITT (0-100)'); ax1.set_xticks(ANIOS)

ax2 = axes[1]
dims = ['score_seguridad', 'score_movilidad', 'score_entorno_u', 'score_educ_des', 'score_cohesion']
dim_lbl = ['Seguridad', 'Movilidad (ref)', 'EntornoU (ref)', 'EducDes (ref)', 'Cohesion']
dim_p = [PESOS['Seguridad'], PESOS['Movilidad'], PESOS['EntornoU'], PESOS['EducDes'], PESOS['Cohesion']]
dim_c = [C_SEG, C_MOV, '#43A047', '#FB8C00', C_COH]
bottom = np.zeros(len(ANIOS))
for dim, lbl, peso, col in zip(dims, dim_lbl, dim_p, dim_c):
    vals = base_scores[dim].values * peso
    ax2.bar(ANIOS, vals, bottom=bottom, label=f'{lbl} ({peso:.0%})', color=col, alpha=0.8, edgecolor='white', width=0.5)
    bottom += vals
ax2.plot(ANIOS, base_scores['ITT'], 'D-', color='black', linewidth=2, markersize=8, label='ITT Total', zorder=5)
for y0, y1, c, l in band_configs: ax2.axhspan(y0, y1, alpha=0.1, color=c)
ax2.set_title('Composicion ITT', fontweight='bold', pad=10); ax2.set_ylim(0, 115); ax2.set_ylabel('Score ponderado'); ax2.set_xticks(ANIOS)
ax2.legend(loc='upper right', fontsize=7)
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_pulmon_global.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Radar ITT: 5 dimensiones
# ══════════════════════════════════════════════════════════
DIMS_LBL = ['Seguridad', 'Movilidad\n(ref)', 'Cohesion\nSocial', 'Entorno\nUrbano (ref)', 'Educ y\nDes (ref)']
N_DIMS = 5
angles = [i / N_DIMS * 2 * np.pi for i in range(N_DIMS)] + [0]
COLORES_R = ['#42A5F5', '#2E7D32', '#E53935', '#FF6F00']

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), facecolor=BG)
fig.suptitle('Radar ITT — Pulmon de Oriente | 5 Dimensiones', fontsize=13, fontweight='bold', color='#1B2631')
ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(DIMS_LBL, fontsize=9)
ax.set_ylim(0, 100); ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7, color='gray')
ax.yaxis.grid(True, linestyle='--', alpha=0.4)

for idx, año in enumerate(ANIOS):
    row = base_scores[base_scores['año'] == año].iloc[0]
    vals = [row['score_seguridad'], row['score_movilidad'], row['score_cohesion'], row['score_entorno_u'], row['score_educ_des']]
    vals_c = vals + [vals[0]]
    ax.plot(angles, vals_c, 'o-', color=COLORES_R[idx], linewidth=2, markersize=5, label=str(año))
    ax.fill(angles, vals_c, alpha=0.08, color=COLORES_R[idx])
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_pulmon_radar.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Exportar a Excel
# ══════════════════════════════════════════════════════════
EXPORT_PATH = IMG_DIR + 'ITT_Pulmon_Oriente_2025.xlsx'
with pd.ExcelWriter(EXPORT_PATH, engine='openpyxl') as writer:
    base_scores.round(2).to_excel(writer, sheet_name='ITT_Anual', index=False)
    corr_trim.round(2).to_excel(writer, sheet_name='Series_Trimestrales', index=False)
    base.to_excel(writer, sheet_name='Conteos_Anuales', index=False)

print(f'\nExportado: {EXPORT_PATH}')

# ══════════════════════════════════════════════════════════
# Resumen final
# ══════════════════════════════════════════════════════════
print('\n' + '=' * 50)
print('IMAGENES GENERADAS')
print('=' * 50)
png_files = [f for f in os.listdir(IMG_DIR) if f.endswith('.png')]
print(f'Total: {len(png_files)} imagenes en {IMG_DIR}')
for f in sorted(png_files):
    size_kb = os.path.getsize(os.path.join(IMG_DIR, f)) / 1024
    print(f'  OK  {f} ({size_kb:.1f} KB)')

print('\n' + '=' * 50)
print(f'ITT PULMON DE ORIENTE — {ANIOS[0]}-{ANIOS[-1]}')
print(f'Datos reales: Seguridad (homicidios, hurtos), Cohesion parcial (VIF)')
print(f'Referentes: Movilidad={REF_MOVILIDAD}, EntornoU={REF_ENTORNO_U}, EducDes={REF_EDUC_DES}')
print('=' * 50)
