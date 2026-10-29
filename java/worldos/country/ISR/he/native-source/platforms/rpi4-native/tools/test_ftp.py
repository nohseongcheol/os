#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/נסה_פרוטוקול_העברת_קבצים.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('נסה_פרוטוקול_העברת_קבצים', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('נסה_פרוטוקול_העברת_קבצים')
    대응 = {'timeout': '시간제한', 'payload': 'מטען_נתונים', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'נתונים', 'proc': 'תהליך', 'code': 'הוראה_רצף', 'linux': '리눅스파일', 'archive': 'ארכיון', 'main': 'הפעלה', 'net_source': 'נטו_מקור', 'temporary': '임시자원', 'static_source': 'סטטי_מקור', 'java_source': '자바원문', 'echo': 'הד_שרת_ערך', 'ROOT': 'לשקף_בסיס', 'text': 'טקסט', 'marker': 'סמן', 'EchoFixture': '되돌림시험서버', 'command': 'פקודה', 'out': 'תוצאה_נתונים', 'expected': '예상결과', 'server_source': 'שרת_מקור', 'shell': 'מעטפת', 'upload': 'העלה_קבצים', 'transcript': 'תמליל', 'port': 'מספר_יציאה', 'native': 'מקורי', 'elf': '실행파일', 'server_udp_port': 'שרת_יחידת_נתונים_הסב', 'packed': '묶인자료', 'bridge': 'גשר', 'selector': 'בורר', 'end': 'סיים_שיחה_היסט', 'e': '보조항목', 'ftp': 'העברת_קבצים_קשר', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'עמית_ערך', 'result': 'תוצאה', 'unchanged': '보존자료', 'line': 'שורה', 'server_tcp_port': 'שרת_זרם_הסב', 'source': '원본자료', 'NetworkBridge': 'גשר_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'לקבל_דואר', 'report': 'אימות_דוח'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
