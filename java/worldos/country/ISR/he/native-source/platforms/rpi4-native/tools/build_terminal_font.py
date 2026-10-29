#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/בנה_מסוף_גופן.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('בנה_מסוף_גופן', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('בנה_מסוף_גופן')
    대응 = {'data': 'נתונים', 'img': 'ציור_ערך', 'bits': '비트들', 'x': 'קואורדינטת_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'נתיב_רשימה', 'y': '세로좌표', 'main': 'הפעלה', 'src': '원본주소', 'fonts': 'גופן_רשימה', 'ROOT': 'לשקף_בסיס', 'p': 'נתונים_עמדה', 'cp': 'תו_קידוד', 'target': 'יעד'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
