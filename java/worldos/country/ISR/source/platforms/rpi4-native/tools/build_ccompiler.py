#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/בנה_מ_מהדר.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('בנה_מ_מהדר', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('בנה_מ_מהדר')
    대응 = {'out': 'תוצאה_נתונים', 'builtins': '내장연산', 'header': 'כותרת_ערך', 'sdk': 'ערכת_פיתוח', 'build_ccompiler': 'ליצור_מ_מהדר', 'i': '순번', 'elf': '실행파일', 'run': 'לבצע_פקודה', 'flags': '설정비트', 'path': 'נתיב', 'p': 'נתונים_עמדה', 'cc': 'מ_מהדר', 'obj': 'קובץ_יעד_ffac9b48', 'flag': 'הגדרות_ערך', 'ld': '연결편집기', 'objects': 'יעד_קבצים', 'repo': 'מאגר_נתיב', 'v': '임시값', 'upstream': 'במעלה', 'root': 'בסיס_למען', 'assets': '탑재자료', 'source': '원본자료', 'name': 'שם', 'includes': '포함인수'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
