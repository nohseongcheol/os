#!/usr/bin/env python3
"""자체 Java lokalni_opseg 이름을 바꾼다. string_VALUE·주석·iz_eksternog_izvora_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

projicirati_koijen = Path(__file__).resolve().parents[1]
대응 = json.loads((projicirati_koijen / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_red = []
for Direktorij_VALUE in ('IZVOR', 'korisnik/자바', '한국어자바'):
    for Putanja in sorted((projicirati_koijen / Direktorij_VALUE).rglob('*.java')):
        IZVOR = Putanja.read_text()
        토막들 = list(토막식.finditer(IZVOR))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokalni_opseg' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_red.append((str(Putanja.relative_to(projicirati_koijen)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Pokreni, 끝, 새이름 in reversed(수정): IZVOR = IZVOR[:Pokreni] + 새이름 + IZVOR[끝:]
        if 수정: Putanja.write_text(IZVOR)
(projicirati_koijen / '명명/자바이름대응.tsv').write_text('Fajl\t이전\t이후\n' + ''.join('\t'.join(unos_VALUE)+'\n' for unos_VALUE in sorted(set(LOG_red))))
print('Java Naziv Reference promijeniti_VALUE:', len(LOG_red))
