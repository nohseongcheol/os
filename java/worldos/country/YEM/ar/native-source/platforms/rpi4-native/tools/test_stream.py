#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/يختبر_بث.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('يختبر_بث', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('يختبر_بث')
    대응 = {'out': 'مقياس_بيانات', 'main': 'تشغيل', 'ROOT': 'يعرض_جذر', 'p': 'بيانات_منصب', 'text': 'نص', 'report': 'التحقق_من_صحة_إبلاغ'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
