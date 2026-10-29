#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/예제빌드.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'תוצאה_נתונים', 'build_examples': '예제만들기', 'files': 'קובץ_רשימה', 'java': '자바실행', 'run': 'לבצע_פקודה', 'path': 'נתיב', 'p': 'נתונים_עמדה', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': 'הוראה_רצף', 'index': 'חפושׂ_מדד', 'classes': 'כיתה_נתיב', 'repo': 'מאגר_נתיב', 'root': 'בסיס_למען', 'content': 'תוכן_ערך', 'source': '원본자료', 'name': 'שם', 'target': 'יעד', 'manifest': 'חבילה_מניפסט', 'language': 'שפה'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
