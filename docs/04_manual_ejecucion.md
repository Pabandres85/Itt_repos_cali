# Manual de ejecucion

## 1. Preparar ambiente

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Librerias base del proyecto:

- `pandas`
- `numpy`
- `geopandas`
- `pyproj`
- `shapely`
- `matplotlib`
- `seaborn`
- `folium`
- `openpyxl`

## 2. Preparar datos

Ubicar los insumos de cada zona en:

```text
data/itt_roosevelt/
data/itt_avenida_ciudad_de_cali/
data/itt_barrio_obrero/
```

Notas practicas:

- Barrio Obrero hoy tiene `obrero.zip` dentro del repo.
- Avenida Ciudad de Cali no tiene los GeoJSON fuente versionados en el repo.
- Roosevelt ya tiene `Roosevelt.zip` y una carpeta descomprimida de trabajo en `data/itt_roosevelt/Roosevelt_unzipped/`.

## 3. Ejecutar notebooks por zona

Orden sugerido:

```text
notebooks/01_itt_roosevelt.ipynb
notebooks/02_itt_avenida_ciudad_de_cali.ipynb
notebooks/03_itt_barrio_obrero.ipynb
```

Estado recomendado de uso:

- `01_itt_roosevelt.ipynb`: implementado y alineado con la estructura de Barrio Obrero.
- `02_itt_avenida_ciudad_de_cali.ipynb`: funcional, pero pendiente de migracion a `ref_min/ref_max`.
- `03_itt_barrio_obrero.ipynb`: referencia actual de implementacion.

Nota operativa para Roosevelt:

- Mantener la convencion `año` en las tablas del notebook para evitar inconsistencias entre celdas.
- Si se ejecuta en Colab despues de cambios locales, conviene reiniciar entorno y correr desde la celda que construye `base`.

Nota operativa para Barrio Obrero:

- En Colab, el flujo reciente ha sido clonar el repo en `/content/itt_repos_cali`.
- Luego se descomprime `data/itt_barrio_obrero/obrero.zip` a `/content/obrero`.
- La ruta base de trabajo resultante queda en `/content/obrero/obrero/Geojson_Barrio_Obrero/`.
- El notebook incluye `Celda 3B` para recalcular `Entorno Urbano` con `deficit habitacional` y `Celda 3C` para visualizar sus componentes 2024.

## 4. Criterio metodologico

Metodo vigente:

- Usar `ref_min/ref_max` fijos por indicador.
- Mantener como provisionales las dimensiones con referentes de Pulmon de Oriente.
- No usar min-max relativo para la muestra de una zona pequena.
- En Barrio Obrero, `Entorno Urbano` puede sobrescribir el referente fijo con un proxy experimental de `Comuna 9` usando `BD_DEFICIT_HABITACIONAL_COM_CORREG_2024 (1).xlsx`.
- Ese proxy de `Entorno Urbano` es anual `2024`; no debe presentarse como serie mensual o trimestral observada.

Referencia principal:

```text
agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md
```

## 5. Exportar resultados

Cada notebook debe exportar sus salidas a:

```text
outputs/itt_roosevelt/
outputs/itt_avenida_ciudad_de_cali/
outputs/itt_barrio_obrero/
```

Hoy el repo no contiene outputs generados; solo la estructura base.

## 5.1 Aplicar scripts auxiliares en Colab (Pulmon de Oriente)

Para el notebook `04_itt_pulmon_oriente_2026_v2.ipynb`, los scripts auxiliares en `notebooks/` contienen la logica actualizada:

1. Ejecutar el notebook hasta Celda 5 normalmente
2. Reemplazar **Celda 6** con el contenido de `notebooks/celda6_procesamiento_dedup.py`
3. Reemplazar **Celda 7** con el contenido de `notebooks/celda7_normalizacion_itt.py`
4. Re-ejecutar desde Celda 6 en adelante
5. Los graficos mostraran 4 trimestres completos para 2026 (Q1 real + Q2-Q4 Proxy**)

Estos scripts garantizan:
- Deduplicacion por fecha+coordenada
- Generacion de valores Proxy para Q2-Q4 2026
- Normalizacion con 4 trimestres completos
- Visualizaciones con serie temporal continua

## 6. Ejecutar comparativo

Luego ejecutar:

```text
notebooks/05_comparativo_itt_zonas.ipynb
```

Condicion para que tenga sentido:

- Deben existir resultados homologos de las zonas a comparar.

Las salidas consolidadas van en:

```text
outputs/consolidado/
```

## 7. Alimentar agentes

Actualizar estas carpetas despues de cambios metodologicos o nuevos resultados:

```text
agent/context/
agent/knowledge_base/
```

Minimo recomendado para agentes:

- Contexto del proyecto.
- Estado de notebooks y zonas.
- Metodologia vigente.
- Fuentes disponibles y faltantes.
- Resultados exportados.

## 8. Valores Proxy 2026

Para Pulmon de Oriente, los trimestres Q2, Q3 y Q4 de 2026 no tienen datos reales. El notebook `04_itt_pulmon_oriente_2026_v2.ipynb` genera automaticamente valores Proxy basados en el promedio historico trimestral de 2023-2025.

Reglas:
- Los valores Proxy se marcan con doble asterisco (`**`) en todas las salidas.
- Deben reemplazarse por datos reales en cuanto esten disponibles.
- La logica de calculo esta en `notebooks/celda6_procesamiento_dedup.py`.

> **Nota metodologica:** Los valores correspondientes a los trimestres Q2, Q3 y Q4 del año 2026 fueron estimados mediante valores Proxy calculados a partir de la linea base historica de los años 2023–2025, con el fin de normalizar la informacion y garantizar comparabilidad estadistica y visual en el analisis.

## 9. Sincronizacion de documentacion

Los archivos `.md` son la fuente principal de documentacion del proyecto. Cada ajuste implementado en calculos, tablas o graficos debe reflejarse inmediatamente en los `.md`. No debe existir informacion desactualizada entre los datos procesados y la documentacion.
