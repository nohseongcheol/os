#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/exportovať_SDK.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('exportovať_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('exportovať_SDK')
    mapovanie_VALUE = {'out': 'KR_údaje', 'obj': 'cieľový_súbor', 'relative': '상대경로', 'compiler_archive': 'kompilátor_Archív', 'sdk': 'Development_Kit', 'dist': '배포경로', 'archive': 'Archív', 'main': 'Spustiť_2', 'posix': '포직스경로', 'files': 'Súbor_Zoznam', 'source': '원본자료', 'name': 'Názov', 'target': 'cieľová_hodnota', 'ROOT': 'akcia_koreň', 'destination': 'cieľ_údaje_adresa', 'manifest': 'zväzok_manifest_zostáv', 'work': '작업경로'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
