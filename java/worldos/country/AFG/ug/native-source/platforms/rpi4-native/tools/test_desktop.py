#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/바탕화면시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_كوردىنات', 'typing': '글자입력', 'message': '알림문', 'start': 'ئىجرا_قىل_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'بەلگە', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'جەريان', 'data': 'مەلۇمات', 'main': 'ئىجرا_قىل_2', 'w': '너비값', 'init': '초기값', 'block': 'مەلۇمات_چەكلەش', 'ROOT': 'كۆرسىتىش_يىلتىز', 'text': 'تېكىست', 'marker': '확인표시', 'report': 'دەلىللەش_خەۋەر', 'until': '까지', 'clipboard': 'كېسىپ_چاپلاش_تاختىسى_قىممىتى', 'dst': 'نىشان_ئادرېس_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ئاغما_قىممىتى', 'h': '높이값', 'src': '원본주소', 'event': 'ھادىسە', 'encoding': 'ھەرپ_بەلگە_توپلىمى', 'size': 'چوڭلۇقى', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'بەلگە_قىممىتى', 'client': 'ئابۇنىتېر', 'char': 'ھەرپ_بەلگە_مەلۇمات', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
