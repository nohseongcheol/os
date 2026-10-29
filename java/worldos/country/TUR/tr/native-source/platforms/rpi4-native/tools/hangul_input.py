#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/한글입력.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('한글입력')
    eşleme_değer = {'old': 'Önceki_öğe', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'tuş_Düzen', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': '조합확정', 'feed': 'akış_tuş', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'göndermek', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Geçmiş', 'pair': '한쌍', 'char': 'karakter_verileri', 'VOWEL': '가운뎃소리목록', 'right': 'hak', 'value': 'değer', 'text': 'metin'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
