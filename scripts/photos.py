"""Build photos/ from a folder of exported originals and a picks file.

picks.json maps each stop key to an ordered list of original filenames, e.g.
{"vof": ["IMG_1234.HEIC", ...]}. Writes photos/<key>-<n>.jpg (1600px long edge)
and photos/thumbs/<key>-<n>.jpg (360px), strips all metadata (GPS included),
then updates the PHOTOS constant in index.html with the count per stop.

Usage: python3 scripts/photos.py <export-dir> <picks.json>
HEIC files are converted with macOS `sips`.
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
src, picks = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
out, thumbs = ROOT / "photos", ROOT / "photos" / "thumbs"
thumbs.mkdir(parents=True, exist_ok=True)
for f in list(out.glob("*.jpg")) + list(thumbs.glob("*.jpg")):
    f.unlink()

def load(path):
    if path.suffix.lower() in (".heic", ".heif"):
        tmp = Path(tempfile.mkdtemp()) / (path.stem + ".jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", str(path), "--out", str(tmp)], check=True, capture_output=True)
        path = tmp
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")

counts = {}
for key, names in picks.items():
    for n, name in enumerate(names, 1):
        im = load(src / name)
        big = im.copy(); big.thumbnail((1600, 1600), Image.LANCZOS)
        big.save(out / f"{key}-{n}.jpg", quality=82, optimize=True, progressive=True)
        sm = im.copy(); sm.thumbnail((360, 360), Image.LANCZOS)
        sm.save(thumbs / f"{key}-{n}.jpg", quality=78, optimize=True)
    counts[key] = len(names)

html = ROOT / "index.html"
s = html.read_text()
s = re.sub(r"const PHOTOS = .*?;\n", f"const PHOTOS = {json.dumps(counts)};\n", s, count=1)
html.write_text(s)
print(counts)
