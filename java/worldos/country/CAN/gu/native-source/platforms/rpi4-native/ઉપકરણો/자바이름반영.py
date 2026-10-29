#!/usr/bin/env python3
"""자체 Java સ્થાનિક_અવકાશ 이름을 바꾼다. સ્ટ્રિંગ_મૂલ્ય·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
대응 = json.loads((પ્રોજેક્ટ_રૂટ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
લૉગ_પંક્તિ = []
for નિર્દેશિકા_મૂલ્ય in ('સ્રોત', 'ઉપયોગકર્તા/자바', '한국어자바'):
    for પથ in sorted((પ્રોજેક્ટ_રૂટ / નિર્દેશિકા_મૂલ્ય).rglob('*.java')):
        સ્રોત = પથ.read_text()
        토막들 = list(토막식.finditer(સ્રોત))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'સ્થાનિક_અવકાશ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                લૉગ_પંક્તિ.append((str(પથ.relative_to(પ્રોજેક્ટ_રૂટ)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ચલાવો_2, 끝, 새이름 in reversed(수정): સ્રોત = સ્રોત[:ચલાવો_2] + 새이름 + સ્રોત[끝:]
        if 수정: પથ.write_text(સ્રોત)
(પ્રોજેક્ટ_રૂટ / '명명/자바이름대응.tsv').write_text('ફાઈલ\t이전\t이후\n' + ''.join('\t'.join(પ્રવેશ_મૂલ્ય)+'\n' for પ્રવેશ_મૂલ્ય in sorted(set(લૉગ_પંક્તિ))))
print('Java નામ સંદર્ભ પરિવર્તન_કરો_મૂલ્ય:', len(લૉગ_પંક્તિ))
