#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/نۇسخا_تور.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('نۇسخا_تور', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نۇسخا_تور')
    대응 = {'obj': 'نىشان_ھۆججەت', 'objects': 'نىشان_ھۆججەت_417c7a10', 'library': 'ئامبار', 'output': '출력결과', 'port': '접속번호', 'root': 'يىلتىز_ئادرېس', 'files': 'ھۆججەت_تىزىم', 'source': '원본자료', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'flags': '설정비트', 'path': 'يول', 'build_network': 'قۇرۇش_تور_48d29d6d', 'cc': '시언어번역기', 'ar': 'ئارخىپ_قورال'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
