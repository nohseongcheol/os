#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/한글입력.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('한글입력')
    대응 = {'old': '이전', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'مفتاح_تخطيط', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'تثبيت_تركيب', 'feed': 'موجز_مفتاح', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'يرسل', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'سجل', 'pair': '한쌍', 'char': 'بيانات_الأحرف', 'VOWEL': '가운뎃소리목록', 'right': 'حق', 'value': 'قيمة', 'text': 'نص'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
