#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/한글입력.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'калид_Тарҳбандӣ', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'веб_канал_калид', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'фиристодан', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Таърих', 'pair': '한쌍', 'char': 'аломат_иттилоот_4d9f8719', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': 'қимат', 'text': 'Матн'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
