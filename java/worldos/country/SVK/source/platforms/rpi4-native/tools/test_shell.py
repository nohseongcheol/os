#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    mapovanie_VALUE = {'timeout': '시간제한', 'x': 'X_súradnica', 'msg': 'sieť_e_mail', 'i': '순번', 'reply': 'odozva', 'call': '호출', 'args': 'argument_pole', 'chunk': '조각', 'data': 'údaje', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'odoslať', 'file': 'Súbor', 'main': 'Spustiť_2', 'found': 'Hľadať_KR', 'ROOT': 'akcia_koreň', 'text': 'Spracovanie_textu', 'marker': 'fixka', 'command': 'Príkaz', 'expected': '예상결과', 'pixel': 'pixel', 'shell': '셸', 'poll': '준비살피미', 'transcript': 'prepis', 'end': 'ukončiť_hovor_Posun', 'image': 'IMAGE', 'key': '누름값', 'y': 'Y_súradnica', 'output': '출력결과', 'result': 'KR', 'client': 'klient', 'line': 'riadok', 'stream': 'Stream_VALUE', 'name': 'Názov', 'value': 'VALUE', 'receive': 'dostať_e_mail', 'report': 'overenie_správa', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
