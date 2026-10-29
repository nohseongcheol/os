#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/실행파일시험.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'תוצאה_נתונים', 'expected': '예상결과', 'phoff': 'תוכנית_כותרת_היסט', 'offset': 'היסט_ערך', 'invalid': 'לא_חוקי_נתונים', 'path': 'נתיב', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'תוצאה', 'format_': 'לעצב_b87fd068', 'main': 'הפעלה', 'content': 'תוכן_ערך', 'source': '원본자료', 'name': 'שם', 'reference': 'השוואה_בסיס', 'ROOT': 'לשקף_בסיס', 'value': 'ערך', 'report': 'אימות_דוח'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
