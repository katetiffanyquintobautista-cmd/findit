#!/usr/bin/env python3
"""Check HTML structure for proper nesting"""

with open(r'c:\Users\User\Documents\AUDIT\highschoolmap\school_map_project\schoolmap\mapapp\templates\home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("HTML Structure Analysis:")
print("=" * 50)

# Track key elements
body_start = None
sidebar_start = None
sidebar_end = None
main_content_start = None
main_content_end = None
body_end = None

for i, line in enumerate(lines, 1):
    if '<body>' in line:
        body_start = i
        print(f"Line {i}: <body>")
    elif '<div class="sidebar">' in line:
        sidebar_start = i
        print(f"Line {i}: <div class=\"sidebar\">")
    elif '<div class="main-content">' in line:
        main_content_start = i
        print(f"Line {i}: <div class=\"main-content\">")
    elif '</body>' in line:
        body_end = i
        print(f"Line {i}: </body>")

# Count divs
total_open = sum(1 for line in lines if '<div' in line)
total_close = sum(1 for line in lines if '</div>' in line)

print("\n" + "=" * 50)
print(f"Total <div tags: {total_open}")
print(f"Total </div> tags: {total_close}")
print(f"Difference: {total_open - total_close}")

if total_open != total_close:
    print("\n⚠️  WARNING: Unbalanced div tags!")
else:
    print("\n✓ Div tags are balanced")
