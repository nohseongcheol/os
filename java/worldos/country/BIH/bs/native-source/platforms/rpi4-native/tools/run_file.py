#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/Izvrši_fajl.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Izvrši_fajl', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvrši_fajl')
    대응 = {'timeout': '시간제한', 's': 'string_podaci', 'i': '순번', 'match': '일치', 'files': 'fajl_spisak', 'program': 'program', 'executable': '실행가능파일', 'args': 'argument_niz', 'chunk': '조각', 'data': 'podaci', 'proc': 'proces', 'send': 'poslati', 'main': 'Pokreni', 'marker': '확인표시', 'command': 'Naredba', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Izvrši_komanda', 'p': 'podaci_položaj', 'parser': '인수해석기', 'options': 'Opcije', 'kind': 'oblast_VALUE', 'selector': 'birač', 'upload_data': 'Upload_podaci', 'end': 'završiti_Pomak', 'n': 'stavka_COUNT', 'd': 'odredište_podaci', 'key': '누름값', 'output': '출력결과', 'line': 'Linija', 'name': 'Naziv', 'upload_name': 'Upload_naziv', 'receive': '수신하기'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
