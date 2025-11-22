#!/usr/bin/env python3
"""
Quick script to fix the corrupted home.html file
"""

# Read the file
with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where the clean HTML ends (first </head>)
# Find where the script tags start
clean_end = None
script_start = None

for i, line in enumerate(lines):
    if '</head>' in line and clean_end is None:
        clean_end = i + 1  # Include the </head> line
    if '<!-- JavaScript files -->' in line:
        script_start = i  # Keep updating to get the LAST occurrence

print(f"Clean HTML ends at line: {clean_end}")
print(f"Script tags start at line: {script_start}")

# Keep only the clean part and the script tags
if clean_end and script_start:
    clean_html = lines[:clean_end]
    script_section = lines[script_start:]
    
    # Combine them
    fixed_html = clean_html + ['\n'] + script_section
    
    # Write the fixed file
    with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home_fixed.html', 'w', encoding='utf-8') as f:
        f.writelines(fixed_html)
    
    print(f"\n✓ Fixed file created: home_fixed.html")
    print(f"  - Kept lines 1-{clean_end} (clean HTML)")
    print(f"  - Kept lines {script_start}-{len(lines)} (script tags)")
    print(f"  - Removed {script_start - clean_end} lines of corrupted JavaScript")
    print(f"\nNext steps:")
    print(f"  1. Review home_fixed.html")
    print(f"  2. If it looks good, rename it to home.html")
else:
    print("ERROR: Could not find clean end or script start")
