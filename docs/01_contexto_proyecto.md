# Contexto del proyecto

El proyecto `itt-transformacion-territorial` calcula el **Indice de Transformacion Territorial (ITT)** para zonas de intervencion urbana en Cali, Colombia.

El ITT busca medir, en escala 0-100, el grado de transformacion positiva de un territorio como resultado de inversion publica e intervenciones institucionales.

## Proposito

El repositorio esta pensado para:

- Calcular el ITT por zona.
- Documentar la metodologia y las fuentes de datos.
- Exportar resultados comparables.
- Facilitar la interpretacion de resultados por parte de agentes de IA y equipos tecnicos.

## Zonas del proyecto

| Zona | Notebook | Estado |
|---|---|---|
| ITT Roosevelt | `notebooks/01_itt_roosevelt.ipynb` | Implementado |
| Avenida Ciudad de Cali | `notebooks/02_itt_avenida_ciudad_de_cali.ipynb` | Implementado |
| Barrio Obrero | `notebooks/03_itt_barrio_obrero.ipynb` | Implementado |
| Pulmon de Oriente 2026 | `notebooks/04_itt_pulmon_oriente_2026.ipynb` | Parcial |
| Comparativo | `notebooks/05_comparativo_itt_zonas.ipynb` | Plantilla |

## Diferencias tecnicas por zona

### Avenida Ciudad de Cali

- Analisis por 8 tramos buffer de 100 m sobre corredor vial.
- Requiere spatial join de eventos a tramos.
- Usa datos con CRS mixtos segun indicador.
- Tiene implementacion funcional, pero sigue pendiente de migrar a `ref_min/ref_max` fijos.

### Barrio Obrero

- Analisis sobre un poligono unico de barrio.
- No requiere spatial join por tramo.
- Los datos ya vienen filtrados a la zona.
- Usa `ref_min/ref_max` fijos por indicador y es la referencia metodologica vigente del repo.
- `Entorno Urbano` ya no depende solo del referente fijo: el notebook incluye un proxy experimental con `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`.
- Ese proxy usa `Comuna 9` como aproximacion territorial a `Barrio Obrero` y combina `Deficit Cualitativo` con su proporcion dentro del `Deficit Habitacional`.
- La visualizacion recomendada para ese proxy es un `heatmap` de componentes del deficit cualitativo 2024, no una serie mensual o trimestral observada.

### Roosevelt

- Analisis sobre corredor con buffer de 100 m y eventos 2023-2025.
- El notebook ya fue implementado siguiendo la estructura funcional de Barrio Obrero.
- Usa `ref_min/ref_max` fijos y valores Proxy para Entorno Urbano, Educacion y Desarrollo, y Vulnerabilidad.
- La data ya esta disponible en `data/itt_roosevelt/` como ZIP y carpeta descomprimida de trabajo.

## Avances recientes

- Se normalizo el criterio metodologico para agentes y documentacion corta.
- Roosevelt paso de plantilla a notebook implementado.
- Se incorporaron insumos de referencia de vivienda en `data/referencia/` para evaluar mejoras en la dimension `Entorno Urbano`.
- El archivo de deficit habitacional ya se usa de forma experimental en `03_itt_barrio_obrero.ipynb` para recalcular `REF_ENTORNO_U`.
- `Predios titulados` y `subsidios de mejoramiento` siguen como insumos complementarios en evaluacion, pero aun no entran al calculo actual de la dimension.

## Estado documental

La capa metodologica mas actualizada para agentes esta en:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`

## Valores Proxy 2026

Para Pulmon de Oriente, el año 2026 solo dispone de datos reales de Q1. Los trimestres Q2, Q3 y Q4 se estiman mediante valores Proxy (promedio historico trimestral 2023-2025). Estos valores se marcan con doble asterisco (`**`) en todas las tablas y graficos.

> **Nota metodologica:** Los valores correspondientes a los trimestres Q2, Q3 y Q4 del año 2026 fueron estimados mediante valores Proxy calculados a partir de la linea base historica de los años 2023–2025, con el fin de normalizar la informacion y garantizar comparabilidad estadistica y visual en el analisis.

Referencia completa: `docs/05_nota_metodologica_proxy_2026.md`
