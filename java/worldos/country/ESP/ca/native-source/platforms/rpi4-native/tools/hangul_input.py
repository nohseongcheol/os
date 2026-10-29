#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/한글입력.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Clau_disseny', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'font_Clau', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'enviar', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historial', 'pair': '한쌍', 'char': 'caràcter_dades', 'VOWEL': '가운뎃소리목록', 'right': 'DRETA', 'value': 'VALOR', 'text': 'SMS'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
