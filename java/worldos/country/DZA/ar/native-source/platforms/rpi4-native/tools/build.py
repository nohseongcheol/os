#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/بنية_نظام.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('بنية_نظام', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بنية_نظام')
    대응 = {'network': 'شبكة', 'BUILD': 'بنية_مسار', 'ar': 'أرشيف_أداة', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'خط_بيانات', 'flags': 'تكوين_خدمة_النقل_الذكي_في_الخلفية', 'a': '첫째값', 'cc': 'الرمز_البريدي_محول_برمجي', 'args': 'وسيطة_صفيف', 'source_flags': '원본설정', 'ld': 'برنامج_ربط_أداة', 'method': 'أسلوب_إدخال', 'main': 'تشغيل', 'objcopy': 'عنصر_ملف_محوّل', 'ROOT': 'يعرض_جذر', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'محول_برمجي_أداة', 'build_users': 'فتح_مستخدم_مساحة', 'f': 'ملف_إدخال_3d0c1245', 'extra': '추가영역', 'exports': 'تصدير_جدول', 'jobs': '빌드작업', 'run': 'ينفذ_أمر', 'path': 'مسار', 'REPO': 'مستودع_جذر', 'tool': 'أدوات', 'classes': 'فئة_مسار', 'output': 'الناتج', 'samples': '예제들', 'symbol': 'رمز_قيمة', 'source': '원본자료', 'name': 'اسم', 'build_network': 'فتح_شبكة_48d29d6d', 'font_info': 'خط_معلومات', 'manifest': 'يُجمع_بيان', 'work': '작업경로'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
