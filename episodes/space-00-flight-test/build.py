"""Builds index.html from index.template.html by inlining bank.json (the question bank)."""
import json, pathlib
here = pathlib.Path(__file__).parent
bank = json.loads((here / "bank.json").read_text())
html = (here / "index.template.html").read_text().replace("__BANK__", json.dumps(bank, ensure_ascii=False))
(here / "index.html").write_text(html)
print("built index.html")
