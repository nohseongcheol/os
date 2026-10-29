#!/usr/bin/env python3
"""oma Java kohalik_skoop 이름을 바꾼다. string_VALUE·주석·väline_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_juur = Path(__file__).resolve().parents[1]
vastendamine_VALUE = json.loads((Project_juur / '명명/자바이름.json').read_text())
kogum_avaldis = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_kirje = []
for kaust_VALUE in ('ALLIKAS', 'kasutaja/자바', '한국어자바'):
    for RADA in sorted((Project_juur / kaust_VALUE).rglob('*.java')):
        ALLIKAS = RADA.read_text()
        토막들 = list(kogum_avaldis.finditer(ALLIKAS))
        사용이름 = {kogum_kirje.group() for kogum_kirje in 토막들 if re.search('[가-힣]', kogum_kirje.group())}
        faili_vastendamine = {}
        for 이전, 이후 in vastendamine_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'kohalik_skoop' + 새이름
            faili_vastendamine[이전] = 새이름
        수정 = []
        이전토막 = ''
        for kogum_kirje in 토막들:
            낱말 = kogum_kirje.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in faili_vastendamine and 이전토막 != '.':
                수정.append((kogum_kirje.start(), kogum_kirje.end(), faili_vastendamine[낱말]))
                LOG_kirje.append((str(RADA.relative_to(Project_juur)), 낱말, faili_vastendamine[낱말]))
            이전토막 = 낱말
        for Käivita_2, 끝, 새이름 in reversed(수정): ALLIKAS = ALLIKAS[:Käivita_2] + 새이름 + ALLIKAS[끝:]
        if 수정: RADA.write_text(ALLIKAS)
(Project_juur / '명명/자바이름대응.tsv').write_text('Fail\t이전\t이후\n' + ''.join('\t'.join(kirje_VALUE)+'\n' for kirje_VALUE in sorted(set(LOG_kirje))))
print('Java Nimi_2 viide muutma_VALUE:', len(LOG_kirje))
