#!/usr/bin/env python3
"""자체 Java थळावो_मळ 이름을 바꾼다. स्ट्रिंग_मोल·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
대응 = json.loads((प्रॉजॅक्ट_रूट / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_नोंद = []
for नामावळ_मोल in ('स्त्रोत', 'उपेगकर्तो/자바', '한국어자바'):
    for पाथ in sorted((प्रॉजॅक्ट_रूट / नामावळ_मोल).rglob('*.java')):
        स्त्रोत = पाथ.read_text()
        토막들 = list(토막식.finditer(स्त्रोत))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'थळावो_मळ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_नोंद.append((str(पाथ.relative_to(प्रॉजॅक्ट_रूट)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for चलोवप, 끝, 새이름 in reversed(수정): स्त्रोत = स्त्रोत[:चलोवप] + 새이름 + स्त्रोत[끝:]
        if 수정: पाथ.write_text(स्त्रोत)
(प्रॉजॅक्ट_रूट / '명명/자바이름대응.tsv').write_text('फायल\t이전\t이후\n' + ''.join('\t'.join(प्रवेश_मोल)+'\n' for प्रवेश_मोल in sorted(set(LOG_नोंद))))
print('Java नांव संदर्भ बदलचें_मोल:', len(LOG_नोंद))
