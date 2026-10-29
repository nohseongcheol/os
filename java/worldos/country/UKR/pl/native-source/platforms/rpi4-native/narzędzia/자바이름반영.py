#!/usr/bin/env python3
"""własny Java lokalny_Scope 이름을 바꾼다. ciąg_WARTOŚĆ·주석·zewnętrzny_WARTOŚĆ 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

Project_korzeń = Path(__file__).resolve().parents[1]
mapowanie_WARTOŚĆ = json.loads((Project_korzeń / '명명/자바이름.json').read_text())
fragment_wyrażenie = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
LOG_zapis = []
for Katalog_WARTOŚĆ in ('plik_źródłowy', 'przestrzeń_użytkownika/자바', '한국어자바'):
    for ścieżka_2 in sorted((Project_korzeń / Katalog_WARTOŚĆ).rglob('*.java')):
        plik_źródłowy = ścieżka_2.read_text()
        토막들 = list(fragment_wyrażenie.finditer(plik_źródłowy))
        사용이름 = {fragment_wpis.group() for fragment_wpis in 토막들 if re.search('[가-힣]', fragment_wpis.group())}
        mapowanie_pliku = {}
        for Wstecz_towar, 이후 in mapowanie_WARTOŚĆ.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            새이름 = 이후
            while 새이름 in 사용이름: 새이름 = 'lokalny_Scope' + 새이름
            mapowanie_pliku[Wstecz_towar] = 새이름
        수정 = []
        Wstecz_fragment = ''
        for fragment_wpis in 토막들:
            낱말 = fragment_wpis.group()
            if 낱말.startswith(('//', '/*', '"', "'")): continue
            if 낱말 in mapowanie_pliku and Wstecz_fragment != '.':
                수정.append((fragment_wpis.start(), fragment_wpis.end(), mapowanie_pliku[낱말]))
                LOG_zapis.append((str(ścieżka_2.relative_to(Project_korzeń)), 낱말, mapowanie_pliku[낱말]))
            Wstecz_fragment = 낱말
        for Uruchom_2, 끝, 새이름 in reversed(수정): plik_źródłowy = plik_źródłowy[:Uruchom_2] + 새이름 + plik_źródłowy[끝:]
        if 수정: ścieżka_2.write_text(plik_źródłowy)
(Project_korzeń / '명명/자바이름대응.tsv').write_text('nazwa_pliku\t이전\t이후\n' + ''.join('\t'.join(wpis_WARTOŚĆ)+'\n' for wpis_WARTOŚĆ in sorted(set(LOG_zapis))))
print('Java Nazwa odwołanie zmienić_WARTOŚĆ:', len(LOG_zapis))
