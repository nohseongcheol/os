#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/ערכת_פיתוח_תוכנה_בנה.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('ערכת_פיתוח_תוכנה_בנה', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ערכת_פיתוח_תוכנה_בנה')
    대응 = {'compiler': 'מהדר_כלי', 'obj': 'קובץ_יעד_ffac9b48', 'sdk': 'ערכת_פיתוח', 'output': 'פלט', 'main': 'הפעלה', 'elf': '실행파일', 'is_c': 'מערכות_מידע_מ_שפה', 'parser': 'מנתח', 'language': 'שפה', 'work': '작업경로', 'args': 'ארגומנט_מערך'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
