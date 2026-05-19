# =============================================================================
# CORRECCIONES para que Celda 5 (Mapa) y Celda 15 (Excel) usen valores unicos
# =============================================================================
# Estas correcciones se aplican DESPUES de ejecutar la Celda 6 con deduplicacion.
# =============================================================================


# =============================================================================
# CELDA 5 — Mapa de geolocalizacion (CORREGIDA)
# =============================================================================
# Reemplazar la seccion donde se pintan los puntos en el mapa.
# En vez de iterar sobre raw_hom['features'], raw_hur['features'], etc.,
# usamos los DataFrames deduplicados (df_hom, df_hur, df_vif).
#
# NOTA: La Celda 6 debe ejecutarse ANTES de la Celda 5, o bien,
# mover la deduplicacion antes del mapa.
#
# Si el orden del notebook es: Celda 4 (carga) -> Celda 5 (mapa) -> Celda 6 (proceso),
# entonces hay dos opciones:
#   A) Mover la Celda 6 ANTES de la Celda 5
#   B) Hacer la deduplicacion dentro de la Celda 5 tambien
#
# OPCION RECOMENDADA: Mover Celda 6 antes de Celda 5.
# Si no es posible, usar este bloque en la Celda 5:
# =============================================================================

# --- Reemplazo para la seccion de capas en Celda 5 ---
# Donde antes decia:
#   capas = [
#       ('Homicidios', raw_hom, 'red', 'exclamation-sign'),
#       ('Hurtos',     raw_hur, 'blue', 'shopping-cart'),
#       ('VIF',        raw_vif, 'purple', 'home'),
#   ]
#   for nombre, raw, color, icon in capas:
#       fg = folium.FeatureGroup(name=nombre, show=False)
#       for feat in raw['features']:
#           ...
#
# Reemplazar con:

capas_df = [
    ('Homicidios', df_hom, 'red', 'exclamation-sign'),
    ('Hurtos',     df_hur, 'blue', 'shopping-cart'),
    ('VIF',        df_vif, 'purple', 'home'),
]
for nombre, df_capa, color, icon in capas_df:
    fg = folium.FeatureGroup(name=nombre, show=False)
    for _, row in df_capa.iterrows():
        lat, lon = row.get('_lat'), row.get('_lon')
        if pd.notna(lat) and pd.notna(lon):
            popup_text = f"<b>{nombre}</b><br>{row.get('_fecha', '')}"
            folium.Marker(
                [lat, lon],
                icon=folium.Icon(color=color, icon=icon, prefix='glyphicon'),
                popup=popup_text
            ).add_to(fg)
    fg.add_to(m)
    print(f'  {nombre}: {len(df_capa)} puntos unicos en mapa')

# Arboles (deduplicados)
if not df_arb.empty:
    fg_a = folium.FeatureGroup(name='Arboles', show=False)
    for _, row in df_arb.iterrows():
        lat, lon = row.get('_lat'), row.get('_lon')
        if pd.notna(lat) and pd.notna(lon):
            folium.CircleMarker([lat, lon], radius=3, color='green',
                fill=True, fillOpacity=0.6).add_to(fg_a)
    fg_a.add_to(m)

# Sedes educativas (deduplicadas)
if not df_sed.empty:
    for _, row in df_sed.iterrows():
        lat, lon = row.get('_lat'), row.get('_lon')
        if pd.notna(lat) and pd.notna(lon):
            folium.Marker([lat, lon],
                icon=folium.Icon(color='orange', icon='education', prefix='glyphicon'),
                popup=f"Sede: {row.get('nombre', row.get('NOMBRE', 'N/A'))}"
            ).add_to(m)

# CAI (deduplicados)
if not df_cai.empty:
    for _, row in df_cai.iterrows():
        lat, lon = row.get('_lat'), row.get('_lon')
        if pd.notna(lat) and pd.notna(lon):
            folium.Marker([lat, lon],
                icon=folium.Icon(color='darkblue', icon='tower', prefix='glyphicon'),
                popup=f"CAI: {row.get('nombre', row.get('NOMBRE', 'N/A'))}"
            ).add_to(m)


# =============================================================================
# CELDA 15 — Exportar a Excel (CORRECCION)
# =============================================================================
# Donde antes decia:
#   est = pd.DataFrame({'Elemento':['Arboles','Sedes Educativas','CAI/MECAL'],
#       'Cantidad':[len(raw_arb['features']),len(raw_sed['features']),len(raw_cai['features'])]})
#
# Reemplazar con:

est = pd.DataFrame({
    'Elemento': ['Arboles', 'Sedes Educativas', 'CAI/MECAL'],
    'Cantidad': [len(df_arb), len(df_sed), len(df_cai)]
})
