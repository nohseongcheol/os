#!/usr/bin/env python3
"""자체 Java mahalliy_soha 이름을 바꾼다. satr_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_ildiz = Path(__file__).resolve().parents[1]
대응 = json.loads((Project_ildiz / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_satr = []
for katalog_VALUE in ('manba', 'foydalanuvchi/자바', '한국어자바'):
    for yo_l in sorted((Project_ildiz / katalog_VALUE).rglob('*.java')):
        manba = yo_l.read_text()
        토막들 = list(토막식.finditer(manba))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'mahalliy_soha' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_satr.append((str(yo_l.relative_to(Project_ildiz)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Bajarish, 끝, 새이름 in reversed(수정): manba = manba[:Bajarish] + 새이름 + manba[끝:]
        if 수정: yo_l.write_text(manba)
(Project_ildiz / '명명/자바이름대응.tsv').write_text('Fayl\t이전\t이후\n' + ''.join('\t'.join(kiritish_VALUE)+'\n' for kiritish_VALUE in sorted(set(LOG_satr))))
print('Java Nomi Ma_lumotnomalar o_zgartirmoq_VALUE:', len(LOG_satr))
