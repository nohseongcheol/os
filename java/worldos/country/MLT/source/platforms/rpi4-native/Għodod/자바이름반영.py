#!/usr/bin/env python3
"""자체 Java lokali_ambitu 이름을 바꾼다. string_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

pprojetta_għerq = Path(__file__).resolve().parents[1]
대응 = json.loads((pprojetta_għerq / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for direttorju_VALUE in ('sors', 'utent/자바', '한국어자바'):
    for mogħdija in sorted((pprojetta_għerq / direttorju_VALUE).rglob('*.java')):
        sors = mogħdija.read_text()
        토막들 = list(토막식.finditer(sors))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokali_ambitu' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_RECORD.append((str(mogħdija.relative_to(pprojetta_għerq)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for serje, 끝, 새이름 in reversed(수정): sors = sors[:serje] + 새이름 + sors[끝:]
        if 수정: mogħdija.write_text(sors)
(pprojetta_għerq / '명명/자바이름대응.tsv').write_text('fajl\t이전\t이후\n' + ''.join('\t'.join(entrata_VALUE)+'\n' for entrata_VALUE in sorted(set(LOG_RECORD))))
print('Java isem Referenza bidel_VALUE:', len(LOG_RECORD))
