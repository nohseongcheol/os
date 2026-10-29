#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/test_Shell.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('test_Shell', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('test_Shell')
    tilknytning_VÆRDI = {'timeout': 'udførelse_TIMEOUT', 'x': 'X_koordinat', 'msg': 'netværk_mail', 'i': '순번', 'reply': 'svar', 'call': '호출', 'args': 'argument_MATRIX', 'chunk': '조각', 'data': 'data', 'proc': 'Proces', 'long_text': '긴글', 'restored': '복원자료', 'send': 'maile', 'file': 'Fil', 'main': 'Kør_2', 'found': 'SØG_KR', 'ROOT': 'To_do_rod', 'text': 'Tekst', 'marker': 'mærke', 'command': 'Kommando', 'expected': '예상결과', 'pixel': 'pixel', 'shell': 'Shell', 'poll': '준비살피미', 'transcript': 'afskrift', 'end': 'afslutte_et_opkald_FORSKYDNING', 'image': 'Image', 'key': '누름값', 'y': 'Y_koordinat', 'output': 'produktoutput', 'result': 'KR', 'client': 'klient', 'line': 'Linje', 'stream': 'strøm_VÆRDI', 'name': 'Navn', 'value': 'VÆRDI', 'receive': 'modtage_mail', 'report': 'validering_rapport', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
