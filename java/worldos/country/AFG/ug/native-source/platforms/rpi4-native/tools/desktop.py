#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/ئۈستەليۈزى_كۆرۈنمە.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('ئۈستەليۈزى_كۆرۈنمە', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ئۈستەليۈزى_كۆرۈنمە')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'خاتالىق', 'exact': '정확한값', 'network': 'تور', 'closed': '닫힘', 'length': 'ئۇزۇنلۇق_قىممىتى', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'مۇلازىمىتېر_قىممىتى', 'resources': 'بايلىقلار', 'data': 'مەلۇمات', 'shift': 'SHIFT_كۇنۇپكىسى', 'send': 'ئەۋەتمەك', 'run_desktop': 'قوزغىتىش_ئۈستەليۈزى', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'باقار', 'text': 'تېكىست', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'كۆۋرۈك', 'kind': 'تۈر_قىممىتى', 'tail': '끝부분', 'size': 'چوڭلۇقى', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ئابۇنىتېر', 'char': 'ھەرپ_بەلگە_مەلۇمات', 'work': '작업경로', 'Keyboard': 'كۇنۇپكا_تاختىسى', 'x': 'x_كوردىنات', 'down': '누르는중', 'net': 'تور_كۆۋرۈك_كىرگۈزۈش', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'دەلىل_رەت', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'جەريان', 'Desktop': 'ئۇلاش_ئۈستەليۈزى', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ئۆزگەرتمەك_ھالەت', 'command': 'بۇيرۇق', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'كونترول_ئاچقۇچ', 'path': 'يول', 'cp': 'ھەرپ_بەلگە_كودىلاش', 'terminate': '종료시키기', 'security': 'خەۋپسىز', 'vnc_port': '원격화면접속번호', 'body': 'مەزمۇن', 'index': 'ئىزدەش_ئىندېكس', 'exited': '종료됨', 'keysym': 'ئاچقۇچ_بەلگە', 'output': '출력결과', 'keyboard': 'كۇنۇپكا_تاختىسى_كىرگۈزۈش', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ئوقۇغۇچ', 'NetworkBridge': 'تور_كۆۋرۈك', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
