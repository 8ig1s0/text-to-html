# This is a python script that automatically converts from normal text to html and stores into index.html
import os
import shutil
from pathlib import Path

path = Path("index.html.bak")
if path.exists():
    confirmdelete = input("Confirm that you want to delete index.html.bak? (Y/n)")
    if confirmdelete.lower() == 'y':
        Path("index.html.bak").unlink(missing_ok=True) # Delete backup file
        print("index.html.bak deleted")
    else:
        print("Nothing was deleted, operation could not continue")
        exit()

path = Path("index.html")
if path.exists():
    os.rename("index.html", "index.html.bak")
    print("index.html moved to index.html.bak")

# Setup
# Templates map fields using {0}, {1}, {2} sequentially
structure_map = {
    "title:":   "<title>{0}</title>",
    "text:":    "<p>{0}</p>",
    "head:":    "<h1>{0}</h1>",
    "sub:":     "<h2>{0}</h2>",
    "note:":    "<i>{0}</i>",
    "css:":     '<link rel="stylesheet" href="{0}">', # Load CSS from file
    "line":     "<hr>",
    "break":    "<br>",
    "comment:": "<!-- {0} -->",
    
    # 2 Fields: Link URL | Link Text
    "link:":    '<a href="{0}">{1}</a>',
    
    # 3 Fields: Image Link URL | Image Source File | Alt Description
    "imglink:": '<a href="{0}"><img src="{1}" alt="{2}"></a>'
}

head_elements = []
body_elements = []
current_section = "BODY"  # Default section
page_title = "Default Title"

# Process input
with open('input.txt', 'r') as infile:
    for line in infile:
        clean = line.strip()
        if not clean: continue

        # Check for section switches
        if "SECTION:HEAD" in clean.upper():
            current_section = "HEAD"
            continue
        elif "SECTION:BODY" in clean.upper():
            current_section = "BODY"
            continue

        # Handle standalone tags (no content)
        if clean == "line":
            body_elements.append("    " + structure_map["line"] + "\n")
            continue
        elif clean == "break":
            body_elements.append("    " + structure_map["break"] + "\n")
            continue

        # Handle tags with content
        for marker, template in structure_map.items():
            if clean.startswith(marker):
                raw_content = clean[len(marker):].strip()
                
                # Split content into multiple fields using '|' and clean up spaces
                fields = [field.strip() for field in raw_content.split('|')]
                
                # FIXED FALLBACK: Safely counts and pads missing arguments with the first field
                expected_fields = template.count('{')
                while len(fields) < expected_fields:
                    fields.append(fields[0] if fields else "")
                
                # Automatically unpack fields into the HTML template (*fields)
                formatted = template.format(*fields) + "\n"
                
                if marker == "title:":
                    page_title = fields[0] # Set the title global variable
                elif current_section == "HEAD":
                    head_elements.append("    " + formatted)
                else:
                    body_elements.append("    " + formatted)
                break

# Generate HTML file
html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{page_title}</title>
{"".join(head_elements)}</head>
<body>
{"".join(body_elements)}</body>
</html>"""

# Write to file
with open('index.html', 'w') as outfile:
    outfile.write(html_template)

print("Done! Check your index.html file.")
