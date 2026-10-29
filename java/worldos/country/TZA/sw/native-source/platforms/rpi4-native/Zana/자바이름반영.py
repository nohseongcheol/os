#!/usr/bin/env python3
"""자체 Java jirani_upeo 이름을 바꾼다. tungo_thamani·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
대응 = json.loads((기준 / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
batli_REKODI = []
for Saraka_thamani in ('chanzo', 'mtumiaji/자바', '한국어자바'):
    for njia in sorted((기준 / Saraka_thamani).rglob('*.java')):
        chanzo = njia.read_text()
        토막들 = list(토막식.finditer(chanzo))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'jirani_upeo' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                batli_REKODI.append((str(njia.relative_to(기준)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for endesha, 끝, 새이름 in reversed(수정): chanzo = chanzo[:endesha] + 새이름 + chanzo[끝:]
        if 수정: njia.write_text(chanzo)
(기준 / '명명/자바이름대응.tsv').write_text('faili\t이전\t이후\n' + ''.join('\t'.join(ingizo_thamani)+'\n' for ingizo_thamani in sorted(set(batli_REKODI))))
print('Java Jina Marejeleo badilisha_thamani_16f64fe4:', len(batli_REKODI))
