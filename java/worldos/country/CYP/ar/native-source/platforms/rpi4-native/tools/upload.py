#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/تحميل_الملفات.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('تحميل_الملفات', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('تحميل_الملفات')
    대응 = {'data': 'بيانات', 'i': '순번', 'name': 'اسم', 'c': 'رمز_الحرف', 'p': 'بيانات_منصب', 'args': 'وسيطة_صفيف'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
