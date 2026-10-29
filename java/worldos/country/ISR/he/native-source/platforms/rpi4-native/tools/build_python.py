#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/파이썬빌드.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': 'ארכיון', 'SHA256': 'אימות_קוד_Hash', 'build_python': '파이썬만들기', 'root': 'בסיס_למען', 'source': '원본자료', 'name': 'שם', 'path': 'נתיב', 'VERSION': 'מהדורה_ערך', 'cc': 'מ_מהדר', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'חבר'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
