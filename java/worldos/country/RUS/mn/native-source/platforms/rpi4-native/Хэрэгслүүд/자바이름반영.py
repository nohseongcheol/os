#!/usr/bin/env python3
"""자체 Java локал_хамрах_хүрээ 이름을 바꾼다. мөр_утга_6ca8363c·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
대응 = json.loads((기준 / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
бичих_мөр_6e8b375a = []
for лавлах_утга in ('ЭХ', 'хэрэглэгч/자바', '한국어자바'):
    for ЗАМ in sorted((기준 / лавлах_утга).rglob('*.java')):
        ЭХ = ЗАМ.read_text()
        토막들 = list(토막식.finditer(ЭХ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'локал_хамрах_хүрээ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                бичих_мөр_6e8b375a.append((str(ЗАМ.relative_to(기준)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Ажиллуулах, 끝, 새이름 in reversed(수정): ЭХ = ЭХ[:Ажиллуулах] + 새이름 + ЭХ[끝:]
        if 수정: ЗАМ.write_text(ЭХ)
(기준 / '명명/자바이름대응.tsv').write_text('Файл\t이전\t이후\n' + ''.join('\t'.join(оролт_утга)+'\n' for оролт_утга in sorted(set(бичих_мөр_6e8b375a))))
print('Java Нэр Толь_лавлах өөрчлөх_утга:', len(бичих_мөр_6e8b375a))
