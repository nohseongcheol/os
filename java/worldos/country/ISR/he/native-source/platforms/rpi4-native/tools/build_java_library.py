#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'כותרת_ערך', 'sources': '원문목록', 'i': '순번', 'info': 'מידע_מערכת', 'payload': 'מטען_נתונים', 'src': '원본주소', 'run': 'לבצע_פקודה', 'build_java_library': '자바라이브러리만들기', 'relative': 'נתיב_יחסי', 'classes': 'כיתה_נתיב', 'dist': 'הפצה_נתיב', 'archive': 'ארכיון', 'output': 'פלט', 'root': 'בסיס_למען', 'name': 'שם', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
