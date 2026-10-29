#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/예제되돌림서버.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': 'נתונים', 'sock': '소켓', 'tcp_port': 'יציאת_TCP', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'יחידת_נתונים_נקודת_אחיזה_בקשה', 'thread': 'משימתרקע', 'echo': 'הד_שרת_ערך', 'TCP': 'נקודת_אחיזה_קשר_בקשה', 'EchoServers': 'הד_שרתים', 'parser': 'מנתח', 'server': 'שרת_ערך', 'udp_port': 'פרוטוקול_יחידת_נתונים_של_משתמש_הסב', 'args': 'ארגומנט_מערך'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
