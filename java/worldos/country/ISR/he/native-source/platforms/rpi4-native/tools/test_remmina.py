#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/원격한글시험.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'הפעלה', 'profile': 'פרופיל', 'focused': 'ממוקד', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'שרת_ערך', 'log': 'לרשום_שיא', 'args': 'ארגומנט_מערך', 'deadline': 'תאריך_יעד_זמן', 'data': 'נתונים', 'candidate': '후보', 'logs': '기록들', 'kw': 'ארגומנט_בעל_שם', 'number': '수치', 'main': 'הפעלה', 'ready': '준비완료', 'found': 'חפש_תוצאה', 'guest': 'אורח', 'ROOT': 'לשקף_בסיס', 'marker': 'סמן', 'text': 'טקסט', 'out': 'תוצאה_נתונים', 'env': 'סביבה', 'f': 'קובץ_ערך', 'port': 'מספר_יציאה', 'offset': 'היסט_ערך', 'version': 'מספר_גירסה', 'p': 'נתונים_עמדה', 'selector': 'בורר', 'xvfb': 'וירטואלי_צג', 'display': 'צג', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'וירטואלי_קלט_כלי', 'name': 'שם', 'window': 'חלון', 'report': 'אימות_דוח', 'work': '작업경로'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
