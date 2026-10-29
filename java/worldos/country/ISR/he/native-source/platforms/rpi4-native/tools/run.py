#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/לבצע_פקודה.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('לבצע_פקודה', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('לבצע_פקודה')
    대응 = {'supported': '지원목록', 'parser': 'מנתח', 'qemu': '모의기계', 'run_desktop': 'להפעיל_מחשב_שולחני', 'main': 'הפעלה', 'host': 'ארח', 'status': 'מצב_ערך', 'NetworkBridge': 'גשר_3de4fe3a', 'ROOT': 'לשקף_בסיס', 'bridge': 'גשר', 'loader': 'מטען', 'base': 'טפט_ערך', 'options': 'אפשרויות', 'binary': 'בינארי', 'args': 'ארגומנט_מערך', 'command': 'פקודה'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
