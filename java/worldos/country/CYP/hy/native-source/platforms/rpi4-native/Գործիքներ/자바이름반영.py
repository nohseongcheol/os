#!/usr/bin/env python3
"""자체 Java տեղային_շրջանակ 이름을 바꾼다. տող_արժեք_6ca8363c·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

արձակել_արմատ = Path(__file__).resolve().parents[1]
대응 = json.loads((արձակել_արմատ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
մատյան_տող = []
for գրացուցակ_արժեք in ('ԱՂԲՅՈՒՐ', 'օգտվող/자바', '한국어자바'):
    for Ճանապարհ in sorted((արձակել_արմատ / գրացուցակ_արժեք).rglob('*.java')):
        ԱՂԲՅՈՒՐ = Ճանապարհ.read_text()
        토막들 = list(토막식.finditer(ԱՂԲՅՈՒՐ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'տեղային_շրջանակ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                մատյան_տող.append((str(Ճանապարհ.relative_to(արձակել_արմատ)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Գործարկել, 끝, 새이름 in reversed(수정): ԱՂԲՅՈՒՐ = ԱՂԲՅՈՒՐ[:Գործարկել] + 새이름 + ԱՂԲՅՈՒՐ[끝:]
        if 수정: Ճանապարհ.write_text(ԱՂԲՅՈՒՐ)
(արձակել_արմատ / '명명/자바이름대응.tsv').write_text('Ֆայլ\t이전\t이후\n' + ''.join('\t'.join(մուտքագրում_արժեք)+'\n' for մուտքագրում_արժեք in sorted(set(մատյան_տող))))
print('Java Անուն Տեղեկատուներ փոխել_արժեք:', len(մատյան_տող))
