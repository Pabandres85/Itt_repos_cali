# Estructura del notebook 03_itt_barrio_obrero.ipynb

## Proposito

Este notebook calcula el ITT (Indice de Transformacion Territorial) para Barrio Obrero, Comuna 9, Cali. Esta disenado para ejecutarse en **Google Colab** usando la extension de Colab en Kiro/VS Code.

Periodo: 2023-2026 (2026 = Proxy**, promedio historico 2023-2025, sin datos reales).

## Flujo completo de ejecucion

```
Colab clona el repo → descomprime datos → calcula ITT → genera graficas →
guarda imagenes en el repo clonado → hace push a GitHub
```

Despues del push, haces `git pull` en tu maquina local y las imagenes aparecen en `outputs/IMAGENES_POR_ITT/itt_barrio_obrero/`.

---

## Estructura de celdas

### Bloque 1 — Preparacion del entorno (solo Colab)

| Celda | Funcion |
|---|---|
| **Celda 1** | Instala dependencias (`geopandas`, `folium`, etc.) |
| **Celda 2** | Importaciones y configuracion visual (colores, estilos matplotlib) |
| **Exploracion** | `!pwd`, `!ls /content` — verifica el entorno Colab |
| **Clone** | Clona el fork `j0rg3c45/Itt_repos_cali` branch `jorge_itt` en `/content/` |
| **Celda 3A** | Descomprime `obrero.zip` en `/content/obrero/` |

### Bloque 2 — Parametros y configuracion

| Celda | Funcion |
|---|---|
| **Celda 3** | Define `BASE` (ruta datos), `PATHS` (archivos GeoJSON), `ANIOS`, `PESOS`, `REFS` (umbrales ref_min/ref_max), `REF_ENTORNO_U`, `REF_EDUC_DES`, `REF_VULNERABILIDAD`, `IMG_DIR` (carpeta de salida de imagenes) |

Aqui se define `IMG_DIR = '/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_barrio_obrero/'` que es donde se guardan todas las graficas.

### Bloque 3 — Proxy de Entorno Urbano (opcional)

| Celda | Funcion |
|---|---|
| **Celda 3B** | Recalcula `REF_ENTORNO_U` usando deficit habitacional de Comuna 9. Si no encuentra el Excel, conserva el valor fijo (39.2) |
| **Grafica barras** | Proxy de Entorno Urbano (barras) → `itt_obrero_proxy_entorno_barras.png` |
| **Grafica linea** | Construccion del proxy (linea) → `itt_obrero_proxy_entorno_linea.png` |
| **Celda 3C** | Heatmap de componentes del deficit cualitativo 2024 → `itt_obrero_heatmap_deficit_cualitativo_2024.png` |

### Bloque 4 — Carga y procesamiento de datos

| Celda | Funcion |
|---|---|
| **Celda 4** | Carga todos los GeoJSON (homicidios, hurtos, siniestros, VIF, comparendos, arboles, sedes, CAI) |
| **Celda 5** | Mapa interactivo Folium con todas las capas (no genera PNG) |
| **Celda 6** | Procesa indicadores: parsea fechas, extrae ano/trimestre, agrega conteos anuales y trimestrales |

### Bloque 5 — Calculo del ITT

| Celda | Funcion |
|---|---|
| **Celda 7** | Normaliza indicadores con `ref_min/ref_max`, calcula scores por dimension, calcula ITT ponderado, clasifica nivel |

### Bloque 6 — Visualizaciones (todas guardan PNG en IMG_DIR)

| Celda | Grafica generada | Archivo |
|---|---|---|
| **Celda 8** | Cards de metricas clave | `itt_obrero_cards.png` |
| **Celda 9** | Heatmap Seguridad trimestral | `itt_obrero_heatmap_seg.png` |
| **Celda 10** | Heatmap Movilidad trimestral | `itt_obrero_heatmap_mov.png` |
| **Celda 11** | Heatmap Cohesion Social trimestral | `itt_obrero_heatmap_coh.png` |
| **Celda 12** | Barras trimestrales Seguridad | `itt_obrero_seg_trim.png` |
| **Celda 13** | Barras trimestrales Movilidad | `itt_obrero_mov_trim.png` |
| **Celda 14** | Barras trimestrales Cohesion | `itt_obrero_coh_trim.png` |
| **Celda 15** | ITT Global + composicion por dimension | `itt_obrero_global.png` |
| **Celda 16** | Radar 5 dimensiones | `itt_obrero_radar.png` |

### Bloque 7 — Exportacion y push

| Celda | Funcion |
|---|---|
| **Celda 17** | Exporta Excel `ITT_Barrio_Obrero.xlsx` con hojas: ITT_Anual, Series_Trimestrales, Datos_Estaticos, Umbrales_RefMinMax, Metodologia |
| **Celda 18** | Valida que las imagenes se generaron (lista PNGs con tamano) y hace `git add` + `git commit` + `git push` al repo |

---

## Donde se guardan las imagenes

En Colab: `/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_barrio_obrero/`

Esa ruta esta dentro del repo clonado, por eso la Celda 18 puede hacer push y las imagenes llegan a GitHub.

## Imagenes generadas (12 total)

```
itt_obrero_proxy_entorno_barras.png
itt_obrero_proxy_entorno_linea.png
itt_obrero_heatmap_deficit_cualitativo_2024.png
itt_obrero_cards.png
itt_obrero_heatmap_seg.png
itt_obrero_heatmap_mov.png
itt_obrero_heatmap_coh.png
itt_obrero_seg_trim.png
itt_obrero_mov_trim.png
itt_obrero_coh_trim.png
itt_obrero_global.png
itt_obrero_radar.png
```

## Como funciona el push desde Colab (Celda 18)

```python
# 1. Configura usuario git (necesario en Colab)
git config user.email "colab@itt.local"
git config user.name "ITT Colab"

# 2. Agrega las imagenes
git add outputs/IMAGENES_POR_ITT/

# 3. Commit
git commit -m "feat: imagenes ITT Barrio Obrero generadas desde Colab"

# 4. Push
git push
```

Para que el push funcione, el clone debe usar un token de acceso personal en la URL:
```
https://<TOKEN>@github.com/j0rg3c45/Itt_repos_cali.git
```

## Requisitos para replicar en otro ITT

Para crear un notebook equivalente para otra zona, se necesita:

1. **Datos**: ZIP con GeoJSON de la zona en `data/<zona>/`
2. **Parametros**: Ajustar `PATHS`, `REFS`, `ZONA_NOMBRE`, `IMG_DIR`
3. **Prefijo de imagenes**: Cambiar `itt_obrero_` por `itt_<zona>_`
4. **Celda 18**: Ajustar la ruta del `git add` si cambia la subcarpeta

## Relacion con el script .py

El archivo `notebooks_py/03_itt_barrio_obrero.py` es la version local equivalente:
- Hace lo mismo pero corre en Windows con `uv run`
- No necesita Colab ni push (guarda directo en disco)
- No incluye el mapa Folium interactivo
