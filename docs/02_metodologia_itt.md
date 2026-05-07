# Metodología ITT

El **Índice de Transformación Territorial (ITT)** mide el grado de transformación positiva de un territorio en una escala de 0 a 100.

## Dimensiones base

| Dimensión | Peso sugerido | Tipo general |
|---|---:|---|
| Seguridad | 30% | Inverso |
| Movilidad | 25% | Inverso |
| Entorno Urbano | 20% | Positivo o referente |
| Educación y Desarrollo | 13% | Mixto o referente |
| Cohesión Social | 12% | Inverso / neutro |

La suma de los pesos debe ser igual a 1.0 o 100%.

## Normalización min-max

Para indicadores donde un mayor valor significa mejor resultado:

```text
Score = ((X - Xmin) / (Xmax - Xmin)) * 100
```

Para indicadores donde un menor valor significa mejor resultado:

```text
Score = 100 - ((X - Xmin) / (Xmax - Xmin)) * 100
```

El resultado debe limitarse al rango 0 a 100.

## Score por dimensión

Cada dimensión puede calcularse como el promedio simple de sus indicadores normalizados:

```text
Score_dimensión = promedio(scores_indicadores)
```

## Cálculo del ITT

```text
ITT = 0.30*Seguridad + 0.25*Movilidad + 0.20*Entorno_Urbano + 0.13*Educación_Desarrollo + 0.12*Cohesión_Social
```

## Clasificación sugerida

| Rango | Nivel |
|---:|---|
| 0 - 40 | Emergencia |
| 40 - 60 | Consolidación |
| 60 - 80 | Avance |
| 80 - 100 | Transformación |
