#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/한글입력.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'khii_Sebopego', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'fiti_ya_RSS_khii', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'Romela', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Histori', 'pair': '한쌍', 'char': 'tlhaka_data', 'VOWEL': '가운뎃소리목록', 'right': '오른쪽', 'value': 'boleng', 'text': 'Sengwalwa'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
