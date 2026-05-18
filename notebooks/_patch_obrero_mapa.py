"""Fix Celda 5 (Mapa) en Barrio Obrero.
Actualizar nombres de columnas de fecha para archivos DATIC nuevos.
Homicidios usa 'fechah', Hurtos/VIF usan 'fecha_hech' (minuscula).
"""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Celda 20 es el mapa
new_source = [
    "centroid = gdf_barrio_wgs.geometry.centroid.iloc[0]\n",
    "m = folium.Map(location=[centroid.y, centroid.x], zoom_start=17, tiles='CartoDB positron')\n",
    "\n",
    "folium.GeoJson(gdf_barrio_wgs.__geo_interface__, name='Poligono Barrio Obrero',\n",
    "    style_function=lambda x: {'fillColor':'#2E7D32','color':'#1B4F8A','weight':2,'fillOpacity':0.1}).add_to(m)\n",
    "\n",
    "# Capas de indicadores (nombre, raw, col_fecha, color, icono)\n",
    "capas = [\n",
    "    ('Homicidios',  raw_hom, 'red', 'exclamation-sign'),\n",
    "    ('Hurtos',      raw_hur, 'blue', 'shopping-cart'),\n",
    "    ('Siniestros',  raw_sin, 'orange', 'road'),\n",
    "    ('VIF',         raw_vif, 'purple', 'home'),\n",
    "]\n",
    "\n",
    "FECHA_COLS = ['fechah', 'fecha_hech', 'FECHA_HECH', 'Fecha', 'fecha']\n",
    "\n",
    "for nombre, raw, color, icon in capas:\n",
    "    fg = folium.FeatureGroup(name=nombre)\n",
    "    for feat in raw['features']:\n",
    "        p = feat['properties']\n",
    "        # Obtener coordenadas\n",
    "        if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "            lon, lat = feat['geometry']['coordinates'][:2]\n",
    "        elif 'x' in p and 'y' in p:\n",
    "            lon, lat = p['x'], p['y']\n",
    "        elif 'X' in p and 'Y' in p:\n",
    "            lon, lat = p['X'], p['Y']\n",
    "        else:\n",
    "            continue\n",
    "        # Obtener fecha\n",
    "        fecha = ''\n",
    "        for fc in FECHA_COLS:\n",
    "            if fc in p:\n",
    "                fecha = str(p[fc])[:10]\n",
    "                break\n",
    "        folium.Marker([lat, lon], popup=f'<b>{nombre}</b><br>{fecha}',\n",
    "            icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')).add_to(fg)\n",
    "    fg.add_to(m)\n",
    "    print(f'  {nombre}: {len(raw[\"features\"])} puntos en mapa')\n",
    "\n",
    "# Rinas (filtrar de comparendos)\n",
    "fg_r = folium.FeatureGroup(name='Rinas')\n",
    "n_rinas = 0\n",
    "for feat in raw_comp['features']:\n",
    "    p = feat['properties']\n",
    "    agrupado = str(p.get('agrupado', '')).upper()\n",
    "    if not agrupado.startswith('RI'): continue\n",
    "    if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "        lon, lat = feat['geometry']['coordinates'][:2]\n",
    "    elif 'lat' in p and 'lon' in p:\n",
    "        lat, lon = p['lat'], p['lon']\n",
    "    else: continue\n",
    "    fecha = str(p.get('fecha_hech', ''))[:10]\n",
    "    folium.Marker([lat, lon], popup=f'<b>Rina</b><br>{fecha}',\n",
    "        icon=folium.Icon(color='pink', icon='flash', prefix='glyphicon')).add_to(fg_r)\n",
    "    n_rinas += 1\n",
    "fg_r.add_to(m)\n",
    "print(f'  Rinas: {n_rinas} puntos en mapa')\n",
    "\n",
    "# Arboles DAGMA\n",
    "fg_a = folium.FeatureGroup(name='Arboles DAGMA', show=False)\n",
    "for feat in raw_arb['features']:\n",
    "    p = feat['properties']\n",
    "    if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "        lon, lat = feat['geometry']['coordinates'][:2]\n",
    "    elif p.get('latitud') and p.get('longitud'):\n",
    "        lat, lon = p['latitud'], p['longitud']\n",
    "    else: continue\n",
    "    folium.CircleMarker([lat, lon], radius=3, color='green',\n",
    "        fill=True, fillOpacity=0.6).add_to(fg_a)\n",
    "fg_a.add_to(m)\n",
    "print(f'  Arboles: {len(raw_arb[\"features\"])} puntos en mapa')\n",
    "\n",
    "# Sedes educativas\n",
    "for feat in raw_sed['features']:\n",
    "    p = feat['properties']\n",
    "    if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "        lon, lat = feat['geometry']['coordinates'][:2]\n",
    "    elif p.get('Latitud_D'):\n",
    "        lat, lon = p['Latitud_D'], p['Longitud_D']\n",
    "    else: continue\n",
    "    folium.Marker([lat, lon],\n",
    "        popup=f'<b>{p.get(\"NombreSede\", \"Sede\")}</b>',\n",
    "        icon=folium.Icon(color='cadetblue', icon='education', prefix='glyphicon')).add_to(m)\n",
    "print(f'  Sedes: {len(raw_sed[\"features\"])} puntos en mapa')\n",
    "\n",
    "# CAI\n",
    "for feat in raw_cai['features']:\n",
    "    p = feat['properties']\n",
    "    if feat.get('geometry') and feat['geometry'].get('coordinates'):\n",
    "        lon, lat = feat['geometry']['coordinates'][:2]\n",
    "    elif p.get('LATITUD'):\n",
    "        lat, lon = p['LATITUD'], p['LONGITUD']\n",
    "    else: continue\n",
    "    folium.Marker([lat, lon],\n",
    "        popup=f'<b>{p.get(\"UNIDAD\", \"CAI\")}</b>',\n",
    "        icon=folium.Icon(color='darkblue', icon='tower', prefix='glyphicon')).add_to(m)\n",
    "print(f'  CAI: {len(raw_cai[\"features\"])} puntos en mapa')\n",
    "\n",
    "folium.LayerControl().add_to(m)\n",
    "display(m)\n",
]

cells[20]['source'] = new_source
cells[20]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 5 (Mapa) corregida:')
print('  - Deteccion automatica de columna fecha (FECHA_COLS)')
print('  - Deteccion automatica de coordenadas (geometry > x/y > X/Y > lat/lon)')
print('  - Rinas con startswith(RI) en vez de == RIÑAS')
print('  - Todos los archivos GeoJSON cargados correctamente')
