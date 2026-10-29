#!/usr/bin/env python3
"""기존 مسار 호환 نقطة_الإدخال. الفعلي_بيانات 구현: ../أدوات/جسر_3de4fe3a.py"""
import importlib as 가져오기
import sys as نظام_تشغيل_قيمة
from pathlib import Path as مسار
نظام_تشغيل_قيمة.path.insert(0, str(مسار(__file__).resolve().parents[1] / 'أدوات'))
if __name__ == '__main__':
    import runpy as تطبيق_مشغّل
    تطبيق_مشغّل.run_module('جسر_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('جسر_3de4fe3a')
    대응 = {'response': 'رد_1262b476', 'parts': 'مسار_مكون', 's': 'سلسلة_بيانات', 'i': '순번', 'close': 'إغلاق', 'forward': '전달규칙', 'slip_input': 'بروتوكول_الخط_التسلسلي_للإنترنت_إدخال', 'self': '자신', 'item': 'إدخال_قيمة_962f286b', 'flags': 'تكوين_خدمة_النقل_الذكي_في_الخلفية', 'ftp_port': 'نقل_الملفات_رقم_المنفذ', 'args': 'وسيطة_صفيف', 'server': 'خادم_قيمة', 'data': 'بيانات', 'ethernet_input': '이더넷입력', 'trace_packet': 'أثر_حزمة', 'GATEWAY': 'بوابة_أجهزة_عنوان', 'rule': 'تصفية_قيمة', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'مضيف', 'ack': '확인번호', 'serial_port': 'منفذ_COM_رقم', 'readers': '읽기대상들', 'guest': 'ضيف', 'destination': 'وجهة_بيانات_عنوان', 'ethernet_port': 'منفذ_Ethernet', 'b': '둘째값', 'MAC': 'عنوان_حقيقي', 'arp': 'عنوان_دقة_حزمة', 'writable': 'قابل_للكتابة', 'direction': '방향', 'seq': 'أمر_رقم', 'frame': '실행틀', 'loop': 'دورة_قيمة', 'port': 'رقم_المنفذ', 'offset': 'إزاحة_قيمة', 'readable': '읽을수있음', 'c': 'رمز_الحرف', 'p': 'بيانات_منصب', 'writers': '쓰기대상들', 'IP': 'عنوان_الإنترنت_قيمة', 'e': '보조항목', 'n': '개수', 'packet': 'حزمة_بيانات', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'جسر_3de4fe3a', 'window': 'نافذة', 'capture': 'يسجل'}
    for 이전, حديث_عنصر in 대응.items():
        if hasattr(구현, حديث_عنصر): globals()[이전] = getattr(구현, حديث_عنصر)
