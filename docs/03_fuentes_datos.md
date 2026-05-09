# Fuentes de datos

Este documento registra el inventario operativo de datos por zona y deja trazabilidad para el uso por notebooks y agentes.

## Estado actual por zona

### ITT Roosevelt

Estado actual:

- `data/itt_roosevelt/` ya contiene `Roosevelt.zip`.
- Existe carpeta de trabajo descomprimida `data/itt_roosevelt/Roosevelt_unzipped/`.
- El notebook `01_itt_roosevelt.ipynb` ya fue adaptado para esta estructura de insumos.

Insumos identificados en la zona Roosevelt:

| Indicador / capa | Archivo identificado | Observaciones |
|---|---|---|
| Buffer / tramos | `Geojson_tramos_Roosevelt_Buffer_100.geojson` | Base espacial del corredor |
| Tramos | `Geojson_tramos_Roosevelt.geojson` | Geometria auxiliar |
| Homicidios | `HOMICIDIOS_2023_2025_Roosevelt.geojson` | Eventos 2023-2025 |
| Hurtos | `HURTOS_2023_2025_Roosevelt.geojson` | Eventos 2023-2025 |
| Comparendos | `COMPARENDOS_2023_2025_Roosevelt.geojson` | Filtrar `agrupado="RINAS"` si aplica |
| Siniestros | `BD_SINIESTROS_2023_2025_COMUNA_BARRIO_4326_Roosevelt.geojson` | Base de movilidad |
| VIF | `VIOLENCIA_INTRAFAMILIAR_2023_2025_Roosevelt.geojson` | Cohesion social |
| VBG | `VBG_2025_Roosevelt.geojson` | Insumo complementario, aun no incorporado al ITT |
| Sedes | `Sedes_educativas_oficiales_Roosevelt.geojson` | Solo mapa / apoyo territorial |

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
- En Colab, el flujo operativo reciente ha sido clonar el repo en `/content/itt_repos_cali`, descomprimir `data/itt_barrio_obrero/obrero.zip` y usar `BASE = /content/obrero/obrero/Geojson_Barrio_Obrero/`.

Soporte metodologico adicional para `Entorno Urbano` en Barrio Obrero:

| Fuente complementaria | Uso actual en notebook | Periodicidad real | Observaciones |
|---|---|---|---|
| `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx` | Proxy experimental de `Entorno Urbano` | Anual `2024` | Usa `Comuna 9` como proxy territorial para Barrio Obrero |
| `BD_PREDIOS_TITULADOS 2023-2025 (1).xlsx` | No usado en calculo actual | Anual `2023-2025` | Contexto de formalizacion |
| `BD_SUBSIDIOS_MEJORAMIENTO_VIV_AÑOS_2024_2025 (1).xlsx` | No usado en calculo actual | Anual `2024-2025` | Contexto de intervencion en vivienda |

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

## Nuevas referencias territoriales

La carpeta `data/referencia/` ahora incluye insumos de vivienda y mejoramiento que pueden servir como soporte metodologico futuro:

| Archivo | Uso potencial | Estado |
|---|---|---|
| `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx` | Proxy de `Entorno Urbano` por deficit habitacional | Ya usado de forma experimental en `03_itt_barrio_obrero.ipynb` |
| `BD_PREDIOS_TITULADOS 2023-2025 (1).xlsx` | Indicador de formalizacion / gestion | En analisis, no usado en calculo actual |
| `BD_SUBSIDIOS_MEJORAMIENTO_VIV_AÑOS_2024_2025 (1).xlsx` | Indicador de intervencion en vivienda | En analisis, no usado en calculo actual |

Nota metodologica:

- El archivo de deficit habitacional no tiene granularidad mensual ni trimestral; solo aporta un corte anual 2024.
- Por eso, en Barrio Obrero la visualizacion incorporada al notebook es un `heatmap` de componentes del deficit cualitativo 2024, no una serie temporal observada.
