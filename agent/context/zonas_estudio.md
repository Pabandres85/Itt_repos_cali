# Zonas de estudio

## ITT Roosevelt

- Estado: implementado.
- Notebook: `notebooks/01_itt_roosevelt.ipynb`
- Unidad de analisis: corredor con buffer de 100 m.
- Metodo espacial: uso de capa buffer y eventos territoriales de la zona.
- Periodo: 2023-2025.
- Metodologia: usa `ref_min/ref_max` fijos y la estructura funcional de Barrio Obrero.
- Valores Proxy: Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Datos en repo: `Roosevelt.zip` presente y carpeta descomprimida de trabajo disponible.
- Observacion: notebook operativo, pendiente de afinacion futura de referentes si se incorporan nuevos indicadores de entorno.

## ITT Avenida Ciudad de Cali

- Estado: implementado.
- Notebook: `notebooks/02_itt_avenida_ciudad_de_cali.ipynb`
- Unidad de analisis: 8 tramos buffer de 100 m sobre corredor vial.
- Metodo espacial: spatial join de eventos a tramos.
- Periodo: 2023-2025.
- Metodologia: funcional, pero pendiente de migracion a `ref_min/ref_max` fijos.
- Valores Proxy: Entorno Urbano 39.2, Educacion y Desarrollo 54.9.
- Datos en repo: estructura creada, pero insumos fuente no versionados.

## ITT Barrio Obrero

- Estado: implementado.
- Notebook: `notebooks/03_itt_barrio_obrero.ipynb`
- Unidad de analisis: poligono unico del barrio.
- Metodo espacial: no requiere spatial join por tramo.
- Periodo: 2023-2026 (Q1 2026 real, sin Proxy).
- Periodo anual (base): solo 2023-2025 (años completos con datos reales).
- Periodo trimestral (corr_trim): 2023 Q1-Q4, 2024 Q1-Q4, 2025 Q1-Q4, 2026 Q1 (solo dato real, NO Proxy).
- Metodologia: usa `ref_min/ref_max` fijos por indicador.
- Valores Proxy de base: Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Estado actual de Entorno Urbano: el notebook ya puede sobrescribir `39.2` con un proxy experimental usando `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`.
- Base territorial del proxy: `Comuna 9` como aproximacion a Barrio Obrero.
- Periodicidad real del proxy de Entorno Urbano: anual `2024`, no mensual ni trimestral observada.
- Visualizacion interna reciente: `heatmap` de componentes del deficit cualitativo 2024.
- Datos en repo: `obrero.zip` presente; capas se cargan por descompresion o Colab.
- Archivos GeoJSON DATIC: `DATIC_homicidios_2023_2026T1_Barrio_O.geojson`, `DATIC_hurtos_2023_2026T1_Barrio_O.geojson`, `DATIC_violencia_intrafamiliar_2023_2026T1_Barrio_O.geojson`, `DATIC_comparendos_2023_2026T1_Barrio_O.geojson`.
- Visualizacion trimestral: heatmaps y barras incluyen Q1 2026 real con 4to color naranja (#FF6F00). Trimestres sin datos (Q2-Q4 2026) muestran `-` en heatmaps.
- Cards, ITT Global, Radar: solo 2023-2025 (años completos).
- NO se usan valores Proxy para Q2-Q4 2026 en esta zona (solo Pulmon de Oriente usa Proxy).

## ITT Pulmon de Oriente

- Estado: implementado.
- Notebook: `notebooks/04_itt_pulmon_oriente_2026_v2.ipynb`
- Unidad de analisis: zona agregada multiples comunas (>200K hab).
- Metodo espacial: no requiere spatial join (eventos ya filtrados a la zona).
- Periodo: 2023-2026.
- Metodologia: usa `ref_min/ref_max` fijos trimestrales (zona grande, guia metodologica seccion 4.1).
- Valores Proxy: Movilidad 35.0, Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Datos en repo: `Pulmon_De_Oriente_2026.zip` presente con ZIP consolidado.
- Deduplicacion: automatica por fecha+coordenada (elimina duplicados en hurtos, VIF y comparendos).
- Periodo 2026: solo T1 tiene datos reales; Q2, Q3 y Q4 se estiman con valores Proxy.
- Valores Proxy: calculados como promedio historico trimestral de 2023-2025.
- Marcado: todos los valores Proxy se identifican con doble asterisco (`**`).

> **Nota metodologica:** Los valores correspondientes a los trimestres Q2, Q3 y Q4 del año 2026 fueron estimados mediante valores Proxy calculados a partir de la linea base historica de los años 2023–2025, con el fin de normalizar la informacion y garantizar comparabilidad estadistica y visual en el analisis.
