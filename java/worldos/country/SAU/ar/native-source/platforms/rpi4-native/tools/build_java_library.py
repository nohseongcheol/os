#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'عنوان_قيمة_4a42eba5', 'sources': '원문목록', 'i': '순번', 'info': 'معلومات_النظام', 'payload': 'حمولة_بيانات', 'src': '원본주소', 'run': 'ينفذ_أمر', 'build_java_library': '자바라이브러리만들기', 'relative': 'مسار_نسبي', 'classes': 'فئة_مسار', 'dist': 'توزيع_مسار', 'archive': 'أرشيف', 'output': 'الناتج', 'root': 'جذر_عنوان', 'name': 'اسم', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
