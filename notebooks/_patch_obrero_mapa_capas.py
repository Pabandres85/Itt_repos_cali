"""Fix: Sedes y CAI deben estar en FeatureGroup para aparecer en el control de capas."""
import json
from pathlib import Path

nb_path = Path(__file__).parent / '03_itt_barrio_obrero.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Celda 20 (mapa) - reemplazar la seccion de Sedes y CAI
source = cells[20]['source']
new_source = []
skip_sedes = False
skip_cai = False

for line in source:
    # Reemplazar seccion Sedes
    if '# Sedes educativas' in line:
        skip_sedes = True
        new_source.append("# Sedes educativas\n")
        new_source.append("fg_s = folium.FeatureGroup(name='Sedes Educativas')\n")
        new_source.append("for feat in raw_sed['features']:\n")
        new_source.append("    p = feat['properties']\n")
        new_source.append("    if feat.get('geometry') and feat['geometry'].get('coordinates'):\n")
        new_source.append("        lon, lat = feat['geometry']['coordinates'][:2]\n")
        new_source.append("    elif p.get('Latitud_D'):\n")
        new_source.append("        lat, lon = p['Latitud_D'], p['Longitud_D']\n")
        new_source.append("    else: continue\n")
        new_source.append("    folium.Marker([lat, lon],\n")
        new_source.append("        popup=f'<b>{p.get(\"NombreSede\", \"Sede\")}</b>',\n")
        new_source.append("        icon=folium.Icon(color='cadetblue', icon='education', prefix='glyphicon')).add_to(fg_s)\n")
        new_source.append("fg_s.add_to(m)\n")
        new_source.append("print(f'  Sedes: {len(raw_sed[\"features\"])} puntos en mapa')\n")
        new_source.append("\n")
        continue
    if skip_sedes:
        if '# CAI' in line:
            skip_sedes = False
        else:
            continue

    # Reemplazar seccion CAI
    if '# CAI' in line:
        skip_cai = True
        new_source.append("# CAI\n")
        new_source.append("fg_c = folium.FeatureGroup(name='CAI / MECAL')\n")
        new_source.append("for feat in raw_cai['features']:\n")
        new_source.append("    p = feat['properties']\n")
        new_source.append("    if feat.get('geometry') and feat['geometry'].get('coordinates'):\n")
        new_source.append("        lon, lat = feat['geometry']['coordinates'][:2]\n")
        new_source.append("    elif p.get('LATITUD'):\n")
        new_source.append("        lat, lon = p['LATITUD'], p['LONGITUD']\n")
        new_source.append("    else: continue\n")
        new_source.append("    folium.Marker([lat, lon],\n")
        new_source.append("        popup=f'<b>{p.get(\"UNIDAD\", \"CAI\")}</b>',\n")
        new_source.append("        icon=folium.Icon(color='darkblue', icon='tower', prefix='glyphicon')).add_to(fg_c)\n")
        new_source.append("fg_c.add_to(m)\n")
        new_source.append("print(f'  CAI: {len(raw_cai[\"features\"])} puntos en mapa')\n")
        new_source.append("\n")
        continue
    if skip_cai:
        if 'folium.LayerControl' in line:
            skip_cai = False
            new_source.append(line)
        continue

    new_source.append(line)

cells[20]['source'] = new_source
cells[20]['outputs'] = []

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print('Celda 5 (Mapa): Sedes y CAI ahora en FeatureGroup (aparecen en control de capas)')
