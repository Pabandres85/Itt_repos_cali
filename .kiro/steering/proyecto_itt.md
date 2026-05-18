# Steering — Proyecto ITT Transformacion Territorial

## Entorno de desarrollo

- Sistema operativo: Windows
- Gestor de paquetes Python: **uv**
- Ejecucion de scripts: `uv run notebooks_py/<script>.py`
- No usar pip directamente; uv gestiona dependencias via PEP 723 inline metadata
- Los notebooks .ipynb se ejecutan en Google Colab (Linux)
- Los scripts .py se ejecutan localmente con uv

## Proyecto

- Repositorio: `Itt_repos_cali` (fork de j0rg3c45, upstream Pabandres85)
- Rama de trabajo: `jorge_itt`
- Objetivo: Calcular el ITT (Indice de Transformacion Territorial) para zonas urbanas de Cali
- Metodologia: ref_min/ref_max fijos, 5 dimensiones ponderadas (Seg 30%, Mov 25%, Entorno 20%, Educ 13%, Cohesion 12%)

## Zonas

| Zona | Notebook | Script .py | Periodo |
|---|---|---|---|
| Roosevelt | 01_itt_roosevelt_v2.ipynb | notebooks_py/01_itt_roosevelt.py | 2023-2025 (datos reales) |
| Av. Ciudad de Cali | 02_itt_avenida_ciudad_de_cali.ipynb | — | 2023-2025 |
| Barrio Obrero | 03_itt_barrio_obrero.ipynb | notebooks_py/03_itt_barrio_obrero.py | 2023-2026 (Q1 2026 real, sin Proxy) |
| Pulmon de Oriente | 04_itt_pulmon_oriente_2026_v2.ipynb | notebooks_py/04_itt_pulmon_oriente_2025.py | 2023-2026 (Q1 real, Q2-Q4 Proxy**) |

## Terminologia unificada

- **PROXY** = cualquier valor que no viene de datos reales observados de la zona (score fijo heredado, promedio historico, calculo experimental)
- **COMPLETA** = datos reales propios
- **PARCIAL** = mezcla de datos reales + Proxy
- Los valores Proxy se marcan con doble asterisco (**) en tablas, graficos, etiquetas y leyendas

## Archivos clave

- Metodologia: `agent/knowledge_base/Guia_ITT_Metodologia_Notebook.md`
- Contexto maestro: `agent/context/contexto_agente_master.md`
- Consolidado: `outputs/CONSOLIDADO_ITT_ZONAS.txt`
- Nota Proxy: `docs/05_nota_metodologica_proxy_2026.md`

## Reglas

- Los archivos .md deben mantenerse sincronizados con los calculos y notebooks
- Siempre hacer push a la rama `jorge_itt` (nunca a main/master)
- Remote origin: `https://github.com/j0rg3c45/Itt_repos_cali.git`
- No usar min-max relativo para normalizar indicadores
- Distinguir siempre entre dato real, valor Proxy y resultado calculado

## Regla de periodos y Proxy

- **Informacion general (anual):** Solo mostrar años con datos completos reales. No incluir un año si no tiene datos reales completos para esa zona.
- **Indicadores por trimestre:** Cuando una zona tenga datos reales de algun trimestre de un año (ej: Pulmon de Oriente con Q1 2026), mostrar la serie trimestral completa con los datos disponibles + Proxy** para los faltantes. Tablas y graficos de tendencia claros.
- **Roosevelt:** Solo 2023-2025 (no tiene datos 2026). Sin Proxy.
- **Barrio Obrero:** 2023-2026 (Q1 2026 real, sin Proxy). Analisis anual solo 2023-2025; serie trimestral incluye Q1 2026 real. Heatmaps y barras trimestrales usan 4to color naranja (#FF6F00) para 2026.
- **Pulmon de Oriente:** 2023-2025 anual completo + serie trimestral 2023-2026 (Q1 real, Q2-Q4 Proxy**).
