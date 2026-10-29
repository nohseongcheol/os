#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/되돌림시험서버.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'مەلۇمات', 'e': '보조항목', 'connection': 'ئۇلىنىش_e05f319b', 'f': 'ھۆججەت_كىرگۈزۈش', 'peer': 'باراۋەرلىك_قىممىتى', 'self': '자신', 'udp': '전문제어', 't': 'تېرمىنال_كىرگۈزۈش', 'tcp': 'ئۇلىنىش_كونترول', 'EchoFixture': '되돌림시험서버', 'args': 'دەلىل_رەت', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
