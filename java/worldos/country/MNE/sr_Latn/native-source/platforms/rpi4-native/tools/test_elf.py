#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    mapiranje_VALUE = {'out': 'KR_podaci', 'expected': '예상결과', 'phoff': 'program_Zaglavlje_Pomak', 'offset': 'Pomak_VALUE', 'invalid': 'nevažeći_podaci', 'path': 'putanja', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'KR', 'format_': 'format_b87fd068', 'main': 'koristiti', 'content': 'Sadržaj_VALUE', 'source': '원본자료', 'name': 'ime', 'reference': 'Poređenje_osnova', 'ROOT': 'radnja_koren', 'value': 'VALUE', 'report': 'provera_valjanosti_izveštaj'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
