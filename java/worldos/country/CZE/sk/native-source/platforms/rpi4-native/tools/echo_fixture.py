#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    mapovanie_VALUE = {'data': 'údaje', 'e': '보조항목', 'connection': 'kontakt_e05f319b', 'f': 'Súbor_položka', 'peer': 'partnerský_uzol_VALUE', 'self': '자신', 'udp': 'datagram_riadenie', 't': 'Terminál_položka', 'tcp': 'kontakt_riadenie', 'EchoFixture': '되돌림시험서버', 'args': 'argument_pole', 'chunk': '조각'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
