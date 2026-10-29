#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/코딩시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'مقياس_بيانات', 'expected': '예상결과', 'sdk': 'أداة_التطوير', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'تشغيل', 'elf': '실행파일', 'run': 'ينفذ_أمر', 'name': 'اسم', 'path': 'مسار', 'p': 'بيانات_منصب', 'ROOT': 'يعرض_جذر', 'report': 'التحقق_من_صحة_إبلاغ', 'args': 'وسيطة_صفيف'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
