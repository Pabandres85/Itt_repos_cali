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
- Referentes provisionales: Entorno Urbano 39.2, Educacion y Desarrollo 54.9, Vulnerabilidad 54.1.
- Datos en repo: `obrero.zip` presente; capas se cargan por descompresion o Colab.
