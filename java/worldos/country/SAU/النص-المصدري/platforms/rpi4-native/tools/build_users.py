#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/بنية_مستخدم_مساحة.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('بنية_مستخدم_مساحة', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بنية_مستخدم_مساحة')
    대응 = {'mode': 'أسلوب_الوضع', 'header': 'عنوان_قيمة_4a42eba5', 'i': '순번', 'build_ccompiler': 'فتح_الرمز_البريدي_محول_برمجي', 'ar': 'أرشيف_أداة', 'posix': '포직스경로', 'payload': 'حمولة_بيانات', 'flags': 'تكوين_خدمة_النقل_الذكي_في_الخلفية', 'cases': 'حالة_اختبار', 'cc': 'الرمز_البريدي_محول_برمجي', 'data': 'بيانات', 'build_java_library': '자바라이브러리만들기', 'ld': 'برنامج_ربط_أداة', 'repo': 'مستودع_مسار', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'نص', 'headers': 'عنوان_قائمة', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'بنية', 'build_users': 'فتح_مستخدم_مساحة', 'compiler': 'محول_برمجي_أداة', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'تطبيق_عنوان_إزاحة', 'offset': 'إزاحة_قيمة', 'text_address': 'أمر_عنوان', 'abi': '호출규약', 'assembly': 'تجميع', 'run': 'ينفذ_أمر', 'path': 'مسار', 'p': 'بيانات_منصب', 'changed': '바뀐자료', 'n': '개수', 'flag': 'إعدادات_قيمة', 'index': 'البحث_فهرس', 'classes': 'فئة_مسار', 'output': 'الناتج', 'loads': '적재구획', 'data_address': 'بيانات_عنوان', 'symbol': 'رمز_قيمة', 'root': 'جذر_عنوان', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'اسم', 'value': 'قيمة', 'fmt': 'تنسيق', 'work': '작업경로'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
