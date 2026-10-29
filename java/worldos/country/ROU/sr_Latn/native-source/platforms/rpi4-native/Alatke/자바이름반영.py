#!/usr/bin/env python3
"""자체 Java lokalni_skup 이름을 바꾼다. niska_VALUE·주석·spoljni_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

radnja_koren = Path(__file__).resolve().parents[1]
mapiranje_VALUE = json.loads((radnja_koren / '명명/자바이름.json').read_text())
odlomak_izraz = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_snimi = []
for Imenik_VALUE in ('izvor', 'korisnik/자바', '한국어자바'):
    for putanja in sorted((radnja_koren / Imenik_VALUE).rglob('*.java')):
        izvor = putanja.read_text()
        토막들 = list(odlomak_izraz.finditer(izvor))
        사용이름 = {odlomak_stavka.group() for odlomak_stavka in 토막들 if re.search('[가-힣]', odlomak_stavka.group())}
        mapiranje_datoteke = {}
        for 이전, 이후 in mapiranje_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokalni_skup' + 새이름
            mapiranje_datoteke[이전] = 새이름
        수정 = []
        이전토막 = ''
        for odlomak_stavka in 토막들:
            낱말 = odlomak_stavka.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapiranje_datoteke and 이전토막 != '.':
                수정.append((odlomak_stavka.start(), odlomak_stavka.end(), mapiranje_datoteke[낱말]))
                LOG_snimi.append((str(putanja.relative_to(radnja_koren)), 낱말, mapiranje_datoteke[낱말]))
            이전토막 = 낱말
        for koristiti, 끝, 새이름 in reversed(수정): izvor = izvor[:koristiti] + 새이름 + izvor[끝:]
        if 수정: putanja.write_text(izvor)
(radnja_koren / '명명/자바이름대응.tsv').write_text('Datoteka\t이전\t이후\n' + ''.join('\t'.join(stavka_VALUE)+'\n' for stavka_VALUE in sorted(set(LOG_snimi))))
print('Java ime referenca promeniti_VALUE:', len(LOG_snimi))
