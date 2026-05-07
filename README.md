# ITT — Transformación Territorial

Proyecto base para calcular y comparar el **Índice de Transformación Territorial (ITT)** en tres zonas de ciudad:

1. ITT Roosevelt
2. ITT Avenida Ciudad de Cali
3. ITT Barrio Obrero

La estructura está diseñada para trabajar de forma sencilla:

- Un notebook por cada zona.
- Un notebook consolidado para comparar los resultados.
- Una carpeta de datos por cada ITT.
- Una carpeta de salidas por cada ITT.
- Documentación mínima de metodología, fuentes y ejecución.
- Carpeta de agente para guardar contexto, prompts y conocimiento base.

## Estructura del proyecto

```text
itt-transformacion-territorial/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── itt_roosevelt/
│   ├── itt_avenida_ciudad_de_cali/
│   ├── itt_barrio_obrero/
│   └── referencia/
│
├── notebooks/
│   ├── 01_itt_roosevelt.ipynb
│   ├── 02_itt_avenida_ciudad_de_cali.ipynb
│   ├── 03_itt_barrio_obrero.ipynb
│   └── 04_comparativo_itt_zonas.ipynb
│
├── outputs/
│   ├── itt_roosevelt/
│   ├── itt_avenida_ciudad_de_cali/
│   ├── itt_barrio_obrero/
│   └── consolidado/
│
├── docs/
│   ├── 01_contexto_proyecto.md
│   ├── 02_metodologia_itt.md
│   ├── 03_fuentes_datos.md
│   └── 04_manual_ejecucion.md
│
└── agent/
    ├── context/
    ├── prompts/
    └── knowledge_base/
```

## Orden sugerido de ejecución

1. Cargar los datos fuente en `data/`.
2. Ejecutar el notebook de cada ITT:
   - `notebooks/01_itt_roosevelt.ipynb`
   - `notebooks/02_itt_avenida_ciudad_de_cali.ipynb`
   - `notebooks/03_itt_barrio_obrero.ipynb`
3. Guardar los resultados en la carpeta correspondiente dentro de `outputs/`.
4. Ejecutar `notebooks/04_comparativo_itt_zonas.ipynb`.
5. Usar la carpeta `agent/` para alimentar un agente con contexto metodológico y resultados.

## Recomendación

Mantener los nombres de carpetas sin espacios facilita el trabajo con Python, Git, rutas relativas y notebooks.
