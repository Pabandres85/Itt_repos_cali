# Zonas de estudio

## ITT Roosevelt

- Estado: implementado.
- Notebook: `notebooks/01_itt_roosevelt.ipynb`
- Unidad de analisis: corredor con buffer de 100 m.
- Metodo espacial: uso de capa buffer y eventos territoriales de la zona.
- Periodo: 2023-2025.
- Metodologia: usa `ref_min/ref_max` fijos y la estructura funcional de Barrio Obrero.
- Referentes provisionales: Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Datos en repo: `Roosevelt.zip` presente y carpeta descomprimida de trabajo disponible.
- Observacion: notebook operativo, pendiente de afinacion futura de referentes si se incorporan nuevos indicadores de entorno.

## ITT Avenida Ciudad de Cali

- Estado: implementado y actualizado (ref_min/ref_max fijos, 3 ZIPs, heatmaps por tramo con orden geografico).
- Notebook: `notebooks/02_itt_avenida_ciudad_de_cali.ipynb` — 42 celdas.
- Unidad de analisis: 8 tramos buffer de 100 m sobre corredor vial (~4.5 km).
- Metodo espacial: spatial join de eventos a tramos usando `gdf_tramos['tramo'].astype(int)` (orden norte→sur).
- Periodo: 2023-2026 T1. Movilidad solo 2023-2025 (sin datos 2026 — peso redistribuido en ITT).
- Metodologia: usa `ref_min/ref_max` fijos por indicador. ITT 2026 excluye Movilidad (NaN, no proxy).
- Referentes provisionales: Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Datos en repo: 3 ZIPs versionados en `data/itt_avenida_ciudad_de_cali/`.
- Fuentes: ZIP1 (poligono + estaticas), ZIP2 (DATIC seguridad/cohesion), ZIP3 (siniestros movilidad).
- Tramo sin datos: T8 (extremo sur) tiene 0 siniestros en ZIP3 — dato real confirmado.
- Ejecucion Colab: celda git pull (si repo ya existe) + Cell 3A extrae 3 ZIPs + Cell 3 verifica paths.

## ITT Barrio Obrero

- Estado: implementado.
- Notebook: `notebooks/03_itt_barrio_obrero.ipynb`
- Unidad de analisis: poligono unico del barrio.
- Metodo espacial: no requiere spatial join por tramo.
- Periodo: 2023-2025.
- Metodologia: usa `ref_min/ref_max` fijos por indicador.
- Referentes provisionales de base: Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Estado actual de Entorno Urbano: el notebook ya puede sobrescribir `39.2` con un proxy experimental usando `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`.
- Base territorial del proxy: `Comuna 9` como aproximacion a Barrio Obrero.
- Periodicidad real del proxy de Entorno Urbano: anual `2024`, no mensual ni trimestral observada.
- Visualizacion interna reciente: `heatmap` de componentes del deficit cualitativo 2024.
- Datos en repo: `obrero.zip` presente; capas se cargan por descompresion o Colab.
