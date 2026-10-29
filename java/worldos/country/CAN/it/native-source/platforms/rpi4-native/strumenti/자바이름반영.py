#!/usr/bin/env python3
"""nativo Java locale_Scope 이름을 바꾼다. stringa_VALORE·주석·esterno_VALORE 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

azione_radice = Path(__file__).resolve().parents[1]
mapping_VALORE = json.loads((azione_radice / '명명/자바이름.json').read_text())
blocco_espressione = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_riga = []
for elenco_VALORE in ('codiceSorgente', 'spazio_utente/자바', '한국어자바'):
    for percorso in sorted((azione_radice / elenco_VALORE).rglob('*.java')):
        codiceSorgente = percorso.read_text()
        토막들 = list(blocco_espressione.finditer(codiceSorgente))
        사용이름 = {blocco_voce.group() for blocco_voce in 토막들 if re.search('[가-힣]', blocco_voce.group())}
        mapping_del_file = {}
        for Indietro_articolo, 이후 in mapping_VALORE.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'locale_Scope' + 새이름
            mapping_del_file[Indietro_articolo] = 새이름
        수정 = []
        Indietro_blocco = ''
        for blocco_voce in 토막들:
            낱말 = blocco_voce.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapping_del_file and Indietro_blocco != '.':
                수정.append((blocco_voce.start(), blocco_voce.end(), mapping_del_file[낱말]))
                LOG_riga.append((str(percorso.relative_to(azione_radice)), 낱말, mapping_del_file[낱말]))
            Indietro_blocco = 낱말
        for avvia, 끝, 새이름 in reversed(수정): codiceSorgente = codiceSorgente[:avvia] + 새이름 + codiceSorgente[끝:]
        if 수정: percorso.write_text(codiceSorgente)
(azione_radice / '명명/자바이름대응.tsv').write_text('file\t이전\t이후\n' + ''.join('\t'.join(voce_VALORE)+'\n' for voce_VALORE in sorted(set(LOG_riga))))
print('Java Nome fonti cambiare_VALORE:', len(LOG_riga))
