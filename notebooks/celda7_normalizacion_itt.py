# =============================================================================
# Celda 7 — Normalizacion con ref_min / ref_max e ITT (con Proxy 2026)
# =============================================================================
# Copiar este contenido completo en la Celda 7 del notebook
# 04_itt_pulmon_oriente_2026_v2.ipynb en Colab
#
# REQUISITO: La Celda 6 debe haberse ejecutado primero con la logica Proxy.
# El DataFrame corr_trim ya debe tener valores en Q2, Q3, Q4 de 2026.
#
# CAMBIO CLAVE vs version anterior:
# - Se elimina el filtro TRIM_CON_DATOS que excluia Q2-Q4 de 2026
# - Ahora TODOS los trimestres de 2026 tienen valores (Q1 real, Q2-Q4 Proxy)
# - El ITT anual 2026 es el promedio de los 4 trimestres (incluyendo Proxy)
# =============================================================================

def score_ref(valor, ref_min, ref_max, inverso):
    if ref_max == ref_min: return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw

# Scores trimestrales por indicador
for ind, (rmin, rmax, inv, desc) in REFS.items():
    corr_trim[f'score_{ind}'] = corr_trim[ind].apply(lambda v, rm=rmin, rx=rmax, i=inv: score_ref(v, rm, rx, i))

# Scores trimestrales por dimension
corr_trim['score_seguridad'] = (corr_trim['score_homicidios'] + corr_trim['score_hurtos']) / 2
corr_trim['score_cohesion']  = (corr_trim['score_vif'] + corr_trim['score_rinas'] + REF_VULNERABILIDAD) / 3
corr_trim['score_movilidad'] = REF_MOVILIDAD
corr_trim['score_entorno_u'] = REF_ENTORNO_U
corr_trim['score_educ_des']  = REF_EDUC_DES

corr_trim['ITT'] = (
    PESOS['Seguridad'] * corr_trim['score_seguridad'] +
    PESOS['Movilidad'] * corr_trim['score_movilidad'] +
    PESOS['EntornoU']  * corr_trim['score_entorno_u'] +
    PESOS['EducDes']   * corr_trim['score_educ_des'] +
    PESOS['Cohesion']  * corr_trim['score_cohesion']
)

def clasificar(v):
    if v < 40: return 'Emergencia'
    elif v < 60: return 'Consolidacion'
    elif v < 80: return 'Avance'
    else: return 'Transformacion'

corr_trim['nivel'] = corr_trim['ITT'].apply(clasificar)

# ITT anual = promedio de los 4 trimestres (incluyendo Proxy para 2026)
base = corr_trim.groupby('año').agg({
    'homicidios': 'sum', 'hurtos': 'sum', 'vif': 'sum',
    'score_seguridad': 'mean', 'score_cohesion': 'mean',
    'score_movilidad': 'mean', 'score_entorno_u': 'mean', 'score_educ_des': 'mean',
    'ITT': 'mean'
}).reset_index()
base['nivel'] = base['ITT'].apply(clasificar)

print('ITT Pulmon de Oriente — Normalizacion con ref_min/ref_max fijos')
print(f'\nReferentes: Movilidad={REF_MOVILIDAD}, EntornoU={REF_ENTORNO_U}, EducDes={REF_EDUC_DES}')
print('\nScores por dimension e ITT (anual = promedio 4 trimestres):')
print(base[['año','score_seguridad','score_movilidad','score_cohesion','score_entorno_u','score_educ_des','ITT','nivel']].round(1).to_string(index=False))

print('\n' + '='*60)
print('NOTA: El ITT anual 2026 incluye valores Proxy para Q2, Q3 y Q4.')
print('Los trimestres estimados se calcularon con promedio historico 2023-2025.')
print('='*60)
