#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/원격한글시험.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'تشغيل', 'profile': 'يحلل', 'focused': 'المركّز_عليه', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'خادم_قيمة', 'log': 'سجل_سجل', 'args': 'وسيطة_صفيف', 'deadline': 'موعد_نهائي_وقت', 'data': 'بيانات', 'candidate': '후보', 'logs': '기록들', 'kw': 'وسيطات_مسمّاة', 'number': '수치', 'main': 'تشغيل', 'ready': '준비완료', 'found': 'بحث_مقياس', 'guest': 'ضيف', 'ROOT': 'يعرض_جذر', 'marker': 'علامة', 'text': 'نص', 'out': 'مقياس_بيانات', 'env': 'بيئة_التشغيل', 'f': 'ملف_إدخال_3d0c1245', 'port': 'رقم_المنفذ', 'offset': 'إزاحة_قيمة', 'version': 'رقم_الإصدار', 'p': 'بيانات_منصب', 'selector': 'محدد', 'xvfb': 'ظاهري_يعرض', 'display': 'جهاز_عرض', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'ظاهري_إدخال_أداة', 'name': 'اسم', 'window': 'نافذة', 'report': 'التحقق_من_صحة_إبلاغ', 'work': '작업경로'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
