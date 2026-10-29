#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/verzija_korisnik_prostor.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_korisnik_prostor', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_korisnik_prostor')
    대응 = {'mode': 'metoda_mod', 'header': 'Zaglavlje_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arhiva_alatka', 'posix': '포직스경로', 'payload': 'korisni_sadržaj_podaci', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'podaci', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Create_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Tekst', 'headers': 'Zaglavlje_spisak', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'verzija', 'build_users': 'Create_korisnik_prostor', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Zaglavlje_Pomak', 'offset': 'Pomak_VALUE', 'text_address': 'komanda_adresa', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'Izvrši_komanda', 'path': 'Putanja', 'p': 'podaci_položaj', 'changed': '바뀐자료', 'n': 'stavka_COUNT', 'flag': 'Postavke_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'klasa_put', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'podaci_adresa', 'symbol': 'simbol_VALUE', 'root': 'koijen_adresa', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Naziv', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
