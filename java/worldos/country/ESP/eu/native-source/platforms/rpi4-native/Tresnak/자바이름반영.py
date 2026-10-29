#!/usr/bin/env python3
"""자체 Java lokal_esparru 이름을 바꾼다. kate_balio·주석·외부 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_erro = Path(__file__).resolve().parents[1]
대응 = json.loads((Project_erro / '명명/자바이름.json').read_text())
토막식 = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_marka = []
for direktorio_balio in ('ITURBURUA', 'erabiltzaile/자바', '한국어자바'):
    for Bide_izena in sorted((Project_erro / direktorio_balio).rglob('*.java')):
        ITURBURUA = Bide_izena.read_text()
        토막들 = list(토막식.finditer(ITURBURUA))
        사용이름 = {토막.group() for 토막 in 토막들 if re.search('[가-힣]', 토막.group())}
        이파일대응 = {}
        for 이전, 이후 in 대응.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokal_esparru' + 새이름
            이파일대응[이전] = 새이름
        수정 = []
        이전토막 = ''
        for 토막 in 토막들:
            낱말 = 토막.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in 이파일대응 and 이전토막 != '.':
                수정.append((토막.start(), 토막.end(), 이파일대응[낱말]))
                LOG_marka.append((str(Bide_izena.relative_to(Project_erro)), 낱말, 이파일대응[낱말]))
            이전토막 = 낱말
        for Exekutatu_2, 끝, 새이름 in reversed(수정): ITURBURUA = ITURBURUA[:Exekutatu_2] + 새이름 + ITURBURUA[끝:]
        if 수정: Bide_izena.write_text(ITURBURUA)
(Project_erro / '명명/자바이름대응.tsv').write_text('Fitxategia\t이전\t이후\n' + ''.join('\t'.join(sarrera_balio)+'\n' for sarrera_balio in sorted(set(LOG_marka))))
print('Java Izena Erreferentzia_materiala aldatu_balio:', len(LOG_marka))
