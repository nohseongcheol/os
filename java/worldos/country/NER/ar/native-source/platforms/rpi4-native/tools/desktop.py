#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/سطح_مكتب_عرض.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('سطح_مكتب_عرض', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('سطح_مكتب_عرض')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'خطأ', 'exact': '정확한값', 'network': 'شبكة', 'closed': 'أنظمة_المعلومات_مغلق', 'length': '길이', 'opened': '열림', 'ftp_port': 'نقل_الملفات_رقم_المنفذ', 'server': 'خادم_قيمة', 'resources': 'المصادر', 'data': 'بيانات', 'shift': 'مفتاح_SHIFT', 'send': 'يرسل', 'run_desktop': 'يشغّل_سطح_مكتب', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'مضيف', 'text': 'نص', 'korean': '한글여부', 'port': 'رقم_المنفذ', 'signum': 'إشارة_رقم', 'version': 'رقم_الإصدار', 'parser': 'المحلل', 'bridge': 'جسر', 'kind': 'فئة_قيمة', 'tail': '끝부분', 'size': 'حجم', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'الزر_Y_إحداثيات', 'prefix': '앞부분', 'client': 'عميل', 'char': 'بيانات_الأحرف', 'work': '작업경로', 'Keyboard': 'لوحة_المفاتيح', 'x': 'الإحداثي_س', 'down': '누르는중', 'net': 'جسر_إدخال', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'وسيطة_صفيف', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'عملية', 'Desktop': 'يتصل_سطح_مكتب', 'buttons': '단추들', 'thread': 'خيطالعمل', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'تبديل_الوضع', 'command': 'أمر', 'sock': 'مأخذ_التوصيل_قيمة', 'frame': '실행틀', 'ctrl': 'مفتاح_CTRL', 'path': 'مسار', 'cp': 'حرف_ترميز', 'terminate': 'ينهي', 'security': 'أمان', 'vnc_port': '원격화면접속번호', 'body': 'نص_أساسي', 'index': 'البحث_فهرس', 'exited': '종료됨', 'keysym': 'مفتاح_رمز', 'output': 'الناتج', 'keyboard': 'لوحة_المفاتيح_إدخال', 'interrupted': '가로채기됨', 'listener': 'يستلم_منفذ', 'reader': 'قارئ', 'NetworkBridge': 'جسر_3de4fe3a', 'gui': '그림화면', 'worker': 'معالجة_مهمة'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
