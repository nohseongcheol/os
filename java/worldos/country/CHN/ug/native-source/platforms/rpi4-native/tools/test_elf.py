#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/실행파일시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ئۆلچەم_مەلۇمات', 'expected': '예상결과', 'phoff': 'ئەپ_بېشى_ئاغما', 'offset': 'ئاغما_قىممىتى', 'invalid': 'ئۈنۈمسىز_مەلۇمات', 'path': 'يول', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ئۆلچەم', 'format_': 'فورمات_b87fd068', 'main': 'ئىجرا_قىل_2', 'content': 'مەزمۇن_قىممىتى', 'source': '원본자료', 'name': 'ئاتى', 'reference': '비교기준', 'ROOT': 'كۆرسىتىش_يىلتىز', 'value': 'قىممىتى', 'report': 'دەلىللەش_خەۋەر'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
