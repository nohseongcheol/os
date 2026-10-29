#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/بنية_الوحدة_الطرفية_خط.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('بنية_الوحدة_الطرفية_خط', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بنية_الوحدة_الطرفية_خط')
    대응 = {'data': 'بيانات', 'img': 'رسم_قيمة', 'bits': 'خدمة_النقل_الذكي_في_الخلفية_قائمة', 'x': 'الإحداثي_س', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'مسار_قائمة', 'y': 'الزر_Y_إحداثيات', 'main': 'تشغيل', 'src': '원본주소', 'fonts': 'خط_قائمة_922d7e70', 'ROOT': 'يعرض_جذر', 'p': 'بيانات_منصب', 'cp': 'حرف_ترميز', 'target': 'الهدف'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
