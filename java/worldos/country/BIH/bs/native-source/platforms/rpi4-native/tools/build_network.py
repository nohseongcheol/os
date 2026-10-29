#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/verzija_Mreža.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('verzija_Mreža', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('verzija_Mreža')
    대응 = {'obj': 'odredišni_fajl', 'objects': 'odredište_Fajlovi', 'library': 'biblioteka', 'output': '출력결과', 'port': 'broj_priključka', 'root': 'koijen_adresa', 'files': 'fajl_spisak', 'source': '원본자료', 'run': 'Izvrši_komanda', 'flags': '설정비트', 'path': 'Putanja', 'build_network': 'Create_Mreža', 'cc': '시언어번역기', 'ar': 'Arhiva_alatka'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
