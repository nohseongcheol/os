#!/usr/bin/env python3
"""자체 Java жергілікті_Аумақ 이름을 바꾼다. жол_мән_6ca8363c·주석·сыртқы_мән 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

жоба_түбір = Path(__file__).resolve().parents[1]
대응 = json.loads((жоба_түбір / '명명/자바이름.json').read_text())
блок_өрнек = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
журнал_жол = []
for каталог_мән in ('Неден', 'пайдаланушы/자바', '한국어자바'):
    for Жол_2 in sorted((жоба_түбір / каталог_мән).rglob('*.java')):
        Неден = Жол_2.read_text()
        토막들 = list(блок_өрнек.finditer(Неден))
        사용이름 = {блок_енгізу.group() for блок_енгізу in 토막들 if re.search('[가-힣]', блок_енгізу.group())}
        файлдарды_салыстыру = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'жергілікті_Аумақ' + 새이름
            файлдарды_салыстыру[이전] = 새이름
        수정 = []
        이전토막 = ''
        for блок_енгізу in 토막들:
            낱말 = блок_енгізу.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in файлдарды_салыстыру and 이전토막 != '.':
                수정.append((блок_енгізу.start(), блок_енгізу.end(), файлдарды_салыстыру[낱말]))
                журнал_жол.append((str(Жол_2.relative_to(жоба_түбір)), 낱말, файлдарды_салыстыру[낱말]))
            이전토막 = 낱말
        for Орындау_2, 끝, 새이름 in reversed(수정): Неден = Неден[:Орындау_2] + 새이름 + Неден[끝:]
        if 수정: Жол_2.write_text(Неден)
(жоба_түбір / '명명/자바이름대응.tsv').write_text('Файл\t이전\t이후\n' + ''.join('\t'.join(енгізу_мән)+'\n' for енгізу_мән in sorted(set(журнал_жол))))
print('Java Аты Анықтамалық өзгерту_мән:', len(журнал_жол))
