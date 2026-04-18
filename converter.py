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

path = Path("index.html")
if path.exists():
    os.rename("index.html", "index.html.bak")
    print("index.html moved to index.html.bak")

# Setup
TAG_MAP = {
    "title:": "<title>{}</title>",
    "text:":  "<p>{}</p>",
    "head:":  "<h1>{}</h1>",
    "sub:":   "<h2>{}</h2>",
    "note:":  "<i>{}</i>",
    "css:":   '<link rel="stylesheet" href="{}">',
    "line":   "<hr>",
    "break":  "<br>"
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
            body_elements.append("    " + TAG_MAP["line"] + "\n")
            continue
        elif clean == "break":
            body_elements.append("    " + TAG_MAP["break"] + "\n")
            continue

        # Handle tags with content
        for marker, template in TAG_MAP.items():
            if clean.startswith(marker):
                content = clean[len(marker):].strip()
                formatted = template.format(content) + "\n"
                
                if marker == "title:":
                    page_title = content
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