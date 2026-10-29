#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/부팅시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'تور_ئۇچۇر', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ئىجرا_قىل', 'cancel': 'ئىناۋەتسىز_مەشغۇلات', 'cmd_byte': 'بۇيرۇق_بايت', 'reply': 'جاۋابلاش', 'points': '지점들', 'server': 'مۇلازىمىتېر_قىممىتى', 'data': 'مەلۇمات', 'prompt': 'ئەسكەرتمە', 'enter': 'كىرمەك', 'imported': '들여온파일', 'send': 'ئەۋەتمەك', 'main': 'ئىجرا_قىل_2', 'ROOT': 'كۆرسىتىش_يىلتىز', 'text': 'تېكىست', 'first_gui': '첫화면', 'pixel': 'پىكسېل', 'java_class': '자바클래스', 'upload': 'يۈكلىمەك_ھۆججەت', 'pixels_file': 'پىكسېل_ھۆججەت', 'pixels_data': 'پىكسېل_مەلۇمات', 'edit': 'تەھرىرلەش_قىممىتى', 'receive_until': '표시까지받기', 'selector': 'تاللىغۇچ', 'size': 'چوڭلۇقى', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'ئۆلچەم', 'samples': '예제들', 'client': 'ئابۇنىتېر', 'line': 'قۇر', 'report': 'دەلىللەش_خەۋەر', 'work': '작업경로', 'x': 'x_كوردىنات', 'python_checks': '파이썬검사', 'download': 'چۈشۈرۈش', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'جەريان', 'content': 'مەزمۇن_قىممىتى', 'block': 'مەلۇمات_چەكلەش', 'marker': '확인표시', 'command': 'بۇيرۇق', 'expected': '예상결과', 'shell': 'قاپ', 'drawing': 'سىزىش_يول', 'f': 'ھۆججەت_كىرگۈزۈش', 'transcript': '대화기록', 'offset': 'ئاغما_قىممىتى', 'path': 'يول', 'screenshot': 'ئېكراندىن_تۇتۇش', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ئېقىم_قىممىتى', 'cmd': '명령인수', 'name': 'ئاتى', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
