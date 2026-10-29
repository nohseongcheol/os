#!/usr/bin/env python3
"""자체 Java ლოკალური_არეალი 이름을 바꾼다. სტრიქონი_მნიშვნელობა·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]
대응 = json.loads((პროეცირება_ფესვი / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
ჟურნალი_ჩაწერა = []
for საქაღალდე_მნიშვნელობა in ('წყარო', 'მომხმარებელი/자바', '한국어자바'):
    for გეზი in sorted((პროეცირება_ფესვი / საქაღალდე_მნიშვნელობა).rglob('*.java')):
        წყარო = გეზი.read_text()
        토막들 = list(토막식.finditer(წყარო))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'ლოკალური_არეალი' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                ჟურნალი_ჩაწერა.append((str(გეზი.relative_to(პროეცირება_ფესვი)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for გაშვება, 끝, 새이름 in reversed(수정): წყარო = წყარო[:გაშვება] + 새이름 + წყარო[끝:]
        if 수정: გეზი.write_text(წყარო)
(პროეცირება_ფესვი / '명명/자바이름대응.tsv').write_text('ფაილი\t이전\t이후\n' + ''.join('\t'.join(შენატანი_მნიშვნელობა)+'\n' for შენატანი_მნიშვნელობა in sorted(set(ჟურნალი_ჩაწერა))))
print('Java სახელი ცნობარები შეცვლა_მნიშვნელობა:', len(ჟურნალი_ჩაწერა))
