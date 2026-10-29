#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/창시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'الإحداثي_س', 's': 'سلسلة_بيانات', 'xy': 'زوج_إحداثيات', 'sel': 'محدد_a916db4e', 'seconds': '초단위', 'log': 'سجل_سجل', 'at': 'حديث_منصب', 'send': 'يرسل', 'main': 'تشغيل', 'req': 'طلب_قيمة', 'hot': 'اختصار_قيمة', 'pump': 'مؤشر_حدث', 'ROOT': 'يعرض_جذر', 'marker': 'علامة', 'b': '둘째값', 'command': 'أمر', 'shell': '셸', 'f': 'ملف_إدخال_3d0c1245', 'color': '색상', 'click': 'نقرة_زر', 'k': '셋째순번', 'c': 'رمز_الحرف', 'r': '반환값', 'p': 'بيانات_منصب', 'done': 'مكتمل_مبلغ', 'end': 'إنهاء_مكالمة_إزاحة', 'command_mode': 'أمر_الوضع', 'key': '누름값', 'y': 'الزر_Y_إحداثيات', 'pixels': '화소들', 'result': 'نتيجة', 'report': 'التحقق_من_صحة_إبلاغ', 'dest': 'وجهة_قيمة_منصب', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
