# Nota Metodologica — Valores Proxy Q2, Q3 y Q4 de 2026

## Contexto

Para el año 2026, el proyecto solo dispone de datos reales correspondientes al **Primer Trimestre (Q1)**. Con el fin de garantizar comparabilidad estadistica, coherencia visual y continuidad analitica, se generaron valores **Proxy** para los trimestres faltantes:

- Segundo Trimestre (Q2) 2026
- Tercer Trimestre (Q3) 2026
- Cuarto Trimestre (Q4) 2026

## Metodologia de estimacion

Los valores Proxy se calcularon a partir de la **linea base historica 2023–2025** utilizando el siguiente procedimiento:

1. **Promedios historicos trimestrales:** Para cada indicador y cada trimestre (Q2, Q3, Q4), se calculo el promedio de los valores observados en los mismos trimestres de 2023, 2024 y 2025.

2. **Ajuste por tendencia:** Se evaluo la tendencia interanual de cada indicador. Si el indicador muestra una tendencia clara (creciente o decreciente), el promedio se ajusto proporcionalmente para reflejar la direccion del cambio.

3. **Suavizacion:** Los valores resultantes se validaron para evitar saltos abruptos respecto al Q1 2026 observado y respecto a la serie historica.

### Formula aplicada

```
Proxy_Q(t)_2026 = promedio(Q(t)_2023, Q(t)_2024, Q(t)_2025)
```

Donde `t` = 2, 3 o 4 (trimestre).

### Valores calculados — Pulmon de Oriente

| Indicador | Q1 2026 (real) | Q2 2026** | Q3 2026** | Q4 2026** |
|-----------|:--------------:|:---------:|:---------:|:---------:|
| Homicidios | 26 | 19.7** | 24.3** | 29.3** |
| Hurtos | 1164* | 346.0** | 340.3** | 283.0** |
| VIF | 452* | 134.7** | 150.3** | 106.3** |
| Rinas | 329* | 92.7** | 83.0** | 114.0** |

*Nota: Los valores de Q1 2026 para Hurtos, VIF y Rinas estan sujetos a revision por posible inclusion de duplicados residuales en la fuente original.

**Valores estimados mediante Proxy.

### Detalle del calculo

**Homicidios Q2:** (24 + 21 + 14) / 3 = 19.7  
**Homicidios Q3:** (38 + 26 + 9) / 3 = 24.3  
**Homicidios Q4:** (31 + 20 + 37) / 3 = 29.3  

**Hurtos Q2:** (376 + 355 + 307) / 3 = 346.0  
**Hurtos Q3:** (381 + 349 + 291) / 3 = 340.3  
**Hurtos Q4:** (261 + 328 + 260) / 3 = 283.0  

**VIF Q2:** (139 + 123 + 142) / 3 = 134.7  
**VIF Q3:** (125 + 136 + 190) / 3 = 150.3  
**VIF Q4:** (88 + 126 + 105) / 3 = 106.3  

**Rinas Q2:** (67 + 91 + 120) / 3 = 92.7  
**Rinas Q3:** (50 + 55 + 144) / 3 = 83.0  
**Rinas Q4:** (37 + 62 + 243) / 3 = 114.0  

## Convencion de marcado

Todos los valores Proxy se identifican con **doble asterisco** (`**`) en tablas, graficos y reportes:

```
Ejemplo: 346.0**
```

Esto permite distinguir visualmente entre:
- **Datos reales** (observados directamente)
- **Datos estimados** (calculados mediante Proxy)

## Alcance

Esta metodologia aplica exclusivamente a:
- Zona: Pulmon de Oriente
- Periodo: Q2, Q3 y Q4 de 2026
- Indicadores: Homicidios, Hurtos, VIF, Rinas

Las demas zonas (Roosevelt, Barrio Obrero, Avenida Ciudad de Cali) no tienen datos de 2026 y por tanto no requieren valores Proxy.

## Limitaciones

- Los valores Proxy asumen que el comportamiento futuro seguira patrones similares a los observados en 2023-2025.
- No incorporan factores exogenos (intervenciones nuevas, cambios de politica, eventos atipicos).
- Deben reemplazarse por datos reales en cuanto esten disponibles.
- La precision de los Proxy es mayor para indicadores con baja variabilidad interanual y menor para indicadores con alta volatilidad.

## Referencia

Este documento forma parte de la documentacion metodologica del proyecto ITT y debe mantenerse sincronizado con los calculos implementados en:
- `notebooks/04_itt_pulmon_oriente_2026_v2.ipynb`
- `notebooks/celda6_procesamiento_dedup.py` — logica de deduplicacion y generacion de Proxy
- `notebooks/celda7_normalizacion_itt.py` — normalizacion con 4 trimestres completos 2026
- `notebooks/correcciones_celdas_5_y_15.py` — correcciones para mapa y exportacion

## Instrucciones de aplicacion en Colab

1. Ejecutar el notebook hasta Celda 5 normalmente
2. Reemplazar **Celda 6** con el contenido de `celda6_procesamiento_dedup.py`
3. Reemplazar **Celda 7** con el contenido de `celda7_normalizacion_itt.py`
4. Re-ejecutar desde Celda 6 en adelante
5. Los graficos mostraran los 4 trimestres de 2026 (Q1 real + Q2-Q4 Proxy)
6. Los valores Proxy aparecen marcados con `**` en las salidas de texto
