#!/usr/bin/env python3
"""निज Java स्थानीय_क्षेत्र 이름을 바꾼다. स्ट्रिङ_मान·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

परियोजना_रूट = Path(__file__).resolve().parents[1]
대응 = json.loads((परियोजना_रूट / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
लग_रेकर्ड = []
for डाइरेक्टरी_मान in ('स्रोत', 'प्रयोगकर्ता/자바', '한국어자바'):
    for मार्ग in sorted((परियोजना_रूट / डाइरेक्टरी_मान).rglob('*.java')):
        स्रोत = मार्ग.read_text()
        토막들 = list(토막식.finditer(स्रोत))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'स्थानीय_क्षेत्र' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                लग_रेकर्ड.append((str(मार्ग.relative_to(परियोजना_रूट)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for चलाउनुहोस्, 끝, 새이름 in reversed(수정): स्रोत = स्रोत[:चलाउनुहोस्] + 새이름 + स्रोत[끝:]
        if 수정: मार्ग.write_text(स्रोत)
(परियोजना_रूट / '명명/자바이름대응.tsv').write_text('फाइल\t이전\t이후\n' + ''.join('\t'.join(प्रविष्टि_मान)+'\n' for प्रविष्टि_मान in sorted(set(लग_रेकर्ड))))
print('Java नाम निर्देश परिवर्तन_मान:', len(लग_रेकर्ड))
