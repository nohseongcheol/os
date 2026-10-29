#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/לבצע_קובץ.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('לבצע_קובץ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('לבצע_קובץ')
    대응 = {'timeout': '시간제한', 's': 'מחרוזת_נתונים', 'i': '순번', 'match': '일치', 'files': 'קובץ_רשימה', 'program': 'תוכנית', 'executable': '실행가능파일', 'args': 'ארגומנט_מערך', 'chunk': '조각', 'data': 'נתונים', 'proc': 'תהליך', 'send': 'שלח', 'main': 'הפעלה', 'marker': 'סמן', 'command': 'פקודה', 'include': 'לכלול', 'dumped': '갈무리자료', 'run': 'לבצע_פקודה', 'p': 'נתונים_עמדה', 'parser': 'מנתח', 'options': 'אפשרויות', 'kind': 'אזור_ערך', 'selector': 'בורר', 'upload_data': 'העלה_נתונים', 'end': 'סיים_שיחה_היסט', 'n': '개수', 'd': 'יעד_נתונים', 'key': '누름값', 'output': 'פלט', 'line': 'שורה', 'name': 'שם', 'upload_name': 'העלה_שם', 'receive': 'לקבל_דואר'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
