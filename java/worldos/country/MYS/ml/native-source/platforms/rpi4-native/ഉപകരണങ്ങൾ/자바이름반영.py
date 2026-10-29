#!/usr/bin/env python3
"""자체 Java ലോക്കല്_സാധ്യത 이름을 바꾼다. സ്ട്രിംഗ്_മൂല്യം·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]
대응 = json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ലോഗ്_രേഖ = []
for ഡയറക്ടറി_മൂല്യം in ('ഉറവിടം', 'ഉപയോക്താവ്/자바', '한국어자바'):
    for വഴി in sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / ഡയറക്ടറി_മൂല്യം).rglob('*.java')):
        ഉറവിടം = വഴി.read_text()
        토막들 = list(토막식.finditer(ഉറവിടം))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ലോക്കല്_സാധ്യത' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ലോഗ്_രേഖ.append((str(വഴി.relative_to(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for നടപ്പിലാക്കുക, 끝, 새이름 in reversed(수정): ഉറവിടം = ഉറവിടം[:നടപ്പിലാക്കുക] + 새이름 + ഉറവിടം[끝:]
        if 수정: വഴി.write_text(ഉറവിടം)
(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '명명/자바이름대응.tsv').write_text('ഫയല്\t이전\t이후\n' + ''.join('\t'.join(എന്_ട്രി_മൂല്യം)+'\n' for എന്_ട്രി_മൂല്യം in sorted(set(ലോഗ്_രേഖ))))
print('Java പേരു് റഫറൻസ് മാറ്റികൊടുക്കുക_മൂല്യം:', len(ലോഗ്_രേഖ))
