# Progresso de Fidelidade Visual (1:1 com o PDF)

Comparação realizada na largura de referência `W_REF = 1024.5 pt` (`deviceScaleFactor: 2` → `2049 × 18834 px`), fatiada em 16 faixas horizontais de `600 pt` (`1200 px`) e avaliada com `magick compare -metric AE -fuzz 6%`.

## Métricas Antes vs. Depois por Faixa

| Faixa | Intervalo `y` (pt) | Seções abrangidas | Antes (% dif.) | Depois (% dif.) | Redução |
|---|---:|---|---:|---:|---:|
| `strip-00` | `0–600` | `brand`, `hero` (título curvo) | 12.11% | **2.51%** | -9.60 pp |
| `strip-01` | `600–1200` | `hero` (subtítulo curvo + topo foto) | 16.05% | **2.87%** | -13.18 pp |
| `strip-02` | `1200–1800` | `hero` (foto + legenda `More Sugar`) | 19.66% | **2.71%** | -16.95 pp |
| `strip-03` | `1800–2400` | `transition`, `about` (título) | 17.61% | **0.20%** | -17.41 pp |
| `strip-04` | `2400–3000` | `about` (cards tracejados + patinhas) | 16.43% | **2.98%** | -13.45 pp |
| `strip-05` | `3000–3600` | `who` (título curvo + critérios + foto) | 19.44% | **1.01%** | -18.43 pp |
| `strip-06` | `3600–4200` | `who` (nota) + `how` (cabeçalho) | 13.79% | **2.29%** | -11.50 pp |
| `strip-07` | `4200–4800` | `how` (gato + etapas) + `procedure` (título) | 13.26% | **3.11%** | -10.15 pp |
| `strip-08` | `4800–5400` | `procedure` (manchas venoso/capilar + tubos) | 16.76% | **5.57%** | -11.19 pp |
| `strip-09` | `5400–6000` | `procedure` (3 glicosímetros + nota) | 22.84% | **2.96%** | -19.88 pp |
| `strip-10` | `6000–6600` | `procedure` (base nota) + `collage` (3 gatos) | 19.31% | **0.90%** | -18.41 pp |
| `strip-11` | `6600–7200` | `difference` + `impact` (topo tracinhos) | 12.16% | **2.58%** | -9.58 pp |
| `strip-12` | `7200–7800` | `impact` (texto) + `safety` (títulos) | 11.98% | **2.61%** | -9.37 pp |
| `strip-13` | `7800–8400` | `safety` (textos) + `team` (título + gato) | 13.09% | **7.97%** | -5.12 pp |
| `strip-14` | `8400–9000` | `team` (lista de membros + patinhas) | 15.83% | **3.27%** | -12.56 pp |
| `strip-15` | `9000–9417` | `footer` (projeto + card de contato) | 16.92% | **6.07%** | -10.85 pp |
| **Total** | **`0–9417`** | **Página completa** | **16.07%** | **3.04%** | **-13.03 pp** |

## O que ainda difere do PDF (>3% em faixas específicas) e por quê

1. **Sombras raster embutidas pelo Canva (`strip-08`, `strip-13`, `strip-15`):** No PDF original, cada bloco de texto possui uma imagem PNG raster com canal alfa (`smask`) gerada pelo motor de efeitos do Canva (`drop-shadow` / `lift`), enquanto no HTML/CSS os textos utilizam `text-shadow` / `feDropShadow` nativos sobre fontes vivas.
2. **Renderização e antialiasing de fontes (`More Sugar`, `League Spartan`, `Chewy`):** Mesmo utilizando os subsets originais extraídos do PDF (`league-spartan-canva.woff2`, `glacial-indifference-*.woff2`, `noto-sans-canva.woff2`), o rasterizador Skia/FreeType do Chromium aplica hinting e suavização ligeiramente distintos do `pdftoppm`/Cairo, além do espaçamento por caractere (`TJ` kerning individual do Canva) em parágrafos longos.
3. **Compressão WebP das fotos recortadas (`strip-07`, `strip-13`):** Pequenas diferenças de luminância nos pelos dos gatos (`gato-tigrado.webp` e `gato-equipe.webp`) frente ao bitmap bruto embutido no PDF.
