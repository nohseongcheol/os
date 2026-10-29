#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/되돌림시험서버.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'נתונים', 'e': '보조항목', 'connection': 'קשר_e05f319b', 'f': 'קובץ_ערך', 'peer': 'עמית_ערך', 'self': '자신', 'udp': 'יחידת_נתונים_פקד', 't': 'מסוף_ערך', 'tcp': 'קשר_פקד', 'EchoFixture': '되돌림시험서버', 'args': 'ארגומנט_מערך', 'chunk': '조각'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
