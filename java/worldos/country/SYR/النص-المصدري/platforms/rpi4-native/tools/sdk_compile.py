#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/عدة_تطوير_البرامج_يحول_برمجياً.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('عدة_تطوير_البرامج_يحول_برمجياً', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('عدة_تطوير_البرامج_يحول_برمجياً')
    대응 = {'compiler': 'محول_برمجي_أداة', 'obj': 'الملف_الوجهة', 'sdk': 'أداة_التطوير', 'output': 'الناتج', 'main': 'تشغيل', 'elf': '실행파일', 'is_c': 'أنظمة_المعلومات_الرمز_البريدي_لغة', 'parser': 'المحلل', 'language': 'لغة', 'work': '작업경로', 'args': 'وسيطة_صفيف'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
