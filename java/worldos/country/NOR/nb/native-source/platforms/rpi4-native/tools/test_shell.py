#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/test_Shell.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('test_Shell', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('test_Shell')
    tildeling_VERDI = {'timeout': 'kjøring_TIMEOUT', 'x': 'x_koordinat', 'msg': 'nettverk_e_post', 'i': '순번', 'reply': 'svar', 'call': '호출', 'args': 'argument_MATRISE', 'chunk': '조각', 'data': 'data', 'proc': 'Prosess', 'long_text': '긴글', 'restored': '복원자료', 'send': 'sende', 'file': 'Fil', 'main': 'Kjør_2', 'found': 'SØK_KR', 'ROOT': 'speile_rot', 'text': 'Tekst', 'marker': 'tusj', 'command': 'Kommando', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'Shell', 'poll': '준비살피미', 'transcript': 'utskrift', 'end': 'avslutte_en_samtale_FORSKYVNING', 'image': 'BILDE', 'key': '누름값', 'y': 'Y_koordinat', 'output': 'produksjon', 'result': 'KR', 'client': 'klient', 'line': 'Linje', 'stream': 'strøm_VERDI', 'name': 'Navn', 'value': 'VERDI', 'receive': 'motta_e_post', 'report': 'validering_rapport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
