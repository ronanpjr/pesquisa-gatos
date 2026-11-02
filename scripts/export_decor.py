#!/usr/bin/env python3
"""Exporta a decoração vetorial real do PDF para SVGs.

- Reconstrói a árvore de clips/grupos de page.get_drawings(extended=True).
- Gera um SVG por seção (faixa y0–y1 em pt), sem texto, sem fundo de página e
  sem os "recipientes" (faixas, cards, ícones), que saem como SVGs próprios
  para serem usados como fundo do elemento HTML correspondente.
- Exporta ícones mistos (vetor + raster embutido, ex. tubos) como WebP com alfa.

Uso: .venv/bin/python scripts/export_decor.py
"""
import json
import os
import subprocess

import pymupdf as fitz

PDF = "dudao_inventando_modas.pdf"
OUT_SVG = "assets/svg"
OUT_IMG = "assets/img"
W = 1024.5

cfg = json.load(open("scripts/decor.config.json"))

doc = fitz.open(PDF)
page = doc[0]


def f2(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def hexcolor(c):
    return "#" + "".join(f"{round(x * 255):02x}" for x in c[:3])


def path_d(items, close):
    out, cur = [], None
    for it in items:
        op = it[0]
        if op == "re":
            r = fitz.Rect(it[1])
            out.append(f"M{f2(r.x0)} {f2(r.y0)}H{f2(r.x1)}V{f2(r.y1)}H{f2(r.x0)}Z")
            cur = None
            continue
        if op == "qu":
            q = it[1]
            pts = [q.ul, q.ur, q.lr, q.ll]
            out.append("M" + "L".join(f"{f2(p.x)} {f2(p.y)}" for p in pts) + "Z")
            cur = None
            continue
        p0 = it[1]
        if cur is None or abs(cur.x - p0.x) > 0.01 or abs(cur.y - p0.y) > 0.01:
            out.append(f"M{f2(p0.x)} {f2(p0.y)}")
        if op == "l":
            p = it[2]
            out.append(f"L{f2(p.x)} {f2(p.y)}")
            cur = p
        elif op == "c":
            c1, c2, p = it[2], it[3], it[4]
            out.append(f"C{f2(c1.x)} {f2(c1.y)} {f2(c2.x)} {f2(c2.y)} {f2(p.x)} {f2(p.y)}")
            cur = p
    if close:
        out.append("Z")
    return "".join(out)


# ---------- árvore ----------
class Node:
    def __init__(self, kind, d=None, level=-1, scissor=None):
        self.kind, self.d, self.level, self.children = kind, d, level, []
        self.scissor = scissor  # retângulo efetivo (interseção dos clips)


root = Node("root", scissor=fitz.Rect(page.rect))
stack = [root]
fills = []
for d in page.get_drawings(extended=True):
    lvl = d["level"]
    while len(stack) > 1 and stack[-1].level >= lvl:
        stack.pop()
    parent = stack[-1]
    if d["type"] == "clip":
        sc = fitz.Rect(d["scissor"]) & parent.scissor
        n = Node("clip", d, lvl, sc)
        parent.children.append(n)
        stack.append(n)
    elif d["type"] == "group":
        n = Node("group", d, lvl, parent.scissor)
        parent.children.append(n)
        stack.append(n)
    else:
        n = Node("fill", d, lvl, parent.scissor)
        n.bbox = fitz.Rect(d["rect"]) & parent.scissor
        n.seq = d["seqno"]
        parent.children.append(n)
        fills.append(n)

page_bg = set(cfg["page_bg_seqnos"])


def node_in(n, rect):
    """fill totalmente contido em rect (com tolerância de 1pt)."""
    r = fitz.Rect(rect)
    r.x0 -= 1; r.y0 -= 1; r.x1 += 1; r.y1 += 1
    return n.bbox.is_empty is False and r.contains(n.bbox)


def visible(n):
    d = n.d
    if d.get("fill_opacity") == 0 or n.bbox.is_empty or n.bbox.width <= 0 or n.bbox.height <= 0:
        return False
    return d.get("fill") is not None or d.get("color") is not None


clip_ids = {}


def emit(node, want, defs):
    """retorna markup dos filhos de node que satisfazem want(fill)."""
    parts = []
    for c in node.children:
        if c.kind == "fill":
            if c.seq in page_bg or not visible(c) or not want(c):
                continue
            d = c.d
            attrs = [f'd="{path_d(d["items"], d.get("closePath"))}"']
            if d.get("fill") is not None:
                attrs.append(f'fill="{hexcolor(d["fill"])}"')
                if d.get("fill_opacity", 1) < 1:
                    attrs.append(f'fill-opacity="{f2(d["fill_opacity"])}"')
                if d.get("even_odd"):
                    attrs.append('fill-rule="evenodd"')
            else:
                attrs.append('fill="none"')
            if d.get("color") is not None and d["type"] in ("s", "fs"):
                attrs.append(f'stroke="{hexcolor(d["color"])}" stroke-width="{f2(d.get("width") or 1)}"')
            parts.append("<path " + " ".join(attrs) + "/>")
        else:
            inner = emit(c, want, defs)
            if not inner:
                continue
            if c.kind == "clip":
                key = id(c)
                if key not in clip_ids:
                    clip_ids[key] = f"c{len(clip_ids)}"
                cid = clip_ids[key]
                cd = c.d
                rule = ' clip-rule="evenodd"' if cd.get("even_odd") else ""
                defs[cid] = f'<clipPath id="{cid}"><path d="{path_d(cd["items"], True)}"{rule}/></clipPath>'
                parts.append(f'<g clip-path="url(#{cid})">{inner}</g>')
            else:
                op = c.d.get("opacity")
                if op is not None and op < 1:
                    parts.append(f'<g opacity="{f2(op)}">{inner}</g>')
                else:
                    parts.append(inner)
    return "".join(parts)


def write_svg(name, vb, want, stretch=False):
    defs = {}
    clip_ids.clear()
    body = emit(root, want, defs)
    x0, y0, x1, y1 = vb
    par = ' preserveAspectRatio="none"' if stretch else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f2(x0)} {f2(y0)} {f2(x1 - x0)} {f2(y1 - y0)}"{par}>'
           + (f"<defs>{''.join(defs.values())}</defs>" if defs else "") + body + "</svg>\n")
    path = os.path.join(OUT_SVG, name + ".svg")
    with open(path, "w") as fh:
        fh.write(svg)
    return path, len(svg)


os.makedirs(OUT_SVG, exist_ok=True)
os.makedirs(OUT_IMG, exist_ok=True)

# ---------- elementos (recipientes e ícones vetoriais) ----------
claimed = set()
for el in cfg["elements"]:
    rect = el["rect"]
    only = set(el.get("seqnos", []))
    exclude = set(el.get("exclude", []))

    def want(n, rect=rect, only=only, exclude=exclude):
        if n.seq in exclude:
            return False
        if only:
            return n.seq in only
        return node_in(n, rect)

    sel = [n.seq for n in fills if visible(n) and n.seq not in page_bg and want(n)]
    if el.get("claim", True):
        claimed.update(sel)
    p, size = write_svg(el["name"], rect, lambda n, s=set(sel): n.seq in s, el.get("stretch", False))
    print(f"elem {el['name']:24} {len(sel):4} paths {size/1024:7.1f} KiB")

for ic in cfg.get("raster_icons", []):
    for n in fills:
        if visible(n) and node_in(n, ic["rect"]):
            claimed.add(n.seq)

# ---------- seções ----------
extra_skip = set(cfg.get("skip_seqnos", []))
for sec in cfg["sections"]:
    y0, y1 = sec["y"]
    band = fitz.Rect(0, y0, W, y1)
    sec_excl = set(sec.get("exclude", []))

    def want(n, band=band, sec_excl=sec_excl):
        return n.seq not in claimed and n.seq not in extra_skip and n.seq not in sec_excl and n.bbox.intersects(band)

    p, size = write_svg("decor-" + sec["name"], (0, y0, W, y1), want)
    print(f"band {sec['name']:24} {y0:6}-{y1:<6} {size/1024:7.1f} KiB")

# ---------- ícones raster (vetor + imagens inline) ----------
# Remove texto e as formas grandes sob o ícone (tocando pontos vazios dos cantos)
for ic in cfg.get("raster_icons", []):
    d2 = fitz.open(PDF)
    p2 = d2[0]
    p2.add_redact_annot(p2.rect)
    p2.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                        graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                        text=fitz.PDF_REDACT_TEXT_REMOVE)
    for pt in ic["bg_points"]:
        x, y = pt
        p2.add_redact_annot(fitz.Rect(x, y, x + 0.5, y + 0.5))
    p2.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                        graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED,
                        text=fitz.PDF_REDACT_TEXT_NONE)
    pix = p2.get_pixmap(dpi=ic.get("dpi", 288), clip=fitz.Rect(ic["rect"]), alpha=True)
    png = f"/tmp/{ic['name']}.png"
    pix.save(png)
    out = os.path.join(OUT_IMG, ic["name"] + ".webp")
    subprocess.run(["magick", png, "-trim", "+repage", "-quality", "90", out], check=True)
    print(f"icon {ic['name']:24} -> {out}")


def extract_xref_rgba(xref):
    info = doc.extract_image(xref)
    pix = fitz.Pixmap(doc, xref)
    sm = info.get("smask")
    if sm:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, sm))
    return pix


# ---------- impact-dashes (xref 185) ----------
pix185 = extract_xref_rgba(185)
pix185.save("/tmp/xref185.png")
subprocess.run(["magick", "/tmp/xref185.png", "-quality", "92", os.path.join(OUT_IMG, "impact-dashes.webp")], check=True)

# ---------- glicosímetros sem corte + raios roxos (xref 173) ----------
pix173 = extract_xref_rgba(173)
pix173.save("/tmp/xref173.png")
for name, crop, size in [
    ("glicosimetro-accu-chek.webp", "300x354+174+34", "280x330!"),
    ("glicosimetro-on-call.webp",   "258x370+565+14", "248x356!"),
    ("glicosimetro-g-tech.webp",    "260x360+938+24", "248x344!"),
]:
    subprocess.run([
        "magick", "/tmp/xref173.png", "-crop", crop, "+repage",
        "-resize", size, "-quality", "92", os.path.join(OUT_IMG, name)
    ], check=True)

pix173_rays = extract_xref_rgba(173)
pix173_rays.set_rect(fitz.IRect(165, 0, 1210, pix173_rays.height), (0, 0, 0, 0))
pix173_rays.save("/tmp/xref173_rays.png")
subprocess.run([
    "magick", "/tmp/xref173_rays.png",
    "-crop", "1297x212+34+33", "+repage", "-quality", "92",
    os.path.join(OUT_IMG, "devices-rays.webp"),
], check=True)
print("exported impact-dashes.webp, devices-rays.webp, and unclipped glucometers")

