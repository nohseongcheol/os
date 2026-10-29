#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/ينفذ_أمر.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('ينفذ_أمر', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ينفذ_أمر')
    대응 = {'supported': '지원목록', 'parser': 'المحلل', 'qemu': '모의기계', 'run_desktop': 'يشغّل_سطح_مكتب', 'main': 'تشغيل', 'host': 'مضيف', 'status': 'حالة_قيمة', 'NetworkBridge': 'جسر_3de4fe3a', 'ROOT': 'يعرض_جذر', 'bridge': 'جسر', 'loader': 'أداة_تحميل', 'base': 'خلفية_قيمة', 'options': 'خيارات', 'binary': 'ثنائي', 'args': 'وسيطة_صفيف', 'command': 'أمر'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
