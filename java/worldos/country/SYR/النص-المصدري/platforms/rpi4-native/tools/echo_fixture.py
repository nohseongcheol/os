#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/되돌림시험서버.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'بيانات', 'e': '보조항목', 'connection': 'صديق_e05f319b', 'f': 'ملف_إدخال_3d0c1245', 'peer': 'نظير_قيمة', 'self': '자신', 'udp': 'مخطط_بيانات_تحكم', 't': 'الوحدة_الطرفية_إدخال', 'tcp': 'صديق_تحكم', 'EchoFixture': '되돌림시험서버', 'args': 'وسيطة_صفيف', 'chunk': '조각'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
