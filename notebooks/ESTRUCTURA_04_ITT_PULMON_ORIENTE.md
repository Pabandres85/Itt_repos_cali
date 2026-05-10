# Estructura del notebook 04_itt_pulmon_oriente_2026_v2.ipynb

## Proposito

Analisis parcial del ITT para Pulmon de Oriente. Solo calcula la **dimension Seguridad** comparando T1 (primer trimestre) entre 2023 y 2026. No es un ITT completo de 5 dimensiones.

El archivo original `04_itt_pulmon_oriente_2026.ipynb` se conserva intacto. Todos los cambios operativos van en la version `_v2`.

## Flujo completo

```
Colab clona el fork → descomprime Pulmon_De_Oriente_2026.zip →
carga homicidios y hurtos → calcula score seguridad T1 →
genera graficas → guarda en outputs/IMAGENES_POR_ITT/itt_pulmon_oriente/ → push a GitHub
```

---

## Estructura de celdas

### Bloque 1 — Preparacion del entorno

| Celda | Funcion |
|---|---|
| Celda 1 | Instala dependencias |
| Celda 2 | Importaciones y configuracion visual |
| Celda 3A | Clone del fork `j0rg3c45` branch `jorge_itt` + descompresion de `Pulmon_De_Oriente_2026.zip` |

### Bloque 2 — Parametros

| Celda | Funcion |
|---|---|
| Celda 3 | Define `ROOT`, `IMG_DIR`, busqueda automatica de archivos con `buscar_archivo()`, `ANIOS_SERIE`, `REFS` trimestrales, `EXPORT_PATH` |

Ruta de datos: `/content/Pulmon_De_Oriente_2026/Pulmon_De_Oriente_2026/`
Ruta de imagenes: `/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_pulmon_oriente/`

### Bloque 3 — Carga y procesamiento

| Celda | Funcion |
|---|---|
| Celda 4 | Carga GeoJSON de homicidios y hurtos (deteccion flexible de columnas) |
| Celda 5 | Mapa interactivo Folium (no genera PNG) |
| Celda 6 | Procesa indicadores de seguridad: parsea fechas, extrae ano/trimestre, agrega conteos |

### Bloque 4 — Calculo del score

| Celda | Funcion |
|---|---|
| Celda 7 | Normaliza con ref_min/ref_max trimestrales, calcula `score_seguridad = (score_homicidios + score_hurtos) / 2` |

### Bloque 5 — Visualizaciones

| Celda | Archivo generado |
|---|---|
| Celda 8 | Cards de metricas clave (sin savefig — solo display) |
| Celda 9 | `itt_pulmon_oriente_heatmap_seguridad_trimestral.png` |
| Celda 10 | `itt_pulmon_Serie_T1_observada_para_Seguridad_2026.png` |

### Bloque 6 — Exportacion y push

| Celda | Funcion |
|---|---|
| Celda 11 | Exporta `ITT_Pulmon_Oriente_Seguridad_T1_2026.xlsx` |
| Celda 12 | Valida imagenes + `git push` al repo |

---

## Diferencias con los otros notebooks

| Aspecto | Barrio Obrero / Roosevelt | Pulmon de Oriente |
|---|---|---|
| Tipo de analisis | ITT completo (5 dimensiones) | Parcial (solo Seguridad) |
| Periodo | 2023-2025 anual | 2023-2026 T1 comparativo |
| Indicadores | 7 (hom, hur, sin, les, mor, vif, rinas) | 2 (homicidios, hurtos) |
| REFS | Anuales por zona | Trimestrales para zona grande |
| Deteccion de archivos | Rutas fijas en PATHS | Busqueda dinamica con `buscar_archivo()` |
| Deteccion de columnas | Nombres fijos | Flexible con candidatos multiples |
| Imagenes generadas | 9-12 | 2-3 |

## Parametros clave (REFS trimestrales)

```
homicidios: (15, 30, True)   — trimestrales, zona grande (~200K+ hab)
hurtos:     (250, 1300, True) — trimestrales, zona grande
```

Estos REFS estan calibrados para volumenes trimestrales de una zona grande. Los valores observados (257 homicidios, 9219 hurtos por trimestre) superan ampliamente los refs, lo que produce scores de 0. Esto es un tema de calibracion pendiente documentado en el proyecto.

## Estructura del ZIP

`Pulmon_De_Oriente_2026.zip` extrae a:
```
Pulmon_De_Oriente_2026/
├── DATIC_homicidios_2023_2026T1_Pulmon_O.geojson
├── DATIC_hurtos_2023_2026T1_Pulmon_O.geojson
└── (otros archivos auxiliares)
```

Al descomprimir en `/content/Pulmon_De_Oriente_2026/`, la ruta final queda:
`/content/Pulmon_De_Oriente_2026/Pulmon_De_Oriente_2026/`

## Deteccion flexible de archivos

Este notebook usa `buscar_archivo()` en vez de rutas hardcoded:
```python
def buscar_archivo(nombres_exactos=None, contiene=None, extensiones=None):
    # Busca recursivamente en /content por nombre exacto o palabras contenidas
```

Esto permite que funcione aunque la estructura interna del ZIP cambie ligeramente.

## Deteccion flexible de columnas

Usa candidatos multiples para encontrar la columna de fecha:
- `fechah`, `fecha_hech`, `fecha_hecho`, `fecha`, `fechao`, `FECHA_HECH`

Y para ano:
- `anio`, `ano`, `año`, `Año`

## Relacion con otros archivos

- `04_itt_pulmon_oriente_2026.ipynb` — original intacto (no tocar)
- `04_itt_pulmon_oriente_2026_v2.ipynb` — version operativa con flujo Colab + push
- `notebooks_py/04_itt_pulmon_oriente_2026.py` — version local ejecutable con `uv run`

---

## Proceso de migracion: de v1 a v2

### Contexto

El notebook original fue creado para ejecutarse en Colab con subida manual del ZIP. Las imagenes se guardaban en el directorio actual sin push automatico.

### Pasos realizados para crear la v2

1. **Copiar el notebook original** — se uso un script Python (`_convert_pulmon.py`) para leer el JSON y generar una copia modificada.

2. **Reemplazar Celda 3A (upload manual)** por una celda que:
   - Clona el fork `j0rg3c45/Itt_repos_cali` branch `jorge_itt`
   - Descomprime `Pulmon_De_Oriente_2026.zip` desde el repo clonado

3. **Agregar `IMG_DIR`** en la Celda 3:
   ```python
   IMG_DIR = '/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_pulmon_oriente/'
   os.makedirs(IMG_DIR, exist_ok=True)
   ```

4. **Prefijo `IMG_DIR +` en los `savefig`** existentes y agregar `savefig` a graficas que solo tenian `plt.show()`.

5. **Agregar Celda 12 (validacion + push)** al final.

6. **Limpiar outputs** embebidos para reducir tamano.

### Herramienta usada

Script temporal `_convert_pulmon.py` que:
- Lee el JSON del notebook original
- Aplica modificaciones programaticamente
- Guarda como `04_itt_pulmon_oriente_2026_v2.ipynb`
- Se elimino despues de usarse

### Resultado

El notebook v2 se ejecuta en Colab, genera las graficas de seguridad T1, las guarda en el repo y hace push automatico a GitHub.
