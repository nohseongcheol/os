#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/한글입력.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('한글입력')
    сопоставление_ЗНАЧЕН = {'old': 'Назад_товар', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Ключ_Макет', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'фиксация_состав', 'feed': 'канал_Ключ', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'написать', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'журнал', 'pair': '한쌍', 'char': 'символьные_данные', 'VOWEL': '가운뎃소리목록', 'right': 'право', 'value': 'ЗНАЧЕН', 'text': 'текст'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
