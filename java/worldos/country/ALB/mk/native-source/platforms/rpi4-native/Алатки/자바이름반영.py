#!/usr/bin/env python3
"""자체 Java локален_обем 이름을 바꾼다. низа_VALUE_6ca8363c·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_корен = Path(__file__).resolve().parents[1]
대응 = json.loads((Project_корен / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_ред = []
for Именик_VALUE in ('ИЗВОР', 'корисник/자바', '한국어자바'):
    for ПАТЕКА in sorted((Project_корен / Именик_VALUE).rglob('*.java')):
        ИЗВОР = ПАТЕКА.read_text()
        토막들 = list(토막식.finditer(ИЗВОР))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'локален_обем' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_ред.append((str(ПАТЕКА.relative_to(Project_корен)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Изврши_2, 끝, 새이름 in reversed(수정): ИЗВОР = ИЗВОР[:Изврши_2] + 새이름 + ИЗВОР[끝:]
        if 수정: ПАТЕКА.write_text(ИЗВОР)
(Project_корен / '명명/자바이름대응.tsv').write_text('Датотека\t이전\t이후\n' + ''.join('\t'.join(внес_VALUE)+'\n' for внес_VALUE in sorted(set(LOG_ред))))
print('Java Име Референци измени_VALUE:', len(LOG_ред))
