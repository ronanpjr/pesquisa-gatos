#!/usr/bin/env python3
"""Extrai e converte as fontes exatas do PDF para WOFF2 em assets/fonts/."""
import os
import pymupdf as fitz
from fontTools.ttLib import TTFont
from fontTools.merge import Merger

doc = fitz.open("dudao_inventando_modas.pdf")
OUT_DIR = "assets/fonts"
os.makedirs(OUT_DIR, exist_ok=True)

targets = [
    ("glacial-indifference-bold.woff2", [571]),
    ("glacial-indifference-regular.woff2", [735]),
    ("league-spartan-canva.woff2", [452, 516]),
    ("noto-sans-canva.woff2", [764]),
]

for filename, xrefs in targets:
    paths = []
    for x in xrefs:
        _, _, _, content = doc.extract_font(x)
        p = f"/tmp/pdf_font_{x}.ttf"
        with open(p, "wb") as fh:
            fh.write(content)
        paths.append(p)
    tt = TTFont(paths[0]) if len(paths) == 1 else Merger().merge(paths)
    # Garantir que OS/2 usWinAscent/usWinDescent e hhea batam para renderização consistente no Linux/macOS
    tt.flavor = "woff2"
    out_path = os.path.join(OUT_DIR, filename)
    tt.save(out_path)
    print(f"wrote {out_path} ({os.path.getsize(out_path)} bytes)")
