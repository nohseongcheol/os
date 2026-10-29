#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/코딩시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'ئۆلچەم_مەلۇمات', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'ئىجرا_قىل_2', 'elf': '실행파일', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'name': 'ئاتى', 'path': 'يول', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'ROOT': 'كۆرسىتىش_يىلتىز', 'report': 'دەلىللەش_خەۋەر', 'args': 'دەلىل_رەت'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
