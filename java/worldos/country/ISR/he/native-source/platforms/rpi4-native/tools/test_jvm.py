#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/נסה_מחשב_וירטואלי_java.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('נסה_מחשב_וירטואלי_java', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('נסה_מחשב_וירטואלי_java')
    대응 = {'message': 'הודעה_טקסט', 's': 'מחרוזת_נתונים', 'actual': 'בפועל_תוצאה', 'match': '일치', 'payload': 'מטען_נתונים', 'cases': 'מפרט_בדיקה', 'fixture': 'נסה_נתונים', 'main': 'הפעלה', 'ROOT': 'לשקף_בסיס', 'text': 'טקסט', 'valid': '유효함', 'includes': '포함인수', 'include': 'לכלול', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'הושלם_סכום', 'classes': 'כיתה_נתיב', 'output': 'פלט', 'result': 'תוצאה', 'cmd': '명령인수', 'name': 'שם', 'jar': '자바꾸러미', 'report': 'אימות_דוח', 'tests': 'רשימת_בדיקות'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
