import re
import base64
import os

HTML_FILE = "/home/user/iEros/ieros_website-1.html"
OUTPUT_DIR = "/home/user/iEros/images"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the HTML file
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Match base64-encoded images inside url(...) CSS or src="..." / src='...' attributes
# Captures: image type and base64 data
pattern = re.compile(
    r'data:(image/[^;]+);base64,([A-Za-z0-9+/=]+)',
    re.IGNORECASE
)

matches = pattern.findall(html)

# Deduplicate while preserving order
seen = []
unique_matches = []
for mime, b64data in matches:
    key = b64data[:64]          # use first 64 chars as a fingerprint
    if key not in seen:
        seen.append(key)
        unique_matches.append((mime, b64data))

print(f"Found {len(matches)} total base64 image occurrences, {len(unique_matches)} unique image(s).\n")

extension_map = {
    "image/jpeg": "jpg",
    "image/jpg":  "jpg",
    "image/png":  "png",
    "image/gif":  "gif",
    "image/webp": "webp",
}

for i, (mime, b64data) in enumerate(unique_matches, start=1):
    ext = extension_map.get(mime.lower(), "jpg")
    filename = f"img{i}.{ext}"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Decode and write
    image_bytes = base64.b64decode(b64data)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes / 1024
    print(f"  {filename}  —  {size_bytes:,} bytes  ({size_kb:.1f} KB)")

print(f"\nAll images saved to: {OUTPUT_DIR}")
