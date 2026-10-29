#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    preslikava_VALUE = {'out': 'KR_podatki', 'expected': '예상결과', 'phoff': 'aplikacija_Glava_odmik', 'offset': 'odmik_VALUE', 'invalid': 'neveljaven_podatki', 'path': 'POT', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'REZULTAT', 'format_': 'oblika_b87fd068', 'main': 'Zaženi', 'content': 'vsebina_VALUE', 'source': '원본자료', 'name': 'Ime', 'reference': 'Primerjava_osnova', 'ROOT': 'pobuda_koren', 'value': 'VALUE', 'report': 'preverjanje_veljavnosti_prijavi'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
