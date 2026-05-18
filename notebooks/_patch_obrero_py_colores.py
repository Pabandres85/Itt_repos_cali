"""Sync colores y logica de barras en 03_itt_barrio_obrero.py con el notebook."""
from pathlib import Path

p = Path(__file__).parent.parent / 'notebooks_py' / '03_itt_barrio_obrero.py'
content = p.read_text(encoding='utf-8')

# Fix colores Seguridad
content = content.replace(
    "COLORES = ['#42A5F5', '#1B4F8A', '#E53935', '#FF6F00']",
    "COLORES_SEG = ['#90CAF9', '#42A5F5', '#1565C0', '#003366']"
)

# Fix Movilidad - reemplazar bloque completo de colores
old_cmov = "CMOV = [['#F5A742', '#D95F2B', '#B71C1C', '#FF6F00'], ['#F5A742', '#D95F2B', '#B71C1C', '#FF6F00'], ['#FF8A80', '#E53935', '#7F0000', '#FF6F00']]"
new_cmov = "COLORES_MOV = ['#FFCC80', '#FB8C00', '#E65100', '#4E2600']"
content = content.replace(old_cmov, new_cmov)

# Fix Cohesion - reemplazar colores
old_coh = "CVIF = ['#CE93D8', '#7B1FA2', '#4A148C', '#FF6F00']; CRIN = ['#F48FB1', '#D81B60', '#880E4F', '#FF6F00']"
new_coh = "COLORES_COH = ['#CE93D8', '#8E24AA', '#4A148C', '#1A0033']"
content = content.replace(old_coh, new_coh)

# Fix references in bar loops
content = content.replace("color=COLORES[idx]", "color=COLORES_SEG[idx]")
content = content.replace("c = CMOV[pi]\n", "")
content = content.replace("color=c[idx]", "color=COLORES_MOV[idx]")
content = content.replace("for ax, col, colores, tp in [(axes[0], 'vif', CVIF, 'VIF'), (axes[1], 'rinas', CRIN, 'Rinas')]:", "for ax, col, tp in [(axes[0], 'vif', 'VIF'), (axes[1], 'rinas', 'Rinas')]:")
content = content.replace("color=colores[idx]", "color=COLORES_COH[idx]")
content = content.replace("for ax, col, colores, tp in", "for ax, col, tp in")

p.write_text(content, encoding='utf-8')
print('03_itt_barrio_obrero.py: colores actualizados')
print('  COLORES_SEG = azul gradiente')
print('  COLORES_MOV = naranja gradiente')
print('  COLORES_COH = purpura gradiente')
