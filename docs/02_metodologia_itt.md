# Metodologia ITT

El **Indice de Transformacion Territorial (ITT)** mide el grado de transformacion positiva de un territorio en una escala de 0 a 100.

## Dimensiones y pesos

| Dimension | Peso | Tipo general |
|---|---:|---|
| Seguridad | 30% | Inverso |
| Movilidad | 25% | Inverso |
| Entorno Urbano | 20% | Referente o positivo |
| Educacion y Desarrollo | 13% | Referente o mixto |
| Cohesion Social | 12% | Inverso / neutro |

La suma de pesos debe ser 1.0.

## Regla metodologica vigente

El proyecto debe usar **umbrales fijos `ref_min/ref_max` por indicador**.

No se debe usar min-max relativo calculado desde la propia muestra de la zona cuando el territorio es pequeno o los conteos son bajos, porque eso produce scores artificialmente extremos.

## Normalizacion correcta

```python
def score_ref(valor, ref_min, ref_max, inverso):
    if ref_max == ref_min:
        return 100.0
    raw = np.clip((valor - ref_min) / (ref_max - ref_min) * 100, 0, 100)
    return 100 - raw if inverso else raw
```

Interpretacion:

- Indicador inverso: menor valor = mejor score.
- Indicador positivo: mayor valor = mejor score.

## Scores por dimension

Cada dimension se calcula como promedio simple de sus indicadores.

Ejemplos:

```text
Seguridad = promedio(Homicidios, Hurtos)
Movilidad = promedio(Siniestralidad, Lesionados, Mortales)
Cohesion = promedio(VIF, Rinas, Vulnerabilidad)
```

## ITT compuesto

```text
ITT = 0.30*Seguridad
    + 0.25*Movilidad
    + 0.20*Entorno_Urbano
    + 0.13*Educacion_Desarrollo
    + 0.12*Cohesion_Social
```

## Referentes provisionales actuales

Mientras una zona no tenga datos propios para ciertas dimensiones, el proyecto usa scores referentes del ITT Pulmon de Oriente:

| Elemento | Valor referente |
|---|---:|
| Entorno Urbano | 39.2 |
| Educacion y Desarrollo | 54.9 |
| Vulnerabilidad en Cohesion | 54.1 |

Estos valores deben quedar marcados como provisionales en resultados y documentacion.

## Clasificacion

| Rango | Nivel |
|---:|---|
| 0 - 40 | Emergencia |
| 40 - 60 | Consolidacion |
| 60 - 80 | Avance |
| 80 - 100 | Transformacion |

## Estado de implementacion en notebooks

- `03_itt_barrio_obrero.ipynb` ya sigue este metodo.
- `02_itt_avenida_ciudad_de_cali.ipynb` aun debe migrarse a este metodo.
- `01_itt_roosevelt.ipynb` sigue siendo plantilla.

## Referencia principal

La guia metodologica mas completa y vigente del proyecto esta en:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`
