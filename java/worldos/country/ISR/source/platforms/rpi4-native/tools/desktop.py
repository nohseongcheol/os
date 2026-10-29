#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/מחשב_שולחני_הצג.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('מחשב_שולחני_הצג', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('מחשב_שולחני_הצג')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'שגיאה', 'exact': '정확한값', 'network': 'רשת', 'closed': 'מערכות_מידע_נסגר', 'length': '길이', 'opened': '열림', 'ftp_port': 'העברת_קבצים_מספר_יציאה', 'server': 'שרת_ערך', 'resources': 'משאבים', 'data': 'נתונים', 'shift': 'מקש_SHIFT', 'send': 'שלח', 'run_desktop': 'להפעיל_מחשב_שולחני', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'ארח', 'text': 'טקסט', 'korean': '한글여부', 'port': 'מספר_יציאה', 'signum': '신호번호', 'version': 'מספר_גירסה', 'parser': 'מנתח', 'bridge': 'גשר', 'kind': 'אזור_ערך', 'tail': '끝부분', 'size': 'גודל', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'לקוח', 'char': 'נתוני_תווים', 'work': '작업경로', 'Keyboard': 'מקלדת', 'x': 'קואורדינטת_x', 'down': '누르는중', 'net': 'גשר_ערך_d01f7493', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ארגומנט_מערך', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'תהליך', 'Desktop': 'לקשר_מחשב_שולחני', 'buttons': '단추들', 'thread': 'משימתרקע', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'מתג_מצב', 'command': 'פקודה', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'מקש_CTRL', 'path': 'נתיב', 'cp': 'תו_קידוד', 'terminate': 'סיום_7f587623', 'security': 'אבטחה', 'vnc_port': '원격화면접속번호', 'body': 'גוף_הטקסט', 'index': 'חפושׂ_מדד', 'exited': '종료됨', 'keysym': 'מקש_סימן', 'output': 'פלט', 'keyboard': 'מקלדת_ערך', 'interrupted': '가로채기됨', 'listener': 'לקבל_הסב', 'reader': 'קורא', 'NetworkBridge': 'גשר_3de4fe3a', 'gui': '그림화면', 'worker': 'עיבוד_משימה'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
