#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/ייצא_ערכת_פיתוח_תוכנה.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('ייצא_ערכת_פיתוח_תוכנה', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ייצא_ערכת_פיתוח_תוכנה')
    대응 = {'out': 'תוצאה_נתונים', 'obj': 'קובץ_יעד_ffac9b48', 'relative': 'נתיב_יחסי', 'compiler_archive': 'מהדר_ארכיון', 'sdk': 'ערכת_פיתוח', 'dist': 'הפצה_נתיב', 'archive': 'ארכיון', 'main': 'הפעלה', 'posix': '포직스경로', 'files': 'קובץ_רשימה', 'source': '원본자료', 'name': 'שם', 'target': 'יעד', 'ROOT': 'לשקף_בסיס', 'destination': 'יעד_נתונים_למען', 'manifest': 'חבילה_מניפסט', 'work': '작업경로'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
