#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'بېشى_قىممىتى', 'sources': '원문목록', 'i': '순번', 'info': 'سىستېما_ئۇچۇرى', 'payload': 'يۈك_مەلۇمات', 'src': '원본주소', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'تۈركۈم_يول', 'dist': '배포경로', 'archive': 'ئارخىپ', 'output': '출력결과', 'root': 'يىلتىز_ئادرېس', 'name': 'ئاتى', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
