# Auditoria de Fontes (`pdffonts` vs. `assets/fonts/`)

## Saída de `pdffonts dudao_inventando_modas.pdf`

```text
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
CAAAAA+LeagueSpartan-Bold            CID TrueType      Identity-H       yes yes yes    452  0
AAAAAA+GlacialIndifference-Bold      CID TrueType      Identity-H       yes yes yes    571  0
BAAAAA+GlacialIndifference-Regular   CID TrueType      Identity-H       yes yes yes    735  0
DAAAAA+Chewy-Regular                 CID TrueType      Identity-H       yes yes yes    601  0
EAAAAA+MoreSugarRegular              CID TrueType      Identity-H       yes yes yes    750  0
AAAAAA+MoreSugarRegular              CID TrueType      Identity-H       yes yes yes    515  0
BAAAAA+LeagueSpartan-Bold            CID TrueType      Identity-H       yes yes yes    516  0
CAAAAA+Chewy-Regular                 CID TrueType      Identity-H       yes yes yes    673  0
DAAAAA+NotoSans-Regular              CID TrueType      Identity-H       yes yes yes    764  0
```

> O Canva divide páginas muito altas em dois blocos (acima e abaixo de `y = 5800 pt`), por isso `LeagueSpartan-Bold`, `Chewy-Regular` e `MoreSugarRegular` aparecem duplicadas na tabela de fontes do PDF.

## Comparação com `assets/fonts/`

| Fonte no PDF (xref) | Onde é usada no flyer | Estado anterior em `assets/fonts/` | Diagnóstico de métricas | Solução adotada |
|---|---|---|---|---|
| `LeagueSpartan-Bold` (`452`, `516`) | Corpo principal, listas, subtítulos, procedimentos, impacto, segurança, contato | `league-spartan-latin.woff2` (Google Fonts v2 variável, `upm=2000`, avanço de `a` = `0.504 em`) | **Diferença severa (~35% mais estreita):** o Canva usa a versão clássica **League Spartan v1** (`upm=1000`, `asc=900`, `dsc=-350`, avanço de `a` = `0.683 em`). A v2 mudava todas as quebras de linha. | Extraída e mesclada de `452` + `516` (`cmap` Unicode intacto, 60 glifos) para `assets/fonts/league-spartan-canva.woff2`, mantendo a v2 como fallback. |
| `Chewy-Regular` (`601`, `673`) | Títulos principais (`.hero__title`, faixas `.ribbon`, `.who__title`, `.how__pill`, `.proc h3`, `.safety-card__title`, `.team h2`, `.contact-card h2`) | `chewy-latin.woff2` (`upm=1024`, `asc=1003`, `dsc=-310`, avanço de `a` = `485`) | **100% idêntica** às métricas embutidas no PDF. | Mantida `assets/fonts/chewy-latin.woff2`. |
| `MoreSugarRegular` (`750`, `515`) | Textos arredondados (`.hero__caption`, `.who__free`, itens de `.proc`, `.note`, `.difference h2`, `.team__list`, `.footer__project`) | `more-sugar.woff` (`upm=1000`, `asc=919`, `dsc=-275`, avanço de `a` = `557`) | **100% idêntica** às métricas embutidas no PDF. | Mantida `assets/fonts/more-sugar.woff`. |
| `GlacialIndifference-Bold` (`571`) | Cabeçalho UNESP (`UNIVERSIDADE ESTADUAL PAULISTA` / `“JÚLIO DE MESQUITA FILHO”`, `27.97 pt`) | **Ausente** (substituída por `Jost` / `Baloo 2`) | `Jost` tem proporções geométricas próximas, mas larguras de caixa alta e aspas diferentes (`upm=1000`, `asc=950`, `dsc=-250`, avanço de `A` = `689`). | Extraída do PDF (`xref 571`, `cmap` Unicode completo) para `assets/fonts/glacial-indifference-bold.woff2`, com `Jost` como fallback. |
| `GlacialIndifference-Regular` (`735`) | Cabeçalho UNESP (`Câmpus de Jaboticabal`, `19.76 pt`) | **Ausente** (substituída por `Jost`) | `upm=1000`, `asc=950`, `dsc=-250`, avanço de `a` = `570`. | Extraída do PDF (`xref 735`, `cmap` Unicode completo) para `assets/fonts/glacial-indifference-regular.woff2`, com `Jost` como fallback. |
| `NotoSans-Regular` (`764`) | Aspas curvas (`“”`) na citação do rodapé (`37.16 pt`) | **Ausente** | Usada pelo Canva apenas para os glifos `“` e `”` no título do projeto de IC (`upm=1000`, `asc=1069`, `dsc=-293`). | Extraída do PDF (`xref 764`) para `assets/fonts/noto-sans-canva.woff2` como fallback de `More Sugar`. |
