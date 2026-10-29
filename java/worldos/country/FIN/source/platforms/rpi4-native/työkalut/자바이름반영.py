#!/usr/bin/env python3
"""oma Java paikallinen_laajuus 이름을 바꾼다. merkkijono_ARVO·주석·ulkoinen_ARVO 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

aloite_juuri = Path(__file__).resolve().parents[1]
yhdistämismääritys_ARVO = json.loads((aloite_juuri / '명명/자바이름.json').read_text())
lohko_lauseke = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_TIETUE = []
for Directory_ARVO in ('lähdetiedosto', 'käyttäjätila/자바', '한국어자바'):
    for polku_2 in sorted((aloite_juuri / Directory_ARVO).rglob('*.java')):
        lähdetiedosto = polku_2.read_text()
        토막들 = list(lohko_lauseke.finditer(lähdetiedosto))
        사용이름 = {lohko_merkintä.group() for lohko_merkintä in 토막들 if re.search('[가-힣]', lohko_merkintä.group())}
        tiedostovastaavuus = {}
        for Edellinen_kohde, 이후 in yhdistämismääritys_ARVO.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'paikallinen_laajuus' + 새이름
            tiedostovastaavuus[Edellinen_kohde] = 새이름
        수정 = []
        Edellinen_lohko = ''
        for lohko_merkintä in 토막들:
            낱말 = lohko_merkintä.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in tiedostovastaavuus and Edellinen_lohko != '.':
                수정.append((lohko_merkintä.start(), lohko_merkintä.end(), tiedostovastaavuus[낱말]))
                LOG_TIETUE.append((str(polku_2.relative_to(aloite_juuri)), 낱말, tiedostovastaavuus[낱말]))
            Edellinen_lohko = 낱말
        for Suorita_2, 끝, 새이름 in reversed(수정): lähdetiedosto = lähdetiedosto[:Suorita_2] + 새이름 + lähdetiedosto[끝:]
        if 수정: polku_2.write_text(lähdetiedosto)
(aloite_juuri / '명명/자바이름대응.tsv').write_text('tiedoston_nimi\t이전\t이후\n' + ''.join('\t'.join(merkintä_ARVO_962f286b)+'\n' for merkintä_ARVO_962f286b in sorted(set(LOG_TIETUE))))
print('Java Nimi viite muuttaa_ARVO:', len(LOG_TIETUE))
