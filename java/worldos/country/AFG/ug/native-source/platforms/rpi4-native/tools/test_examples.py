#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/예제시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'مەلۇمات', 'graphics_command': 'گرافىكلار_بۇيرۇق', 'main': 'ئىجرا_قىل_2', 'row': 'قۇر_ئورۇنلاشتۇرۇش', 'init': '초기값', 'target': 'نىشان', 'ROOT': 'كۆرسىتىش_يىلتىز', 'text': 'تېكىست', 'binary': 'ئىككىلىك', 'out': 'ئۆلچەم_مەلۇمات', 'entry': 'كىرگۈزۈش_نوقتا', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'باشلاش_سىزىش', 'col': 'ئىستون_ئورۇنلاشتۇرۇش', 'begin': 'باشلاش_ئاغما', 'kind': 'تۈر_قىممىتى', 'selector': 'تاللىغۇچ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ئابۇنىتېر', 'line': 'قۇر', 'report': 'دەلىللەش_خەۋەر', 'language': 'تىل', 'x': 'x_كوردىنات', 'start': 'ئىجرا_قىل_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ئەۋەتمەك_تىزىم', 'payload': 'يۈك_مەلۇمات', 'proc': 'جەريان', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'نامى_جەدۋەل', 'content': 'مەزمۇن_قىممىتى', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ھۆججەت_كىرگۈزۈش_نامى', 'shell': 'قاپ', 'color': '색상', 'transcript': '대화기록', 'offset': 'ئاغما_قىممىتى', 'h': '높이값', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'c': 'ھەرپ_كودى', 'path': 'يول', 'encoding': 'ھەرپ_بەلگە_توپلىمى', 'end': 'تاماملىماق_ئاغما', 'ftp': 'ھۆججەت_يوللاش_ئۇلىنىش', 'pixels': '화소들', 'symbol': 'بەلگە_قىممىتى', 'source': '원본자료', 'name': 'ئاتى', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
