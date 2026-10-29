#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'mjera_podaci', 'builtins': '내장연산', 'header': 'Zaglavlje_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Izvrši_komanda', 'flags': '설정비트', 'path': 'Putanja', 'p': 'podaci_položaj', 'cc': '시언어번역기', 'obj': 'odredišni_fajl', 'flag': 'Postavke_VALUE', 'ld': '연결편집기', 'objects': 'odredište_Fajlovi', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'koijen_adresa', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Naziv', 'includes': '포함인수'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
