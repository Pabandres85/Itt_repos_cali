# Proceso de Creacion del Consolidado y Seguimiento de Datasets

## Objetivo

Documentar como se genera el archivo `CONSOLIDADO_ITT_ZONAS.txt` y como este alimenta el archivo `ITT_Seguimiento_Datasets.xlsx` para el seguimiento operativo del proyecto.

---

## Diagrama de Proceso

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FUENTES DE DATOS (GeoJSON)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  data/itt_roosevelt/Roosevelt.zip                                           │
│  data/itt_barrio_obrero/obrero.zip                                          │
│  data/itt_pulmon_oriente/Pulmon_De_Oriente_2026.zip                         │
│  data/itt_avenida_ciudad_de_cali/Geojson_Ciudad_de_Cali.zip                 │
│  data/referencia/*.xlsx (deficit habitacional, predios, subsidios)           │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     NOTEBOOKS (calculo del ITT)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  01_itt_roosevelt_v2.ipynb          → ITT Roosevelt 2023-2026**             │
│  03_itt_barrio_obrero.ipynb         → ITT Barrio Obrero 2023-2026**        │
│  04_itt_pulmon_oriente_2026_v2.ipynb → ITT Pulmon Oriente 2023-2026**      │
│  02_itt_avenida_ciudad_de_cali.ipynb → ITT Av. Cali 2023-2025             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Cada notebook:                                                             │
│    1. Carga GeoJSON                                                         │
│    2. Deduplica por fecha+coordenada                                        │
│    3. Genera valores Proxy** para 2026 (promedio historico 2023-2025)       │
│    4. Normaliza con ref_min/ref_max fijos                                   │
│    5. Calcula scores por dimension e ITT global                             │
│    6. Genera graficos con marcadores **                                     │
│    7. Exporta Excel + imagenes                                              │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              CONSOLIDADO_ITT_ZONAS.txt (sintesis manual)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  Se construye revisando los resultados de cada notebook:                     │
│                                                                             │
│  • Estado de cada dimension por zona (COMPLETA / PROXY / PARCIAL)           │
│  • Scores ITT por año                                                       │
│  • Conteos trimestrales (reales + Proxy**)                                  │
│  • Conteos anuales                                                          │
│  • Valores Proxy calculados                                                 │
│  • Duplicados eliminados                                                    │
│  • Prioridades pendientes                                                   │
│  • Nota metodologica                                                        │
│                                                                             │
│  Ubicacion: outputs/CONSOLIDADO_ITT_ZONAS.txt                               │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│           ITT_Seguimiento_Datasets.xlsx (tracker operativo)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Se genera programaticamente a partir del CONSOLIDADO:                       │
│                                                                             │
│  Hoja 1: Seguimiento Datasets                                               │
│    → 1 fila por cada indicador/zona (37 registros)                          │
│    → Columnas: Zona, Dimension, Indicador, Peso, Estado, Tipo Valor,        │
│      Score, Periodo, Fuente, Formato, Observaciones                         │
│    → Coloreado: verde=COMPLETA, naranja=PROXY                               │
│                                                                             │
│  Hoja 2: Resumen por Zona                                                   │
│    → Tabla cruzada: 4 zonas x 5 dimensiones                                │
│    → Vista rapida del estado de completitud                                 │
│                                                                             │
│  Hoja 3: Nota Metodologica                                                  │
│    → Definicion de PROXY, tipos, marcado visual                             │
│                                                                             │
│  Ubicacion: ITT_Seguimiento_Datasets.xlsx (raiz del proyecto)               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detalle del Flujo

### Paso 1 — Ejecucion de Notebooks

Cada notebook se ejecuta en Google Colab (o localmente con `uv run`):

| Notebook | Zona | Que produce |
|---|---|---|
| `01_itt_roosevelt_v2.ipynb` | Roosevelt | Scores ITT + graficos + Excel |
| `03_itt_barrio_obrero.ipynb` | Barrio Obrero | Scores ITT + graficos + Excel |
| `04_itt_pulmon_oriente_2026_v2.ipynb` | Pulmon de Oriente | Scores ITT + graficos + Excel |
| `02_itt_avenida_ciudad_de_cali.ipynb` | Av. Ciudad de Cali | Scores ITT (sin v2) |

### Paso 2 — Construccion del Consolidado

El archivo `CONSOLIDADO_ITT_ZONAS.txt` se construye revisando:

1. **Salidas de cada notebook** — scores, conteos, estados
2. **Archivos de datos** — que ZIPs existen, que indicadores tienen datos
3. **Metodologia vigente** — que dimensiones son COMPLETA vs PROXY
4. **Valores Proxy** — cuales se calcularon y con que metodo

El consolidado es un archivo de texto plano que sirve como **fuente unica de verdad** del estado del proyecto.

### Paso 3 — Generacion del Excel de Seguimiento

El archivo `ITT_Seguimiento_Datasets.xlsx` se genera con un script Python que:

1. Lee la informacion del consolidado
2. Estructura los datos en formato tabular (1 fila por indicador/zona)
3. Aplica formato visual (colores por estado)
4. Genera la hoja resumen cruzada
5. Incluye la nota metodologica

---

## Cuando Actualizar

| Evento | Accion |
|---|---|
| Se ejecuta un notebook con nuevos datos | Actualizar CONSOLIDADO + regenerar Excel |
| Se agrega una nueva zona | Agregar seccion en CONSOLIDADO + filas en Excel |
| Se reemplazan valores Proxy por datos reales | Actualizar estado en ambos archivos |
| Cambia la metodologia | Actualizar nota metodologica en ambos |
| Se agregan nuevos indicadores | Agregar filas en CONSOLIDADO + Excel |

---

## Reglas de Sincronizacion

1. El `CONSOLIDADO_ITT_ZONAS.txt` es la **fuente principal** — siempre se actualiza primero
2. El `ITT_Seguimiento_Datasets.xlsx` se **deriva** del consolidado — nunca al reves
3. Ambos archivos deben reflejar el mismo estado en todo momento
4. Los valores Proxy se marcan con `**` en ambos archivos
5. Cualquier cambio metodologico debe reflejarse en la nota metodologica de ambos

---

## Archivos Relacionados

| Archivo | Rol |
|---|---|
| `outputs/CONSOLIDADO_ITT_ZONAS.txt` | Fuente de verdad del estado del proyecto |
| `ITT_Seguimiento_Datasets.xlsx` | Tracker operativo derivado del consolidado |
| `docs/05_nota_metodologica_proxy_2026.md` | Detalle metodologico de valores Proxy |
| `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md` | Metodologia completa del ITT |
| `.kiro/steering/proyecto_itt.md` | Reglas del proyecto para el agente |
