#!/usr/bin/env python3
"""savs Java vietējs_Tvērums 이름을 바꾼다. virkne_VALUE·주석·ārējs_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_sakne = Path(__file__).resolve().parents[1]
kartēšana_VALUE = json.loads((Project_sakne / '명명/자바이름.json').read_text())
porcija_izteiksme = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for Direktorijs_VALUE in ('AVOTS', 'lietotājs/자바', '한국어자바'):
    for CEĻŠ in sorted((Project_sakne / Direktorijs_VALUE).rglob('*.java')):
        AVOTS = CEĻŠ.read_text()
        토막들 = list(porcija_izteiksme.finditer(AVOTS))
        사용이름 = {porcija_ievade.group() for porcija_ievade in 토막들 if re.search('[가-힣]', porcija_ievade.group())}
        faila_kartēšana = {}
        for 이전, 이후 in kartēšana_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'vietējs_Tvērums' + 새이름
            faila_kartēšana[이전] = 새이름
        수정 = []
        이전토막 = ''
        for porcija_ievade in 토막들:
            낱말 = porcija_ievade.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in faila_kartēšana and 이전토막 != '.':
                수정.append((porcija_ievade.start(), porcija_ievade.end(), faila_kartēšana[낱말]))
                LOG_RECORD.append((str(CEĻŠ.relative_to(Project_sakne)), 낱말, faila_kartēšana[낱말]))
            이전토막 = 낱말
        for Palaist, 끝, 새이름 in reversed(수정): AVOTS = AVOTS[:Palaist] + 새이름 + AVOTS[끝:]
        if 수정: CEĻŠ.write_text(AVOTS)
(Project_sakne / '명명/자바이름대응.tsv').write_text('Fails\t이전\t이후\n' + ''.join('\t'.join(ievade_VALUE)+'\n' for ievade_VALUE in sorted(set(LOG_RECORD))))
print('Java Nosaukums Uzziņas mainīt_VALUE:', len(LOG_RECORD))
