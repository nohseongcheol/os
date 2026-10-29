#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/실행파일시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'مقياس_بيانات', 'expected': '예상결과', 'phoff': 'تطبيق_عنوان_إزاحة', 'offset': 'إزاحة_قيمة', 'invalid': 'غير_صالح_بيانات', 'path': 'مسار', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'نتيجة', 'format_': 'ينسق_b87fd068', 'main': 'تشغيل', 'content': 'محتوى_قيمة', 'source': '원본자료', 'name': 'اسم', 'reference': 'مقارنة_الأساس', 'ROOT': 'يعرض_جذر', 'value': 'قيمة', 'report': 'التحقق_من_صحة_إبلاغ'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
