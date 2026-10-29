#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/ئىجرا_قىلىش_ھۆججەت.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('ئىجرا_قىلىش_ھۆججەت', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ئىجرا_قىلىش_ھۆججەت')
    대응 = {'timeout': '시간제한', 's': 'ھەرپ_تىزمىسى_مەلۇمات', 'i': '순번', 'match': '일치', 'files': 'ھۆججەت_تىزىم', 'program': 'ئەپ', 'executable': '실행가능파일', 'args': 'دەلىل_رەت', 'chunk': '조각', 'data': 'مەلۇمات', 'proc': 'جەريان', 'send': 'ئەۋەتمەك', 'main': 'ئىجرا_قىل_2', 'marker': '확인표시', 'command': 'بۇيرۇق', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'parser': '인수해석기', 'options': 'تاللانمىلار', 'kind': 'تۈر_قىممىتى', 'selector': 'تاللىغۇچ', 'upload_data': 'يۈكلىمەك_مەلۇمات', 'end': 'تاماملىماق_ئاغما', 'n': '개수', 'd': 'نىشان_مەلۇمات', 'key': '누름값', 'output': '출력결과', 'line': 'قۇر', 'name': 'ئاتى', 'upload_name': 'يۈكلىمەك_نامى', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
