#!/usr/bin/env python3
"""자체 Java يەرلىك_بوشلۇق 이름을 바꾼다. ھەرپ_تىزمىسى_قىممىتى·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]
대응 = json.loads((كۆرسىتىش_يىلتىز / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
خاتىرە_قۇر = []
for مۇندەرىجە_قىممىتى in ('مەنبە', 'ئىشلەتكۈچى/자바', '한국어자바'):
    for يول in sorted((كۆرسىتىش_يىلتىز / مۇندەرىجە_قىممىتى).rglob('*.java')):
        مەنبە = يول.read_text()
        토막들 = list(토막식.finditer(مەنبە))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'يەرلىك_بوشلۇق' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                خاتىرە_قۇر.append((str(يول.relative_to(كۆرسىتىش_يىلتىز)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for ئىجرا_قىل_2, 끝, 새이름 in reversed(수정): مەنبە = مەنبە[:ئىجرا_قىل_2] + 새이름 + مەنبە[끝:]
        if 수정: يول.write_text(مەنبە)
(كۆرسىتىش_يىلتىز / '명명/자바이름대응.tsv').write_text('ھۆججەت\t이전\t이후\n' + ''.join('\t'.join(كىرگۈزۈش_قىممىتى)+'\n' for كىرگۈزۈش_قىممىتى in sorted(set(خاتىرە_قۇر))))
print('Java ئاتى پايدىلانما ئۆزگەرتمەك_قىممىتى:', len(خاتىرە_قۇر))
