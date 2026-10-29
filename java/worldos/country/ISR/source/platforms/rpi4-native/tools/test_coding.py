#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/코딩시험.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'תוצאה_נתונים', 'expected': '예상결과', 'sdk': 'ערכת_פיתוח', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'הפעלה', 'elf': '실행파일', 'run': 'לבצע_פקודה', 'name': 'שם', 'path': 'נתיב', 'p': 'נתונים_עמדה', 'ROOT': 'לשקף_בסיס', 'report': 'אימות_דוח', 'args': 'ארגומנט_מערך'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
