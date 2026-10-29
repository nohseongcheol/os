#!/usr/bin/env python3
"""vlastiti Java lokalno_doseg 이름을 바꾼다. niz_VALUE·주석·vanjski_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

akcija_korijen = Path(__file__).resolve().parents[1]
mapiranje_VALUE = json.loads((akcija_korijen / '명명/자바이름.json').read_text())
blok_izraz = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_zapis = []
for imenik_VALUE in ('IZVOR', 'korisnik/자바', '한국어자바'):
    for PUTANJA in sorted((akcija_korijen / imenik_VALUE).rglob('*.java')):
        IZVOR = PUTANJA.read_text()
        토막들 = list(blok_izraz.finditer(IZVOR))
        사용이름 = {blok_unos.group() for blok_unos in 토막들 if re.search('[가-힣]', blok_unos.group())}
        mapiranje_datoteke = {}
        for 이전, 이후 in mapiranje_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokalno_doseg' + 새이름
            mapiranje_datoteke[이전] = 새이름
        수정 = []
        이전토막 = ''
        for blok_unos in 토막들:
            낱말 = blok_unos.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapiranje_datoteke and 이전토막 != '.':
                수정.append((blok_unos.start(), blok_unos.end(), mapiranje_datoteke[낱말]))
                LOG_zapis.append((str(PUTANJA.relative_to(akcija_korijen)), 낱말, mapiranje_datoteke[낱말]))
            이전토막 = 낱말
        for Pokreni, 끝, 새이름 in reversed(수정): IZVOR = IZVOR[:Pokreni] + 새이름 + IZVOR[끝:]
        if 수정: PUTANJA.write_text(IZVOR)
(akcija_korijen / '명명/자바이름대응.tsv').write_text('Datoteka\t이전\t이후\n' + ''.join('\t'.join(unos_VALUE)+'\n' for unos_VALUE in sorted(set(LOG_zapis))))
print('Java Ime Reference promijeniti_VALUE:', len(LOG_zapis))
