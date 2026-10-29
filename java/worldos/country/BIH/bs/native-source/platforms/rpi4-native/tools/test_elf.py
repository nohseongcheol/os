#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'mjera_podaci', 'expected': '예상결과', 'phoff': 'program_Zaglavlje_Pomak', 'offset': 'Pomak_VALUE', 'invalid': 'nevažeće_podaci', 'path': 'Putanja', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'mjera', 'format_': 'format_b87fd068', 'main': 'Pokreni', 'content': 'Sadržaj_VALUE', 'source': '원본자료', 'name': 'Naziv', 'reference': 'Poređenje_osnovna_linija', 'ROOT': 'projicirati_koijen', 'value': 'VALUE', 'report': 'provjera_izvještaj'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
