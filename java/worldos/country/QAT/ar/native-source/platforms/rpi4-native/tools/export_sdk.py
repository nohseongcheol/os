#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/تصدير_عدة_تطوير_البرامج.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('تصدير_عدة_تطوير_البرامج', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('تصدير_عدة_تطوير_البرامج')
    대응 = {'out': 'مقياس_بيانات', 'obj': 'الملف_الوجهة', 'relative': 'مسار_نسبي', 'compiler_archive': 'محول_برمجي_أرشيف', 'sdk': 'أداة_التطوير', 'dist': 'توزيع_مسار', 'archive': 'أرشيف', 'main': 'تشغيل', 'posix': '포직스경로', 'files': 'ملف_قائمة', 'source': '원본자료', 'name': 'اسم', 'target': 'الهدف', 'ROOT': 'يعرض_جذر', 'destination': 'وجهة_بيانات_عنوان', 'manifest': 'يُجمع_بيان', 'work': '작업경로'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
