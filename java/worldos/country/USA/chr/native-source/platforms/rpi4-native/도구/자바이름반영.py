#!/usr/bin/env python3
"""자체 Java ᎡᏍᎦᏂ_ᎢᎦᎢ 이름을 바꾼다. ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
대응 = json.loads((기준 / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = []
for ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ in ('ᎦᏟᏌᏅᎯ_0201f362', 'ᎬᏗᏍᎩ/자바', '한국어자바'):
    for ᎠᏍᏓᏩᏛᏍᏗ in sorted((기준 / ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ).rglob('*.java')):
        ᎦᏟᏌᏅᎯ_0201f362 = ᎠᏍᏓᏩᏛᏍᏗ.read_text()
        토막들 = list(토막식.finditer(ᎦᏟᏌᏅᎯ_0201f362))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ᎡᏍᎦᏂ_ᎢᎦᎢ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.append((str(ᎠᏍᏓᏩᏛᏍᏗ.relative_to(기준)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ᎠᎢᏎᏍᏗ, 끝, 새이름 in reversed(수정): ᎦᏟᏌᏅᎯ_0201f362 = ᎦᏟᏌᏅᎯ_0201f362[:ᎠᎢᏎᏍᏗ] + 새이름 + ᎦᏟᏌᏅᎯ_0201f362[끝:]
        if 수정: ᎠᏍᏓᏩᏛᏍᏗ.write_text(ᎦᏟᏌᏅᎯ_0201f362)
(기준 / '명명/자바이름대응.tsv').write_text('ᎠᏍᏆᏂᎪᏙᏗ\t이전\t이후\n' + ''.join('\t'.join(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)+'\n' for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in sorted(set(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ))))
print('Java ᏚᏙᎥᎢ 참조 ᎯᏁᏟᏴᎾ_ᏧᎬᏩᎶᏗᏯ:', len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ))
