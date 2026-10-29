#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    mapovanie_VALUE = {'out': 'KR_údaje', 'expected': '예상결과', 'phoff': 'program_Nadpis_Posun', 'offset': 'Posun_VALUE', 'invalid': 'neplatné_údaje', 'path': 'Cesta', 'executable': 'spustiteľný_súbor_IMAGE', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'KR', 'format_': 'formát_b87fd068', 'main': 'Spustiť_2', 'content': 'obsah_VALUE', 'source': '원본자료', 'name': 'Názov', 'reference': 'Porovnanie_pôvodný_plán', 'ROOT': 'akcia_koreň', 'value': 'VALUE', 'report': 'overenie_správa'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
