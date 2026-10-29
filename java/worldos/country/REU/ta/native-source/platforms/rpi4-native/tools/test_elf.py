#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/실행파일시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'அளவிடக்கூடியது_தரவு', 'expected': '예상결과', 'phoff': 'நிரல்_மேற்குறிப்பு_ஆஃப்செட்', 'offset': 'ஆஃப்செட்_மதிப்பு', 'invalid': 'செல்லுபடியாகாத_தரவு', 'path': 'பாதை_2', 'executable': 'செயல்படுத்தக்கூடிய_கோப்பு_படம்', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'அளவிடக்கூடியது', 'format_': 'வடிவமை_b87fd068', 'main': 'செயல்படுத்துக', 'content': 'உள்ளடக்கம்_மதிப்பு', 'source': '원본자료', 'name': 'பெயர்', 'reference': 'ஒப்பிடுதல்_அடிப்படைக்_கோடு', 'ROOT': 'திட்டப்பணி_மூலம்', 'value': 'மதிப்பு', 'report': 'செல்லுபடியாக்கம்_அறிக்கை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
