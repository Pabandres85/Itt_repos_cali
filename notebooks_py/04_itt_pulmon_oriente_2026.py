"""
ITT Pulmon de Oriente — Dimension Seguridad (parcial)
Comparativo T1 · 2023-2026

Zona: Pulmon de Oriente (zona agregada)
Analisis parcial: solo dimension Seguridad
Indicadores: Homicidios, Hurtos
Periodo: 2023-2026 (foco en T1)

Ejecutar con:
    uv run notebooks_py/04_itt_pulmon_oriente_2026.py
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
# ]
# ///

import os, re, warnings, zipfile
from pathlib import Path

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════
# Configuracion visual
# ══════════════════════════════════════════════════════════
C_SEG = '#1B4F8A'; BG = '#F4F6F9'
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': 'white', 'font.family': 'DejaVu Sans',
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.alpha': 0.3
})

# ══════════════════════════════════════════════════════════
# Rutas — detectar raiz del proyecto
# ══════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DATA_DIR = PROJECT_ROOT / 'data' / 'itt_pulmon_oriente'
ZIP_PATH = DATA_DIR / 'Pulmon_De_Oriente_2026.zip'
EXTRACT_DIR = DATA_DIR / 'Pulmon_De_Oriente_2026'

IMG_DIR = PROJECT_ROOT / 'outputs' / 'IMAGENES_POR_ITT' / 'itt_pulmon_oriente'
IMG_DIR.mkdir(parents=True, exist_ok=True)
print(f'Imagenes se guardaran en: {IMG_DIR}')

# ══════════════════════════════════════════════════════════
# Parametros
# ══════════════════════════════════════════════════════════
ANIOS = [2023, 2024, 2025, 2026]
ZONA_NOMBRE = 'Pulmon de Oriente'

REFS = {
    'homicidios': (5, 50, True, 'Homicidios trimestrales Pulmon de Oriente'),
    'hurtos':     (200, 450, True, 'Hurtos trimestrales Pulmon de Oriente'),
}

# ══════════════════════════════════════════════════════════
# Descompresion automatica
# ══════════════════════════════════════════════════════════
if not EXTRACT_DIR.exists():
    if ZIP_PATH.exists():
        print(f'Descomprimiendo {ZIP_PATH}...')
        with zipfile.ZipFile(ZIP_PATH, 'r') as z:
            z.extractall(DATA_DIR)
        print('Listo.')
    else:
        raise FileNotFoundError(f'No se encontro {ZIP_PATH}')

# ══════════════════════════════════════════════════════════
# Busqueda de archivos geojson via os.walk
# ══════════════════════════════════════════════════════════
def find_geojson(base_dir: Path, pattern: str) -> Path | None:
    """Busca recursivamente un archivo geojson que coincida con el patron (case-insensitive)."""
    regex = re.compile(pattern, re.IGNORECASE)
    for root, _dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith('.geojson') and regex.search(f):
                return Path(root) / f
    return None

path_homicidios = find_geojson(DATA_DIR, r'homicidios')
path_hurtos = find_geojson(DATA_DIR, r'hurtos')

print('\nArchivos encontrados:')
print(f'  Homicidios: {path_homicidios or "NO ENCONTRADO"}')
print(f'  Hurtos:     {path_hurtos or "NO ENCONTRADO"}')

if path_homicidios is None or path_hurtos is None:
    # Listar todos los geojson disponibles para diagnostico
    print('\nGeojson disponibles en DATA_DIR:')
    for root, _dirs, files in os.walk(DATA_DIR):
        for f in files:
            if f.lower().endswith('.geojson'):
                print(f'  {Path(root) / f}')
    raise FileNotFoundError('No se encontraron los archivos geojson necesarios (homicidios / hurtos).')

# ══════════════════════════════════════════════════════════
# Utilidad: seleccion flexible de columnas
# ══════════════════════════════════════════════════════════
def pick_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Retorna el primer nombre de columna que exista en el DataFrame."""
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

FECHA_CANDIDATES = ['fechah', 'fecha_hech', 'fecha_hecho', 'fecha', 'fechao', 'FECHA_HECH']
ANIO_CANDIDATES = ['anio', 'ano', 'año', 'Año']

# ══════════════════════════════════════════════════════════
# Carga y procesamiento
# ══════════════════════════════════════════════════════════
def cargar_y_procesar(path: Path, nombre: str) -> pd.DataFrame:
    """Carga un geojson, detecta columna de fecha, extrae año y trimestre."""
    gdf = gpd.read_file(path)
    df = pd.DataFrame(gdf.drop(columns='geometry', errors='ignore'))
    print(f'\n  {nombre}: {len(df)} registros, columnas: {list(df.columns)[:10]}...')

    col_fecha = pick_col(df, FECHA_CANDIDATES)
    col_anio = pick_col(df, ANIO_CANDIDATES)

    if col_fecha:
        df['_fecha'] = pd.to_datetime(df[col_fecha], errors='coerce')
        df['año'] = df['_fecha'].dt.year
        df['trimestre'] = df['_fecha'].dt.quarter
    elif col_anio:
        df['año'] = pd.to_numeric(df[col_anio], errors='coerce')
        df['trimestre'] = np.nan
        print(f'    AVISO: No se encontro columna de fecha, usando columna de año: {col_anio}')
    else:
        raise ValueError(f'No se encontro columna de fecha ni de año en {nombre}. Columnas: {list(df.columns)}')

    df = df.dropna(subset=['año'])
    df['año'] = df['año'].astype(int)
    return df

print('\nCargando datos...')
df_hom = cargar_y_procesar(path_homicidios, 'Homicidios')
df_hur = cargar_y_procesar(path_hurtos, 'Hurtos')

# ══════════════════════════════════════════════════════════
# Agregacion trimestral
# ══════════════════════════════════════════════════════════
def agg_trim(df: pd.DataFrame) -> pd.Series:
    """Agrega conteo por (año, trimestre)."""
    años_disp = sorted(df['año'].unique())
    idx = pd.MultiIndex.from_product([años_disp, [1, 2, 3, 4]], names=['año', 'trimestre'])
    return df.groupby(['año', 'trimestre']).size().reindex(idx, fill_value=0)

trim_hom = agg_trim(df_hom).reset_index(name='homicidios')
trim_hur = agg_trim(df_hur).reset_index(name='hurtos')

# Merge trimestral completo
corr_trim = trim_hom.merge(trim_hur, on=['año', 'trimestre'], how='outer').fillna(0)
corr_trim['periodo'] = corr_trim['año'].astype(str) + '-Q' + corr_trim['trimestre'].astype(int).astype(str)

print('\nSerie trimestral completa:')
print(corr_trim.to_string(index=False))

# ══════════════════════════════════════════════════════════
# Filtro T1 y conteo por año (2023-2026)
# ══════════════════════════════════════════════════════════
t1 = corr_trim[(corr_trim['trimestre'] == 1) & (corr_trim['año'].isin(ANIOS))].copy()
t1 = t1.sort_values('año').reset_index(drop=True)

if t1.empty:
    raise ValueError('No se encontraron datos para T1 en los años 2023-2026.')

print('\nDatos T1 (Trimestre 1) por año:')
print(t1[['año', 'homicidios', 'hurtos']].to_string(index=False))

# ══════════════════════════════════════════════════════════
# Normalizacion con ref_min / ref_max
# ══════════════════════════════════════════════════════════
def score_ref(valor, ref_min, ref_max, inverso):
    """Normaliza un valor entre ref_min y ref_max (0-100). Inverso: menos es mejor."""
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw

rmin_h, rmax_h, inv_h, _ = REFS['homicidios']
rmin_u, rmax_u, inv_u, _ = REFS['hurtos']

t1['score_homicidios'] = t1['homicidios'].apply(lambda v: score_ref(v, rmin_h, rmax_h, inv_h))
t1['score_hurtos'] = t1['hurtos'].apply(lambda v: score_ref(v, rmin_u, rmax_u, inv_u))
t1['score_seguridad'] = (t1['score_homicidios'] + t1['score_hurtos']) / 2

print('\nScores T1:')
print(t1[['año', 'homicidios', 'score_homicidios', 'hurtos', 'score_hurtos', 'score_seguridad']].round(1).to_string(index=False))

# ══════════════════════════════════════════════════════════
# Visualizacion 1: Heatmap Seguridad Trimestral
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=BG)
fig.suptitle(f'Dimension Seguridad — Heatmap Trimestral | {ZONA_NOMBRE}', fontsize=13, fontweight='bold', color='#1B2631')

for ax, col, titulo_h, cmap_h in [(axes[0], 'homicidios', 'Homicidios', 'Blues'),
                                    (axes[1], 'hurtos', 'Hurtos', 'Oranges')]:
    pivot = corr_trim.pivot(index='año', columns='trimestre', values=col)
    pivot.columns = ['Q1', 'Q2', 'Q3', 'Q4']
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap=cmap_h, linewidths=0.5,
                linecolor='#DEE2E6', ax=ax, annot_kws={'size': 11},
                cbar_kws={'label': 'Casos', 'shrink': 0.8})
    ax.set_title(titulo_h, fontweight='bold', pad=8)
    ax.set_ylabel('')
    ax.set_xlabel('')

plt.tight_layout()
plt.savefig(IMG_DIR / 'itt_pulmon_heatmap_seguridad_trimestral.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('\n  OK  itt_pulmon_heatmap_seguridad_trimestral.png')

# ══════════════════════════════════════════════════════════
# Visualizacion 2: Barras agrupadas T1 comparativo
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
fig.suptitle(f'Seguridad T1 Comparativo {ANIOS[0]}-{ANIOS[-1]} | {ZONA_NOMBRE}',
             fontsize=13, fontweight='bold', color='#1B2631')

x_pos = np.arange(len(t1))
w = 0.35

bars_hom = ax.bar(x_pos - w/2, t1['homicidios'], w, label='Homicidios', color='#1B4F8A', alpha=0.85, edgecolor='white')
bars_hur = ax.bar(x_pos + w/2, t1['hurtos'], w, label='Hurtos', color='#E8852A', alpha=0.85, edgecolor='white')

for bar in bars_hom:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, str(int(h)),
                ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in bars_hur:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, str(int(h)),
                ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels(t1['año'].astype(str))
ax.set_ylabel('Casos en T1')
ax.set_xlabel('Año')
ax.legend()
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig(IMG_DIR / 'itt_pulmon_seguridad_t1_comparativo.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('  OK  itt_pulmon_seguridad_t1_comparativo.png')

# ══════════════════════════════════════════════════════════
# Visualizacion 3: Linea score_seguridad T1
# ══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
fig.suptitle(f'Score Seguridad T1 — {ZONA_NOMBRE} | {ANIOS[0]}-{ANIOS[-1]}',
             fontsize=13, fontweight='bold', color='#1B2631')

ax.plot(t1['año'], t1['score_seguridad'], 'o-', color=C_SEG, linewidth=2.5, markersize=9)
for _, row in t1.iterrows():
    ax.text(row['año'], row['score_seguridad'] + 1.5, f"{row['score_seguridad']:.1f}",
            ha='center', va='bottom', fontsize=10, fontweight='bold', color=C_SEG)

# Bandas de referencia
band_configs = [(0, 40, '#FFCDD2', 'Emergencia'), (40, 60, '#FFE0B2', 'Consolidacion'),
                (60, 80, '#C8E6C9', 'Avance'), (80, 100, '#BBDEFB', 'Transformacion')]
for y0, y1, c, lbl in band_configs:
    ax.axhspan(y0, y1, alpha=0.15, color=c)
    ax.text(t1['año'].max() + 0.15, (y0 + y1) / 2, lbl, fontsize=7, color='gray', va='center')

ax.set_ylim(0, 105)
ax.set_xlim(t1['año'].min() - 0.3, t1['año'].max() + 0.6)
ax.set_xticks(t1['año'])
ax.set_ylabel('Score Seguridad (0-100)')
ax.set_xlabel('Año')

plt.tight_layout()
plt.savefig(IMG_DIR / 'itt_pulmon_score_seguridad_t1.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print('  OK  itt_pulmon_score_seguridad_t1.png')

# ══════════════════════════════════════════════════════════
# Exportar a Excel
# ══════════════════════════════════════════════════════════
EXPORT_PATH = IMG_DIR / 'ITT_Pulmon_Oriente_Seguridad_T1_2026.xlsx'
with pd.ExcelWriter(EXPORT_PATH, engine='openpyxl') as writer:
    t1.round(2).to_excel(writer, sheet_name='Seguridad_T1', index=False)
    corr_trim.round(2).to_excel(writer, sheet_name='Series_Trimestrales', index=False)

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
    size_kb = os.path.getsize(IMG_DIR / f) / 1024
    print(f'  OK  {f} ({size_kb:.1f} KB)')

print('\n' + '=' * 50)
print(f'ANALISIS PARCIAL COMPLETADO — {ZONA_NOMBRE}')
print(f'Dimension: Seguridad | Periodo: T1 {ANIOS[0]}-{ANIOS[-1]}')
print('=' * 50)
