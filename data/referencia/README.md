# Datos de referencia

Usar esta carpeta para guardar insumos comunes a los tres ITT:

- Catalogos.
- Scores de referencia.
- Poligonos base.
- Limites administrativos.
- Diccionarios de variables.
- Parametros generales de comparacion.

## Estado actual

Ademas de referencias generales, esta carpeta ya contiene Excel de vivienda y mejoramiento territorial en evaluacion metodologica:

- `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`
- `BD_PREDIOS_TITULADOS 2023-2025 (1).xlsx`
- `BD_SUBSIDIOS_MEJORAMIENTO_VIV_AÑOS_2024_2025 (1).xlsx`

## Uso previsto

- El archivo de deficit habitacional es el principal candidato para evaluar un proxy de `Entorno Urbano`.
- Ese archivo ya se usa de forma experimental en `notebooks/03_itt_barrio_obrero.ipynb` para recalcular `REF_ENTORNO_U` con `Comuna 9` como proxy territorial de `Barrio Obrero`.
- La lectura correcta de ese insumo es anual `2024`; no ofrece serie mensual ni trimestral observada.
- La visualizacion recomendada en el notebook para ese insumo es un `heatmap` de componentes del deficit cualitativo 2024.
- Los archivos de predios titulados y subsidios de mejoramiento se consideran insumos complementarios de intervencion institucional.
- `Predios titulados` y `subsidios de mejoramiento` aun no hacen parte del calculo actual de `Entorno Urbano` en los notebooks.
