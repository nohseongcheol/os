#!/usr/bin/env python3
"""자체 Java ਲੋਕਲ_ਗੁੰਜਾਇਸ਼ 이름을 바꾼다. ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
대응 = json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ਲੌਗ_ਕਤਾਰ = []
for ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ in ('ਸਰੋਤ', 'ਉਪਭੋਗਤਾ/자바', '한국어자바'):
    for ਮਾਰਗ in sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ).rglob('*.java')):
        ਸਰੋਤ = ਮਾਰਗ.read_text()
        토막들 = list(토막식.finditer(ਸਰੋਤ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ਲੋਕਲ_ਗੁੰਜਾਇਸ਼' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ਲੌਗ_ਕਤਾਰ.append((str(ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ਚਲਾਓ_2, 끝, 새이름 in reversed(수정): ਸਰੋਤ = ਸਰੋਤ[:ਚਲਾਓ_2] + 새이름 + ਸਰੋਤ[끝:]
        if 수정: ਮਾਰਗ.write_text(ਸਰੋਤ)
(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '명명/자바이름대응.tsv').write_text('ਫਾਇਲ\t이전\t이후\n' + ''.join('\t'.join(ਦਾਖਲਾ_ਕੀਮਤ)+'\n' for ਦਾਖਲਾ_ਕੀਮਤ in sorted(set(ਲੌਗ_ਕਤਾਰ))))
print('Java ਨਾਂ ਸੰਦਰਭ ਬਦਲੋ_ਕੀਮਤ:', len(ਲੌਗ_ਕਤਾਰ))
