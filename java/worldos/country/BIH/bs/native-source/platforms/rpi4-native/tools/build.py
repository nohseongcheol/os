#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/verzija_sistem.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_sistem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_sistem')
    대응 = {'network': 'Mreža', 'BUILD': 'verzija_put', 'ar': 'Arhiva_alatka', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_podaci', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argument_niz', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metoda_unos', 'main': 'Pokreni', 'objcopy': 'objekt_fajl_pretvarač', 'ROOT': 'projicirati_koijen', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Create_korisnik_prostor', 'f': 'fajl_unos', 'extra': '추가영역', 'exports': 'izvesti_tabela', 'jobs': '빌드작업', 'run': 'Izvrši_komanda', 'path': 'Putanja', 'REPO': '저장소', 'tool': 'Alati', 'classes': 'klasa_put', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Naziv', 'build_network': 'Create_Mreža', 'font_info': 'font_informacija', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
