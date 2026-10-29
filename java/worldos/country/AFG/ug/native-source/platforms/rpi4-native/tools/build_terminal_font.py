#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/نۇسخا_تېرمىنال_خەت_نۇسخا.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('نۇسخا_تېرمىنال_خەت_نۇسخا', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نۇسخا_تېرمىنال_خەت_نۇسخا')
    대응 = {'data': 'مەلۇمات', 'img': 'سىزىش_قىممىتى', 'bits': '비트들', 'x': 'x_كوردىنات', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'يول_تىزىم', 'y': '세로좌표', 'main': 'ئىجرا_قىل_2', 'src': '원본주소', 'fonts': 'خەت_نۇسخا_تىزىم', 'ROOT': 'كۆرسىتىش_يىلتىز', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'cp': 'ھەرپ_بەلگە_كودىلاش', 'target': 'نىشان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
