#!/usr/bin/env python3
"""자체 Java స్థానిక_పరిధి 이름을 바꾼다. అక్షరసరం_మూల్యం·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
대응 = json.loads((ప్రొజెక్ట్_మూలం / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
లాగ్_వరుస = []
for సంచయని_మూల్యం in ('వనరు', 'వినియోగదారు/자바', '한국어자바'):
    for పాత్ in sorted((ప్రొజెక్ట్_మూలం / సంచయని_మూల్యం).rglob('*.java')):
        వనరు = పాత్.read_text()
        토막들 = list(토막식.finditer(వనరు))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'స్థానిక_పరిధి' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                లాగ్_వరుస.append((str(పాత్.relative_to(ప్రొజెక్ట్_మూలం)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for నడుపుము, 끝, 새이름 in reversed(수정): వనరు = వనరు[:నడుపుము] + 새이름 + వనరు[끝:]
        if 수정: పాత్.write_text(వనరు)
(ప్రొజెక్ట్_మూలం / '명명/자바이름대응.tsv').write_text('దస్త్రం\t이전\t이후\n' + ''.join('\t'.join(ప్రవేశం_మూల్యం)+'\n' for ప్రవేశం_మూల్యం in sorted(set(లాగ్_వరుస))))
print('Java పేరు సూచన మార్చు_మూల్యం:', len(లాగ్_వరుస))
