#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/예제시험.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'העברת_קבצים_מספר_יציאה', 'data': 'נתונים', 'graphics_command': 'גרפיקה_פקודה', 'main': 'הפעלה', 'row': 'שורה_עמדה', 'init': '초기값', 'target': 'יעד', 'ROOT': 'לשקף_בסיס', 'text': 'טקסט', 'binary': 'בינארי', 'out': 'תוצאה_נתונים', 'entry': 'נקודת_כניסה', 'got': '받은수', 'port': 'מספר_יציאה', 'graphics_start': 'התחל_ציור', 'col': 'עמודה_עמדה', 'begin': 'התחל_היסט', 'kind': 'אזור_ערך', 'selector': 'בורר', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'לקוח', 'line': 'שורה', 'report': 'אימות_דוח', 'language': 'שפה', 'x': 'קואורדינטת_x', 'start': 'הפעלה', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'שלח_רשימה', 'payload': 'מטען_נתונים', 'proc': 'תהליך', 'w': '너비값', 'temporary': '임시자원', 'echo': 'הד_שרת_ערך', 'label': 'שם_טבלה', 'content': 'תוכן_ערך', 'argument': '전달값', 'EchoServers': 'הד_שרתים', 'marker': 'סמן', 'expected': '예상결과', 'test_language': 'נסה_שפה', 'filename': 'קובץ_ערך_שם', 'shell': 'מעטפת', 'color': '색상', 'transcript': 'תמליל', 'offset': 'היסט_ערך', 'h': 'נדרש_גובה_ערך', 'run': 'לבצע_פקודה', 'c': 'נקודת_קוד', 'path': 'נתיב', 'encoding': 'ערכת_תווים', 'end': 'סיים_שיחה_היסט', 'ftp': 'העברת_קבצים_קשר', 'pixels': '화소들', 'symbol': 'סימן_ערך', 'source': '원본자료', 'name': 'שם', 'receive': 'לקבל_דואר', 'manifest': 'חבילה_מניפסט'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
