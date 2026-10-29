#!/usr/bin/env python3
"""vlastné Java miestny_Rozsah 이름을 바꾼다. reťazec_VALUE·주석·externý_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

akcia_koreň = Path(__file__).resolve().parents[1]
mapovanie_VALUE = json.loads((akcia_koreň / '명명/자바이름.json').read_text())
blok_údajov_výraz = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for Adresár_VALUE in ('ZDROJ', 'používateľ/자바', '한국어자바'):
    for Cesta in sorted((akcia_koreň / Adresár_VALUE).rglob('*.java')):
        ZDROJ = Cesta.read_text()
        토막들 = list(blok_údajov_výraz.finditer(ZDROJ))
        사용이름 = {blok_údajov_položka.group() for blok_údajov_položka in 토막들 if re.search('[가-힣]', blok_údajov_položka.group())}
        mapovanie_súborov = {}
        for 이전, 이후 in mapovanie_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'miestny_Rozsah' + 새이름
            mapovanie_súborov[이전] = 새이름
        수정 = []
        이전토막 = ''
        for blok_údajov_položka in 토막들:
            낱말 = blok_údajov_položka.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapovanie_súborov and 이전토막 != '.':
                수정.append((blok_údajov_položka.start(), blok_údajov_položka.end(), mapovanie_súborov[낱말]))
                LOG_RECORD.append((str(Cesta.relative_to(akcia_koreň)), 낱말, mapovanie_súborov[낱말]))
            이전토막 = 낱말
        for Spustiť_2, 끝, 새이름 in reversed(수정): ZDROJ = ZDROJ[:Spustiť_2] + 새이름 + ZDROJ[끝:]
        if 수정: Cesta.write_text(ZDROJ)
(akcia_koreň / '명명/자바이름대응.tsv').write_text('Súbor\t이전\t이후\n' + ''.join('\t'.join(položka_VALUE)+'\n' for položka_VALUE in sorted(set(LOG_RECORD))))
print('Java Názov zdroj zmeniť_VALUE:', len(LOG_RECORD))
