#!/usr/bin/env python3
"""자체 Java agbègbè_sàkání 이름을 바꾼다. fọ́nrán_iye·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
대응 = json.loads((기준 / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
àkọsílẹ̀_ìṣe_ìlà_ìbú = []
for àkójọpọ̀_fáìlì_iye in ('orísun', 'aṣàmúlò/자바', '한국어자바'):
    for ọ̀nà in sorted((기준 / àkójọpọ̀_fáìlì_iye).rglob('*.java')):
        orísun = ọ̀nà.read_text()
        토막들 = list(토막식.finditer(orísun))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'agbègbè_sàkání' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                àkọsílẹ̀_ìṣe_ìlà_ìbú.append((str(ọ̀nà.relative_to(기준)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Rọ́ọ̀nù, 끝, 새이름 in reversed(수정): orísun = orísun[:Rọ́ọ̀nù] + 새이름 + orísun[끝:]
        if 수정: ọ̀nà.write_text(orísun)
(기준 / '명명/자바이름대응.tsv').write_text('Fáìlì\t이전\t이후\n' + ''.join('\t'.join(ìgbéwọlé_iye)+'\n' for ìgbéwọlé_iye in sorted(set(àkọsílẹ̀_ìṣe_ìlà_ìbú))))
print('Java Orúkọ Ìtọ́ka ṣàyípadà_iye:', len(àkọsílẹ̀_ìṣe_ìlà_ìbú))
