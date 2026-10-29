#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/verzija_korisnik_prostor.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_korisnik_prostor', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_korisnik_prostor')
    mapiranje_VALUE = {'mode': 'metod_MODE', 'header': 'Zaglavlje_VALUE', 'i': '순번', 'build_ccompiler': 'Create_C_kompajler', 'ar': 'Arhiva_alatka', 'posix': '포직스경로', 'payload': 'korisni_podaci_podaci', 'flags': 'konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini', 'cases': '시험사례', 'cc': 'C_kompajler', 'data': 'podaci', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'depo_putanja', 'build_python': 'Create_PYTHON', 'inc': 'uključiti_putanja', 'argument': '전달값', 'text': 'SMS', 'headers': 'Zaglavlje_Lista', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'verzija', 'build_users': 'Create_korisnik_prostor', 'compiler': 'kompajler_alatka', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Zaglavlje_Pomak', 'offset': 'Pomak_VALUE', 'text_address': 'komanda_adresa', 'abi': '호출규약', 'assembly': 'sklop', 'run': 'Izvrši_komanda', 'path': 'putanja', 'p': 'podaci_pozicija', 'changed': '바뀐자료', 'n': 'stavka_COUNT', 'flag': 'Postavke_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Razred_putanja', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'podaci_adresa', 'symbol': 'simbol_VALUE', 'root': 'koren_adresa', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ime', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
