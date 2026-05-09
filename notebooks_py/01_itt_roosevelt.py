"""
ITT Corredor Roosevelt — Cali
Indice de Transformacion Territorial · 5 Dimensiones · 2023-2025

Zona: Corredor Roosevelt — single buffer polygon (100m)
Normalizacion: ref_min / ref_max fijos por indicador (juicio experto)
Dimensiones: Seguridad (30%) · Movilidad (25%) · Entorno Urbano (20% ref) · Educ y Des (13% ref) · Cohesion Social (12%)
Periodo: 2023 - 2025

Ejecutar con:
    uv run notebooks_py/01_itt_roosevelt.py
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

import json, os, warnings, zipfile
from pathlib import Path

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
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
# Rutas — detectar raiz del proyecto
# ══════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Datos
DATA_DIR = PROJECT_ROOT / 'data' / 'itt_roosevelt'
GEOJSON_DIR = DATA_DIR / 'Roosevelt' / 'Geojson_Roosevelt'

# Si no estan descomprimidos, descomprimir
if not GEOJSON_DIR.exists():
    zip_path = DATA_DIR / 'Roosevelt.zip'
    if zip_path.exists():
        print(f'Descomprimiendo {zip_path}...')
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(DATA_DIR)
        print('Listo.')
    else:
        raise FileNotFoundError(f'No se encontro {zip_path}')

BASE = str(GEOJSON_DIR) + os.sep

# Carpeta de salida para imagenes
IMG_DIR = str(PROJECT_ROOT / 'outputs' / 'IMAGENES_POR_ITT' / 'itt_roosevelt') + os.sep
os.makedirs(IMG_DIR, exist_ok=True)
print(f'Imagenes se guardaran en: {IMG_DIR}')

# ══════════════════════════════════════════════════════════
# Parametros
# ══════════════════════════════════════════════════════════
PATHS = {
    'poligono':    BASE + 'Geojson_tramos_Roosevelt_Buffer_100.geojson',
    'homicidios':  BASE + 'HOMICIDIOS_2023_2025_Roosevelt.geojson',
    'hurtos':      BASE + 'HURTOS_2023_2025_Roosevelt.geojson',
    'siniestros':  BASE + 'BD_SINIESTROS_2023_2025_COMUNA_BARRIO_4326_Roosevelt.geojson',
    'vif':         BASE + 'VIOLENCIA_INTRAFAMILIAR_2023_2025_Roosevelt.geojson',
    'comparendos': BASE + 'COMPARENDOS_2023_2025_Roosevelt.geojson',
    'sedes':       BASE + 'Sedes_educativas_oficiales_Roosevelt.geojson',
}

ANIOS = [2023, 2024, 2025]
ZONA_NOMBRE = 'Corredor Roosevelt — Cali'

PESOS = {
    'Seguridad': 0.30, 'Movilidad': 0.25,
    'EntornoU': 0.20, 'EducDes': 0.13, 'Cohesion': 0.12,
}

REFS = {
    'homicidios':     (0,   8,   True, 'Homicidios anuales corredor'),
    'hurtos':         (120, 320, True, 'Hurtos anuales corredor'),
    'siniestralidad': (15,  40,  True, 'Siniestros viales anuales'),
    'lesionados':     (10,  35,  True, 'Accidentes con lesionados anuales'),
    'mortales':       (0,   4,   True, 'Accidentes mortales anuales'),
    'vif':            (4,   18,  True, 'VIF anual corredor'),
    'rinas':          (5,   25,  True, 'Rinas anual corredor'),
}

REF_ENTORNO_U = 39.2
REF_EDUC_DES = 54.9
REF_VULNERABILIDAD = 54.1

# Verificar archivos
print('\nVerificacion de archivos:')
for n, r in PATHS.items():
    e = os.path.exists(r)
    print(f'  {"OK" if e else "FALTA"}  {n}')

print(f'\nPeriodo: {ANIOS[0]}-{ANIOS[-1]}')
print('Pesos:', ' | '.join(f'{k}={v:.0%}' for k, v in PESOS.items()))

# ══════════════════════════════════════════════════════════
# Carga de datos
# ══════════════════════════════════════════════════════════
def load_gj(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

gdf_zona = gpd.read_file(PATHS['poligono'])
gdf_zona_wgs = gdf_zona.to_crs('EPSG:4326')

raw_hom = load_gj(PATHS['homicidios'])
raw_hur = load_gj(PATHS['hurtos'])
raw_sin = load_gj(PATHS['siniestros'])
raw_vif = load_gj(PATHS['vif'])
raw_comp = load_gj(PATHS['comparendos'])
raw_sed = load_gj(PATHS['sedes'])

print('\nRegistros cargados:')
for n, r in [('Homicidios', raw_hom), ('Hurtos', raw_hur), ('Siniestros', raw_sin),
             ('VIF', raw_vif), ('Comparendos', raw_comp), ('Sedes', raw_sed)]:
    print(f'  {n:15s}: {len(r["features"]):>4} registros')

# ══════════════════════════════════════════════════════════
# Procesamiento de indicadores
# ══════════════════════════════════════════════════════════
def procesar(raw, col_fecha, filtro=None, filtro_col=None):
    df = pd.DataFrame([f['properties'] for f in raw['features']])
    if filtro and filtro_col:
        df = df[df[filtro_col].astype(str).str.startswith(filtro)].copy()
    df['_fecha'] = pd.to_datetime(df[col_fecha])
    df['año'] = df['_fecha'].dt.year
    df['trimestre'] = df['_fecha'].dt.quarter
    return df[df['año'].isin(ANIOS)].copy()

def agg_anual(df):
    return df.groupby('año').size().reindex(ANIOS, fill_value=0)

def agg_trim(df):
    idx = pd.MultiIndex.from_product([ANIOS, [1, 2, 3, 4]], names=['año', 'trimestre'])
    return df.groupby(['año', 'trimestre']).size().reindex(idx, fill_value=0)

df_hom = procesar(raw_hom, 'FECHA_HECH')
df_hur = procesar(raw_hur, 'FECHA_HECH')
df_sin = procesar(raw_sin, 'Fecha')
df_les = df_sin[df_sin['Tipo_Confi'] == 'Lesiones'].copy()
df_mor = df_sin[df_sin['Tipo_Confi'] == 'Mortal'].copy()
df_vif = procesar(raw_vif, 'FECHA_HECH')
df_rin = procesar(raw_comp, 'fecha_hech', filtro='RI', filtro_col='agrupado')

# Tabla anual
base = pd.DataFrame({'año': ANIOS})
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('siniestralidad', df_sin),
                       ('lesionados', df_les), ('mortales', df_mor), ('vif', df_vif), ('rinas', df_rin)]:
    base[nombre] = agg_anual(df_src).values

# Tabla trimestral
idx_t = pd.MultiIndex.from_product([ANIOS, [1, 2, 3, 4]], names=['año', 'trimestre'])
corr_trim = pd.DataFrame(index=idx_t).reset_index()
for nombre, df_src in [('homicidios', df_hom), ('hurtos', df_hur), ('siniestralidad', df_sin),
                       ('lesionados', df_les), ('mortales', df_mor), ('vif', df_vif), ('rinas', df_rin)]:
    ser = agg_trim(df_src).reset_index()
    ser.columns = ['año', 'trimestre', nombre]
    corr_trim = corr_trim.merge(ser, on=['año', 'trimestre'], how='left').fillna({nombre: 0})
corr_trim['periodo'] = corr_trim['año'].astype(str) + '-Q' + corr_trim['trimestre'].astype(str)

print('\nIndicadores anuales:')
print(base.to_string(index=False))

# ══════════════════════════════════════════════════════════
# Normalizacion con ref_min / ref_max e ITT
# ══════════════════════════════════════════════════════════
def score_ref(valor, ref_min, ref_max, inverso):
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw

for ind, (rmin, rmax, inv, desc) in REFS.items():
    base[f'score_{ind}'] = base[ind].apply(lambda v, rm=rmin, rx=rmax, i=inv: score_ref(v, rm, rx, i))

base['score_seguridad'] = (base['score_homicidios'] + base['score_hurtos']) / 2
base['score_movilidad'] = (base['score_siniestralidad'] + base['score_lesionados'] + base['score_mortales']) / 3
base['score_cohesion'] = (base['score_vif'] + base['score_rinas'] + REF_VULNERABILIDAD) / 3
base['score_entorno_u'] = REF_ENTORNO_U
base['score_educ_des'] = REF_EDUC_DES

base['ITT'] = (
    PESOS['Seguridad'] * base['score_seguridad'] +
    PESOS['Movilidad'] * base['score_movilidad'] +
    PESOS['EntornoU'] * base['score_entorno_u'] +
    PESOS['EducDes'] * base['score_educ_des'] +
    PESOS['Cohesion'] * base['score_cohesion']
)

def clasificar(v):
    if v < 40: return 'Emergencia'
    elif v < 60: return 'Consolidacion'
    elif v < 80: return 'Avance'
    else: return 'Transformacion'

base['nivel'] = base['ITT'].apply(clasificar)

print(f'\nEntorno Urbano usado: {REF_ENTORNO_U} (referente fijo)')
print('\nScores por dimension e ITT:')
print(base[['año', 'score_seguridad', 'score_movilidad', 'score_cohesion', 'score_entorno_u', 'score_educ_des', 'ITT', 'nivel']].round(1).to_string(index=False))

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
d_ini = base[base['año'] == año_ini].iloc[0]
d_ant = base[base['año'] == año_ant].iloc[0]
d_ult = base[base['año'] == año_ult].iloc[0]

cards = [
    ('Homicidios', int(d_ini['homicidios']), int(d_ant['homicidios']), int(d_ult['homicidios']), True),
    ('Hurtos', int(d_ini['hurtos']), int(d_ant['hurtos']), int(d_ult['hurtos']), True),
    ('Siniestros', int(d_ini['siniestralidad']), int(d_ant['siniestralidad']), int(d_ult['siniestralidad']), True),
    ('VIF', int(d_ini['vif']), int(d_ant['vif']), int(d_ult['vif']), True),
    ('Rinas', int(d_ini['rinas']), int(d_ant['rinas']), int(d_ult['rinas']), True),
    ('Score Seguridad', d_ini['score_seguridad'], d_ant['score_seguridad'], d_ult['score_seguridad'], False),
    ('Score Movilidad', d_ini['score_movilidad'], d_ant['score_movilidad'], d_ult['score_movilidad'], False),
    ('ITT Global', d_ini['ITT'], d_ant['ITT'], d_ult['ITT'], False),
]

fig, axes = plt.subplots(2, 4, figsize=(18, 7), facecolor=BG)
fig.suptitle(f'ITT Roosevelt — Metricas Clave | {año_ini}-{año_ult}', fontsize=14, fontweight='bold', color='#1B2631', y=0.98)
for i, (titulo, v_ini, v_ant, v_ult, inv) in enumerate(cards):
    ax = axes[i // 4][i % 4]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
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
    ref = f'{v_ini:.1f}' if isinstance(v_ini, float) else str(v_ini)
    ax.text(0.5, 0.08, f'{año_ini}: {ref}', ha='center', fontsize=7, color='#ADB5BD')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(IMG_DIR + 'itt_roosevelt_cards.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Heatmaps trimestrales
# ══════════════════════════════════════════════════════════
# Seguridad
fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)
fig.suptitle('Dimension Seguridad — Heatmap Trimestral | Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
for ax, col, titulo_h, cmap_h in [(axes[0], 'homicidios', 'Homicidios', 'Blues'), (axes[1], 'hurtos', 'Hurtos', 'Blues')]:
    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)
    pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap=cmap_h, linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})
    ax.set_title(titulo_h, fontweight='bold', pad=8); ax.set_ylabel(''); ax.set_xlabel('')
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_heatmap_seg.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# Movilidad
fig, axes = plt.subplots(1, 3, figsize=(20, 4), facecolor=BG)
fig.suptitle('Dimension Movilidad — Heatmap Trimestral | Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
for ax, col, titulo_h, cmap_h in [(axes[0], 'siniestralidad', 'Siniestralidad Total', 'Oranges'), (axes[1], 'lesionados', 'Acc. con Lesionados', 'Oranges'), (axes[2], 'mortales', 'Acc. Mortales', 'Reds')]:
    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)
    pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap=cmap_h, linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})
    ax.set_title(titulo_h, fontweight='bold', pad=8); ax.set_ylabel(''); ax.set_xlabel('')
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_heatmap_mov.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# Cohesion
fig, axes = plt.subplots(1, 2, figsize=(16, 4), facecolor=BG)
fig.suptitle('Dimension Cohesion Social — Heatmap Trimestral | Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
for ax, col, titulo_h in [(axes[0], 'vif', 'VIF — Violencia Intrafamiliar'), (axes[1], 'rinas', 'Rinas / Conflictividad')]:
    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)
    pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdPu', linewidths=0.5, linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11}, cbar_kws={'label': 'Casos', 'shrink': 0.8})
    ax.set_title(titulo_h, fontweight='bold', pad=8); ax.set_ylabel(''); ax.set_xlabel('')
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_heatmap_coh.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Evolucion trimestral (barras agrupadas)
# ══════════════════════════════════════════════════════════
x = np.arange(4); n = len(ANIOS); w = 0.8 / n
COLORES = ['#42A5F5', '#1B4F8A', '#E53935']

# Seguridad
fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)
fig.suptitle('Dimension Seguridad - Evolucion Trimestral | Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
for ax, col, tp in [(axes[0], 'homicidios', 'Homicidios'), (axes[1], 'hurtos', 'Hurtos')]:
    for idx, año in enumerate(ANIOS):
        vals = corr_trim[corr_trim['año'] == año][col].values
        offset = (idx - n / 2 + 0.5) * w
        b = ax.bar(x + offset, vals, w, label=str(año), color=COLORES[idx % 3], alpha=0.85, edgecolor='white')
        for bar in b:
            h = bar.get_height()
            if h > 0: ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')
    ax.set_title(tp, fontweight='bold', pad=10); ax.set_xticks(x); ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_seg_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# Movilidad
fig, axes = plt.subplots(1, 3, figsize=(20, 5), facecolor=BG)
fig.suptitle('Dimension Movilidad - Evolucion Trimestral | Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
CMOV = [['#F5A742', '#D95F2B', '#B71C1C'], ['#F5A742', '#D95F2B', '#B71C1C'], ['#FF8A80', '#E53935', '#7F0000']]
for pi, (ax, col, tp) in enumerate([(axes[0], 'siniestralidad', 'Siniestralidad'), (axes[1], 'lesionados', 'Lesionados'), (axes[2], 'mortales', 'Mortales')]):
    c = CMOV[pi]
    for idx, año in enumerate(ANIOS):
        vals = corr_trim[corr_trim['año'] == año][col].values
        offset = (idx - n / 2 + 0.5) * w
        b = ax.bar(x + offset, vals, w, label=str(año), color=c[idx % 3], alpha=0.85, edgecolor='white')
        for bar in b:
            h = bar.get_height()
            if h > 0: ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')
    ax.set_title(tp, fontweight='bold', pad=8); ax.set_xticks(x); ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_mov_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# Cohesion
fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)
fig.suptitle('Dimension Cohesion Social - Evolucion Trimestral | Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
CVIF = ['#CE93D8', '#7B1FA2', '#4A148C']; CRIN = ['#F48FB1', '#D81B60', '#880E4F']
for ax, col, colores, tp in [(axes[0], 'vif', CVIF, 'VIF'), (axes[1], 'rinas', CRIN, 'Rinas')]:
    for idx, año in enumerate(ANIOS):
        vals = corr_trim[corr_trim['año'] == año][col].values
        offset = (idx - n / 2 + 0.5) * w
        b = ax.bar(x + offset, vals, w, label=str(año), color=colores[idx % 3], alpha=0.85, edgecolor='white')
        for bar in b:
            h = bar.get_height()
            if h > 0: ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05, str(int(h)), ha='center', va='bottom', fontsize=7, fontweight='bold')
    ax.set_title(tp, fontweight='bold', pad=8); ax.set_xticks(x); ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.set_ylabel('Casos'); ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.legend()
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_coh_trim.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# ITT Global y composicion por dimension
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)
fig.suptitle('ITT Global — Roosevelt', fontsize=13, fontweight='bold', color='#1B2631')
COLORES_ITT = ['#42A5F5', '#2E7D32', '#E53935']
band_configs = [(0, 40, '#FFCDD2', 'Emergencia'), (40, 60, '#FFE0B2', 'Consolidacion'), (60, 80, '#C8E6C9', 'Avance'), (80, 100, '#BBDEFB', 'Transformacion')]

ax1 = axes[0]
bars = ax1.bar(ANIOS, base['ITT'], color=COLORES_ITT, alpha=0.85, edgecolor='white', width=0.5)
for bar, val, nivel in zip(bars, base['ITT'], base['nivel']):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 1, f'{val:.1f}\n{nivel}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=NIVEL_COLORS.get(nivel, '#1B2631'))
for y0, y1, c, l in band_configs: ax1.axhspan(y0, y1, alpha=0.15, color=c)
ax1.set_title('ITT por Ano', fontweight='bold', pad=10); ax1.set_ylim(0, 115); ax1.set_ylabel('ITT (0-100)'); ax1.set_xticks(ANIOS)

ax2 = axes[1]
dims = ['score_seguridad', 'score_movilidad', 'score_entorno_u', 'score_educ_des', 'score_cohesion']
dim_lbl = ['Seguridad', 'Movilidad', 'EntornoU (ref)', 'EducDes (ref)', 'Cohesion']
dim_p = [PESOS['Seguridad'], PESOS['Movilidad'], PESOS['EntornoU'], PESOS['EducDes'], PESOS['Cohesion']]
dim_c = [C_SEG, C_MOV, '#43A047', '#FB8C00', C_COH]
bottom = np.zeros(len(ANIOS))
for dim, lbl, peso, col in zip(dims, dim_lbl, dim_p, dim_c):
    vals = base[dim].values * peso
    ax2.bar(ANIOS, vals, bottom=bottom, label=f'{lbl} ({peso:.0%})', color=col, alpha=0.8, edgecolor='white', width=0.5)
    bottom += vals
ax2.plot(ANIOS, base['ITT'], 'D-', color='black', linewidth=2, markersize=8, label='ITT Total', zorder=5)
for y0, y1, c, l in band_configs: ax2.axhspan(y0, y1, alpha=0.1, color=c)
ax2.set_title('Composicion ITT', fontweight='bold', pad=10); ax2.set_ylim(0, 115); ax2.set_ylabel('Score ponderado'); ax2.set_xticks(ANIOS)
ax2.legend(loc='upper right', fontsize=7)
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_global.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Radar ITT: 5 dimensiones
# ══════════════════════════════════════════════════════════
DIMS_LBL = ['Seguridad', 'Movilidad', 'Cohesion\nSocial', 'Entorno\nUrbano', 'Educ y\nDesarrollo']
N_DIMS = 5
angles = [i / N_DIMS * 2 * np.pi for i in range(N_DIMS)] + [0]
COLORES_R = ['#42A5F5', '#2E7D32', '#E53935']

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), facecolor=BG)
fig.suptitle('Radar ITT — Roosevelt | 5 Dimensiones', fontsize=13, fontweight='bold', color='#1B2631')
ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(DIMS_LBL, fontsize=9)
ax.set_ylim(0, 100); ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7, color='gray')
ax.yaxis.grid(True, linestyle='--', alpha=0.4)

for idx, año in enumerate(ANIOS):
    row = base[base['año'] == año].iloc[0]
    vals = [row['score_seguridad'], row['score_movilidad'], row['score_cohesion'], row['score_entorno_u'], row['score_educ_des']]
    vals_c = vals + [vals[0]]
    ax.plot(angles, vals_c, 'o-', color=COLORES_R[idx], linewidth=2, markersize=5, label=str(año))
    ax.fill(angles, vals_c, alpha=0.08, color=COLORES_R[idx])
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
plt.tight_layout()
plt.savefig(IMG_DIR + 'itt_roosevelt_radar.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ══════════════════════════════════════════════════════════
# Exportar a Excel
# ══════════════════════════════════════════════════════════
EXPORT_PATH = str(PROJECT_ROOT / 'outputs' / 'IMAGENES_POR_ITT' / 'itt_roosevelt' / 'ITT_Roosevelt.xlsx')
with pd.ExcelWriter(EXPORT_PATH, engine='openpyxl') as writer:
    base.round(2).to_excel(writer, sheet_name='ITT_Anual', index=False)
    corr_trim.to_excel(writer, sheet_name='Series_Trimestrales', index=False)

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
