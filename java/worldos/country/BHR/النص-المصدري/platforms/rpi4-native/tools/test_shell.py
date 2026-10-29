#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/셸시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'الإحداثي_س', 'msg': 'شبكة_رسالة', 'i': '순번', 'reply': 'رد', 'call': '호출', 'args': 'وسيطة_صفيف', 'chunk': '조각', 'data': 'بيانات', 'proc': 'عملية', 'long_text': '긴글', 'restored': '복원자료', 'send': 'يرسل', 'file': 'ملف', 'main': 'تشغيل', 'found': 'بحث_مقياس', 'ROOT': 'يعرض_جذر', 'text': 'نص', 'marker': 'علامة', 'command': 'أمر', 'expected': '예상결과', 'pixel': 'عنصر_صورة', 'shell': '셸', 'poll': '준비살피미', 'transcript': 'نسخة_مكتوبة', 'end': 'إنهاء_مكالمة_إزاحة', 'image': 'صورة', 'key': '누름값', 'y': 'الزر_Y_إحداثيات', 'output': 'الناتج', 'result': 'نتيجة', 'client': 'عميل', 'line': 'سطر', 'stream': 'بث_قيمة', 'name': 'اسم', 'value': 'قيمة', 'receive': 'يستلم_رسالة', 'report': 'التحقق_من_صحة_إبلاغ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
