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

- Estado: implementado.
- Notebook: `notebooks/02_itt_avenida_ciudad_de_cali.ipynb`
- Unidad de analisis: 8 tramos buffer de 100 m sobre corredor vial.
- Metodo espacial: spatial join de eventos a tramos.
- Periodo: 2023-2025.
- Metodologia: funcional, pero pendiente de migracion a `ref_min/ref_max` fijos.
- Referentes provisionales: Entorno Urbano 39.2, Educacion y Desarrollo 54.9.
- Datos en repo: estructura creada, pero insumos fuente no versionados.

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
