#!/usr/bin/env python3
"""saját Java helyi_hatókör 이름을 바꾼다. sztring_ÉRTÉK·주석·külső_ÉRTÉK 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

teendő_gyök = Path(__file__).resolve().parents[1]
leképezés_ÉRTÉK = json.loads((teendő_gyök / '명명/자바이름.json').read_text())
adatrészlet_kifejezés = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_REKORD = []
for címtár_ÉRTÉK in ('FORRÁS', 'felhasználó/자바', '한국어자바'):
    for ÚTVONAL in sorted((teendő_gyök / címtár_ÉRTÉK).rglob('*.java')):
        FORRÁS = ÚTVONAL.read_text()
        토막들 = list(adatrészlet_kifejezés.finditer(FORRÁS))
        사용이름 = {adatrészlet_bejegyzés.group() for adatrészlet_bejegyzés in 토막들 if re.search('[가-힣]', adatrészlet_bejegyzés.group())}
        fájlleképezés = {}
        for Előző_cikk, 이후 in leképezés_ÉRTÉK.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'helyi_hatókör' + 새이름
            fájlleképezés[Előző_cikk] = 새이름
        수정 = []
        Előző_adatrészlet = ''
        for adatrészlet_bejegyzés in 토막들:
            낱말 = adatrészlet_bejegyzés.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in fájlleképezés and Előző_adatrészlet != '.':
                수정.append((adatrészlet_bejegyzés.start(), adatrészlet_bejegyzés.end(), fájlleképezés[낱말]))
                LOG_REKORD.append((str(ÚTVONAL.relative_to(teendő_gyök)), 낱말, fájlleképezés[낱말]))
            Előző_adatrészlet = 낱말
        for Futtatás, 끝, 새이름 in reversed(수정): FORRÁS = FORRÁS[:Futtatás] + 새이름 + FORRÁS[끝:]
        if 수정: ÚTVONAL.write_text(FORRÁS)
(teendő_gyök / '명명/자바이름대응.tsv').write_text('Fájl\t이전\t이후\n' + ''.join('\t'.join(bejegyzés_ÉRTÉK)+'\n' for bejegyzés_ÉRTÉK in sorted(set(LOG_REKORD))))
print('Java Név hivatkozik módosítás_ÉRTÉK:', len(LOG_REKORD))
