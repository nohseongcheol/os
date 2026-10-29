#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/ליצור_תמונה.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('ליצור_תמונה', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ליצור_תמונה')
    대응 = {'total': 'סך_הכל_קיבולת', 'start': 'הפעלה', 'firmware': 'קושחה_ערך', 'files': 'קובץ_רשימה', 'archive_base': '압축기준', 'partition': 'מחיצה_קובץ', 'archive': 'ארכיון', 'main': 'הפעלה', 'block': 'נתונים_בלוק', 'ROOT': 'לשקף_בסיס', 'boot': '부팅경로', 'stage': 'במה_ערך', 'out': 'תוצאה_נתונים', 'expected': '예상결과', 'f': 'קובץ_ערך', 'src': '원본주소', 'path': 'נתיב', 'p': 'נתונים_עמדה', 'extracted': '추출자료', 'member': 'חבר', 'mbr': 'רשומת_אתחול_ראשית', 'image': 'תמונה', 'sector_count': '섹터개수', 'dist': 'הפצה_נתיב', 'sha': '해시계산', 'license_': 'רשיון', 'source': '원본자료', 'name': 'שם', 'value': 'ערך', 'manifest': 'חבילה_מניפסט', 'dest': 'יעד_ערך_עמדה', 'work': '작업경로'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
