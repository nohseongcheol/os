#!/usr/bin/env python3
"""자체 Java ionadail_sgòp 이름을 바꾼다. sreang_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

tilg_freumh = Path(__file__).resolve().parents[1]
대응 = json.loads((tilg_freumh / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_ràgh = []
for eòlaire_VALUE in ('tùs', 'cleachdaiche/자바', '한국어자바'):
    for Slighe in sorted((tilg_freumh / eòlaire_VALUE).rglob('*.java')):
        tùs = Slighe.read_text()
        토막들 = list(토막식.finditer(tùs))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ionadail_sgòp' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_ràgh.append((str(Slighe.relative_to(tilg_freumh)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ruith, 끝, 새이름 in reversed(수정): tùs = tùs[:ruith] + 새이름 + tùs[끝:]
        if 수정: Slighe.write_text(tùs)
(tilg_freumh / '명명/자바이름대응.tsv').write_text('faidhle\t이전\t이후\n' + ''.join('\t'.join(cur_a_steach_VALUE)+'\n' for cur_a_steach_VALUE in sorted(set(LOG_ràgh))))
print('Java Ainm fiosrachadh atharraich_VALUE:', len(LOG_ràgh))
