#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/예제되돌림서버.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': 'بيانات', 'sock': 'مأخذ_التوصيل_قيمة', 'tcp_port': 'TCP_منفذ', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'مخطط_بيانات_مؤشر_طلب', 'thread': 'خيطالعمل', 'echo': 'ارتداد_خادم_إدخال', 'TCP': 'مؤشر_صديق_طلب', 'EchoServers': 'ارتداد_خوادم', 'parser': 'المحلل', 'server': 'خادم_قيمة', 'udp_port': 'بروتوكول_مخطط_بيانات_المستخدم_منفذ', 'args': 'وسيطة_صفيف'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
