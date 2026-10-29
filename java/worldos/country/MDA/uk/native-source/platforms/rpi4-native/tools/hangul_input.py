#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/한글입력.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('한글입력')
    зіставлення_значення = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Ключ_Макет', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'канал_Ключ', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'надсилати', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'журнал', 'pair': '한쌍', 'char': 'символьні_дані', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': 'значення', 'text': 'текст'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
