#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/נסה_מעטפת.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('נסה_מעטפת', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('נסה_מעטפת')
    대응 = {'timeout': '시간제한', 'x': 'קואורדינטת_x', 'msg': 'רשת_דואר', 'i': '순번', 'reply': 'מענה', 'call': '호출', 'args': 'ארגומנט_מערך', 'chunk': '조각', 'data': 'נתונים', 'proc': 'תהליך', 'long_text': '긴글', 'restored': '복원자료', 'send': 'שלח', 'file': 'קובץ', 'main': 'הפעלה', 'found': 'חפש_תוצאה', 'ROOT': 'לשקף_בסיס', 'text': 'טקסט', 'marker': 'סמן', 'command': 'פקודה', 'expected': '예상결과', 'pixel': 'פיקסל', 'shell': 'מעטפת', 'poll': '준비살피미', 'transcript': 'תמליל', 'end': 'סיים_שיחה_היסט', 'image': 'תמונה', 'key': '누름값', 'y': '세로좌표', 'output': 'פלט', 'result': 'תוצאה', 'client': 'לקוח', 'line': 'שורה', 'stream': 'זרם_ערך', 'name': 'שם', 'value': 'ערך', 'receive': 'לקבל_דואר', 'report': 'אימות_דוח', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
