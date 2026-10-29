#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/셸시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_كوردىنات', 'msg': 'تور_ئۇچۇر', 'i': '순번', 'reply': 'جاۋابلاش', 'call': '호출', 'args': 'دەلىل_رەت', 'chunk': '조각', 'data': 'مەلۇمات', 'proc': 'جەريان', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ئەۋەتمەك', 'file': 'ھۆججەت', 'main': 'ئىجرا_قىل_2', 'found': 'ئىزدەش_ئۆلچەم', 'ROOT': 'كۆرسىتىش_يىلتىز', 'text': 'تېكىست', 'marker': '확인표시', 'command': 'بۇيرۇق', 'expected': '예상결과', 'pixel': 'پىكسېل', 'shell': 'قاپ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'تاماملىماق_ئاغما', 'image': 'رەسىم', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'ئۆلچەم', 'client': 'ئابۇنىتېر', 'line': 'قۇر', 'stream': 'ئېقىم_قىممىتى', 'name': 'ئاتى', 'value': 'قىممىتى', 'receive': '수신하기', 'report': 'دەلىللەش_خەۋەر', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
