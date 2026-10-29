#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/부팅시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'رد_1262b476', 'msg': 'شبكة_رسالة', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'تنفيذ', 'cancel': 'يلغي_تشغيل', 'cmd_byte': 'أمر_بايت', 'reply': 'رد', 'points': '지점들', 'server': 'خادم_قيمة', 'data': 'بيانات', 'prompt': 'طلب_1dd14da4', 'enter': 'يدخل', 'imported': '들여온파일', 'send': 'يرسل', 'main': 'تشغيل', 'ROOT': 'يعرض_جذر', 'text': 'نص', 'first_gui': '첫화면', 'pixel': 'عنصر_صورة', 'java_class': '자바클래스', 'upload': 'تحميل_الملفات', 'pixels_file': 'عنصر_صورة_ملف', 'pixels_data': 'عنصر_صورة_بيانات', 'edit': 'يحرر_قيمة', 'receive_until': '표시까지받기', 'selector': 'محدد', 'size': 'حجم', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'الزر_Y_إحداثيات', 'result': 'نتيجة', 'samples': '예제들', 'client': 'عميل', 'line': 'سطر', 'report': 'التحقق_من_صحة_إبلاغ', 'work': '작업경로', 'x': 'الإحداثي_س', 'python_checks': '파이썬검사', 'download': 'تنزيل', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'موعد_نهائي_وقت', 'proc': 'عملية', 'content': 'محتوى_قيمة', 'block': 'بيانات_حظر', 'marker': 'علامة', 'command': 'أمر', 'expected': '예상결과', 'shell': '셸', 'drawing': 'رسم_مسار', 'f': 'ملف_إدخال_3d0c1245', 'transcript': 'نسخة_مكتوبة', 'offset': 'إزاحة_قيمة', 'path': 'مسار', 'screenshot': 'لقطة_شاشة', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'الناتج', 'stream': 'بث_قيمة', 'cmd': '명령인수', 'name': 'اسم', 'qmp': '모의제어접속'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
