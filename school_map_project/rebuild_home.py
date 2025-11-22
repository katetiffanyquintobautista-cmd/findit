#!/usr/bin/env python3
"""
Rebuild home.html properly from the backup
"""

# Read the backup file
with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home_corrupted_backup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find key positions
first_head_close = None
first_body_start = None
second_head_close = None

for i, line in enumerate(lines):
    if '</head>' in line and first_head_close is None:
        first_head_close = i
    elif '<body>' in line and first_body_start is None:
        first_body_start = i
    elif '</head>' in line and second_head_close is None and i > first_body_start:
        second_head_close = i
        break

print(f"First </head> at line: {first_head_close + 1}")
print(f"First <body> at line: {first_body_start + 1}")
print(f"Second </head> (corruption starts) at line: {second_head_close + 1}")

# Extract clean sections
head_section = lines[:first_head_close + 1]
body_section = lines[first_body_start:second_head_close]

# Add script tags
script_tags = [
    '\n',
    '    <!-- JavaScript files -->\n',
    '    <script src="{% static \'js/app.js\' %}"></script>\n',
    '    <script src="{% static \'js/ui.js\' %}"></script>\n',
    '    <script src="{% static \'js/search.js\' %}"></script>\n',
    '    <script src="{% static \'js/image-upload.js\' %}"></script>\n',
    '</body>\n',
    '</html>\n'
]

# Combine
clean_html = head_section + body_section + script_tags

# Write
with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home.html', 'w', encoding='utf-8') as f:
    f.writelines(clean_html)

print(f"\n✓ Rebuilt home.html successfully!")
print(f"  Total lines: {len(clean_html)}")
print(f"  Head section: lines 1-{first_head_close + 1}")
print(f"  Body section: lines {first_body_start + 1}-{second_head_close}")
print(f"  Script tags: added at end")
