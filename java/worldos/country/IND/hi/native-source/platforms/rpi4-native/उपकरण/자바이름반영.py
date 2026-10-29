#!/usr/bin/env python3
"""निज Java स्थानीय_दायरा 이름을 바꾼다. स्ट्रिंग_मान·주석·बाहरी_मान 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]
대응 = json.loads((प्रोजेक्ट_करें_मूल / '명명/자바이름.json').read_text())
चंक_व्यंजक = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
लॉग_रिकॉर्ड = []
for डायरेक्टरी_मान in ('स्रोत', 'उपयोगकर्ता/자바', '한국어자바'):
    for पथ in sorted((प्रोजेक्ट_करें_मूल / डायरेक्टरी_मान).rglob('*.java')):
        स्रोत = पथ.read_text()
        토막들 = list(चंक_व्यंजक.finditer(स्रोत))
        사용이름 = {चंक_एन्ट्री.group() for चंक_एन्ट्री in 토막들 if re.search('[가-힣]', चंक_एन्ट्री.group())}
        फ़ाइल_मैपिंग = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'स्थानीय_दायरा' + 새이름
            फ़ाइल_मैपिंग[이전] = 새이름
        수정 = []
        이전토막 = ''
        for चंक_एन्ट्री in 토막들:
            낱말 = चंक_एन्ट्री.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in फ़ाइल_मैपिंग and 이전토막 != '.':
                수정.append((चंक_एन्ट्री.start(), चंक_एन्ट्री.end(), फ़ाइल_मैपिंग[낱말]))
                लॉग_रिकॉर्ड.append((str(पथ.relative_to(प्रोजेक्ट_करें_मूल)), 낱말, फ़ाइल_मैपिंग[낱말]))
            이전토막 = 낱말
        for चलाएँ, 끝, 새이름 in reversed(수정): स्रोत = स्रोत[:चलाएँ] + 새이름 + स्रोत[끝:]
        if 수정: पथ.write_text(स्रोत)
(प्रोजेक्ट_करें_मूल / '명명/자바이름대응.tsv').write_text('संचिका\t이전\t이후\n' + ''.join('\t'.join(एन्ट्री_मान)+'\n' for एन्ट्री_मान in sorted(set(लॉग_रिकॉर्ड))))
print('Java नाम संदर्भ परिवर्तित_करें_मान:', len(लॉग_रिकॉर्ड))
