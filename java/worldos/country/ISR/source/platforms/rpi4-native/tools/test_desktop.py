#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/נסה_מחשב_שולחני.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('נסה_מחשב_שולחני', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('נסה_מחשב_שולחני')
    대응 = {'x': 'קואורדינטת_x', 'typing': '글자입력', 'message': 'הודעה_טקסט', 'start': 'הפעלה', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'סימן', 'j': '안쪽순번', 'deadline': 'תאריך_יעד_זמן', 'proc': 'תהליך', 'data': 'נתונים', 'main': 'הפעלה', 'w': '너비값', 'init': '초기값', 'block': 'נתונים_בלוק', 'ROOT': 'לשקף_בסיס', 'text': 'טקסט', 'marker': 'סמן', 'report': 'אימות_דוח', 'until': '까지', 'clipboard': 'לוח_ערך', 'dst': 'יעד_למען_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'תמליל', 'port': 'מספר_יציאה', 'offset': 'היסט_ערך', 'h': 'נדרש_גובה_ערך', 'src': '원본주소', 'event': 'אירוע', 'encoding': 'ערכת_תווים', 'size': 'גודל', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': 'פלט', 'symbol': 'סימן_ערך', 'client': 'לקוח', 'char': 'נתוני_תווים', 'rgb': '빛삼원색'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
