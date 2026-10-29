#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/בנה_רשת.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('בנה_רשת', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('בנה_רשת')
    대응 = {'obj': 'קובץ_יעד_ffac9b48', 'objects': 'יעד_קבצים', 'library': 'ספריה', 'output': 'פלט', 'port': 'מספר_יציאה', 'root': 'בסיס_למען', 'files': 'קובץ_רשימה', 'source': '원본자료', 'run': 'לבצע_פקודה', 'flags': '설정비트', 'path': 'נתיב', 'build_network': 'ליצור_רשת', 'cc': 'מ_מהדר', 'ar': 'ארכיון_כלי'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
