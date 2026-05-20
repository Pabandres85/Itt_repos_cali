import json

nb = json.load(open(r'notebooks\04_itt_pulmon_oriente_2026_v2.ipynb', 'r', encoding='utf-8'))

# Full cell 16 source
src16 = ''.join(nb['cells'][16]['source'])
lines = src16.split('\n')
print(f"Cell 16 total lines: {len(lines)}")

# Find PROXY section
for i, line in enumerate(lines):
    if 'PROXY' in line.upper() or 'proxy' in line:
        print(f"  Line {i}: {line[:100]}")

# Print from line where PROXY starts
proxy_start = None
for i, line in enumerate(lines):
    if '====' in line and 'PROXY' in line.upper():
        proxy_start = i
        break

if proxy_start:
    print(f"\n=== PROXY section starts at line {proxy_start} ===")
    print('\n'.join(lines[proxy_start:]))
else:
    print("\nNo PROXY section found with ==== marker")
    # Try alternative
    for i, line in enumerate(lines):
        if 'proxy' in line.lower() and i > len(lines)//2:
            print(f"\n=== From line {i}: ===")
            print('\n'.join(lines[i:i+5]))
            break

# Also check what's before the proxy section (last 5 lines before)
if proxy_start:
    print(f"\n=== 5 lines before PROXY (lines {proxy_start-5} to {proxy_start-1}) ===")
    print('\n'.join(lines[proxy_start-5:proxy_start]))
