#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/بنية_شبكة.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('بنية_شبكة', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بنية_شبكة')
    대응 = {'obj': 'الملف_الوجهة', 'objects': 'وجهة_الملفات', 'library': 'مكتبة', 'output': 'الناتج', 'port': 'رقم_المنفذ', 'root': 'جذر_عنوان', 'files': 'ملف_قائمة', 'source': '원본자료', 'run': 'ينفذ_أمر', 'flags': 'تكوين_خدمة_النقل_الذكي_في_الخلفية', 'path': 'مسار', 'build_network': 'فتح_شبكة_48d29d6d', 'cc': 'الرمز_البريدي_محول_برمجي', 'ar': 'أرشيف_أداة'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
