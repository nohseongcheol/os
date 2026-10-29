#!/usr/bin/env python3
"""자체 Java ក្នុងតំបន់_ដែនកំណត់_វិសាលភាព 이름을 바꾼다. សំនុំអក្សរ_តំលៃ·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
대응 = json.loads((បញ្ចាំង_ឬស / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
កំណត់_ហេតុ_ថត = []
for បញ្ជី_តំលៃ in ('ប្រភព', 'អ្នកប្រើ/자바', '한국어자바'):
    for ផ្លូវ in sorted((បញ្ចាំង_ឬស / បញ្ជី_តំលៃ).rglob('*.java')):
        ប្រភព = ផ្លូវ.read_text()
        토막들 = list(토막식.finditer(ប្រភព))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ក្នុងតំបន់_ដែនកំណត់_វិសាលភាព' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                កំណត់_ហេតុ_ថត.append((str(ផ្លូវ.relative_to(បញ្ចាំង_ឬស)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for រត់, 끝, 새이름 in reversed(수정): ប្រភព = ប្រភព[:រត់] + 새이름 + ប្រភព[끝:]
        if 수정: ផ្លូវ.write_text(ប្រភព)
(បញ្ចាំង_ឬស / '명명/자바이름대응.tsv').write_text('ឯកសារ\t이전\t이후\n' + ''.join('\t'.join(ការបញ្ចូល_តំលៃ)+'\n' for ការបញ្ចូល_តំលៃ in sorted(set(កំណត់_ហេតុ_ថត))))
print('Java ឈ្មោះ យោង កែប្រែ_តំលៃ:', len(កំណត់_ហេតុ_ថត))
