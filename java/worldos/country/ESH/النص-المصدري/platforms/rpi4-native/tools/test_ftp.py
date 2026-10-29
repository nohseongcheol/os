#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/يختبر_بروتوكول_نقل_الملفات.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('يختبر_بروتوكول_نقل_الملفات', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('يختبر_بروتوكول_نقل_الملفات')
    대응 = {'timeout': '시간제한', 'payload': 'حمولة_بيانات', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'بيانات', 'proc': 'عملية', 'code': 'تعليمة_تسلسل', 'linux': '리눅스파일', 'archive': 'أرشيف', 'main': 'تشغيل', 'net_source': 'صافي_مصدر', 'temporary': '임시자원', 'static_source': 'ثابت_مصدر', 'java_source': '자바원문', 'echo': 'ارتداد_خادم_إدخال', 'ROOT': 'يعرض_جذر', 'text': 'نص', 'marker': 'علامة', 'EchoFixture': '되돌림시험서버', 'command': 'أمر', 'out': 'مقياس_بيانات', 'expected': '예상결과', 'server_source': 'خادم_مصدر', 'shell': '셸', 'upload': 'تحميل_الملفات', 'transcript': 'نسخة_مكتوبة', 'port': 'رقم_المنفذ', 'native': 'أصلي', 'elf': '실행파일', 'server_udp_port': 'خادم_مخطط_بيانات_منفذ', 'packed': '묶인자료', 'bridge': 'جسر', 'selector': 'محدد', 'end': 'إنهاء_مكالمة_إزاحة', 'e': '보조항목', 'ftp': 'نقل_الملفات_صديق', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'نظير_قيمة', 'result': 'نتيجة', 'unchanged': '보존자료', 'line': 'سطر', 'server_tcp_port': 'خادم_بث_منفذ', 'source': '원본자료', 'NetworkBridge': 'جسر_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'يستلم_رسالة', 'report': 'التحقق_من_صحة_إبلاغ'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
