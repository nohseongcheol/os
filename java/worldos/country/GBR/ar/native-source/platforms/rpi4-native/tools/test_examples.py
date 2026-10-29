#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/예제시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'نقل_الملفات_رقم_المنفذ', 'data': 'بيانات', 'graphics_command': 'رسومات_أمر', 'main': 'تشغيل', 'row': 'صف_منصب', 'init': '초기값', 'target': 'الهدف', 'ROOT': 'يعرض_جذر', 'text': 'نص', 'binary': 'ثنائي', 'out': 'مقياس_بيانات', 'entry': 'نقطة_الإدخال', 'got': '받은수', 'port': 'رقم_المنفذ', 'graphics_start': 'بدء_رسم', 'col': 'عمود_منصب', 'begin': 'بدء_إزاحة', 'kind': 'فئة_قيمة', 'selector': 'محدد', 'n': '개수', 'key': '누름값', 'y': 'الزر_Y_إحداثيات', 'client': 'عميل', 'line': 'سطر', 'report': 'التحقق_من_صحة_إبلاغ', 'language': 'لغة', 'x': 'الإحداثي_س', 'start': 'تشغيل', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'يرسل_قائمة', 'payload': 'حمولة_بيانات', 'proc': 'عملية', 'w': '너비값', 'temporary': '임시자원', 'echo': 'ارتداد_خادم_إدخال', 'label': 'اسم_جدول', 'content': 'محتوى_قيمة', 'argument': '전달값', 'EchoServers': 'ارتداد_خوادم', 'marker': 'علامة', 'expected': '예상결과', 'test_language': 'يختبر_لغة', 'filename': 'ملف_إدخال_اسم', 'shell': '셸', 'color': '색상', 'transcript': 'نسخة_مكتوبة', 'offset': 'إزاحة_قيمة', 'h': 'مطلوب_ارتفاع_قيمة', 'run': 'ينفذ_أمر', 'c': 'رمز_الحرف', 'path': 'مسار', 'encoding': 'مجموعة_أحرف', 'end': 'إنهاء_مكالمة_إزاحة', 'ftp': 'نقل_الملفات_صديق', 'pixels': '화소들', 'symbol': 'رمز_قيمة', 'source': '원본자료', 'name': 'اسم', 'receive': 'يستلم_رسالة', 'manifest': 'يُجمع_بيان'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
