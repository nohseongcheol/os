#!/usr/bin/env python3
"""자체 Java ಸ್ಥಳೀಯ_ವ್ಯಾಪ್ತಿ 이름을 바꾼다. ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
대응 = json.loads((ಬಿಂಬಿಸು_ಮೂಲ / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ಲಾಗ್_ದಾಖಲೆ = []
for ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ in ('ಮೂಲ', 'ಬಳಕೆದಾರ/자바', '한국어자바'):
    for ಮಾರ್ಗ in sorted((ಬಿಂಬಿಸು_ಮೂಲ / ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ).rglob('*.java')):
        ಮೂಲ = ಮಾರ್ಗ.read_text()
        토막들 = list(토막식.finditer(ಮೂಲ))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ಸ್ಥಳೀಯ_ವ್ಯಾಪ್ತಿ' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ಲಾಗ್_ದಾಖಲೆ.append((str(ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ಚಲಾಯಿಸು_2, 끝, 새이름 in reversed(수정): ಮೂಲ = ಮೂಲ[:ಚಲಾಯಿಸು_2] + 새이름 + ಮೂಲ[끝:]
        if 수정: ಮಾರ್ಗ.write_text(ಮೂಲ)
(ಬಿಂಬಿಸು_ಮೂಲ / '명명/자바이름대응.tsv').write_text('ಕಡತ\t이전\t이후\n' + ''.join('\t'.join(ನಮೂದು_ಮೌಲ್ಯ)+'\n' for ನಮೂದು_ಮೌಲ್ಯ in sorted(set(ಲಾಗ್_ದಾಖಲೆ))))
print('Java ಹೆಸರು ಉಲ್ಲೇಖ ಬದಲಿಸು_ಮೌಲ್ಯ:', len(ಲಾಗ್_ದಾಖಲೆ))
