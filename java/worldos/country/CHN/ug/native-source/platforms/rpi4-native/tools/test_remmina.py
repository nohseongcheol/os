#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/원격한글시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ئىجرا_قىل_2', 'profile': 'ئارخىپ_1c9b560a', 'focused': 'نۇقتىلىق', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'مۇلازىمىتېر_قىممىتى', 'log': 'خاتىرە_قۇر', 'args': 'دەلىل_رەت', 'deadline': '마감시각', 'data': 'مەلۇمات', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ئىجرا_قىل_2', 'ready': '준비완료', 'found': 'ئىزدەش_ئۆلچەم', 'guest': 'مېھمان', 'ROOT': 'كۆرسىتىش_يىلتىز', 'marker': '확인표시', 'text': 'تېكىست', 'out': 'ئۆلچەم_مەلۇمات', 'env': '환경', 'f': 'ھۆججەت_كىرگۈزۈش', 'port': '접속번호', 'offset': 'ئاغما_قىممىتى', 'version': '판번호', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'selector': 'تاللىغۇچ', 'xvfb': 'مەۋھۇم_كۆرسەتكۈچ', 'display': 'كۆرسەتكۈچ', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'ئاتى', 'window': 'كۆزنەك', 'report': 'دەلىللەش_خەۋەر', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
