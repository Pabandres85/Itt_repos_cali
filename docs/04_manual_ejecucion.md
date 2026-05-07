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
- Roosevelt sigue pendiente de datos.

## 3. Ejecutar notebooks por zona

Orden sugerido:

```text
notebooks/01_itt_roosevelt.ipynb
notebooks/02_itt_avenida_ciudad_de_cali.ipynb
notebooks/03_itt_barrio_obrero.ipynb
```

Estado recomendado de uso:

- `01_itt_roosevelt.ipynb`: plantilla.
- `02_itt_avenida_ciudad_de_cali.ipynb`: funcional, pero pendiente de migracion a `ref_min/ref_max`.
- `03_itt_barrio_obrero.ipynb`: referencia actual de implementacion.

## 4. Criterio metodologico

Metodo vigente:

- Usar `ref_min/ref_max` fijos por indicador.
- Mantener como provisionales las dimensiones con referentes de Pulmon de Oriente.
- No usar min-max relativo para la muestra de una zona pequena.

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

## 6. Ejecutar comparativo

Luego ejecutar:

```text
notebooks/04_comparativo_itt_zonas.ipynb
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
