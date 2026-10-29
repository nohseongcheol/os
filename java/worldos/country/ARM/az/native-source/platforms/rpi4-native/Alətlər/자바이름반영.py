#!/usr/bin/env python3
"""자체 Java lokal_miqyas 이름을 바꾼다. sətir_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_kök = Path(__file__).resolve().parents[1]
대응 = json.loads((Project_kök / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_yaz = []
for kataloq_VALUE in ('QAYNAQ', 'istifadəçi/자바', '한국어자바'):
    for Cığır in sorted((Project_kök / kataloq_VALUE).rglob('*.java')):
        QAYNAQ = Cığır.read_text()
        토막들 = list(토막식.finditer(QAYNAQ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_miqyas' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_yaz.append((str(Cığır.relative_to(Project_kök)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for İcra_Et, 끝, 새이름 in reversed(수정): QAYNAQ = QAYNAQ[:İcra_Et] + 새이름 + QAYNAQ[끝:]
        if 수정: Cığır.write_text(QAYNAQ)
(Project_kök / '명명/자바이름대응.tsv').write_text('FAYL\t이전\t이후\n' + ''.join('\t'.join(daxiletmə_VALUE)+'\n' for daxiletmə_VALUE in sorted(set(LOG_yaz))))
print('Java Ad İstinad dəyişdirmək_VALUE:', len(LOG_yaz))
