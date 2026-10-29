#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/يختبر_سطح_مكتب.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('يختبر_سطح_مكتب', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('يختبر_سطح_مكتب')
    대응 = {'x': 'الإحداثي_س', 'typing': '글자입력', 'message': 'إشعار_نص', 'start': 'تشغيل', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'رمز', 'j': '안쪽순번', 'deadline': 'موعد_نهائي_وقت', 'proc': 'عملية', 'data': 'بيانات', 'main': 'تشغيل', 'w': '너비값', 'init': '초기값', 'block': 'بيانات_حظر', 'ROOT': 'يعرض_جذر', 'text': 'نص', 'marker': 'علامة', 'report': 'التحقق_من_صحة_إبلاغ', 'until': '까지', 'clipboard': 'حافظة_قيمة', 'dst': 'وجهة_عنوان', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'نسخة_مكتوبة', 'port': 'رقم_المنفذ', 'offset': 'إزاحة_قيمة', 'h': 'مطلوب_ارتفاع_قيمة', 'src': '원본주소', 'event': 'حدث', 'encoding': 'مجموعة_أحرف', 'size': 'حجم', 'key': '누름값', 'pixels': '화소들', 'y': 'الزر_Y_إحداثيات', 'output': 'الناتج', 'symbol': 'رمز_قيمة', 'client': 'عميل', 'char': 'بيانات_الأحرف', 'rgb': '빛삼원색'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
