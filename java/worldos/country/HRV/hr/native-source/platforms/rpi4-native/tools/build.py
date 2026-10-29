#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/međuverzija_sustav.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('međuverzija_sustav', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('međuverzija_sustav')
    mapiranje_VALUE = {'network': 'mreža', 'BUILD': 'međuverzija_put', 'ar': 'Arhiva_alat', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_podaci', 'flags': 'konfiguracija_Pozadinski_pametni_servis_za_transfer', 'a': '첫째값', 'cc': 'C_kompilator', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'postupak_unos', 'main': 'Pokreni', 'objcopy': 'objekt_Datoteka_pretvornik', 'ROOT': 'akcija_korijen', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilator_alat', 'build_users': 'Create_korisnik_Space', 'f': 'Datoteka_unos', 'extra': '추가영역', 'exports': 'izvezi_tablica', 'jobs': '빌드작업', 'run': 'Izvrši_naredba', 'path': 'PUTANJA', 'REPO': 'spremište_korijen', 'tool': 'Alati', 'classes': 'poduka_put', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Ime', 'build_network': 'Create_mreža', 'font_info': 'font_informacija', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
