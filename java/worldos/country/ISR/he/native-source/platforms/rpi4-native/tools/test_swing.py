#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/נסה_מוסיקת_סווינג.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('נסה_מוסיקת_סווינג', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('נסה_מוסיקת_סווינג')
    대응 = {'wait': '기다리기', 'x': 'קואורדינטת_x', 's': 'מחרוזת_נתונים', 'i': '순번', 'sel': 'בורר_a916db4e', 'seconds': '초단위', 'log': 'לרשום_שיא', 'data': 'נתונים', 'at': 'נוכחי_עמדה', 'send': 'שלח', 'main': 'הפעלה', 'req': 'בקשה_ערך', 'hot': 'קיצור_דרך_ערך', 'pump': 'נקודת_אחיזה_אירוע', 'ROOT': 'לשקף_בסיס', 'marker': 'סמן', 'b': '둘째값', 'command': 'פקודה', 'shell': 'מעטפת', 'f': 'קובץ_ערך', 'click': 'לחץ_מקש', 'k': '셋째순번', 'c': 'נקודת_קוד', 'r': '반환값', 'p': 'נתונים_עמדה', 'command_mode': 'פקודה_מצב', 'end': 'סיים_שיחה_היסט', 'classes': 'כיתה_נתיב', 'key': '누름값', 'y': '세로좌표', 'result': 'תוצאה', 'report': 'אימות_דוח', 'dest': 'יעד_ערך_עמדה', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
