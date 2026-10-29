#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/בנייה.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('בנייה', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('בנייה')
    대응 = {'network': 'רשת', 'BUILD': 'בנה_נתיב', 'ar': 'ארכיון_כלי', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'גופן_נתונים', 'flags': '설정비트', 'a': '첫째값', 'cc': 'מ_מהדר', 'args': 'ארגומנט_מערך', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'פעולת_שירות_ערך_5c76dce4', 'main': 'הפעלה', 'objcopy': 'אובייקט_קובץ_ממיר', 'ROOT': 'לשקף_בסיס', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'מהדר_כלי', 'build_users': 'ליצור_משתמש_חלל', 'f': 'קובץ_ערך', 'extra': '추가영역', 'exports': 'ייצא_טבלה', 'jobs': '빌드작업', 'run': 'לבצע_פקודה', 'path': 'נתיב', 'REPO': 'מאגר_בסיס', 'tool': 'כלים', 'classes': 'כיתה_נתיב', 'output': 'פלט', 'samples': '예제들', 'symbol': 'סימן_ערך', 'source': '원본자료', 'name': 'שם', 'build_network': 'ליצור_רשת', 'font_info': 'גופן_מידע', 'manifest': 'חבילה_מניפסט', 'work': '작업경로'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
