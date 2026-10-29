#!/usr/bin/env python3
"""자체 Java lokal_område 이름을 바꾼다. streng_VALUE·주석·ekstern_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

spegle_rot = Path(__file__).resolve().parents[1]
대응 = json.loads((spegle_rot / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_rad = []
for katalog_VALUE in ('KJELDE', 'brukar/자바', '한국어자바'):
    for STIGE in sorted((spegle_rot / katalog_VALUE).rglob('*.java')):
        KJELDE = STIGE.read_text()
        토막들 = list(토막식.finditer(KJELDE))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_område' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_rad.append((str(STIGE.relative_to(spegle_rot)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Køyr_2, 끝, 새이름 in reversed(수정): KJELDE = KJELDE[:Køyr_2] + 새이름 + KJELDE[끝:]
        if 수정: STIGE.write_text(KJELDE)
(spegle_rot / '명명/자바이름대응.tsv').write_text('Fil\t이전\t이후\n' + ''.join('\t'.join(oppføring_VALUE)+'\n' for oppføring_VALUE in sorted(set(LOG_rad))))
print('Java Namn Oppslagsverk endre_VALUE:', len(LOG_rad))
