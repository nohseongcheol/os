#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    mapiranje_VALUE = {'header': 'Zaglavlje_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'korisni_podaci_podaci', 'src': '원본주소', 'run': 'Izvrši_komanda', 'build_java_library': '자바라이브러리만들기', 'relative': 'relativna_putanja', 'classes': 'Razred_putanja', 'dist': '배포경로', 'archive': 'Arhiva', 'output': '출력결과', 'root': 'koren_adresa', 'name': 'ime', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
