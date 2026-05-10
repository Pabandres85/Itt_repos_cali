# Estructura del notebook 04_itt_pulmon_oriente_2026_v2.ipynb

## Proposito

Calcula el ITT para Pulmon de Oriente con datos reales en Seguridad y Cohesion Social, y referentes provisionales en las demas dimensiones. Periodo 2023-2026 (2026 solo T1 disponible).

El archivo original `04_itt_pulmon_oriente_2026.ipynb` se conserva intacto. Todos los cambios operativos van en la version `_v2`.

## Flujo completo

```
Colab clona el fork → descomprime ZIP consolidado → elimina duplicados →
calcula ITT trimestral y anual → genera graficas → guarda en outputs/ → push a GitHub
```

---

## Datos disponibles

### ZIP consolidado: `Pulmon_De_Oriente_2026.zip`

Todo esta en una sola carpeta `Pulmon_De_Oriente_2026/`:

| Archivo | Indicador | Periodo |
|---|---|---|
| `DATIC_homicidios_2023_2026T1_Pulmon_O.geojson` | Homicidios | 2023-2026 T1 |
| `DATIC_hurtos_2023_2026T1_Pulmon_O.geojson` | Hurtos | 2023-2026 T1 |
| `DATIC_violencia_intrafamiliar_2023_2026T1.geojson` | VIF | 2023-2026 T1 |
| `DATIC_comparendos_2023_2026T1_Pulmon_O.geojson` | Comparendos/Rinas | 2023-2026 T1 |
| `poligonos.geojson` | Poligono zona | — |
| `ARBOLES_PULMON.geojson` | Arboles | — |
| `Sedes_educativas_oficiales_PULMON_1K.geojson` | Sedes educativas | — |
| `CAI_MECAL_CALI_PULMON.geojson` | CAI | — |
| `VBG_2025_PULMON.geojson` | VBG | 2025 |

### Duplicados en la data

| Indicador | Total registros | Duplicados exactos | Sin duplicados |
|---|---|---|---|
| Homicidios | 313 | 0 | 313 |
| Hurtos | 5,171 | 896 | 4,275 |
| VIF | 25,769 | 5,257 | 20,512 |
| Comparendos | 29,485 | 385 | 29,100 |

Los duplicados se concentran en 2026 y se eliminan automaticamente con `drop_duplicates()` en la funcion `procesar()`.

### Periodo y trimestres

- `ANIOS = [2023, 2024, 2025, 2026]`
- 2026 solo tiene datos de T1
- T2, T3, T4 de 2026 quedan como NaN (no como 0)
- Se usa `TRIM_CON_DATOS` para distinguir trimestres con datos reales

---

## Estructura de celdas

### Bloque 1 — Preparacion del entorno

| Celda | Funcion |
|---|---|
| Celda 1 | Instala dependencias |
| Celda 2 | Importaciones y configuracion visual |
| Celda 3A | Clone del fork `j0rg3c45` branch `jorge_itt` + descompresion del ZIP consolidado |

### Bloque 2 — Parametros

| Celda | Funcion |
|---|---|
| Celda 3 | Define `DATA_DIR`, `IMG_DIR`, `PATHS` (busqueda flexible), `ANIOS`, `PESOS`, `REFS`, referentes provisionales |

Ruta de datos: `DATA_DIR / 'Pulmon_De_Oriente_2026/'`
Ruta de imagenes: `/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_pulmon_oriente/`

### Bloque 3 — Carga y procesamiento

| Celda | Funcion |
|---|---|
| Celda 4 | Carga GeoJSON (homicidios, hurtos, VIF, comparendos, arboles, sedes, CAI) |
| Celda 5 | Mapa Folium con todas las capas (desactivadas por defecto, usuario activa manualmente) |
| Celda 6 | Procesa indicadores: elimina duplicados, parsea fechas, filtra rinas de comparendos, agrega conteos |

### Bloque 4 — Calculo del ITT

| Celda | Funcion |
|---|---|
| Celda 7 | Normaliza trimestralmente con ref_min/ref_max, calcula scores por dimension, ITT trimestral y anual |

### Bloque 5 — Visualizaciones

| Celda | Archivo generado |
|---|---|
| Celda 8 | `itt_pulmon_cards.png` — Cards metricas clave |
| Celda 9 | `itt_pulmon_heatmap_seg.png` — Heatmap Seguridad |
| Celda 10 | `itt_pulmon_heatmap_vif.png` — Heatmap VIF |
| Celda 11 | `itt_pulmon_seg_trim.png` — Barras trimestrales Seguridad |
| Celda 12 | `itt_pulmon_coh_trim.png` — Barras trimestrales VIF |
| Celda 13 | `itt_pulmon_global.png` — ITT Global + composicion |
| Celda 14 | `itt_pulmon_radar.png` — Radar 5 dimensiones |

### Bloque 6 — Exportacion y push

| Celda | Funcion |
|---|---|
| Celda 15 | Exporta `ITT_Pulmon_Oriente.xlsx` |
| Celda 16 | Valida imagenes + `git push` al repo |

---

## Parametros clave

### REFS trimestrales (zona grande, guia metodologica seccion 4.1)

```
homicidios:  (5,   50,  True)  — Homicidios trimestrales
hurtos:      (200, 450, True)  — Hurtos trimestrales
vif:         (60,  200, True)  — VIF trimestral
rinas:       (20,  160, True)  — Rinas trimestral
```

### Referentes provisionales

- Movilidad: 35.0 (Score Pulmon de Oriente T4-2025)
- Entorno Urbano: 39.2 (guia metodologica)
- Educacion y Desarrollo: 54.9 (guia metodologica)
- Vulnerabilidad: 54.1 (Sec. Bienestar Social)

### Dimensiones con datos reales vs referentes

| Dimension | Estado | Indicadores |
|---|---|---|
| Seguridad (30%) | Datos reales | Homicidios, Hurtos |
| Movilidad (25%) | Referente fijo | No hay siniestros en ZIP |
| Entorno Urbano (20%) | Referente fijo | — |
| Educacion (13%) | Referente fijo | — |
| Cohesion Social (12%) | Parcial | VIF + Rinas reales, Vulnerabilidad referente |

---

## Diferencias con Barrio Obrero y Roosevelt

| Aspecto | Barrio Obrero | Roosevelt | Pulmon de Oriente |
|---|---|---|---|
| Unidad de analisis | Poligono unico | Corredor buffer 100m | Zona agregada multiples comunas |
| Tamano | ~5K hab | ~50K-100K hab | >200K hab |
| Periodo | 2023-2025 | 2023-2025 | 2023-2026 (T1) |
| Datos Seguridad | Completos | Completos | Completos |
| Datos Movilidad | Completos | Completos | No disponibles (referente) |
| Datos Cohesion | Completos | Completos | Parcial (VIF + Rinas, sin Vulnerabilidad) |
| Normalizacion | Anual | Anual | Trimestral |
| Duplicados | No reportados | No reportados | Si (se eliminan automaticamente) |
| Colores graficas | 3 (2023-2025) | 3 (2023-2025) | 4 (2023-2026) |

---

## Mapa Folium

Todas las capas arrancan con `show=False` (desactivadas) para evitar bloqueo por volumen de datos:

- Poligono Pulmon de Oriente (visible por defecto)
- Homicidios (rojo) — desactivada
- Hurtos (azul) — desactivada
- VIF (morado) — desactivada
- Arboles (verde) — desactivada
- Sedes Educativas (azul claro) — desactivada
- CAI/MECAL (azul oscuro) — desactivada

El usuario activa manualmente las capas que quiera ver desde el control de capas.

---

## Relacion con otros archivos

- `04_itt_pulmon_oriente_2026.ipynb` — original intacto (no tocar)
- `04_itt_pulmon_oriente_2026_v2.ipynb` — version operativa con flujo Colab + push
- `notebooks_py/04_itt_pulmon_oriente_2025.py` — version local ejecutable con `uv run` (periodo 2023-2025)
- `notebooks_py/04_itt_pulmon_oriente_2026.py` — version local parcial (solo Seguridad T1)

---

## Proceso de migracion y actualizaciones

### Version inicial (parcial)

- Solo dimension Seguridad (homicidios + hurtos)
- Solo ZIP 2026
- Periodo: comparativo T1 2023-2026

### Actualizacion a version completa

1. **ZIP consolidado** — toda la data se unio en un solo ZIP (`Pulmon_De_Oriente_2026.zip`)
2. **Comparendos/Rinas agregados** — filtro `agrupado.str.startswith('RI')`
3. **VIF integrado** — archivo `DATIC_violencia_intrafamiliar_2023_2026T1.geojson`
4. **Periodo extendido** — `ANIOS = [2023, 2024, 2025, 2026]`
5. **Duplicados** — `drop_duplicates()` en `procesar()` con reporte de cuantos se eliminan
6. **NaN en trimestres sin datos** — 2026 T2-T4 quedan vacios, no como 0
7. **4 colores** — naranja (`#FF6F00`) agregado para 2026 en todas las graficas
8. **Mapa completo** — todas las capas en FeatureGroup con `show=False`
9. **Celda push** — condicional (solo en Colab, en local solo valida)
