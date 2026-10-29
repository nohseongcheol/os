#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'verilənlər', 'e': '보조항목', 'connection': 'qoşulma_e05f319b', 'f': 'fayl_daxiletmə', 'peer': 'eynisəviyyəli_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_daxiletmə', 'tcp': 'qoşulma_nəzarət', 'EchoFixture': '되돌림시험서버', 'args': 'arqument_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
