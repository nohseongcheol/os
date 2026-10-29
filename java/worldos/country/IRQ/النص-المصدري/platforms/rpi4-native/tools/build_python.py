#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/파이썬빌드.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': 'برنامج_ربط_أداة', 'archive': 'أرشيف', 'SHA256': 'التحقق_من_صحة_تجزئة', 'build_python': '파이썬만들기', 'root': 'جذر_عنوان', 'source': '원본자료', 'name': 'اسم', 'path': 'مسار', 'VERSION': '배포판', 'cc': 'الرمز_البريدي_محول_برمجي', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'عضو'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
