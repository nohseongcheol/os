#!/usr/bin/env python3
"""propriu Java local_gamă 이름을 바꾼다. șir_VALUE·주석·extern_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_rădăcină = Path(__file__).resolve().parents[1]
mapare_VALUE = json.loads((Project_rădăcină / '명명/자바이름.json').read_text())
bloc_expresie = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for Director_VALUE in ('SURSĂ', 'utilizator/자바', '한국어자바'):
    for Cale in sorted((Project_rădăcină / Director_VALUE).rglob('*.java')):
        SURSĂ = Cale.read_text()
        토막들 = list(bloc_expresie.finditer(SURSĂ))
        사용이름 = {bloc_intrare.group() for bloc_intrare in 토막들 if re.search('[가-힣]', bloc_intrare.group())}
        mapare_fișier = {}
        for Anteriorul_element, 이후 in mapare_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'local_gamă' + 새이름
            mapare_fișier[Anteriorul_element] = 새이름
        수정 = []
        Anteriorul_bloc = ''
        for bloc_intrare in 토막들:
            낱말 = bloc_intrare.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapare_fișier and Anteriorul_bloc != '.':
                수정.append((bloc_intrare.start(), bloc_intrare.end(), mapare_fișier[낱말]))
                LOG_RECORD.append((str(Cale.relative_to(Project_rădăcină)), 낱말, mapare_fișier[낱말]))
            Anteriorul_bloc = 낱말
        for Pornește, 끝, 새이름 in reversed(수정): SURSĂ = SURSĂ[:Pornește] + 새이름 + SURSĂ[끝:]
        if 수정: Cale.write_text(SURSĂ)
(Project_rădăcină / '명명/자바이름대응.tsv').write_text('Fișier\t이전\t이후\n' + ''.join('\t'.join(intrare_VALUE)+'\n' for intrare_VALUE in sorted(set(LOG_RECORD))))
print('Java Nume referință schimba_VALUE:', len(LOG_RECORD))
