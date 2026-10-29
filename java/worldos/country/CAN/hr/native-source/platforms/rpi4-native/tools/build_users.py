#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/međuverzija_korisnik_Space.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('međuverzija_korisnik_Space', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('međuverzija_korisnik_Space')
    mapiranje_VALUE = {'mode': 'postupak_MODE', 'header': 'Zaglavlje_VALUE', 'i': '순번', 'build_ccompiler': 'Create_C_kompilator', 'ar': 'Arhiva_alat', 'posix': '포직스경로', 'payload': 'korisni_podaci_podaci', 'flags': 'konfiguracija_Pozadinski_pametni_servis_za_transfer', 'cases': '시험사례', 'cc': 'C_kompilator', 'data': 'podaci', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'spremište_put', 'build_python': 'Create_PYTHON', 'inc': 'obuhvaćati_put', 'argument': '전달값', 'text': 'Tekst', 'headers': 'Zaglavlje_Popis', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'međuverzija', 'build_users': 'Create_korisnik_Space', 'compiler': 'kompilator_alat', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Zaglavlje_pomak', 'offset': 'pomak_VALUE', 'text_address': 'naredba_adresa', 'abi': '호출규약', 'assembly': 'sklop', 'run': 'Izvrši_naredba', 'path': 'PUTANJA', 'p': 'podaci_položaj', 'changed': '바뀐자료', 'n': 'artikl_COUNT', 'flag': 'Postavke_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'poduka_put', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'podaci_adresa', 'symbol': 'simbol_VALUE', 'root': 'korijen_adresa', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ime', 'value': 'VALUE', 'fmt': 'oblik_932e03c8', 'work': '작업경로'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
