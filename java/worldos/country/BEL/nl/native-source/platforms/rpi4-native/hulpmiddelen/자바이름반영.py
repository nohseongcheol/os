#!/usr/bin/env python3
"""Eigen Java lokaal_scope 이름을 바꾼다. tekenreeks_WAARDE·주석·extern_WAARDE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Taken_wortel = Path(__file__).resolve().parents[1]
toewijzing_WAARDE = json.loads((Taken_wortel / '명명/자바이름.json').read_text())
chunk_expressie = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_RECORD = []
for map_WAARDE in ('broncode', 'gebruikersruimte/자바', '한국어자바'):
    for pad in sorted((Taken_wortel / map_WAARDE).rglob('*.java')):
        broncode = pad.read_text()
        토막들 = list(chunk_expressie.finditer(broncode))
        사용이름 = {chunk_invoer.group() for chunk_invoer in 토막들 if re.search('[가-힣]', chunk_invoer.group())}
        bestandstoewijzing = {}
        for Vorige_item, 이후 in toewijzing_WAARDE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokaal_scope' + 새이름
            bestandstoewijzing[Vorige_item] = 새이름
        수정 = []
        Vorige_chunk = ''
        for chunk_invoer in 토막들:
            낱말 = chunk_invoer.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in bestandstoewijzing and Vorige_chunk != '.':
                수정.append((chunk_invoer.start(), chunk_invoer.end(), bestandstoewijzing[낱말]))
                LOG_RECORD.append((str(pad.relative_to(Taken_wortel)), 낱말, bestandstoewijzing[낱말]))
            Vorige_chunk = 낱말
        for starten, 끝, 새이름 in reversed(수정): broncode = broncode[:starten] + 새이름 + broncode[끝:]
        if 수정: pad.write_text(broncode)
(Taken_wortel / '명명/자바이름대응.tsv').write_text('bestand\t이전\t이후\n' + ''.join('\t'.join(invoer_WAARDE_962f286b)+'\n' for invoer_WAARDE_962f286b in sorted(set(LOG_RECORD))))
print('Java Naam verwijzen wijzigen_WAARDE:', len(LOG_RECORD))
