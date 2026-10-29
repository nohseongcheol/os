#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/자바가상기계시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'சரம்_தரவு', 'actual': 'அசல்_அளவிடக்கூடியது', 'match': '일치', 'payload': 'பேலோட்_தரவு', 'cases': 'சோதனைப்_பெட்டி', 'fixture': '시험자료', 'main': 'செயல்படுத்துக', 'ROOT': 'திட்டப்பணி_மூலம்', 'text': 'உரை', 'valid': 'தகுதியான', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'பிரிவு_பாதை', 'output': '출력결과', 'result': 'அளவிடக்கூடியது', 'cmd': '명령인수', 'name': 'பெயர்', 'jar': '자바꾸러미', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'tests': 'சோதனைப்_பட்டியல்'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
