#!/usr/bin/env python3
"""자체 Java தனி_நோக்கி 이름을 바꾼다. சரம்_மதிப்பு·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]
대응 = json.loads((திட்டப்பணி_மூலம் / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
பதிவு_பதிவு = []
for கோப்பகம்_மதிப்பு in ('மூலக்_கோப்பு', 'பயனர்/자바', '한국어자바'):
    for பாதை_2 in sorted((திட்டப்பணி_மூலம் / கோப்பகம்_மதிப்பு).rglob('*.java')):
        மூலக்_கோப்பு = பாதை_2.read_text()
        토막들 = list(토막식.finditer(மூலக்_கோப்பு))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'தனி_நோக்கி' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                பதிவு_பதிவு.append((str(பாதை_2.relative_to(திட்டப்பணி_மூலம்)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for செயல்படுத்துக, 끝, 새이름 in reversed(수정): மூலக்_கோப்பு = மூலக்_கோப்பு[:செயல்படுத்துக] + 새이름 + மூலக்_கோப்பு[끝:]
        if 수정: பாதை_2.write_text(மூலக்_கோப்பு)
(திட்டப்பணி_மூலம் / '명명/자바이름대응.tsv').write_text('கோப்பின்_பெயர்\t이전\t이후\n' + ''.join('\t'.join(உள்ளீடு_மதிப்பு)+'\n' for உள்ளீடு_மதிப்பு in sorted(set(பதிவு_பதிவு))))
print('Java பெயர் மேற்கோள் மாற்று_மதிப்பு_16f64fe4:', len(பதிவு_பதிவு))
