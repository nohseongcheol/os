#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/העלה_קבצים.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('העלה_קבצים', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('העלה_קבצים')
    대응 = {'data': 'נתונים', 'i': '순번', 'name': 'שם', 'c': 'נקודת_קוד', 'p': 'נתונים_עמדה', 'args': 'ארגומנט_מערך'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
