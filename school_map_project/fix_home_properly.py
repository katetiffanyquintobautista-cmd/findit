#!/usr/bin/env python3
"""
Properly fix home.html by keeping the clean body content
"""

# Read the backup file
with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home_corrupted_backup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the first </head> (end of clean head section)
# Find the first <body> after that (start of clean body)
# Find the second </head> (this marks where corruption starts)
# Find the last <!-- JavaScript files --> (start of script tags)

first_head_close = None
first_body_start = None
second_head_close = None
script_comment = None

for i, line in enumerate(lines):
    if '</head>' in line:
        if first_head_close is None:
            first_head_close = i
        elif second_head_close is None:
            second_head_close = i
    
    if '<body>' in line and first_body_start is None and first_head_close is not None:
        first_body_start = i
    
    if '<!-- JavaScript files -->' in line:
        script_comment = i  # Keep updating to get the last one

print(f"First </head> at line: {first_head_close}")
print(f"First <body> at line: {first_body_start}")
print(f"Second </head> (corruption starts) at line: {second_head_close}")
print(f"Script comment at line: {script_comment}")

if all([first_head_close, first_body_start, second_head_close, script_comment]):
    # Keep: head section + body section (until corruption) + script tags
    head_section = lines[:first_head_close + 1]  # Include </head>
    body_section = lines[first_body_start:second_head_close]  # Body content until corruption
    script_section = lines[script_comment:]  # Script tags to end
    
    # Combine them
    fixed_html = head_section + body_section + ['\n'] + script_section
    
    # Write the fixed file
    with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home.html', 'w', encoding='utf-8') as f:
        f.writelines(fixed_html)
    
    print(f"\n✓ Fixed file created!")
    print(f"  - Head section: lines 1-{first_head_close + 1}")
    print(f"  - Body section: lines {first_body_start + 1}-{second_head_close}")
    print(f"  - Script section: lines {script_comment + 1}-{len(lines)}")
    print(f"  - Total lines: {len(fixed_html)}")
    print(f"\n✓ home.html has been fixed with body content!")
else:
    print("ERROR: Could not find all required sections")
    print(f"  first_head_close: {first_head_close}")
    print(f"  first_body_start: {first_body_start}")
    print(f"  second_head_close: {second_head_close}")
    print(f"  script_comment: {script_comment}")
