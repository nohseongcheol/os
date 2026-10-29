#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/verzija_sistem.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_sistem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_sistem')
    mapiranje_VALUE = {'network': 'Mreža', 'BUILD': 'verzija_putanja', 'ar': 'Arhiva_alatka', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_podaci', 'flags': 'konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini', 'a': '첫째값', 'cc': 'C_kompajler', 'args': 'argument_niz', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metod_stavka', 'main': 'koristiti', 'objcopy': 'objekat_Datoteka_konvertor', 'ROOT': 'radnja_koren', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompajler_alatka', 'build_users': 'Create_korisnik_prostor', 'f': 'Datoteka_stavka', 'extra': '추가영역', 'exports': 'izvesti_tabela', 'jobs': '빌드작업', 'run': 'Izvrši_komanda', 'path': 'putanja', 'REPO': 'depo_koren', 'tool': 'Alatke', 'classes': 'Razred_putanja', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'ime', 'build_network': 'Create_Mreža', 'font_info': 'font_informacije', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
