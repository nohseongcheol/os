#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/test_JVM.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('test_JVM')
    대응 = {'message': 'povinnost_zvěřejnit_SMS', 's': 'řetězec_data', 'actual': 'skutečný_KV', 'match': '일치', 'payload': 'vytížení_data', 'cases': 'testovací_případ', 'fixture': 'test_data', 'main': 'Spustit_2', 'ROOT': 'akce_kořen', 'text': 'text', 'valid': 'platný', 'includes': '포함인수', 'include': 'zahrnout', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'dokončeno_částka', 'classes': 'Třída_cesta', 'output': 'výstup', 'result': 'VÝSLEDEK', 'cmd': '명령인수', 'name': 'Název', 'jar': '자바꾸러미', 'report': 'ověření_Zpráva', 'tests': 'seznam_testů'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
