#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/예제빌드.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'مقياس_بيانات', 'build_examples': '예제만들기', 'files': 'ملف_قائمة', 'java': '자바실행', 'run': 'ينفذ_أمر', 'path': 'مسار', 'p': 'بيانات_منصب', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': 'تعليمة_تسلسل', 'index': 'البحث_فهرس', 'classes': 'فئة_مسار', 'repo': 'مستودع_مسار', 'root': 'جذر_عنوان', 'content': 'محتوى_قيمة', 'source': '원본자료', 'name': 'اسم', 'target': 'الهدف', 'manifest': 'يُجمع_بيان', 'language': 'لغة'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
