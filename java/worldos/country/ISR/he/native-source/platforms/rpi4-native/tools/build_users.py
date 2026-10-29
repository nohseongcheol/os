#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/בנה_משתמש_חלל.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('בנה_משתמש_חלל', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('בנה_משתמש_חלל')
    대응 = {'mode': 'פעולת_שירות_מצב', 'header': 'כותרת_ערך', 'i': '순번', 'build_ccompiler': 'ליצור_מ_מהדר', 'ar': 'ארכיון_כלי', 'posix': '포직스경로', 'payload': 'מטען_נתונים', 'flags': '설정비트', 'cases': 'מפרט_בדיקה', 'cc': 'מ_מהדר', 'data': 'נתונים', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'מאגר_נתיב', 'build_python': '파이썬만들기', 'inc': 'לכלול_נתיב', 'argument': '전달값', 'text': 'טקסט', 'headers': 'כותרת_רשימה', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'בנה', 'build_users': 'ליצור_משתמש_חלל', 'compiler': 'מהדר_כלי', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'תוכנית_כותרת_היסט', 'offset': 'היסט_ערך', 'text_address': 'פקודה_למען', 'abi': '호출규약', 'assembly': 'הרכבה', 'run': 'לבצע_פקודה', 'path': 'נתיב', 'p': 'נתונים_עמדה', 'changed': '바뀐자료', 'n': '개수', 'flag': 'הגדרות_ערך', 'index': 'חפושׂ_מדד', 'classes': 'כיתה_נתיב', 'output': 'פלט', 'loads': '적재구획', 'data_address': 'נתונים_למען', 'symbol': 'סימן_ערך', 'root': 'בסיס_למען', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'שם', 'value': 'ערך', 'fmt': 'עיצוב', 'work': '작업경로'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
