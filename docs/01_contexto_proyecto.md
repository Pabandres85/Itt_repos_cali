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
| ITT Roosevelt | `notebooks/01_itt_roosevelt.ipynb` | Plantilla |
| Avenida Ciudad de Cali | `notebooks/02_itt_avenida_ciudad_de_cali.ipynb` | Implementado |
| Barrio Obrero | `notebooks/03_itt_barrio_obrero.ipynb` | Implementado |
| Comparativo | `notebooks/04_comparativo_itt_zonas.ipynb` | Plantilla |

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

### Roosevelt

- Aun no tiene implementacion final ni datos cargados en el repo.
- El notebook actual es solo una base para adaptar cuando lleguen los insumos.

## Estado documental

La capa metodologica mas actualizada para agentes esta en:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`

Los documentos de `docs/` resumen el proyecto y deben mantenerse consistentes con esa guia.
