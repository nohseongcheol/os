#!/usr/bin/env python3
"""자체 Java lokal_Beräich 이름을 바꾼다. Zeechefolleg_VALUE·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

projezéieren_Racinn = Path(__file__).resolve().parents[1]
대응 = json.loads((projezéieren_Racinn / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_Rei = []
for Verzeechnes_VALUE in ('Quell', 'Benotzer/자바', '한국어자바'):
    for Wee in sorted((projezéieren_Racinn / Verzeechnes_VALUE).rglob('*.java')):
        Quell = Wee.read_text()
        토막들 = list(토막식.finditer(Quell))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_Beräich' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_Rei.append((str(Wee.relative_to(projezéieren_Racinn)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Laf, 끝, 새이름 in reversed(수정): Quell = Quell[:Laf] + 새이름 + Quell[끝:]
        if 수정: Wee.write_text(Quell)
(projezéieren_Racinn / '명명/자바이름대응.tsv').write_text('Fichier\t이전\t이후\n' + ''.join('\t'.join(Agab_VALUE)+'\n' for Agab_VALUE in sorted(set(LOG_Rei))))
print('Java Numm Referenzen änneren_VALUE:', len(LOG_Rei))
