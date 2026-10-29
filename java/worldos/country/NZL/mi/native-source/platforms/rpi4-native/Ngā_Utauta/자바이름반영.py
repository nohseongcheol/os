#!/usr/bin/env python3
"""자체 Java paetata_whānuitanga 이름을 바꾼다. aho_uara·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

whakaatu_pūtake = Path(__file__).resolve().parents[1]
대응 = json.loads((whakaatu_pūtake / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for whaiaronga_uara in ('pūtake', 'kaiwhakamahi/자바', '한국어자바'):
    for ara in sorted((whakaatu_pūtake / whaiaronga_uara).rglob('*.java')):
        pūtake = ara.read_text()
        토막들 = list(토막식.finditer(pūtake))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'paetata_whānuitanga' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_RECORD.append((str(ara.relative_to(whakaatu_pūtake)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for whakahaere, 끝, 새이름 in reversed(수정): pūtake = pūtake[:whakahaere] + 새이름 + pūtake[끝:]
        if 수정: ara.write_text(pūtake)
(whakaatu_pūtake / '명명/자바이름대응.tsv').write_text('Kōnae\t이전\t이후\n' + ''.join('\t'.join(tāurunga_uara)+'\n' for tāurunga_uara in sorted(set(LOG_RECORD))))
print('Java Ingoa Pūranga_kōrero huri_uara:', len(LOG_RECORD))
