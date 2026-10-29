#!/usr/bin/env python3
"""기존 נתיב 호환 נקודת_כניסה. בפועל_נתונים 구현: ../כלים/부팅시험.py"""
import importlib as 가져오기
import sys as מערכת_הפעלה_ערך
from pathlib import Path as נתיב
מערכת_הפעלה_ערך.path.insert(0, str(נתיב(__file__).resolve().parents[1] / 'כלים'))
if __name__ == '__main__':
    import runpy as תוכנית_מפעיל
    תוכנית_מפעיל.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'תגובה', 'msg': 'רשת_דואר', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'בצע', 'cancel': 'לבטל_ניתוח', 'cmd_byte': 'פקודה_בית', 'reply': 'מענה', 'points': '지점들', 'server': 'שרת_ערך', 'data': 'נתונים', 'prompt': 'לבקש', 'enter': 'הזן', 'imported': '들여온파일', 'send': 'שלח', 'main': 'הפעלה', 'ROOT': 'לשקף_בסיס', 'text': 'טקסט', 'first_gui': '첫화면', 'pixel': 'פיקסל', 'java_class': '자바클래스', 'upload': 'העלה_קבצים', 'pixels_file': 'פיקסל_קובץ', 'pixels_data': 'פיקסל_נתונים', 'edit': 'ערוך_ערך', 'receive_until': '표시까지받기', 'selector': 'בורר', 'size': 'גודל', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'תוצאה', 'samples': '예제들', 'client': 'לקוח', 'line': 'שורה', 'report': 'אימות_דוח', 'work': '작업경로', 'x': 'קואורדינטת_x', 'python_checks': '파이썬검사', 'download': 'הורד', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'תאריך_יעד_זמן', 'proc': 'תהליך', 'content': 'תוכן_ערך', 'block': 'נתונים_בלוק', 'marker': 'סמן', 'command': 'פקודה', 'expected': '예상결과', 'shell': 'מעטפת', 'drawing': 'ציור_נתיב', 'f': 'קובץ_ערך', 'transcript': 'תמליל', 'offset': 'היסט_ערך', 'path': 'נתיב', 'screenshot': 'גזירת_מסך', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'פלט', 'stream': 'זרם_ערך', 'cmd': '명령인수', 'name': 'שם', 'qmp': '모의제어접속'}
    for 이전, נוכחי_פריט in 대응.items():
        if hasattr(구현, נוכחי_פריט): globals()[이전] = getattr(구현, נוכחי_פריט)
