#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/رایانه_نما.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('رایانه_نما', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('رایانه_نما')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'خطا', 'exact': '정확한값', 'network': 'شبکه', 'closed': '닫힘', 'length': 'طول_مقدار', 'opened': '열림', 'ftp_port': 'فایل_انتقال_شماره_درگاه', 'server': 'سرور_مقدار', 'resources': 'منابع', 'data': 'داده_ها', 'shift': 'کلید_SHIFT', 'send': 'ارسال', 'run_desktop': 'اجرا_رایانه', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'میزبان', 'text': 'متن', 'korean': '한글여부', 'port': 'شماره_درگاه', 'signum': '신호번호', 'version': '판번호', 'parser': 'مفسر', 'bridge': 'پل', 'kind': 'دسته_مقدار', 'tail': '끝부분', 'size': 'اندازه', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'دکمه_Y_مختصات', 'prefix': '앞부분', 'client': 'سرویس_گیرنده', 'char': 'نویسه_داده_ها', 'work': '작업경로', 'Keyboard': 'صفحه_کلید', 'x': 'مختصات_x', 'down': '누르는중', 'net': 'شبکه_پل_ورودی', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'آرگومان_آرايه', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'فرآیند', 'Desktop': 'اتصال_رایانه', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'جابجایی_حالت', 'command': 'فرمان', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'کلید_CTRL', 'path': 'مسیر', 'cp': 'نویسه_رمزگذاری', 'terminate': '종료시키기', 'security': 'امنیت', 'vnc_port': '원격화면접속번호', 'body': 'متن_اصلی', 'index': 'جستجو_فهرست', 'exited': '종료됨', 'keysym': 'کلید_نماد', 'output': '출력결과', 'keyboard': 'صفحه_کلید_ورودی', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'خواننده', 'NetworkBridge': 'شبکه_پل', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
