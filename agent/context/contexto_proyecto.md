# Contexto para agente - Proyecto ITT

Este agente apoya consulta, interpretacion y explicacion del **Indice de Transformacion Territorial (ITT)** dentro del repositorio `itt-transformacion-territorial`.

## Objetivo del proyecto

Calcular el ITT para zonas de intervencion urbana en Cali y comparar resultados entre zonas.

## Zonas del repo

- ITT Roosevelt.
- Avenida Ciudad de Cali.
- Barrio Obrero.

## Estado actual

- `01_itt_roosevelt.ipynb`: plantilla.
- `02_itt_avenida_ciudad_de_cali.ipynb`: implementado, pero aun usa min-max relativo en la normalizacion de indicadores reales.
- `03_itt_barrio_obrero.ipynb`: implementado y alineado con `ref_min/ref_max` fijos.
- `04_comparativo_itt_zonas.ipynb`: plantilla comparativa.

## Regla metodologica para agentes

La referencia metodologica vigente del proyecto esta en:

- `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`

Los agentes deben asumir como correcto:

- Uso de `ref_min/ref_max` fijos.
- Referentes provisionales para dimensiones sin datos propios.
- Necesidad de escalar refs segun tamano de zona.

Los agentes no deben asumir como vigente:

- Min-max relativo como metodo recomendado general.

## Uso esperado por el agente

El agente debe diferenciar entre:

- Metodologia vigente.
- Implementacion ya migrada.
- Implementacion pendiente de migrar.
- Datos presentes en el repo.
- Datos esperados pero no versionados.
