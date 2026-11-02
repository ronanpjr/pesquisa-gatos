#!/usr/bin/env python3
"""Extrai layout.json do PDF de referência (texto, imagens, formas) com PyMuPDF.

Uso: python3 scripts/extract_layout.py [pdf] [saida]
Todas as coordenadas estão em pontos do PDF (origem no canto superior esquerdo).
"""
import json
import sys

import fitz  # PyMuPDF

PDF = sys.argv[1] if len(sys.argv) > 1 else "dudao_inventando_modas.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "layout.json"


def r(v, n=2):
    return round(float(v), n)


def rect(b):
    return [r(b[0]), r(b[1]), r(b[2]), r(b[3])]


def color(c):
    if c is None:
        return None
    if isinstance(c, int):
        return f"#{c:06x}"
    return "#" + "".join(f"{round(x * 255):02x}" for x in c[:3])


doc = fitz.open(PDF)
page = doc[0]
out = {"page": rect(page.rect), "spans": [], "chars": [], "images": [], "drawings": []}

raw = page.get_text("rawdict")
for bi, block in enumerate(raw["blocks"]):
    if block.get("type") != 0:
        continue
    for li, line in enumerate(block["lines"]):
        for span in line["spans"]:
            text = "".join(ch["c"] for ch in span["chars"])
            out["spans"].append({
                "block": bi, "line": li, "text": text,
                "bbox": rect(span["bbox"]), "origin": [r(span["origin"][0]), r(span["origin"][1])],
                "font": span["font"], "size": r(span["size"]), "color": color(span["color"]),
                "dir": [r(line["dir"][0], 4), r(line["dir"][1], 4)],
            })
            for ch in span["chars"]:
                out["chars"].append({
                    "c": ch["c"], "bbox": rect(ch["bbox"]),
                    "origin": [r(ch["origin"][0]), r(ch["origin"][1])],
                    "font": span["font"], "size": r(span["size"]),
                })

for info in page.get_image_info(xrefs=True):
    out["images"].append({
        "xref": info.get("xref"), "bbox": rect(info["bbox"]),
        "width": info.get("width"), "height": info.get("height"),
        "transform": [r(v, 4) for v in info.get("transform", [])],
    })

for d in page.get_drawings(extended=True):
    items = []
    for it in d.get("items", []):
        op = it[0]
        pts = []
        for p in it[1:]:
            if isinstance(p, fitz.Point):
                pts.append([r(p.x), r(p.y)])
            elif isinstance(p, fitz.Rect):
                pts.append(rect(p))
            elif isinstance(p, fitz.Quad):
                pts.append([[r(q.x), r(q.y)] for q in (p.ul, p.ur, p.lr, p.ll)])
        items.append([op] + pts)
    out["drawings"].append({
        "type": d.get("type"), "level": d.get("level"), "seqno": d.get("seqno"),
        "rect": rect(d["rect"]) if d.get("rect") else None,
        "fill": color(d.get("fill")), "stroke": color(d.get("color")),
        "width": r(d["width"]) if d.get("width") else None,
        "fill_opacity": d.get("fill_opacity"), "stroke_opacity": d.get("stroke_opacity"),
        "even_odd": d.get("even_odd"), "close": d.get("closePath"),
        "items": items,
    })

with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False)
print(f"{OUT}: {len(out['spans'])} spans, {len(out['images'])} imagens, {len(out['drawings'])} drawings")
