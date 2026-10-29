#!/usr/bin/env python3
"""자체 Java የአካባቢ_ስፋት 이름을 바꾼다. ኅብረቁምፊ_እሴት·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

አሳይ_ስር = Path(__file__).resolve().parents[1]
대응 = json.loads((አሳይ_ስር / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
መዝግብ_ረድፍ = []
for ማውጫ_እሴት in ('ምንጭ', 'ተጠቃሚ/자바', '한국어자바'):
    for መተላለፊያ in sorted((አሳይ_ስር / ማውጫ_እሴት).rglob('*.java')):
        ምንጭ = መተላለፊያ.read_text()
        토막들 = list(토막식.finditer(ምንጭ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'የአካባቢ_ስፋት' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                መዝግብ_ረድፍ.append((str(መተላለፊያ.relative_to(አሳይ_ስር)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ማስኬጃ, 끝, 새이름 in reversed(수정): ምንጭ = ምንጭ[:ማስኬጃ] + 새이름 + ምንጭ[끝:]
        if 수정: መተላለፊያ.write_text(ምንጭ)
(አሳይ_ስር / '명명/자바이름대응.tsv').write_text('ፋይል\t이전\t이후\n' + ''.join('\t'.join(ምዝግብ_እሴት)+'\n' for ምዝግብ_እሴት in sorted(set(መዝግብ_ረድፍ))))
print('Java ስም ማጣቀሻ ለውጥ_እሴት:', len(መዝግብ_ረድፍ))
