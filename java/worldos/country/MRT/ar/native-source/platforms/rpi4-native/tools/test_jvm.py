#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/يختبر_جهاز_Java_ظاهري.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('يختبر_جهاز_Java_ظاهري', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('يختبر_جهاز_Java_ظاهري')
    대응 = {'message': 'إشعار_نص', 's': 'سلسلة_بيانات', 'actual': 'الفعلي_مقياس', 'match': '일치', 'payload': 'حمولة_بيانات', 'cases': 'حالة_اختبار', 'fixture': 'يختبر_بيانات', 'main': 'تشغيل', 'ROOT': 'يعرض_جذر', 'text': 'نص', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'مكتمل_مبلغ', 'classes': 'فئة_مسار', 'output': 'الناتج', 'result': 'نتيجة', 'cmd': '명령인수', 'name': 'اسم', 'jar': '자바꾸러미', 'report': 'التحقق_من_صحة_إبلاغ', 'tests': 'قائمة_الاخبارات'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
