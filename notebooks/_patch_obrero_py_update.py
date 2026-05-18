"""Actualizar 03_itt_barrio_obrero.py con nuevas rutas y ANIOS 2026."""
from pathlib import Path

p = Path(__file__).parent.parent / 'notebooks_py' / '03_itt_barrio_obrero.py'
content = p.read_text(encoding='utf-8')

# 1. Actualizar rutas
content = content.replace('HOMICIDIOS_2023_2025_Obrero.geojson', 'DATIC_homicidios_2023_2026T1_Barrio_O.geojson')
content = content.replace('HURTOS_2023_2025_OBRERO.geojson', 'DATIC_hurtos_2023_2026T1_Barrio_O.geojson')
content = content.replace('VIOLENCIA_INTRAFAMILIAR_2023_2025_OBRERO.geojson', 'DATIC_violencia_intrafamiliar_2023_2026T1_Barrio_O.geojson')
content = content.replace('COMPARENDOS_2023_2025_OBRERO.geojson', 'DATIC_comparendos_2023_2026T1_Barrio_O.geojson')

# 2. ANIOS
content = content.replace('ANIOS = [2023, 2024, 2025]', 'ANIOS = [2023, 2024, 2025, 2026]')

# 3. Colores
content = content.replace("COLORES = ['#42A5F5', '#1B4F8A', '#E53935']", "COLORES = ['#42A5F5', '#1B4F8A', '#E53935', '#FF6F00']")

p.write_text(content, encoding='utf-8')
print('03_itt_barrio_obrero.py actualizado:')
print('  - Rutas GeoJSON -> 2026T1')
print('  - ANIOS = [2023, 2024, 2025, 2026]')
print('  - 4 colores')
