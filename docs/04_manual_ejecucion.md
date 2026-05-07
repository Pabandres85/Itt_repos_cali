# Manual de ejecución

## 1. Preparar ambiente

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 2. Cargar datos

Ubicar los archivos de cada zona en:

```text
data/itt_roosevelt/
data/itt_avenida_ciudad_de_cali/
data/itt_barrio_obrero/
```

## 3. Ejecutar notebooks por zona

Ejecutar en este orden:

```text
notebooks/01_itt_roosevelt.ipynb
notebooks/02_itt_avenida_ciudad_de_cali.ipynb
notebooks/03_itt_barrio_obrero.ipynb
```

Cada notebook debe exportar sus resultados a:

```text
outputs/itt_roosevelt/
outputs/itt_avenida_ciudad_de_cali/
outputs/itt_barrio_obrero/
```

## 4. Ejecutar comparativo

Luego ejecutar:

```text
notebooks/04_comparativo_itt_zonas.ipynb
```

Este notebook debe leer los resultados de las tres zonas y generar archivos consolidados en:

```text
outputs/consolidado/
```

## 5. Alimentar agente

Copiar documentación, resultados y resúmenes a:

```text
agent/knowledge_base/
```

Actualizar los archivos de contexto en:

```text
agent/context/
```
