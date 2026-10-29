#!/usr/bin/env python3
"""savas Java vietinis_Aprėptis 이름을 바꾼다. eilutė_VALUE·주석·išorinis_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_šaknis = Path(__file__).resolve().parents[1]
susiejimas_VALUE = json.loads((Project_šaknis / '명명/자바이름.json').read_text())
segmentas_reiškinys = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for Katalogas_VALUE in ('ŠALTINIS', 'naudotojas/자바', '한국어자바'):
    for KELIAS in sorted((Project_šaknis / Katalogas_VALUE).rglob('*.java')):
        ŠALTINIS = KELIAS.read_text()
        토막들 = list(segmentas_reiškinys.finditer(ŠALTINIS))
        사용이름 = {segmentas_įrašas.group() for segmentas_įrašas in 토막들 if re.search('[가-힣]', segmentas_įrašas.group())}
        failo_susiejimas = {}
        for 이전, 이후 in susiejimas_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'vietinis_Aprėptis' + 새이름
            failo_susiejimas[이전] = 새이름
        수정 = []
        이전토막 = ''
        for segmentas_įrašas in 토막들:
            낱말 = segmentas_įrašas.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in failo_susiejimas and 이전토막 != '.':
                수정.append((segmentas_įrašas.start(), segmentas_įrašas.end(), failo_susiejimas[낱말]))
                LOG_RECORD.append((str(KELIAS.relative_to(Project_šaknis)), 낱말, failo_susiejimas[낱말]))
            이전토막 = 낱말
        for Paleisti, 끝, 새이름 in reversed(수정): ŠALTINIS = ŠALTINIS[:Paleisti] + 새이름 + ŠALTINIS[끝:]
        if 수정: KELIAS.write_text(ŠALTINIS)
(Project_šaknis / '명명/자바이름대응.tsv').write_text('Failas\t이전\t이후\n' + ''.join('\t'.join(įrašas_VALUE)+'\n' for įrašas_VALUE in sorted(set(LOG_RECORD))))
print('Java Pavadinimas_2 nuoroda keisti_VALUE:', len(LOG_RECORD))
