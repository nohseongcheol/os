#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/نۇسخا_سىستېما.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('نۇسخا_سىستېما', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نۇسخا_سىستېما')
    대응 = {'network': 'تور', 'BUILD': 'نۇسخا_يول', 'ar': 'ئارخىپ_قورال', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'خەت_نۇسخا_مەلۇمات', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'دەلىل_رەت', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ئۇسۇل_كىرگۈزۈش', 'main': 'ئىجرا_قىل_2', 'objcopy': 'ئوبيېكت_ھۆججەت_ئايلاندۇرغۇچ', 'ROOT': 'كۆرسىتىش_يىلتىز', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'قۇرۇش_ئىشلەتكۈچى_بوشلۇق', 'f': 'ھۆججەت_كىرگۈزۈش', 'extra': '추가영역', 'exports': 'چىقىرىش_جەدۋەل', 'jobs': '빌드작업', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'path': 'يول', 'REPO': '저장소', 'tool': 'قوراللار', 'classes': 'تۈركۈم_يول', 'output': '출력결과', 'samples': '예제들', 'symbol': 'بەلگە_قىممىتى', 'source': '원본자료', 'name': 'ئاتى', 'build_network': 'قۇرۇش_تور_48d29d6d', 'font_info': 'خەت_نۇسخا_ئۇچۇر', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
