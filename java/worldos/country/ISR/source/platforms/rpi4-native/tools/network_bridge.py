#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/גשר_3de4fe3a.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('גשר_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('גשר_3de4fe3a')
    대응 = {'response': 'תגובה', 'parts': 'נתיב_רכיב', 's': 'מחרוזת_נתונים', 'i': '순번', 'close': 'סגירה', 'forward': '전달규칙', 'slip_input': 'פרוטוקול_אינטרנט_לקו_טורי_קלט', 'self': '자신', 'item': 'ערך_ערך', 'flags': '설정비트', 'ftp_port': 'העברת_קבצים_מספר_יציאה', 'args': 'ארגומנט_מערך', 'server': 'שרת_ערך', 'data': 'נתונים', 'ethernet_input': '이더넷입력', 'trace_packet': 'עקבה_מנה', 'GATEWAY': 'שער_חומרה_למען', 'rule': 'כלל_ערך', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'ארח', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'אורח', 'destination': 'יעד_נתונים_למען', 'ethernet_port': '이더넷접속번호', 'b': '둘째값', 'MAC': 'כתובת_ממשית', 'arp': 'למען_רזולוציה_מנה', 'writable': 'ניתן_לכתיבה', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'מחזור_ערך', 'port': 'מספר_יציאה', 'offset': 'היסט_ערך', 'readable': '읽을수있음', 'c': 'נקודת_קוד', 'p': 'נתונים_עמדה', 'writers': '쓰기대상들', 'IP': 'כתובת_אינטרנט_ערך', 'e': '보조항목', 'n': '개수', 'packet': 'מנה_נתונים', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'גשר_3de4fe3a', 'window': 'חלון', 'capture': 'לכוד'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
