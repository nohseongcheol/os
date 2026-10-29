#!/usr/bin/env python3
"""vlastní Java místní_obor 이름을 바꾼다. řetězec_HODNOTA·주석·externí_HODNOTA 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

akce_kořen = Path(__file__).resolve().parents[1]
대응 = json.loads((akce_kořen / '명명/자바이름.json').read_text())
blok_dat_výraz = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOGZ_ZÁZNAM = []
for Adresář_HODNOTA in ('zdrojový_soubor', 'uživatelský_prostor/자바', '한국어자바'):
    for cesta_2 in sorted((akce_kořen / Adresář_HODNOTA).rglob('*.java')):
        zdrojový_soubor = cesta_2.read_text()
        토막들 = list(blok_dat_výraz.finditer(zdrojový_soubor))
        사용이름 = {blok_dat_položka.group() for blok_dat_položka in 토막들 if re.search('[가-힣]', blok_dat_položka.group())}
        mapování_souborů = {}
        for Předchozí_zboží, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'místní_obor' + 새이름
            mapování_souborů[Předchozí_zboží] = 새이름
        수정 = []
        Předchozí_blok_dat = ''
        for blok_dat_položka in 토막들:
            낱말 = blok_dat_položka.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapování_souborů and Předchozí_blok_dat != '.':
                수정.append((blok_dat_položka.start(), blok_dat_položka.end(), mapování_souborů[낱말]))
                LOGZ_ZÁZNAM.append((str(cesta_2.relative_to(akce_kořen)), 낱말, mapování_souborů[낱말]))
            Předchozí_blok_dat = 낱말
        for Spustit_2, 끝, 새이름 in reversed(수정): zdrojový_soubor = zdrojový_soubor[:Spustit_2] + 새이름 + zdrojový_soubor[끝:]
        if 수정: cesta_2.write_text(zdrojový_soubor)
(akce_kořen / '명명/자바이름대응.tsv').write_text('název_souboru\t이전\t이후\n' + ''.join('\t'.join(položka_HODNOTA)+'\n' for položka_HODNOTA in sorted(set(LOGZ_ZÁZNAM))))
print('Java Název odkaz změnit_HODNOTA:', len(LOGZ_ZÁZNAM))
