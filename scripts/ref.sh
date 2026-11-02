#!/usr/bin/env bash
# Renderiza a referência 2x (W_REF = 1024.5 pt -> 2049 px) e fatia em faixas de 1200 px.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p ref
pdftoppm -png -r 144 -singlefile dudao_inventando_modas.pdf ref/pagina
rm -f ref/strip-*.png
# "100%x1200" aplicaria % às duas dimensões; usar largura explícita.
magick ref/pagina.png -crop 2049x1200 +repage ref/strip-%02d.png
# pdftocairo -svg aborta (assert do cairo) neste PDF; ref/pagina.svg (gerado antes) serve de conferência.
if [ ! -f ref/original.svg ] || [ ! -s ref/original.svg ]; then
  pdftocairo -svg dudao_inventando_modas.pdf ref/original.svg || cp ref/pagina.svg ref/original.svg
fi
identify ref/pagina.png
ls ref/strip-*.png | wc -l
