#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/ينفذ_ملف.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('ينفذ_ملف', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ينفذ_ملف')
    대응 = {'timeout': '시간제한', 's': 'سلسلة_بيانات', 'i': '순번', 'match': '일치', 'files': 'ملف_قائمة', 'program': 'تطبيق', 'executable': '실행가능파일', 'args': 'وسيطة_صفيف', 'chunk': '조각', 'data': 'بيانات', 'proc': 'عملية', 'send': 'يرسل', 'main': 'تشغيل', 'marker': 'علامة', 'command': 'أمر', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ينفذ_أمر', 'p': 'بيانات_منصب', 'parser': 'المحلل', 'options': 'خيارات', 'kind': 'فئة_قيمة', 'selector': 'محدد', 'upload_data': 'تحميل_بيانات', 'end': 'إنهاء_مكالمة_إزاحة', 'n': '개수', 'd': 'وجهة_بيانات', 'key': '누름값', 'output': 'الناتج', 'line': 'سطر', 'name': 'اسم', 'upload_name': 'تحميل_اسم', 'receive': 'يستلم_رسالة'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
