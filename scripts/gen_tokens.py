#!/usr/bin/env python3
"""Gera tokens.css a partir de layout.json (tamanhos de fonte, line-heights,
alturas de seção e coordenadas exatas em pontos do PDF).
"""
import json

L = json.load(open("layout.json"))
cfg = json.load(open("scripts/decor.config.json"))


def span_matching(substr, y_min=0, y_max=9500):
    for s in L["spans"]:
        if y_min <= s["bbox"][1] <= y_max and substr in s["text"]:
            return s
    raise KeyError(substr)


def line_height_ratio(substr1, substr2, y_min=0, y_max=9500):
    s1 = span_matching(substr1, y_min, y_max)
    s2 = span_matching(substr2, y_min, y_max)
    dy = abs(s2["origin"][1] - s1["origin"][1])
    return round(dy / s1["size"], 4)


tokens = [
    ("w-ref", 1024.5),
    ("h-ref", 9417),
]

# Alturas de cada seção a partir do mapa de seções
for sec in cfg["sections"]:
    y0, y1 = sec["y"]
    tokens.append((f"{sec['name']}-y0", y0))
    tokens.append((f"{sec['name']}-h", round(y1 - y0, 2)))

# Font-sizes (size do span em layout.json) e line-heights (Δbaseline / size)
typography = [
    ("brand-strong-fs", span_matching("UNIVERSIDADE")["size"]),
    ("brand-strong-lh", line_height_ratio("UNIVERSIDADE", "JÚLIO")),
    ("brand-sub-fs",    span_matching("Câmpus")["size"]),
    ("hero-title-fs",   span_matching("faz", 180, 360)["size"]),
    ("hero-accent-fs",  span_matching("ci", 360, 560)["size"]),
    ("hero-intro-fs",   span_matching("udan", 660, 760)["size"]),
    ("hero-caption-fs", span_matching("Sua participação contribui")["size"]),
    ("hero-caption-lh", line_height_ratio("Sua participação contribui", "para um atendimento")),
    ("about-title-fs",  span_matching("roj", 2280, 2400)["size"]),
    ("about-card-fs",   span_matching("Medir os níveis")["size"]),
    ("about-card-lh",   line_height_ratio("Medir os níveis", "no sangue é essencial")),
    ("who-title-fs",    span_matching("ci", 3080, 3230)["size"]),
    ("who-lead-fs",     span_matching("Gatos saudáveis")["size"]),
    ("who-lead-lh",     line_height_ratio("Gatos saudáveis", "serão submetidos")),
    ("who-free-fs",     span_matching("Não há restrição")["size"]),
    ("who-free-lh",     line_height_ratio("Não há restrição", "idade ou raça")),
    ("how-title-fs",    span_matching("Como será a")["size"]),
    ("how-title-lh",    line_height_ratio("Como será a", "pesquisa?")),
    ("how-step-fs",     span_matching("Exame físico")["size"]),
    ("proc-title-fs",   span_matching("O procedimento:")["size"]),
    ("proc-intro-fs",   span_matching("Durante os períodos")["size"]),
    ("proc-intro-lh",   line_height_ratio("Durante os períodos", "trans e pós-operatório")),
    ("proc-col-h3-fs",  span_matching("Sangue venoso")["size"]),
    ("proc-sub-fs",     span_matching("será destinado para:", 4900, 4950)["size"]),
    ("proc-item-fs",    span_matching("Tubo com fluoreto")["size"]),
    ("proc-item-lh",    line_height_ratio("Tubo com fluoreto", "de sódio e EDTA")),
    ("proc-note-fs",    span_matching("(coletado da ponta")["size"]),
    ("proc-note-lh",    line_height_ratio("(coletado da ponta", "com lancetas estéreis)")),
    ("devices-h3-fs",   span_matching("Serão utilizados os")["size"]),
    ("devices-h3-lh",   line_height_ratio("Serão utilizados os", "glicosímetros:")),
    ("device-label-fs", span_matching("Accu-Chek")["size"]),
    ("device-label-lh", line_height_ratio("Accu-Chek", "Active")),
    ("note-fs",         span_matching("Os resultados laboratoriais")["size"]),
    ("note-lh",         line_height_ratio("Os resultados laboratoriais", "glicosímetros serão comparados")),
    ("diff-title-fs",   span_matching("Sua participação faz")["size"]),
    ("diff-title-lh",   line_height_ratio("Sua participação faz", "a diferença !")),
    ("impact-fs",       span_matching("Seu gatinho pode contribuir")["size"]),
    ("impact-lh",       line_height_ratio("Seu gatinho pode contribuir", "para a produção de")),
    ("safety-h3-1-fs",  span_matching("Mas é seguro?")["size"]),
    ("safety-h3-2-fs",  span_matching("Confidencialidade:")["size"]),
    ("safety-p1-fs",    span_matching("Os procedimentos")["size"]),
    ("safety-p1-lh",    line_height_ratio("Os procedimentos", "apresentam")),
    ("safety-p2-fs",    span_matching("Todas as informações")["size"]),
    ("safety-p2-lh",    line_height_ratio("Todas as informações", "obtidas serão mantidas")),
    ("team-title-fs",   span_matching("Equipe responsável:")["size"]),
    ("team-item-fs",    span_matching("Maria Eduarda Desiderio")["size"]),
    ("team-item-lh",    line_height_ratio("Maria Eduarda Desiderio", "Grigolete (discente)")),
    ("footer-h2-fs",    span_matching("Projeto de Iniciação")["size"]),
    ("footer-h2-lh",    line_height_ratio("Projeto de Iniciação", "Científica")),
    ("footer-quote-fs", span_matching("Análise Comparativa da")["size"]),
    ("footer-quote-lh", line_height_ratio("Análise Comparativa da", "Acurácia de Glicosímetros")),
    ("footer-unesp-fs", span_matching("UNESP - FCAV")["size"]),
    ("contact-h2-fs",   span_matching("Em caso de dúvidas,")["size"]),
    ("contact-h2-lh",   line_height_ratio("Em caso de dúvidas,", "entre em contato:")),
    ("contact-tel-fs",  span_matching("(16) 99756-4911")["size"]),
    ("contact-mail-fs", span_matching("m.grigolete@unesp.br")["size"]),
    ("contact-note-fs", span_matching("(Maria Eduarda - discente")["size"]),
]
tokens.extend(typography)

lines = ["/* Gerado automaticamente por scripts/gen_tokens.py a partir de layout.json */", ":root {"]
for k, v in tokens:
    lines.append(f"  --{k}: {v};")
lines.append("}\n")

with open("tokens.css", "w") as fh:
    fh.write("\n".join(lines))
print(f"tokens.css: {len(tokens)} variáveis geradas")
