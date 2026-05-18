# notebooks_py — Scripts ITT ejecutables con uv

## Que es esta carpeta

Contiene los scripts `.py` equivalentes a los notebooks `.ipynb` del proyecto, adaptados para ejecutarse localmente en Windows con `uv run`. Cada script genera todas las graficas, las guarda como PNG en `outputs/IMAGENES_POR_ITT/<zona>/` y exporta un Excel con los resultados.

## Por que se crearon

Los notebooks `.ipynb` estan disenados para Google Colab (Linux). Al ejecutarlos localmente en Windows surgen problemas:

- Las rutas `/content/...` no existen en Windows.
- Los magic commands (`!`, `%`) no son Python valido y generan errores de sintaxis.
- El kernel de Colab no guarda archivos en el disco local.
- Las imagenes generadas quedan en la VM de Google y no se descargan automaticamente.

Los scripts `.py` resuelven todo eso: detectan el entorno, usan rutas relativas al proyecto, descomprimen datos automaticamente y guardan las imagenes directamente en tu maquina.

## Como ejecutar

Desde la raiz del proyecto:

```bash
uv run notebooks_py/03_itt_barrio_obrero.py
uv run notebooks_py/01_itt_roosevelt.py
uv run notebooks_py/04_itt_pulmon_oriente_2026.py
```

`uv` se encarga de instalar las dependencias automaticamente la primera vez (PEP 723 inline metadata).

## Requisitos

- Python >= 3.11
- `uv` instalado (https://docs.astral.sh/uv/getting-started/installation/)

No necesitas crear un entorno virtual manualmente. `uv run` lo gestiona por ti.

## Scripts disponibles

| Script | Zona | Tipo de analisis | Imagenes generadas |
|---|---|---|---|
| `01_itt_roosevelt.py` | Corredor Roosevelt | ITT completo (5 dimensiones) | 9 PNG + Excel |
| `03_itt_barrio_obrero.py` | Barrio Obrero, Comuna 9 | ITT completo + proxy Entorno Urbano | 12 PNG + Excel |
| `04_itt_pulmon_oriente_2025.py` | Pulmon de Oriente | ITT completo con Proxy** Q2-Q4 2026 | 7 PNG + Excel |

## Scripts auxiliares en notebooks/

Ademas de los scripts ejecutables, existen scripts auxiliares en `notebooks/` que contienen el codigo fuente para reemplazar celdas del notebook de Colab:

| Script | Funcion | Aplica a |
|---|---|---|
| `notebooks/celda6_procesamiento_dedup.py` | Deduplicacion + generacion de valores Proxy Q2-Q4 2026 | Celda 6 de `04_itt_pulmon_oriente_2026_v2.ipynb` |
| `notebooks/celda7_normalizacion_itt.py` | Normalizacion con 4 trimestres completos 2026 (Proxy incluido) | Celda 7 de `04_itt_pulmon_oriente_2026_v2.ipynb` |
| `notebooks/correcciones_celdas_5_y_15.py` | Mapa y exportacion usando DataFrames deduplicados | Celdas 5 y 15 de `04_itt_pulmon_oriente_2026_v2.ipynb` |

### Como aplicar en Colab

1. Ejecutar el notebook hasta Celda 5 normalmente
2. Reemplazar **Celda 6** con `celda6_procesamiento_dedup.py`
3. Reemplazar **Celda 7** con `celda7_normalizacion_itt.py`
4. Re-ejecutar desde Celda 6 en adelante
5. Los graficos mostraran 4 trimestres completos para 2026 (Q1 real + Q2-Q4 Proxy**)

> **Nota metodologica:** Los valores correspondientes a los trimestres Q2, Q3 y Q4 del año 2026 fueron estimados mediante valores Proxy calculados a partir de la linea base historica de los años 2023–2025. Se identifican con doble asterisco (`**`).

## Donde se guardan las salidas

```
outputs/IMAGENES_POR_ITT/
├── itt_barrio_obrero/       ← imagenes + Excel de Barrio Obrero
├── itt_roosevelt/           ← imagenes + Excel de Roosevelt
└── itt_pulmon_oriente/      ← imagenes + Excel de Pulmon de Oriente
```

## Flujo interno de cada script

1. **Detectar raiz del proyecto** — usa `Path(__file__).resolve().parent.parent`
2. **Descomprimir datos** — si el ZIP existe pero no esta extraido, lo descomprime automaticamente en `data/<zona>/`
3. **Verificar archivos** — confirma que todos los GeoJSON necesarios existen
4. **Cargar datos** — lee GeoJSON con geopandas/json
5. **Procesar indicadores** — parsea fechas, extrae ano/trimestre, agrega conteos anuales y trimestrales
6. **Normalizar con ref_min/ref_max** — aplica umbrales fijos por indicador (no min-max relativo)
7. **Calcular scores por dimension e ITT** — suma ponderada segun pesos oficiales
8. **Generar graficas** — cards, heatmaps, barras trimestrales, ITT global, radar
9. **Guardar imagenes** — `plt.savefig()` en `outputs/IMAGENES_POR_ITT/<zona>/`
10. **Exportar Excel** — tabla anual + series trimestrales
11. **Imprimir resumen** — lista de imagenes generadas con tamano

## Diferencias con los notebooks .ipynb

| Aspecto | Notebook (.ipynb) | Script (.py) |
|---|---|---|
| Entorno | Google Colab (Linux) | Local Windows con uv |
| Rutas | Hardcoded `/content/...` | Relativas al proyecto |
| Dependencias | `!pip install` | PEP 723 inline metadata |
| Imagenes | Se ven inline pero no se guardan localmente | Se guardan en disco automaticamente |
| Ejecucion | Celda por celda | Un solo comando `uv run` |
| Mapa Folium | Interactivo en Colab | No incluido (requiere navegador) |

## Notas

- Los datos fuente (ZIPs) deben estar en `data/<zona>/`. Ya estan versionados en el repo.
- Los archivos descomprimidos estan en `.gitignore` — no se suben al repo.
- Las imagenes generadas si se versionan en `outputs/IMAGENES_POR_ITT/`.
- Para Avenida Ciudad de Cali no hay script `.py` porque los datos fuente no estan disponibles en el repo.
