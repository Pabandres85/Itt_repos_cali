# Fuentes de datos

Este documento registra el inventario operativo de datos por zona y deja trazabilidad para el uso por notebooks y agentes.

## Estado actual por zona

### ITT Roosevelt

Estado actual:

- Sin datos cargados en el repo.
- `data/itt_roosevelt/` solo contiene archivo de referencia y estructura.

### ITT Avenida Ciudad de Cali

Estado esperado segun notebook `02_itt_avenida_ciudad_de_cali.ipynb`:

| Indicador / capa | Archivo esperado | Observaciones |
|---|---|---|
| Tramos | `ciudad_de_Cali_100m.geojson` | 8 buffers del corredor |
| Homicidios | `HOMICIDIOS_2023_2025_tramos.geojson` | Coordenadas WGS84 |
| Hurtos | `HURTOS_2023_2025_tramos.geojson` | Coordenadas WGS84 |
| Comparendos | `COMPARENDOS_2023_2025_tramos.geojson` | Filtrar `agrupado="RINAS"` |
| Siniestros | `BD_SINIESTROS_2023_2025_tramos.geojson` | CRS EPSG:3115 |
| VIF | `VIOLENCIA_INTRAFAMILIAR_2023_2025_tramos.geojson` | Requiere georreferenciacion |

Estado en repo:

- `data/itt_avenida_ciudad_de_cali/` no contiene aun los insumos fuente versionados.
- La ejecucion actual depende de cargas externas o Colab.

### ITT Barrio Obrero

Estado esperado segun notebook `03_itt_barrio_obrero.ipynb`:

| Indicador / capa | Archivo esperado | Observaciones |
|---|---|---|
| Poligono | `Geojson_Barrio_Obrero.geojson` | Poligono unico |
| Homicidios | `HOMICIDIOS_2023_2025_Obrero.geojson` | Conteo anual bajo |
| Hurtos | `HURTOS_2023_2025_OBRERO.geojson` | Eventos del periodo |
| Siniestros | `BD_SINIESTROS_2023_2025_COMUNA_BARRIO_OBRERO.geojson` | Analisis anual y trimestral |
| VIF | `VIOLENCIA_INTRAFAMILIAR_2023_2025_OBRERO.geojson` | Cohesion social |
| Comparendos | `COMPARENDOS_2023_2025_OBRERO.geojson` | Filtrar `agrupado="RINAS"` |
| Arboles | `Arboles_Dagma_OBRERO.geojson` | Solo mapa |
| Sedes | `Sedes_educativas_oficiales_OBRERO.geojson` | Solo mapa |
| CAI | `CAI_MECAL_CALI_OBRERO.geojson` | Solo mapa |

Estado en repo:

- `data/itt_barrio_obrero/` contiene `obrero.zip`.
- Los GeoJSON no estan expandidos dentro del repo; la carga actual esta pensada para descompresion o subida en Colab.

## Recomendaciones de trazabilidad

Para cada insumo registrar:

- Nombre exacto del archivo.
- Entidad fuente.
- Fecha de entrega o descarga.
- Periodo cubierto.
- CRS.
- Campos clave.
- Transformaciones aplicadas antes del notebook.
- Observaciones de calidad.

## Nota para agentes

Si una fuente no esta presente en el repo, debe marcarse como:

- No versionada en repositorio.
- Disponible solo en Colab o carga manual.
- Pendiente de entrega.
