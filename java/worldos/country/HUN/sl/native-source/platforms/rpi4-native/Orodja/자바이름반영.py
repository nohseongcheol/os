#!/usr/bin/env python3
"""lastno Java lokalen_krajeven_obseg 이름을 바꾼다. niz_VALUE·주석·zunanji_VALUE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

pobuda_koren = Path(__file__).resolve().parents[1]
preslikava_VALUE = json.loads((pobuda_koren / '명명/자바이름.json').read_text())
košček_izraz = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_zapis = []
for Imenik_VALUE in ('VIR', 'uporabnik/자바', '한국어자바'):
    for POT in sorted((pobuda_koren / Imenik_VALUE).rglob('*.java')):
        VIR = POT.read_text()
        토막들 = list(košček_izraz.finditer(VIR))
        사용이름 = {košček_vnos.group() for košček_vnos in 토막들 if re.search('[가-힣]', košček_vnos.group())}
        preslikava_datoteke = {}
        for 이전, 이후 in preslikava_VALUE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokalen_krajeven_obseg' + 새이름
            preslikava_datoteke[이전] = 새이름
        수정 = []
        이전토막 = ''
        for košček_vnos in 토막들:
            낱말 = košček_vnos.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in preslikava_datoteke and 이전토막 != '.':
                수정.append((košček_vnos.start(), košček_vnos.end(), preslikava_datoteke[낱말]))
                LOG_zapis.append((str(POT.relative_to(pobuda_koren)), 낱말, preslikava_datoteke[낱말]))
            이전토막 = 낱말
        for Zaženi, 끝, 새이름 in reversed(수정): VIR = VIR[:Zaženi] + 새이름 + VIR[끝:]
        if 수정: POT.write_text(VIR)
(pobuda_koren / '명명/자바이름대응.tsv').write_text('Datoteka\t이전\t이후\n' + ''.join('\t'.join(vnos_VALUE)+'\n' for vnos_VALUE in sorted(set(LOG_zapis))))
print('Java Ime Gradiva spremeniti_VALUE:', len(LOG_zapis))
