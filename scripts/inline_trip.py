"""Copy data/trip.json into the TRIP constant in index.html."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
page = ROOT / "index.html"
s = page.read_text()
i = s.index("const TRIP = ") + len("const TRIP = ")
j = s.index(";\n", i)
page.write_text(s[:i] + (ROOT / "data/trip.json").read_text() + s[j:])
print("Updated", page)
