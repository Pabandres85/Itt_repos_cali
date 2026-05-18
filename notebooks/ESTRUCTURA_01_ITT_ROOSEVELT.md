# Estructura del notebook 01_itt_roosevelt_v2.ipynb

## Proposito

Calcula el ITT para el Corredor Roosevelt (buffer 100m) en Cali. Disenado para ejecutarse en Google Colab con la extension de Colab en Kiro/VS Code.

El archivo original `01_itt_roosevelt.ipynb` se conserva intacto. Todos los cambios operativos van en la version `_v2`.

Periodo: 2023-2026 (2026 = Proxy**, promedio historico 2023-2025, sin datos reales).

## Flujo completo

```
Colab clona el fork → descomprime Roosevelt.zip → calcula ITT →
genera 9 graficas → guarda en outputs/IMAGENES_POR_ITT/itt_roosevelt/ → push a GitHub
```

---

## Estructura de celdas

### Bloque 1 — Preparacion del entorno

| Celda | Funcion |
|---|---|
| Celda 1 | Instala dependencias |
| Celda 2 | Importaciones y configuracion visual |
| Celda 3A | Clone del fork `j0rg3c45` branch `jorge_itt` + descompresion de `Roosevelt.zip` |

### Bloque 2 — Parametros

| Celda | Funcion |
|---|---|
| Celda 3 | Define `BASE`, `PATHS`, `ANIOS`, `PESOS`, `REFS`, referentes provisionales, `IMG_DIR` |

Ruta de datos: `/content/Roosevelt/Roosevelt/Geojson_Roosevelt/`
Ruta de imagenes: `/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_roosevelt/`

### Bloque 3 — Carga y procesamiento

| Celda | Funcion |
|---|---|
| Celda 4 | Carga GeoJSON (homicidios, hurtos, siniestros, VIF, comparendos, VBG, sedes) |
| Celda 5 | Mapa interactivo Folium (no genera PNG) |
| Celda 6 | Procesa indicadores: fechas, ano/trimestre, conteos anuales y trimestrales |

### Bloque 4 — Calculo del ITT

| Celda | Funcion |
|---|---|
| Celda 7 | Normaliza con ref_min/ref_max, calcula scores por dimension, ITT ponderado |

### Bloque 5 — Visualizaciones

| Celda | Archivo generado |
|---|---|
| Celda 8 | `itt_roosevelt_cards.png` |
| Celda 9 | `itt_roosevelt_heatmap_seg.png` |
| Celda 10 | `itt_roosevelt_heatmap_mov.png` |
| Celda 11 | `itt_roosevelt_heatmap_coh.png` |
| Celda 12 | `itt_roosevelt_seg_trim.png` |
| Celda 13 | `itt_roosevelt_mov_trim.png` |
| Celda 14 | `itt_roosevelt_coh_trim.png` |
| Celda 15 | `itt_roosevelt_global.png` |
| Celda 16 | `itt_roosevelt_radar.png` |

### Bloque 6 — Exportacion y push

| Celda | Funcion |
|---|---|
| Celda 17 | Exporta `ITT_Roosevelt.xlsx` |
| Celda 18 | Valida imagenes + `git push` al repo |

---

## Diferencias con Barrio Obrero

| Aspecto | Barrio Obrero | Roosevelt |
|---|---|---|
| Unidad de analisis | Poligono unico | Corredor con buffer 100m |
| Proxy Entorno Urbano | Si (deficit habitacional Comuna 9) | No (usa referente fijo 39.2) |
| Filtro de rinas | Exacto (`== 'RIÑAS'`) | Startswith (`str.startswith('RI')`) |
| Datos adicionales | Arboles, CAI | VBG |
| REFS homicidios | (0, 5) | (0, 8) |
| REFS hurtos | (10, 60) | (120, 320) |
| Imagenes generadas | 12 | 9 |

## Parametros clave (REFS)

```
homicidios:     (0,   8,   True)  — corredor mediano
hurtos:         (120, 320, True)
siniestralidad: (15,  40,  True)
lesionados:     (10,  35,  True)
mortales:       (0,   4,   True)
vif:            (4,   18,  True)
rinas:          (5,   25,  True)
```

## Referentes provisionales

- Entorno Urbano: 39.2 (Pulmon de Oriente)
- Educacion y Desarrollo: 54.9 (Pulmon de Oriente)
- Vulnerabilidad: 54.1 (Sec. Bienestar Social)

## Estructura del ZIP

`Roosevelt.zip` extrae a:
```
Roosevelt/
├── Geojson_Roosevelt/    ← archivos .geojson usados por el notebook
└── shape_Roosevelt/      ← shapefiles (no usados directamente)
```

Al descomprimir en `/content/Roosevelt/`, la ruta final queda:
`/content/Roosevelt/Roosevelt/Geojson_Roosevelt/`

## Relacion con otros archivos

- `01_itt_roosevelt.ipynb` — original intacto (no tocar)
- `01_itt_roosevelt_v2.ipynb` — version operativa con flujo Colab + push
- `notebooks_py/01_itt_roosevelt.py` — version local ejecutable con `uv run`

---

## Proceso de migracion: de v1 a v2

### Contexto

El notebook original (`01_itt_roosevelt.ipynb`) fue creado para ejecutarse en Colab con subida manual del ZIP. Funcionaba bien pero:
- Las imagenes se generaban en el directorio actual de Colab (no en el repo)
- No habia push automatico a GitHub
- Cada vez habia que subir el ZIP manualmente

### Pasos realizados para crear la v2

1. **Copiar el notebook original** — se uso un script Python para leer el JSON del `.ipynb` y generar una copia modificada, sin tocar el original.

2. **Reemplazar Celda 3A (upload manual)** por una celda que:
   - Clona el fork `j0rg3c45/Itt_repos_cali` branch `jorge_itt`
   - Descomprime `Roosevelt.zip` desde el repo clonado
   - Elimina la dependencia de subida manual

3. **Agregar `IMG_DIR`** en la Celda 3 de parametros:
   ```python
   IMG_DIR = '/content/itt_repos_cali/outputs/IMAGENES_POR_ITT/itt_roosevelt/'
   os.makedirs(IMG_DIR, exist_ok=True)
   ```

4. **Prefijo `IMG_DIR +` en todos los `savefig`** — los 9 `plt.savefig('itt_roosevelt_...')` se cambiaron a `plt.savefig(IMG_DIR + 'itt_roosevelt_...')` para que las imagenes se guarden dentro del repo clonado.

5. **Agregar Celda 18 (validacion + push)** al final:
   - Lista las imagenes generadas con tamano
   - Hace `git add outputs/IMAGENES_POR_ITT/`
   - Commit con mensaje descriptivo
   - Push al fork en GitHub

6. **Limpiar outputs** — se eliminaron los outputs embebidos del notebook para reducir tamano.

7. **Corregir ruta BASE** — el ZIP extrae a `Roosevelt/Geojson_Roosevelt/` (con carpeta padre), por lo que la ruta final es `/content/Roosevelt/Roosevelt/Geojson_Roosevelt/` (no `/content/Roosevelt/Geojson_Roosevelt/`).

### Herramienta usada

Se creo un script temporal `_convert_roosevelt.py` que:
- Lee el JSON del notebook original
- Aplica las modificaciones programaticamente (reemplazar celdas, insertar lineas, agregar celdas nuevas)
- Guarda como `01_itt_roosevelt_v2.ipynb`
- Se elimino despues de usarse

### Resultado

El notebook v2 se ejecuta de punta a punta en Colab:
1. Clona el repo actualizado
2. Descomprime datos
3. Calcula el ITT completo
4. Genera 9 imagenes + Excel
5. Hace push automatico a GitHub

Despues del push, en la maquina local solo se hace `git pull` y las imagenes aparecen en `outputs/IMAGENES_POR_ITT/itt_roosevelt/`.
